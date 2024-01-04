import numpy as np
import pandas as pd

from ..predict_explanations.utils import prepare_result_df
from ..predict_explanations.object import PredictSurvSHAP
from tqdm import tqdm
import matplotlib.pyplot as plt
from statsmodels.graphics.functional import fboxplot
from scipy.integrate import trapezoid
from sksurv.ensemble import RandomSurvivalForest
import shap
import warnings


def calculate_individual_explanations(
    explainer,
    new_observations,
    function_type,
    path,
    B,
    max_shap_value_inputs,
    random_state,
    calculation_method,
    aggregation_method,
    timestamps,
    save_individual_explanations,
    **kwargs,
):
    individual_explanations = []
    concatenated_results = pd.DataFrame()
    preds = explainer.predict(explainer.data, function_type)

    if timestamps is None:
        timestamps = preds[0].x
        preds = [f.y for f in preds]
    else:
        if calculation_method == "treeshap":
            if not isinstance(explainer.model, RandomSurvivalForest):
                raise TypeError("explained model must be of class sksurv.ensemble.RandomSurvivalForest")
            warnings.warn(
                "timestamps are ignored for calculation_method = 'treeshap' \n SurvSHAP(t) values are calculated for explainer.model.unique_times_"
            )
            timestamps = explainer.model.unique_times_
            preds = [f.y for f in preds]
        else:
            preds = [f(timestamps) for f in preds]

    baseline_f = np.mean(preds, axis=0)

    if calculation_method in ["shap_kernel", "treeshap"]:
        if calculation_method == "shap_kernel":

            def predict_function(X):
                all_functions = explainer.predict(X, function_type)
                preds = np.array([f(timestamps) for f in all_functions])
                return preds

            # as shap convert pd.DataFrame to np.array
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=UserWarning)
                exp = shap.KernelExplainer(predict_function, explainer.data, **kwargs)
                res = exp.shap_values(new_observations)
            tmp = np.dstack(res).flatten()

        elif calculation_method == "treeshap":
            if function_type == "sf":
                start_index = 1
            elif function_type == "chf":
                start_index = 0

            n_estimators = len(explainer.model.estimators_)
            tree_ensemble_model = {"trees": [estimator.tree_ for estimator in explainer.model.estimators_]}

            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=UserWarning)
                exp = shap.TreeExplainer(tree_ensemble_model, explainer.data, **kwargs)
                res = exp.shap_values(new_observations, **kwargs)
            res = res[start_index::2]
            tmp = np.dstack(res).flatten() / n_estimators

        new_observations_shape = new_observations.shape
        tmp = tmp.reshape(new_observations_shape[0] * new_observations_shape[1], len(timestamps))
        variable_names = explainer.data.columns

        exp_y_names = explainer.y.dtype.names
        event_inds = explainer.y[exp_y_names[0]]
        event_times = explainer.y[exp_y_names[1]]

        for i in range(new_observations_shape[0]):
            survSHAP_obj = PredictSurvSHAP(
                function_type=function_type,
                calculation_method=calculation_method,
                aggregation_method=aggregation_method,
                random_state=random_state,
            )
            survSHAP_obj.result = prepare_result_df(
                new_observations.iloc[[i]],
                variable_names,
                tmp[(new_observations_shape[1] * i) : (new_observations_shape[1] * (i + 1)), :],
                timestamps,
                aggregation_method,
            )
            survSHAP_obj.simplified_result = survSHAP_obj.result[survSHAP_obj.result["B"] == 0].iloc[:, 1:5]
            survSHAP_obj.predicted_function = preds[i]
            survSHAP_obj.baseline_function = baseline_f
            survSHAP_obj.timestamps = timestamps

            survSHAP_obj.event_inds = event_inds
            survSHAP_obj.event_times = event_times

            if save_individual_explanations:
                individual_explanations.append(survSHAP_obj)
            tmp_results = survSHAP_obj.result
            tmp_results.insert(5, "index", i)
            concatenated_results = pd.concat((concatenated_results, tmp_results), axis=0)
    else:
        for i in tqdm(range(len(new_observations))):
            survSHAP_obj = PredictSurvSHAP(
                function_type=function_type,
                path=path,
                B=B,
                max_shap_value_inputs=max_shap_value_inputs,
                calculation_method=calculation_method,
                aggregation_method=aggregation_method,
                random_state=random_state,
            )
            survSHAP_obj.fit(explainer, new_observations.iloc[[i]], timestamps)
            if save_individual_explanations:
                individual_explanations.append(survSHAP_obj)
            tmp_results = survSHAP_obj.result
            tmp_results.insert(5, "index", i)
            concatenated_results = pd.concat((concatenated_results, tmp_results), axis=0)
    if timestamps is None:
        timestamps = survSHAP_obj.timestamps
    return concatenated_results, individual_explanations, timestamps


def create_boxplot_with_outliers(variable, full_result, wfactor=3):
    boxplot_data = full_result[(full_result["variable_name"] == variable) & (full_result["B"] == 0)].iloc[:, 6:].values
    fbxplt = fboxplot(boxplot_data, wfactor=wfactor)
    plt.close()
    outliers_ids = fbxplt[3]
    without_outliers_data = np.delete(boxplot_data, outliers_ids, axis=0)
    upper_whisker = np.max(without_outliers_data, axis=0)
    lower_whisker = np.min(without_outliers_data, axis=0)
    median_idx = fbxplt[2][0]
    return outliers_ids, median_idx, upper_whisker, lower_whisker


def aggregate_change(average_changes, aggregation_method, timestamps):
    if aggregation_method == "sum_of_squares":
        return np.sum(average_changes**2, axis=1)
    if aggregation_method == "max":
        return np.max(average_changes, axis=1)
    if aggregation_method == "mean":
        return np.mean(average_changes, axis=1)
    if aggregation_method == "integral":
        return trapezoid(average_changes.values, timestamps)


def calculate_risk_table(ticks, times, event_ind):
    n_at_risk = []
    n_censored = []
    n_events = []
    for i in ticks:
        n_at_risk.append((times > i).sum())
        n_events.append(event_ind[times <= i].sum())
        n_censored.append((~event_ind[times <= i]).sum())
    return n_at_risk, n_events, n_censored

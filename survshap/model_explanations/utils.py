from copy import deepcopy
from dataclasses import dataclass
import numpy as np
import pandas as pd
from ..predict_explanations.object import PredictSurvSHAP
from tqdm import tqdm
import matplotlib.pyplot as plt
from statsmodels.graphics.functional import fboxplot
from scipy.integrate import trapezoid


def calculate_individual_explanations(
    explainer,
    function_type,
    path,
    B,
    random_state,
    calculation_method,
    aggregation_method,
    timestamps,
    save_individual_explanations,
):
    individual_explanations = []
    concatenated_results = pd.DataFrame()
    for i in tqdm(range(len(explainer.data))):
        survSHAP_obj = PredictSurvSHAP(
            function_type=function_type,
            path=path,
            B=B,
            calculation_method=calculation_method,
            aggregation_method=aggregation_method,
            random_state=random_state,
        )
        if explainer.y is not None:
            y_true_i = explainer.y[i]
        else:
            y_true_i = None
        survSHAP_obj.fit(explainer, explainer.data.iloc[[i]], timestamps, y_true_i)
        if save_individual_explanations:
            individual_explanations.append(survSHAP_obj)
        tmp_results = survSHAP_obj.result
        tmp_results.insert(5, "index", i)
        concatenated_results = pd.concat((concatenated_results, tmp_results), axis=0)
    if timestamps is None:
        timestamps = survSHAP_obj.timestamps
    return concatenated_results, individual_explanations, timestamps


def create_boxplot_with_outliers(variable, full_result, wfactor=3):
    boxplot_data = (
        full_result[
            (full_result["variable_name"] == variable) & (full_result["B"] == 0)
        ]
        .iloc[:, 6:]
        .values
    )
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

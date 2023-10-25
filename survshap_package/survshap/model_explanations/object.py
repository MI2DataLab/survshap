from .plot import model_plot_mean_abs_shap_values, model_plot_shap_lines_for_all_individuals
import pandas as pd
import numpy as np
import pandas as pd
from .utils import aggregate_change, calculate_individual_explanations
import warnings


class ModelSurvSHAP:
    def __init__(
        self,
        function_type="sf",
        calculation_method="kernel",
        aggregation_method="integral",
        path="average",
        B=25,
        random_state=None,
    ):
        """Constructor for class ModelSurvSHAP

        Args:
            function_type (str, optional): Either "sf" representing survival function or "chf" representing cumulative hazard function. Type of function to be evaluated for explanation. Defaults to "sf".
            calculation_method (str, optional): Chooses the method for SurvSHAP(t) calculation. "shap_kernel" for shap.KernelExplainer, "kernel" for exact KernelSHAP, "sampling" for sampling method, or "treeshap" for shap.TreeExplainer. Defaults to "kernel".
            aggregation_method (str, optional): One of "sum_of_squares", "max_abs", "mean_abs" or "integral". Type of method  Defaults to "integral".
            path (list of int or str, optional): If specified, then attributions for this path will be plotted. Defaults to "average".
            B (int, optional): Number of random paths to calculate variable attributions. Defaults to 25.
            random_state (int, optional): Set seed for random number generator. Defaults to None.
        """
        self.explainer = None
        self.function_type = function_type
        self.calculation_method = calculation_method
        self.aggregation_method = aggregation_method
        self.path = path
        self.B = B
        self.result = pd.DataFrame()
        self.timestamps = None
        self.random_state = random_state
        self.event_ind = None  # full y
        self.event_times = None  # full y
        self.full_result = None

    def _repr_html_(self):
        return self.result[self.result["B"] == 0]._repr_html_()

    def fit(self, explainer, new_observations=None, timestamps=None, save_individual_explanations=True, **kwargs):
        """Calculate SurvSHAP(t) for many new observations and aggregate results.

        Args:
            explainer (SurvivalModelExplainer): A wrapper object for the model to be explained.
            new_observations (pandas.DataFrame, optional): A DataFrame containing the observations to be explained. If None observations from explainer are explained. Defaults to None.
            timestamps (numpy.Array, optional): An array of timestamps at which SurvSHAP(t) values should be calculated. Defaults to None.
            save_individual_explanations (bool, optional): Whether to save PredictSurvSHAP objects (explanations for individual observations). Defaults to True.
            **kwargs (optional): Additional parameters passed for shap.KernelExplainer.
        """
        # based on original shap warning
        data_len = len(explainer.data)

        if data_len > 100 and self.calculation_method != "treeshap":
            warnings.warn(
                "Using "
                + str(data_len)
                + " background data samples could cause slower run times.\n"
                + "Consider using a smaller sample."
            )

        if new_observations is None:
            new_observations = explainer.data

        (
            self.full_result,
            self.individual_explanations,
            self.timestamps,
        ) = calculate_individual_explanations(
            explainer,
            new_observations,
            self.function_type,
            self.path,
            self.B,
            self.random_state,
            self.calculation_method,
            self.aggregation_method,
            timestamps,
            save_individual_explanations,
            **kwargs
        )

        names = explainer.y.dtype.names
        self.event_ind = explainer.y[names[0]]
        self.event_times = explainer.y[names[1]]

        result = self.full_result.copy()

        result = (
            result[result["B"] == 0]
            .drop("variable_str", axis=1)
            .groupby(["variable_name"])
            .agg(lambda x: x.abs().mean())
            .reset_index()
        )

        result["aggregated_change"] = aggregate_change(result.iloc[:, 5:], self.aggregation_method, self.timestamps)
        result = result.sort_values("aggregated_change", ascending=False)
        self.result = result

    def get_mean_abs_shap_values(
        self,
        aggregation_method="sum_of_squares",
    ):
        result = self.full_result.copy()

        result = (
            result[result["B"] == 0]
            .drop("variable_str", axis=1)
            .groupby(["variable_name"])
            .agg(lambda x: x.abs().mean())
            .reset_index()
        )

        result["aggregated_change"] = aggregate_change(result.iloc[:, 5:], aggregation_method, self.timestamps)
        result = result.sort_values("aggregated_change", ascending=False)
        self.result = result

    def plot_mean_abs_shap_values(
        self,
        variables=None,
        max_vars=10,
        x_range=None,
        kind="default",
        show_risk_table=True,
        title=None,
        show=True,
    ):
        if len(self.result) == 0:
            self.get_mean_abs_shap_values()
        return model_plot_mean_abs_shap_values(
            self.result,
            self.timestamps,
            self.event_ind,
            self.event_times,
            variables,
            max_vars,
            x_range,
            kind,
            show_risk_table,
            title,
            show,
        )

    def plot_shap_lines_for_all_individuals(
        self,
        variable,
        x_range=None,
        kind="default",
        boxplot=False,
        wfactor=3,
        show_risk_table=True,
        show=True,
        title=None,
    ):
        return model_plot_shap_lines_for_all_individuals(
            self.full_result,
            self.timestamps,
            self.event_ind,
            self.event_times,
            variable,
            x_range,
            kind,
            boxplot,
            wfactor,
            show_risk_table,
            show,
            title,
        )

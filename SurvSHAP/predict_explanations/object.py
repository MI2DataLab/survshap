from .plot import predict_plot
import pandas as pd
import numpy as np
import pandas as pd
from .utils import check_new_observation, shap_kernel, shap_sampling


class PredictSurvSHAP:
    def __init__(
        self,
        function_type="sf",
        calculation_method="kernel",
        aggregation_method="integral",
        path="average",
        B=25,
        random_state=None,
        exact=False,
    ):
        """Constructor for class PredictSurvSHAP

        Args:
            function_type (str, optional): Either "sf" representing survival function or "chf" representing cumulative hazard function. Type of function to be evaluated for explanation. Defaults to "sf".
            calculation_method (str, optional): Either "kernel" for kernelSHAP or "sampling" for sampling method. Chooses type of survSHAP calculation . Defaults to "kernel".
            aggregation_method (str, optional): One of "sum_of_squares", "max_abs", "mean_abs" or "integral". Type of method  Defaults to "integral".
            path (list of int or str, optional): If specified, then attributions for this path will be plotted. Defaults to "average".
            B (int, optional): Number of random paths to calculate variable attributions. Defaults to 25.
            random_state (int, optional): Set seed for random number generator. Defaults to None.
            exact (bool, optional): Calculates all paths. If this is set to True parameter B is overriden. Defaults to False.
        """
        self.function = function_type
        self.calculation_method = calculation_method
        self.aggregation_method = aggregation_method
        self.path = path
        self.B = B
        self.result = pd.DataFrame()
        self.timestamps = None
        self.predicted_function = None
        self.baseline_function = None
        self.changes = None
        self.random_state = random_state
        self.exact = exact
        self.event_inds = None  # full y
        self.event_times = None  # full y
        self.y_true_time = None  # for this instance
        self.y_true_ind = None  # for this instance
        self.r2 = None

    def _repr_html_(self):
        return self.simplified_result._repr_html_()

    def fit(self, explainer, new_observation, timestamps=None, y_true=None):
        """Calculate SurvSHAP(t) for an observation

        Args:
            explainer (SurvivalModelExplainer): A wrapper object for the model to be explained.
            new_observation (pandas.DataFrame): A DataFrame with a single row, containing the observation to be explained.
            timestamps (numpy.Array, optional): An array of timestamps at which SurvSHAP(t) values should be calculated. Defaults to None.
            y_true (pandas.DataFrame, optional): A DataFrame containing the observed time and status of the explained observation. Used for plotting. Defaults to None.

        Raises:
            ValueError: if calculation_method is invalid
        """
        new_observation = check_new_observation(new_observation, explainer)
        names = explainer.y.dtype.names
        self.event_inds = explainer.y[names[0]]
        self.event_times = explainer.y[names[1]]
        if y_true is not None:
            self.y_true_ind = y_true[names[0]]
            self.y_true_time = y_true[names[1]]

        if self.calculation_method == "kernel":
            (
                self.result,
                self.predicted_function,
                self.baseline_function,
                self.timestamps,
                self.r2,
            ) = shap_kernel(
                explainer,
                new_observation,
                self.function,
                self.aggregation_method,
                timestamps,
            )
        elif self.calculation_method == "sampling":
            (
                self.result,
                self.predicted_function,
                self.baseline_function,
                self.timestamps,
            ) = shap_sampling(
                explainer,
                new_observation,
                self.function,
                self.path,
                self.B,
                self.random_state,
                self.aggregation_method,
                timestamps,
                self.exact,
            )
        else:
            raise ValueError("calculation_method should be 'kernel' or 'sampling'")

        self.simplified_result = self.result[self.result["B"] == 0].iloc[:, 1:5]

    def plot(
        self,
        max_vars=10,
        variables=None,
        x_range=None,
        kind="default",
        add_to_baseline=False,
        show_prediction=True,
        show_overall_change=False,
        show_y_info=True,
        show_risk_table=True,
        title=None,
        show=True,
    ):
        """Plot SurvSHAP(t) explanation

        Args:
            max_vars (int, optional): Maximum number of most important variables to show on the plot. Defaults to 10.
            variables (array_like, optional): Names of variables to be included to be shown on the plot. If None, all variables are considered (and max_vars most important ones are shown). Defaults to None.
            x_range (array_like, optional): Array containing two numbers, start and end time to be plotted. Defaults to None.
            kind (str, optional): Either "default" or "ratio", if "ratio" then SurvSHAP(t) values are normalized by the sum of SurvSHAP(t) absolute values for all variables. Defaults to "default".
            add_to_baseline (bool, optional): If True the SurvSHAP(t) values are added to survival function, not plotted directly. Defaults to False.
            show_prediction (bool, optional): If True the black-box model's survival function prediction is plotted. Defaults to True.
            show_overall_change (bool, optional): If True, the overall change, compared to average is shown on the plot (black-box prediction - average prediction). Defaults to False.
            show_y_info (bool, optional): If True, the true observed time and status are included on the plot. Defaults to True.
            show_risk_table (bool, optional): If True, a table is shown below the x-axis showing how many observations observed the event, are at risk and how many are censored up to this time. Defaults to True.
            title (str, optional): A title of the plot. Defaults to None.
            show (bool, optional): If True, the plot is shown, if False a plotly Figure object is returned. Defaults to True.

        Returns:
            plotly.graph_objects.Figure: If show is `False` then a plotly Figure is returned.
        """

        return predict_plot(
            self.result,
            self.predicted_function,
            self.baseline_function,
            self.timestamps,
            self.event_inds,
            self.event_times,
            self.y_true_ind,
            self.y_true_time,
            max_vars,
            variables,
            x_range,
            kind,
            add_to_baseline,
            show_prediction,
            show_overall_change,
            show_y_info,
            show_risk_table,
            title,
            show,
        )

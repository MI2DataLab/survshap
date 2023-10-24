import pandas as pd
import numpy as np
import sklearn
from sksurv.nonparametric import nelson_aalen_estimator
from scipy.optimize import minimize
import matplotlib
import plotly.subplots
import plotly.graph_objects
from pyDOE2 import lhs
from scipy.stats.distributions import norm
import collections


class SurvLIME:
    def __init__(
        self,
        random_state=None,
        N=100,
        distance_metric="euclidean",
        kernel_width=None,
        sampling_method="gaussian",
        sample_around_instance=True,
        max_iter=10000,
    ):
        self.N = N
        self.max_iter = max_iter
        self.distance_metric = distance_metric
        self.kernel_width = kernel_width
        self.sampling_method = sampling_method
        self.sample_around_instance = sample_around_instance
        self.result = pd.DataFrame()
        self.predicted_sf = None
        self.survlime_sf = None
        self.categorical_variables = None
        self.random_state = random_state
        self.y_time = None
        self.y_event = None
        self.opt_result = None

    def _repr_html_(self):
        return self.result._repr_html_()

    def fit(
        self,
        explainer,
        new_observation,
        categorical_variables=None,
        kernel=None,
        neighbourhood=None,
        k=5,
        timestamps=None,
    ):
        self.categorical_variables = categorical_variables
        event_field, time_field = explainer.y.dtype.names
        self.y_event = explainer.y[event_field]
        self.y_time = explainer.y[time_field]
        nel_aal_estimator = nelson_aalen_estimator(self.y_event, self.y_time)
        if timestamps is None:
            self.timestamps = nel_aal_estimator[0]
            na_est = nel_aal_estimator[1] + 1e-32
        else:
            self.timestamps = timestamps
            na_est = nel_aal_estimator[1][
                np.isin(nel_aal_estimator[0], self.timestamps)
            ]

        self.predicted_sf = explainer.predict(new_observation, "sf")[0](self.timestamps)

        new_observation_values = get_values(new_observation)
        if neighbourhood is None:
            ngbh_ind, neighbourhood, scaler = generate_neighbourhood(
                explainer.data,
                new_observation_values,
                self.N,
                categorical_variables,
                self.sampling_method,
                self.sample_around_instance,
                self.random_state,
            )
            scaled_data = (ngbh_ind - scaler.mean_) / scaler.scale_
            distances = sklearn.metrics.pairwise_distances(
                scaled_data, scaled_data[0].reshape(1, -1), metric=self.distance_metric
            ).ravel()
        else:
            distances = sklearn.metrics.pairwise_distances(
                neighbourhood,
                neighbourhood[0].reshape(1, -1),
                metric=self.distance_metric,
            ).ravel()
        self.neighbourhood = neighbourhood
        if self.kernel_width is None:
            self.kernel_width = float(np.sqrt(explainer.data.shape[1]) * 0.75)
        if kernel is None:
            weights = np.sqrt(np.exp(-(distances**2) / (self.kernel_width**2)))
        else:
            weights = kernel(distances)
        model_chfs = explainer.predict(pd.DataFrame(neighbourhood, columns=explainer.data.columns), "chf")
        model_chfs_vals = (
            np.array([chf(self.timestamps) for chf in model_chfs]) + 1e-32 + k
        )

        model_chfs_log_vals = np.log(model_chfs_vals)
        weights_v = model_chfs_vals / model_chfs_log_vals
        t_diffs = np.append(np.diff(self.timestamps), 1e-32)

        def loss(beta):
            return np.sum(
                weights
                * np.sum(
                    (weights_v**2)
                    * (
                        (
                            model_chfs_log_vals
                            - np.log(na_est + k)
                            - (neighbourhood @ beta)[:, None]
                        )
                        ** 2
                    )
                    * t_diffs,
                    axis=1,
                )
            )

        self.opt_result = minimize(
            loss,
            np.ones(explainer.data.shape[1]),
            method="Powell",
            options={"maxiter": self.max_iter},
        )
        model_sf = explainer.predict(pd.DataFrame(neighbourhood, columns=explainer.data.columns), "sf")
        self.neighbourhood_black_box_survival_functions = np.array(
            [sf(self.timestamps) for sf in model_sf]
        )
        self.neighbourhood_explanation_survival_functions = np.array(
            [
                np.exp(-(na_est) * (np.exp(nh_item @ self.opt_result.x)))
                for nh_item in neighbourhood
            ]
        )
        self.survlime_sf = np.exp(
            -(na_est) * (np.exp(self.opt_result.x @ new_observation_values))
        )
        self.result = pd.DataFrame(
            {
                "variable_name": explainer.data.columns,
                "variable_value": new_observation_values,
                "coefficient": self.opt_result.x,
            }
        )

    def plot(self, type="lines", show=True):
        ticker = matplotlib.ticker.MaxNLocator(
            nbins=10, min_n_ticks=4, integer=True, prune="upper"
        )
        ticks = ticker.tick_values(int(min(self.y_time)), int(max(self.y_time))).astype(
            int
        )
        n_at_risk = []
        n_censored = []
        n_events = []
        for i in ticks:
            n_at_risk.append((self.y_time > i).sum())
            n_events.append(self.y_event[self.y_time <= i].sum())
            n_censored.append((~self.y_event[self.y_time <= i]).sum())
        if type == "lines":
            fig = plotly.subplots.make_subplots(
                rows=2, cols=1, print_grid=False, shared_xaxes=True
            )
            fig.add_trace(
                plotly.graph_objs.Scatter(
                    x=self.timestamps,
                    y=self.predicted_sf,
                    mode="lines",
                    line_color="#4378bf",
                    line_width=2,
                    hovertemplate="<b>Predicted SF</b><br>"
                    + "Time: %{x}<br>"
                    + "SF value: %{y:.6f}<extra></extra>",
                    hoverinfo="text",
                ),
                1,
                1,
            )
            fig.add_trace(
                plotly.graph_objs.Scatter(
                    x=self.timestamps,
                    y=self.survlime_sf,
                    mode="lines",
                    line_color="#371ea3",
                    line_width=2,
                    hovertemplate="<b>SurvLIME SF (LIME approx.)</b><br>"
                    + "Time: %{x}<br>"
                    + "SF value: %{y:.6f}<extra></extra>",
                    hoverinfo="text",
                ),
                1,
                1,
            )
            fig.append_trace(
                plotly.graph_objs.Scatter(
                    x=ticks,
                    y=[0.8] * len(ticks),
                    text=n_at_risk,
                    mode="text",
                    showlegend=False,
                ),
                2,
                1,
            )
            fig.append_trace(
                plotly.graph_objs.Scatter(
                    x=ticks,
                    y=[0.5] * len(ticks),
                    text=n_events,
                    mode="text",
                    showlegend=False,
                ),
                2,
                1,
            )
            fig.append_trace(
                plotly.graph_objs.Scatter(
                    x=ticks,
                    y=[0.2] * len(ticks),
                    text=n_censored,
                    mode="text",
                    showlegend=False,
                ),
                2,
                1,
            )
            x_range = [0 - int(max(self.y_time)) * 0.025, int(max(self.y_time)) * 1.025]
            fig.update_xaxes(
                {
                    "matches": None,
                    "showticklabels": True,
                    "title": "timeline",
                    "title_standoff": 0,
                    "type": "linear",
                    "gridwidth": 2,
                    "zeroline": False,
                    "automargin": True,
                    "tickmode": "array",
                    "tickvals": ticks,
                    "ticktext": ticks,
                    "tickcolor": "white",
                    "ticklen": 3,
                    "fixedrange": True,
                    "range": x_range,
                }
            ).update_yaxes(
                {
                    "type": "linear",
                    "gridwidth": 2,
                    "zeroline": False,
                    "automargin": True,
                    "ticks": "outside",
                    "tickcolor": "white",
                    "ticklen": 3,
                    "fixedrange": True,
                }
            ).update_layout(
                {
                    "showlegend": False,
                    "template": "none",
                    "margin_pad": 6,
                    "margin_l": 110,
                }
            ).update_layout(
                yaxis2={
                    "tickvals": [0.2, 0.5, 0.8],
                    "ticktext": ["censored", "events", "at risk"],
                }
            )
            fig["layout"]["xaxis2"]["visible"] = False
            fig["layout"]["yaxis2"]["showgrid"] = False
            fig["layout"]["yaxis"]["domain"] = [0.35, 1]
            fig["layout"]["yaxis2"]["domain"] = [0.0, 0.2]
            fig["layout"]["yaxis2"]["range"] = [0, 1]
        if show:
            fig.show(
                config={
                    "displaylogo": False,
                    "staticPlot": False,
                    "toImageButtonOptions": {
                        "height": None,
                        "width": None,
                    },
                    "modeBarButtonsToRemove": [
                        "sendDataToCloud",
                        "lasso2d",
                        "autoScale2d",
                        "select2d",
                        "zoom2d",
                        "pan2d",
                        "zoomIn2d",
                        "zoomOut2d",
                        "resetScale2d",
                        "toggleSpikelines",
                        "hoverCompareCartesian",
                        "hoverClosestCartesian",
                    ],
                }
            )
        else:
            return fig


def get_values(obs):
    if isinstance(obs, pd.Series):
        return obs.values
    elif isinstance(obs, pd.DataFrame):
        return obs.values[0]
    elif isinstance(obs, np.ndarray):
        return obs


def generate_neighbourhood(
    data_org,
    data_row,
    num_samples,
    categorical_features=None,
    sampling_method="gaussian",
    sample_around_instance=True,
    random_state=None,
):
    training_data = data_org.values
    random_state = sklearn.utils.check_random_state(random_state)
    scaler = sklearn.preprocessing.StandardScaler(with_mean=False)
    scaler.fit(training_data)
    if categorical_features is None:
        categorical_features = []
    # feature values and freqs (for categorical)
    feature_values = {}
    feature_frequencies = {}
    for feature in categorical_features:
        column = training_data[:, feature]
        feature_count = collections.Counter(column)
        values, frequencies = map(list, zip(*(sorted(feature_count.items()))))
        feature_values[feature] = values
        feature_frequencies[feature] = np.array(frequencies) / float(sum(frequencies))
        scaler.mean_[feature] = 0
        scaler.scale_[feature] = 1
    num_cols = data_row.shape[0]
    data = np.zeros((num_samples, num_cols))
    scale = scaler.scale_
    mean = scaler.mean_
    if sampling_method == "gaussian":
        data = random_state.normal(0, 1, num_samples * num_cols).reshape(
            num_samples, num_cols
        )
        data = np.array(data)
    elif sampling_method == "lhs":
        data = lhs(num_cols, samples=num_samples).reshape(num_samples, num_cols)
        for i in range(num_cols):
            data[:, i] = norm(loc=0, scale=1).ppf(data[:, i])
        data = np.array(data)
    if sample_around_instance:
        data = data * scale + data_row
    else:
        data = data * scale + mean
    data[0] = data_row.copy()
    inverse = data.copy()
    for column in categorical_features:
        values = feature_values[column]
        freqs = feature_frequencies[column]
        inverse_column = random_state.choice(
            values, size=num_samples, replace=True, p=freqs
        )
        binary_column = (inverse_column == data_row[column]).astype(int)
        binary_column[0] = 1
        inverse_column[0] = data[0, column]
        data[:, column] = binary_column
        inverse[:, column] = inverse_column
    inverse[0] = data_row
    return data, inverse, scaler

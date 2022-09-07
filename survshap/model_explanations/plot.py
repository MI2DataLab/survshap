import numpy as np
import pandas as pd
import matplotlib.ticker
import plotly.subplots
import plotly.graph_objects
from .utils import calculate_risk_table, create_boxplot_with_outliers
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap, Normalize


def tooltip_text(row):
    return f"<b>{row.variable_name}</b><br>" + f"Value: {row.variable_value:.6f}<br>"


def check_y_range(max_y, min_y, new_vector):
    tmp_max = np.max(new_vector)
    tmp_min = np.min(new_vector)
    if tmp_max > max_y:
        max_y = tmp_max
    if tmp_min < min_y:
        min_y = tmp_min
    return max_y, min_y


def insert_zeros_to_line(x_vals, y_vals):
    put_zero = np.where(np.diff(np.sign(y_vals)) != 0)[0]
    y1 = y_vals[put_zero]
    y2 = y_vals[put_zero + 1]

    x1 = x_vals[put_zero]
    x2 = x_vals[put_zero + 1]
    to_put_x = (x1 * abs(y2) + x2 * abs(y1)) / (abs(y1) + abs(y2))
    new_y = np.insert(y_vals, put_zero + 1, 0)
    new_x = np.insert(x_vals, put_zero + 1, to_put_x)

    return new_x, new_y


def model_plot_mean_abs_shap_values(
    result,
    timestamps,
    event_inds,
    event_times,
    variables,
    max_vars=10,
    x_range=None,
    kind="default",
    show_risk_table=True,
    title=None,
    show=True,
):
    df_prepared_to_plot = result.copy()
    if kind == "ratio":
        df_prepared_to_plot.iloc[:, 5:] = (
            df_prepared_to_plot.iloc[:, 5:]
            / df_prepared_to_plot.iloc[:, 5:].abs().sum()
        )
    if variables is not None:
        df_prepared_to_plot = df_prepared_to_plot[
            df_prepared_to_plot["variable_name"].isin(variables)
        ]
    else:
        df_prepared_to_plot = df_prepared_to_plot.iloc[:max_vars]

    fig = plotly.subplots.make_subplots(
        rows=2, cols=1, print_grid=False, shared_xaxes=True
    )
    max_y, min_y = -1, 1
    fig.add_trace(
        plotly.graph_objs.Scatter(
            x=timestamps,
            y=[0] * len(timestamps),
            mode="lines",
            line_color="#4378bf",
            line_width=3,
            hovertemplate="<b>Average SF</b><br>"
            + "Time: %{x}<br>"
            + "<extra></extra>",
            hoverinfo="text",
        ),
        row=1,
        col=1,
    )

    keyword = "SHAP value: " if kind == "default" else "normalized SHAP value: "

    for index, row in df_prepared_to_plot.iterrows():
        y_vals = row[5:].values

        fig.add_trace(
            plotly.graph_objs.Scatter(
                x=timestamps,
                y=y_vals,
                mode="lines",
                line_color="#4378bf",
                line_width=2,
                hovertemplate="<b>"
                + str(row["variable_name"])
                + "</b><br>"
                + "(Avg) variable value: "
                + str(row["variable_value"])
                + "<br>"
                "Time: %{x}<br>" + keyword + "%{y:.6f}<extra></extra>",
                hoverinfo="text",
            ),
            row=1,
            col=1,
        )
        max_y, min_y = check_y_range(max_y, min_y, y_vals)

    min_y = min_y - 0.05 * abs(min_y)
    max_y = max_y + 0.05 * abs(max_y)

    if x_range is None:
        x_range = [min(timestamps) - max(timestamps) * 0.025, max(timestamps) * 1.025]

    ticker = matplotlib.ticker.MaxNLocator(
        nbins=10, min_n_ticks=4, integer=True, prune="upper"
    )
    ticks = ticker.tick_values(x_range[0], x_range[1])

    if show_risk_table:
        n_at_risk, n_events, n_censored = calculate_risk_table(
            ticks, event_times, event_inds
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

    fig.update_xaxes(
        {
            "matches": None,
            "showticklabels": True,
            "title": "time",
            "title_standoff": 0,
            "type": "linear",
            "gridwidth": 2,
            "zeroline": False,
            "automargin": True,
            "tickmode": "array",
            "tickvals": ticks,
            "ticktext": np.around(ticks, 2),
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
            "range": [min_y, max_y],
        }
    ).update_layout(
        {"showlegend": False, "template": "none", "margin_pad": 6, "margin_l": 110}
    ).update_layout(
        yaxis2={
            "tickvals": [0.2, 0.5, 0.8],
            "ticktext": ["censored", "events", "at risk"],
            "showgrid": False,
            "domain": [0.0, 0.2],
            "range": [0, 1],
        },
        xaxis2={"visible": False},
    )

    if kind == "ratio":
        fig.update_layout(
            yaxis1={"domain": [0.35, 1], "title": "normalized mean(|SHAP value|)"},
        )
    else:
        fig.update_layout(
            yaxis1={"domain": [0.35, 1], "title": "mean(|SHAP value|)"},
        )

    fig.update_layout(
        title_text=title,
        title_x=0.15,
        font={"color": "#371ea3"},
        template="none",
        margin={"t": 78, "b": 71, "r": 30},
    )

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


def model_plot_shap_lines_for_all_individuals(
    full_result,
    timestamps,
    event_inds,
    event_times,
    variable,
    x_range=None,
    kind="default",
    boxplot=False,
    wfactor=3,
    show_risk_table=True,
    show=True,
    title=None,
):
    df_prepared_to_plot = full_result[full_result["variable_name"] == variable]
    df_prepared_to_plot = df_prepared_to_plot[df_prepared_to_plot["B"] == 0]
    if kind == "ratio":
        df_prepared_to_plot.iloc[:, 6:] = (
            df_prepared_to_plot.iloc[:, 6:]
            / df_prepared_to_plot.iloc[:, 6:].abs().sum()
        )
    df_prepared_to_plot = df_prepared_to_plot.reset_index(drop=True)
    if ~boxplot:
        cmap = LinearSegmentedColormap.from_list(
            "dalex", ["#c7f5bf", "#46bac2", "#371ea3"], N=100
        )
        minima = np.min(df_prepared_to_plot["variable_value"])
        maxima = np.max(df_prepared_to_plot["variable_value"])
        norm = matplotlib.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
        mapper = cm.ScalarMappable(norm=norm, cmap=cmap)
        mapped = mapper.to_rgba(df_prepared_to_plot["variable_value"])
        mapped = np.apply_along_axis(
            lambda x: matplotlib.colors.rgb2hex(x[:3]), 1, mapped
        )
        df_prepared_to_plot["index"] = mapped

    fig = plotly.subplots.make_subplots(
        rows=2, cols=1, print_grid=False, shared_xaxes=True
    )

    max_y, min_y = -1, 1

    keyword = "SHAP value: " if kind == "default" else "normalized SHAP value: "

    if boxplot:
        (
            outliers_ids,
            median_idx,
            upper_whisker,
            lower_whisker,
        ) = create_boxplot_with_outliers(variable, full_result, wfactor)
    for i, row in df_prepared_to_plot.iterrows():
        x_vals = timestamps
        y_vals = row[6:].values
        new_x, new_y = insert_zeros_to_line(x_vals, y_vals)
        if boxplot:
            if i in outliers_ids:
                line_color = "#ae2c87"
                line_width = 1.5
            elif i == median_idx:
                line_color = "#ffa58c"
                line_width = 2
            else:
                line_color = "lightgrey"
                line_width = 0.5
        else:
            line_color = row["index"]
            line_width = 0.5
        fig.add_trace(
            plotly.graph_objs.Scatter(
                x=new_x,
                y=new_y,
                mode="lines",
                line_color=line_color,
                line_width=line_width,
                hovertemplate="<b>"
                + str(row["variable_name"])
                + "</b><br>"
                + "Variable value: "
                + str(row["variable_value"])
                + "<br>"
                "Time: %{x}<br>" + keyword + "%{y:.6f}<extra></extra>",
                hoverinfo="text",
            ),
            row=1,
            col=1,
        )
        max_y, min_y = check_y_range(max_y, min_y, y_vals)
    if boxplot:
        fig.add_trace(
            plotly.graph_objs.Scatter(
                x=timestamps,
                y=lower_whisker,
                mode="lines",
                line_color="#ffa58c",
                line_width=2,
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            plotly.graph_objs.Scatter(
                x=timestamps,
                y=upper_whisker,
                mode="lines",
                line_color="#ffa58c",
                line_width=2,
            ),
            row=1,
            col=1,
        )
    min_y = min_y - 0.05 * abs(min_y)
    max_y = max_y + 0.05 * abs(max_y)

    if x_range is None:
        x_range = [min(timestamps) - max(timestamps) * 0.025, max(timestamps) * 1.025]

    ticker = matplotlib.ticker.MaxNLocator(
        nbins=10, min_n_ticks=4, integer=True, prune="upper"
    )
    ticks = ticker.tick_values(x_range[0], x_range[1])

    if show_risk_table:
        n_at_risk, n_events, n_censored = calculate_risk_table(
            ticks, event_times, event_inds
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

    fig.update_xaxes(
        {
            "matches": None,
            "showticklabels": True,
            "title": "time",
            "title_standoff": 0,
            "type": "linear",
            "gridwidth": 2,
            "zeroline": False,
            "automargin": True,
            "tickmode": "array",
            "tickvals": ticks,
            "ticktext": np.around(ticks, 2),
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
            "range": [min_y, max_y],
        }
    ).update_layout(
        {"showlegend": False, "template": "none", "margin_pad": 6, "margin_l": 110}
    ).update_layout(
        yaxis2={
            "tickvals": [0.2, 0.5, 0.8],
            "ticktext": ["censored", "events", "at risk"],
            "showgrid": False,
            "domain": [0.0, 0.2],
            "range": [0, 1],
        },
        xaxis2={"visible": False},
    )
    if kind == "ratio":
        fig.update_layout(
            yaxis1={"domain": [0.35, 1], "title": "normalized SHAP value"},
        )
    else:
        fig.update_layout(
            yaxis1={"domain": [0.35, 1], "title": "SHAP value"},
        )

    fig.update_layout(
        title_text=title,
        title_x=0.15,
        font={"color": "#371ea3"},
        template="none",
        margin={"t": 78, "b": 71, "r": 30},
    )

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


def model_plot_shap_lines_for_variables(
    full_result,
    timestamps,
    event_inds,
    event_times,
    variables,
    to_discretize,
    discretization_method,
    n_bins,
    x_range=None,
    kind="default",
    show_risk_table=True,
    show=True,
    title=None,
):

    full_result_copy = full_result[
        (full_result["variable_name"].isin(variables)) & (full_result["B"] == 0)
    ].reset_index(drop=True)
    if kind == "ratio":
        full_result_copy.iloc[:, 5:] = (
            full_result_copy.iloc[:, 5:] / full_result_copy.iloc[:, 5:].abs().sum()
        )
    for var in to_discretize:
        if discretization_method == "quantile":
            discretize_map = dict(
                pd.qcut(
                    full_result_copy.loc[
                        full_result_copy["variable_name"] == var, "variable_value"
                    ],
                    q=n_bins,
                ).astype(str)
            )
            full_result_copy.loc[
                full_result_copy["variable_name"] == var, "variable_value"
            ] = full_result_copy[full_result_copy["variable_name"] == var]["index"].map(
                discretize_map
            )
            full_result_copy.loc[
                full_result_copy["variable_name"] == var, "variable_value"
            ] = (
                "in "
                + full_result_copy.loc[
                    full_result_copy["variable_name"] == var, "variable_value"
                ]
            )

    df_prepared_to_plot = (
        full_result_copy.groupby(["variable_name", "variable_value"])
        .mean()
        .reset_index()
    )

    fig = plotly.subplots.make_subplots(
        rows=2, cols=1, print_grid=False, shared_xaxes=True
    )

    max_y, min_y = -1, 1
    keyword = "SHAP value: " if kind == "default" else "normalized SHAP value: "
    for index, row in df_prepared_to_plot.iterrows():
        x_vals = timestamps
        y_vals = row[5:].values

        new_x, new_y = insert_zeros_to_line(x_vals, y_vals)

        fig.add_trace(
            plotly.graph_objs.Scatter(
                x=new_x,
                y=new_y,
                mode="lines",
                line_color="#8bdcbe",
                line_width=2,
                hovertemplate="<b>"
                + str(row["variable_name"])
                + "</b><br>"
                + "Variable value: "
                + str(row["variable_value"])
                + "<br>"
                "Time: %{x}<br>" + keyword + "%{y:.6f}<extra></extra>",
                hoverinfo="text",
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            plotly.graph_objs.Scatter(
                x=new_x[new_y <= 0],
                y=new_y[new_y <= 0],
                mode="lines",
                line_color="#f05a71",
                line_width=2,
                hovertemplate="<b>"
                + str(row["variable_name"])
                + "</b><br>"
                + "Variable value: "
                + str(row["variable_value"])
                + "<br>"
                "Time: %{x}<br>" + "SF change: " + "%{y:.6f}<extra></extra>",
                hoverinfo="text",
            ),
            row=1,
            col=1,
        )

        max_y, min_y = check_y_range(max_y, min_y, y_vals)

    min_y = min_y - 0.05 * abs(min_y)
    max_y = max_y + 0.05 * abs(max_y)

    if x_range is None:
        x_range = [min(timestamps) - max(timestamps) * 0.025, max(timestamps) * 1.025]

    ticker = matplotlib.ticker.MaxNLocator(
        nbins=10, min_n_ticks=4, integer=True, prune="upper"
    )
    ticks = ticker.tick_values(x_range[0], x_range[1])

    if show_risk_table:
        n_at_risk, n_events, n_censored = calculate_risk_table(
            ticks, event_times, event_inds
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

    fig.update_xaxes(
        {
            "matches": None,
            "showticklabels": True,
            "title": "time",
            "title_standoff": 0,
            "type": "linear",
            "gridwidth": 2,
            "zeroline": False,
            "automargin": True,
            "tickmode": "array",
            "tickvals": ticks,
            "ticktext": np.around(ticks, 2),
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
            "range": [min_y, max_y],
        }
    ).update_layout(
        {"showlegend": False, "template": "none", "margin_pad": 6, "margin_l": 110}
    ).update_layout(
        yaxis2={
            "tickvals": [0.2, 0.5, 0.8],
            "ticktext": ["censored", "events", "at risk"],
            "showgrid": False,
            "domain": [0.0, 0.2],
            "range": [0, 1],
        },
        xaxis2={"visible": False},
    )

    if kind == "ratio":
        fig.update_layout(
            yaxis1={"domain": [0.35, 1], "title": "normalized SHAP value"},
        )
    else:
        fig.update_layout(
            yaxis1={"domain": [0.35, 1], "title": "SHAP value"},
        )

    fig.update_layout(
        title_text=title,
        title_x=0.15,
        font={"color": "#371ea3"},
        template="none",
        margin={"t": 78, "b": 71, "r": 30},
    )

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

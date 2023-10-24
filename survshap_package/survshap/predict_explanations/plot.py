import numpy as np
import matplotlib.ticker
import plotly.subplots
import plotly.graph_objects
from .utils import calculate_risk_table


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


def insert_zeros_to_line(x_vals, y_vals, baseline_function):
    put_zero = np.where(np.diff(np.sign(y_vals)) != 0)[0]
    y1 = y_vals[put_zero]
    y2 = y_vals[put_zero + 1]

    x1 = x_vals[put_zero]
    x2 = x_vals[put_zero + 1]
    to_put_x = (x1 * abs(y2) + x2 * abs(y1)) / (abs(y1) + abs(y2))
    bsf1 = baseline_function[put_zero]
    bsf2 = baseline_function[put_zero + 1]
    to_put_baseline_function = (bsf1 * abs(y2) + bsf2 * abs(y1)) / (abs(y1) + abs(y2))
    new_x = np.insert(x_vals, put_zero + 1, to_put_x)
    new_y = np.insert(y_vals, put_zero + 1, 0)
    new_baseline_function = np.insert(
        baseline_function, put_zero + 1, to_put_baseline_function
    )

    return new_x, new_y, new_baseline_function


def predict_plot(
    result,
    predicted_function,
    baseline_function,
    timestamps,
    event_inds,
    event_times,
    y_true_ind=None,
    y_true_time=None,
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

    # get averaged shap values
    final_result = result[result["B"] == 0]
    if kind == "ratio":
        final_result.iloc[:, 5:] = np.nan_to_num(
            final_result[final_result["B"] == 0].iloc[:, 5:]
            / final_result[final_result["B"] == 0].iloc[:, 5:].abs().sum()
        )
        add_to_baseline = False
        show_prediction = False
        show_overall_change = False

    # choose variables
    if variables is not None:
        df_prepared_to_plot = final_result[
            final_result["variable_name"].isin(variables)
        ].copy()
    else:
        df_prepared_to_plot = final_result.iloc[:max_vars].copy()

    # add tooltips
    df_prepared_to_plot["tooltip_text"] = df_prepared_to_plot.apply(
        lambda row: tooltip_text(row), axis=1
    )

    fig = plotly.subplots.make_subplots(
        rows=2, cols=1, print_grid=False, shared_xaxes=True
    )

    max_y, min_y = -1, 1

    if add_to_baseline:
        fig.add_trace(
            plotly.graph_objs.Scatter(
                x=timestamps,
                y=baseline_function,
                mode="lines",
                line_color="#4378bf",
                line_width=3,
                hovertemplate="<b>Average SF</b><br>"
                + "Time: %{x}<br>"
                + "Avg SF value: %{y:.6f}<extra></extra>",
                hoverinfo="text",
            ),
            row=1,
            col=1,
        )
        max_y, min_y = check_y_range(max_y, min_y, baseline_function)

    else:
        fig.add_trace(
            plotly.graph_objs.Scatter(
                x=timestamps,
                y=[0] * len(timestamps),
                mode="lines",
                line_color="#4378bf",
                line_width=3,
                text=baseline_function,
                hovertemplate="<b>Average SF</b><br>"
                + "Time: %{x}<br>"
                + "Avg SF value: %{text:.6f}<extra></extra>",
                hoverinfo="text",
            ),
            row=1,
            col=1,
        )

    start_idx_preds = np.where(df_prepared_to_plot.columns == f"t = {timestamps[0]}")[
        0
    ][0]
    keyword = (
        "SF value: "
        if add_to_baseline
        else "SHAP value: "
        if kind == "default"
        else "normalized SHAP value: "
    )
    for index, row in df_prepared_to_plot.iterrows():
        x_vals = timestamps
        y_vals = row[start_idx_preds:-1].values

        new_x, new_y, new_baseline_function = insert_zeros_to_line(
            x_vals, y_vals, baseline_function
        )

        fig.add_trace(
            plotly.graph_objs.Scatter(
                x=new_x,
                y=new_y + new_baseline_function if add_to_baseline else new_y,
                mode="lines",
                line_color="#8bdcbe",
                hovertemplate=row["tooltip_text"]
                + "Time: %{x}<br>"
                + keyword
                + "%{y:.6f}<extra></extra>",
                hoverinfo="text",
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            plotly.graph_objs.Scatter(
                x=new_x[new_y <= 0],
                y=new_y[new_y <= 0] + new_baseline_function[new_y <= 0]
                if add_to_baseline
                else new_y[new_y <= 0],
                mode="lines",
                line_color="#f05a71",
                hovertemplate=row["tooltip_text"]
                + "Time: %{x}<br>"
                + keyword
                + "%{y:.6f}<extra></extra>",
                hoverinfo="text",
            ),
            row=1,
            col=1,
        )
        new_vector = (
            row[start_idx_preds:-1].values + baseline_function
            if add_to_baseline
            else row[start_idx_preds:-1].values
        )
        max_y, min_y = check_y_range(max_y, min_y, new_vector)

    if add_to_baseline and show_prediction:
        fig.add_trace(
            plotly.graph_objs.Scatter(
                x=timestamps,
                y=predicted_function,
                mode="lines",
                line_color="#371ea3",
                line_width=3,
                hovertemplate="<b>Predicted SF</b><br>"
                + "Time: %{x}<br>"
                + "Predicted SF value: %{y:.6f}<extra></extra>",
                hoverinfo="text",
            ),
            row=1,
            col=1,
        )
        max_y, min_y = check_y_range(max_y, min_y, predicted_function)
    elif ~(add_to_baseline) and show_overall_change:
        fig.add_trace(
            plotly.graph_objs.Scatter(
                x=timestamps,
                y=predicted_function - baseline_function,
                mode="lines",
                line_color="#371ea3",
                line_width=3,
                hovertemplate="<b>SF change</b><br>"
                + "Time: %{x}<br>"
                + "SF change: %{y:.6f}<extra></extra>",
                hoverinfo="text",
            ),
            row=1,
            col=1,
        )
        max_y, min_y = check_y_range(
            max_y, min_y, predicted_function - baseline_function
        )

    min_y = min_y - 0.05 * abs(min_y)
    max_y = max_y + 0.05 * abs(max_y)

    if show_y_info and y_true_time is not None:
        status = "dead" if y_true_ind else "censored"
        fig.add_trace(
            plotly.graph_objs.Scatter(
                x=[y_true_time] * 100,
                y=np.linspace(min_y, max_y, num=100),
                mode="lines",
                line_color="#ae2c87",
                line_width=2,
                hovertemplate="<b>Outcome</b><br>"
                + "Time to event: %{x}<br>"
                + "Status: "
                + status
                + "<extra></extra>",
                hoverinfo="text",
            ),
            row=1,
            col=1,
        )

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
        yaxis1={"domain": [0.35, 1]},
        xaxis2={"visible": False},
    )
    if add_to_baseline:
        fig.update_layout(yaxis1={"title": "survival function"})
    elif kind == "ratio":
        fig.update_layout(yaxis1={"title": "normalized SHAP value"})
    else:
        fig.update_layout(yaxis1={"title": "SHAP value"})

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

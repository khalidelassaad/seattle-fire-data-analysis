import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell
def _():
    from datetime import datetime

    import altair as alt
    import marimo as mo
    import pandas as pd
    import json

    return json, pd


@app.cell
def _(pd):
    incidents_dataframe = pd.read_csv("public/incidents_last_30_days.csv", index_col=0)
    unit_dispatches_dataframe = pd.read_csv("public/unit_dispatches_last_30_days.csv", index_col=0)
    unit_dataframe = pd.read_csv("public/unit_stats_last_30_days.csv", index_col=0)
    return incidents_dataframe, unit_dispatches_dataframe


@app.cell
def _(incidents_dataframe, unit_dispatches_dataframe):
    # Graph 1 Data
    graph_1_data_list = []

    for _, row in incidents_dataframe.iterrows():
        unit_dispatches_dataframe_filtered_to_incident = unit_dispatches_dataframe[unit_dispatches_dataframe["incident_number"] == row["incident_number"]]
        unit_tuple = tuple(sorted(set(unit_dispatches_dataframe_filtered_to_incident["unit"])))
        if not len(unit_tuple):
            continue
        units = unit_dispatches_dataframe_filtered_to_incident[["unit", "is_in_charge"]]
        units_in_charge_list = list(units[units["is_in_charge"]==True]["unit"])
        unit_in_charge = units_in_charge_list[0] if len(units_in_charge_list) else None
        data_dict = {
            "Time": row["datetime"],
            "Incident Number": row["incident_number"],
            "Incident Type": row["type"],
            "Address": row["address"],
            "Unit Count": len(unit_tuple),
            "Lead Unit": unit_in_charge,
            "Dispatched Units": ", ".join(unit_tuple),
            "Unit Tuple": unit_tuple
        }
        graph_1_data_list.append(data_dict)
    return (graph_1_data_list,)


@app.cell
def _(graph_1_data_list, json):
    with open('public/graph_1_data.json', 'w') as f:
        json.dump(graph_1_data_list, f)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

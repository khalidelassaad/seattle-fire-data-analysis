import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell
def _():
    from datetime import datetime

    import altair as alt
    import marimo as mo
    import pandas as pd

    return alt, datetime, mo, pd


@app.cell
def _(mo, pd):
    async def read_csv_into_dataframe(filename):
        filepath = mo.notebook_location() / "public" / filename
        if "http" not in str(mo.notebook_location()):
            return pd.read_csv(
                filepath, 
                index_col=0
            )
        from pyodide.http import pyfetch
        from io import StringIO
        response = await pyfetch(filepath)
        data = await response.text()
        return pd.read_csv(StringIO(data))

    return (read_csv_into_dataframe,)


@app.cell
async def _(read_csv_into_dataframe):
    incidents_dataframe = await read_csv_into_dataframe("incidents_last_30_days.csv")
    unit_dispatches_dataframe = await read_csv_into_dataframe("unit_dispatches_last_30_days.csv")
    unit_dataframe = await read_csv_into_dataframe("unit_stats_last_30_days.csv")
    return incidents_dataframe, unit_dataframe, unit_dispatches_dataframe


@app.cell
def _(mo):
    mo.md("""
    #Seattle Fire Department - Unit Dispatches Last 30 Days
    """)
    return


@app.cell
def _(mo, unit_dataframe):
    unit_dropdown = mo.ui.dropdown(
        sorted(unit_dataframe["unit"]),
        value = min(unit_dataframe["unit"])
    )
    return (unit_dropdown,)


@app.cell
def _(unit_dropdown):
    unit = unit_dropdown.value
    return (unit,)


@app.cell
def _(datetime, incidents_dataframe, mo):
    incidents_list = [incident for incident in incidents_dataframe["incident_number"] if incident[0] == "F"]
    first_incident = min(incidents_list)
    last_incident = max(incidents_list)
    start_datetime_str = min(incidents_dataframe["datetime"])
    start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%dT%H:%M:%S.%f").strftime("%b %d, %Y")
    end_datetime_str = max(incidents_dataframe["datetime"])
    end_datetime = datetime.strptime(end_datetime_str, "%Y-%m-%dT%H:%M:%S.%f").strftime("%b %d, %Y")

    mo.hstack(
        [
            mo.stat(
                value=len(incidents_dataframe),
                label="Total Incidents in this dataset",
                caption=f"Incidents from {first_incident} to {last_incident}"
            ),
            mo.stat(
                value=start_datetime,
                label="Dataset Start Date",
            ),
            mo.stat(
                value=end_datetime,
                label="Dataset End Date",
            ),
        ]
     )
    return


@app.cell
def _(unit, unit_dataframe):
    selected_unit_dataframe = unit_dataframe[unit_dataframe["unit"] == unit]
    return (selected_unit_dataframe,)


@app.cell
def _(pd):
    def minutes_to_minute_string(minutes):
        if pd.isna(minutes):
            return "0m 0s"
        seconds = int(((minutes % 1) * 60) // 1)
        minutes = int(minutes // 1)
        if minutes >= 60:
            return f"{minutes//60}h {minutes%60}m"
        else:
            return f"{minutes}m {seconds}s"

    return (minutes_to_minute_string,)


@app.cell
def _(minutes_to_minute_string, mo, selected_unit_dataframe, unit):
    stat_list = [
        mo.stat(
            value=unit,
            label="Unit",
        ),
        mo.stat(
            value=selected_unit_dataframe["number_of_incidents"].iloc[0],
            label="# of Incidents",
        ),
        mo.stat(
            value="{:.1f}%".format(selected_unit_dataframe["leadership_rate"].iloc[0]*100),
            label="% of Incidents Led",
        ),
        mo.stat(
            value=minutes_to_minute_string(selected_unit_dataframe["average_time_in_transit"].iloc[0]),
            label="Avg. Time in Transit",
        ),
        mo.stat(
            value=minutes_to_minute_string(selected_unit_dataframe["average_time_on_site"].iloc[0]),
            label="Avg. Time on Site",
        ),
        mo.stat(
            value=minutes_to_minute_string(selected_unit_dataframe["average_time_assigned"].iloc[0]),
            label="Avg. Time Assigned",
        ),
            mo.stat(
            value=minutes_to_minute_string(selected_unit_dataframe["total_time_in_transit"].iloc[0]),
            label="Total Time in Transit",
        ),
        mo.stat(
            value=minutes_to_minute_string(selected_unit_dataframe["total_time_on_site"].iloc[0]),
            label="Total Time on Site",
        ),
        mo.stat(
            value=minutes_to_minute_string(selected_unit_dataframe["total_time_assigned"].iloc[0]),
            label="Total Time Assigned",
        ),
    ]
    return (stat_list,)


@app.cell
def _(mo, stat_list, unit_dropdown):
    mo.vstack(
        [
            mo.md(f"Choose a unit: {unit_dropdown}"),
            mo.hstack(stat_list[:3], justify="center"),
            mo.hstack(stat_list[3:6], justify="center"),
            mo.hstack(stat_list[6:], justify="center"),
        ]
    )
    return


@app.cell
def _(incidents_dataframe, unit_dispatches_dataframe):
    # Graph 1 Data
    data_list = []

    for _, row in incidents_dataframe.iterrows():
        unit_dispatches_dataframe_filtered_to_incident = unit_dispatches_dataframe[unit_dispatches_dataframe["incident_number"] == row["incident_number"]]
        unit_set = set(unit_dispatches_dataframe_filtered_to_incident["unit"])
        if not len(unit_set):
            continue
        units = unit_dispatches_dataframe_filtered_to_incident[["unit", "is_in_charge"]]
        units_in_charge_list = list(units[units["is_in_charge"]==True]["unit"])
        unit_in_charge = units_in_charge_list[0] if len(units_in_charge_list) else None
        data_dict = {
            "Time": row["datetime"],
            "Incident Number": row["incident_number"],
            "Incident Type": row["type"],
            "Address": row["address"],
            "Unit Count": len(unit_set),
            "Lead Unit": unit_in_charge,
            "Dispatched Units": ", ".join(sorted(unit_set)),
            "Unit Set": unit_set
        }
        data_list.append(data_dict)
    return (data_list,)


@app.cell
def _(alt, data_list, unit):
    # Graph 1 Visualization
    data = alt.Data(values=data_list)
    # One mark per incident
    # Incident date on X axis
    # Number of responders on Y axis
    # Color by type of lead unit? type of incident? if unit is selected?
    # Click on mark selects lead unit in dropdown?
    # Hover over incident shows additional incident data...

    chart = alt.Chart(data).mark_point().encode(
        x='Time:T',
        y=alt.Y('Unit Count:Q', scale=alt.Scale(type='log', domain=[1,30])),
        color=alt.condition(
            alt.expr.indexof(alt.datum["Unit Set"], unit) >= 0,
            alt.value('red'),
            alt.value('gray')
        ),
        shape=alt.condition(
            alt.datum["Lead Unit"] == unit,
            alt.value('square'),
            alt.value('circle')
        ),
        size=alt.condition(
            alt.expr.indexof(alt.datum["Unit Set"], unit) >= 0,
            alt.value(100),
            alt.value(20)
        ),
        tooltip=["Incident Number:N", "Incident Type:N", "Time:T", "Address:N", "Lead Unit:N", "Dispatched Units:N", 'Unit Count:Q']
    ).interactive()

    chart
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

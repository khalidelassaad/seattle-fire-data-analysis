import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    return mo, pd


@app.cell
def _(pd):
    incidents_dataframe = pd.read_excel("incidents_last_30_days.xlsx", index_col=0)
    unit_dispatches_dataframe = pd.read_excel("unit_dispatches_last_30_days.xlsx", index_col=0)
    unit_dataframe = pd.read_excel("unit_stats_last_30_days.xlsx", index_col=0)
    return incidents_dataframe, unit_dataframe


@app.cell
def _(mo, unit_dataframe):
    unit_dropdown = mo.ui.dropdown(sorted(unit_dataframe["unit"]))
    return (unit_dropdown,)


@app.cell
def _(mo, unit_dropdown):
    mo.md(f"Choose a unit: {unit_dropdown}")
    return


@app.cell
def _(unit_dropdown):
    unit = unit_dropdown.value
    unit
    return


@app.cell
def _(incidents_dataframe):
    incidents_dataframe
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

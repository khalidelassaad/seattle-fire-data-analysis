import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    return mo, pd


@app.cell
def _(mo, pd):
    incidents_dataframe = pd.read_excel(mo.notebook_location() / "public" / "incidents_last_30_days.xlsx", index_col=0)
    unit_dispatches_dataframe = pd.read_excel(mo.notebook_location() / "public" / "unit_dispatches_last_30_days.xlsx", index_col=0)
    unit_dataframe = pd.read_excel(mo.notebook_location() / "public" / "unit_stats_last_30_days.xlsx", index_col=0)
    unit_dispatches_dataframe_2 = pd.read_excel(mo.notebook_location() / "public" / "unit_dispatches.xlsx", index_col=0)
    return (
        incidents_dataframe,
        unit_dataframe,
        unit_dispatches_dataframe,
        unit_dispatches_dataframe_2,
    )


@app.cell
def _(
    incidents_dataframe,
    mo,
    unit_dataframe,
    unit_dispatches_dataframe,
    unit_dispatches_dataframe_2,
):
    incidents_dataframe.to_csv(mo.notebook_location() / "public" / "incidents_last_30_days.csv", index=False)
    unit_dispatches_dataframe.to_csv(mo.notebook_location() / "public" / "unit_dispatches_last_30_days.csv", index=False)
    unit_dataframe.to_csv(mo.notebook_location() / "public" / "unit_stats_last_30_days.csv", index=False)
    unit_dispatches_dataframe_2.to_csv(mo.notebook_location() / "public" / "unit_dispatches.csv", index=False)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

import pandas as pd
from io import BytesIO


def generate_csv_report(data: pd.DataFrame) -> bytes:
    """Generate a downloadable CSV report."""

    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    return data.to_csv(index=False).encode("utf-8-sig")


def generate_excel_report(reports: dict) -> bytes:
    """Generate a multi-sheet Excel analytics report."""

    if not isinstance(reports, dict) or not reports:
        raise ValueError("Reports must be a non-empty dictionary")

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        for sheet_name, dataframe in reports.items():

            if not isinstance(dataframe, pd.DataFrame):
                raise TypeError(
                    f"Report '{sheet_name}' must be a DataFrame"
                )

            # Excel sheet names have a 31-character limit.
            safe_name = str(sheet_name)[:31]

            dataframe.to_excel(
                writer,
                sheet_name=safe_name,
                index=False
            )

    output.seek(0)

    return output.getvalue()
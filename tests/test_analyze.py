"""第三周特征和汇总指标的单元测试。"""

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.analyze import summarize_metrics  # noqa: E402
from src.features import add_sales_features  # noqa: E402


def _frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "InvoiceNo": ["100", "100", "101", "102"],
            "StockCode": ["A", "B", "A", "C"],
            "Description": ["Apple", "Bag", "Apple", "Cup"],
            "Quantity": [2, 3, 1, 4],
            "InvoiceDate": ["2024-01-03", "2024-01-03", "2024-02-01", "2024-02-02"],
            "UnitPrice": [5.0, 2.0, 5.0, 3.0],
            "CustomerID": [1, 1, 2, 3],
            "Country": ["UK", "UK", "FR", "UK"],
        }
    )


def test_add_sales_features_calculates_line_month_and_order_values():
    featured = add_sales_features(_frame())

    assert featured["Sales"].tolist() == [10.0, 6.0, 5.0, 12.0]
    assert featured["InvoiceMonth"].tolist() == ["2024-01", "2024-01", "2024-02", "2024-02"]
    assert featured["OrderTotal"].tolist() == [16.0, 16.0, 5.0, 12.0]


def test_add_sales_features_does_not_mutate_input():
    frame = _frame()
    add_sales_features(frame)
    assert "Sales" not in frame.columns


def test_summarize_metrics_returns_expected_aggregates():
    summaries = summarize_metrics(add_sales_features(_frame()), top_n=2)

    assert summaries["orders"]["OrderTotal"].tolist() == [16.0, 5.0, 12.0]
    assert summaries["monthly"]["Sales"].tolist() == [16.0, 17.0]
    assert summaries["products"]["Description"].tolist() == ["Apple", "Cup"]
    assert summaries["products"]["Sales"].tolist() == [15.0, 12.0]


def test_country_sales_are_sorted_highest_first():
    countries = summarize_metrics(add_sales_features(_frame()))["countries"]
    assert countries["Country"].tolist() == ["UK", "FR"]
    assert countries["Sales"].tolist() == [28.0, 5.0]


def test_invalid_date_is_reported():
    frame = _frame()
    frame.loc[0, "InvoiceDate"] = "not-a-date"
    with pytest.raises(ValueError, match="无法解析"):
        add_sales_features(frame)


def test_missing_required_column_is_reported():
    with pytest.raises(ValueError, match="InvoiceDate"):
        add_sales_features(_frame().drop(columns="InvoiceDate"))


def test_top_n_must_be_positive():
    with pytest.raises(ValueError, match="正整数"):
        summarize_metrics(add_sales_features(_frame()), top_n=0)

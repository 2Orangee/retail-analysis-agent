"""第二周清洗规则的单元测试。

运行方式（在项目根目录）：
    python -m pytest tests/test_clean.py -q
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.clean import clean_data  # noqa: E402


def _sample_frame() -> pd.DataFrame:
    """构造一个同时含各类脏数据的小表。

    7 行的预期命中情况：
      行0  正常（唯一被保留）
      行1  与行0 完全重复
      行2  InvoiceNo 以 C 开头（取消订单），且数量为负
      行3  CustomerID 缺失
      行4  Quantity == 0
      行5  UnitPrice == 0
      行6  Description 缺失
    """
    return pd.DataFrame(
        {
            "InvoiceNo": ["100001", "100001", "C100003", "100004", "100005", "100006", "100007"],
            "StockCode": ["A001", "A001", "A002", "A003", "A004", "A005", "A006"],
            "Description": ["Notebook", "Notebook", "Pen", "Mug", "Sticker", "Bag", None],
            "Quantity": [2, 2, -1, 1, 0, 3, 2],
            "InvoiceDate": pd.to_datetime(["2024-01-03"] * 7),
            "UnitPrice": [12.5, 12.5, 8.0, 15.0, 2.0, 0.0, 3.0],
            "CustomerID": [10001.0, 10001.0, 10001.0, None, 10003.0, 10004.0, 10005.0],
            "Country": ["United Kingdom"] * 7,
        }
    )


def test_counts_each_reason_independently():
    frame = _sample_frame()
    _, reasons = clean_data(frame)

    assert reasons["duplicate"] == 1
    assert reasons["missing"] == 2
    assert reasons["cancelled"] == 1
    assert reasons["nonpositive_quantity"] == 2  # 行2(-1) 与 行4(0)
    assert reasons["nonpositive_price"] == 1  # 行5(0.0)


def test_clean_data_removes_all_bad_rows():
    frame = _sample_frame()
    cleaned, reasons = clean_data(frame)

    assert reasons["total_removed"] == 6
    assert reasons["total_kept"] == 1
    assert len(cleaned) == 1
    assert cleaned.iloc[0]["InvoiceNo"] == "100001"


def test_clean_data_does_not_mutate_input():
    frame = _sample_frame()
    before = len(frame)
    clean_data(frame)
    assert len(frame) == before


def test_empty_frame():
    empty = pd.DataFrame()
    cleaned, reasons = clean_data(empty)

    assert cleaned.empty
    assert reasons["total_removed"] == 0
    assert reasons["total_kept"] == 0


def test_cancelled_invoice_detected_case_insensitive():
    frame = pd.DataFrame(
        {
            "InvoiceNo": ["c123", "C456"],
            "StockCode": ["A", "B"],
            "Description": ["x", "y"],
            "Quantity": [1, 1],
            "InvoiceDate": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "UnitPrice": [1.0, 1.0],
            "CustomerID": [1.0, 2.0],
            "Country": ["UK", "UK"],
        }
    )
    cleaned, reasons = clean_data(frame)

    assert reasons["cancelled"] == 2
    assert cleaned.empty


def test_clean_data_preserves_clean_rows():
    frame = pd.DataFrame(
        {
            "InvoiceNo": ["100001", "100002"],
            "StockCode": ["A", "B"],
            "Description": ["x", "y"],
            "Quantity": [2, 3],
            "InvoiceDate": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "UnitPrice": [12.5, 8.0],
            "CustomerID": [1.0, 2.0],
            "Country": ["UK", "FR"],
        }
    )
    cleaned, reasons = clean_data(frame)

    assert reasons["total_kept"] == 2
    assert reasons["total_removed"] == 0
    assert list(cleaned["InvoiceNo"]) == ["100001", "100002"]

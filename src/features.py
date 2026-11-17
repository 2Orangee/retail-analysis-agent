"""Create transaction-level features used by the retail analysis.

Week 3 scope: calculate line revenue, transaction month and order totals.
The caller should pass data that has already been cleaned by ``clean_data``.
"""

from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = {
    "InvoiceNo",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
}


def add_sales_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with ``Sales``, ``InvoiceMonth`` and ``OrderTotal``.

    ``Sales`` is the revenue of one transaction row. ``InvoiceMonth`` uses
    ``YYYY-MM`` text so it is easy to save as CSV. ``OrderTotal`` repeats the
    complete invoice value on every row belonging to that invoice.
    """
    missing = sorted(REQUIRED_COLUMNS - set(frame.columns))
    if missing:
        raise ValueError(f"缺少计算指标所需字段：{', '.join(missing)}")

    featured = frame.copy()
    quantity = pd.to_numeric(featured["Quantity"], errors="coerce")
    price = pd.to_numeric(featured["UnitPrice"], errors="coerce")
    invoice_date = pd.to_datetime(featured["InvoiceDate"], errors="coerce", format="mixed")

    invalid = quantity.isna() | price.isna() | invoice_date.isna()
    if invalid.any():
        raise ValueError(f"Quantity、UnitPrice 或 InvoiceDate 含无法解析的值：{int(invalid.sum())} 行")

    featured["Quantity"] = quantity
    featured["UnitPrice"] = price
    featured["InvoiceDate"] = invoice_date
    featured["Sales"] = quantity * price
    featured["InvoiceMonth"] = invoice_date.dt.to_period("M").astype(str)
    featured["OrderTotal"] = featured.groupby("InvoiceNo", dropna=False)["Sales"].transform("sum")
    return featured

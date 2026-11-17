"""Calculate and display the Week 3 retail summary metrics."""

from __future__ import annotations

import argparse

import pandas as pd

from .clean import clean_data
from .features import add_sales_features
from .load_data import load_data


def summarize_metrics(featured: pd.DataFrame, top_n: int = 10) -> dict[str, pd.DataFrame]:
    """Return order, monthly, product and country summaries.

    Popular products are ranked by sales revenue; quantity is also included
    to make the definition visible and auditable.
    """
    if top_n < 1:
        raise ValueError("top_n 必须是正整数")

    required = {"InvoiceNo", "InvoiceMonth", "StockCode", "Description", "Country", "Quantity", "Sales"}
    missing = sorted(required - set(featured.columns))
    if missing:
        raise ValueError(f"缺少汇总指标所需字段：{', '.join(missing)}")

    orders = (
        featured.groupby("InvoiceNo", as_index=False, dropna=False)
        .agg(OrderTotal=("Sales", "sum"), LineCount=("Sales", "size"))
        .sort_values("InvoiceNo", kind="stable")
        .reset_index(drop=True)
    )
    monthly = (
        featured.groupby("InvoiceMonth", as_index=False, dropna=False)
        .agg(Sales=("Sales", "sum"))
        .sort_values("InvoiceMonth", kind="stable")
        .reset_index(drop=True)
    )
    products = (
        featured.groupby(["StockCode", "Description"], as_index=False, dropna=False)
        .agg(Quantity=("Quantity", "sum"), Sales=("Sales", "sum"))
        .sort_values(["Sales", "Quantity", "StockCode"], ascending=[False, False, True], kind="stable")
        .head(top_n)
        .reset_index(drop=True)
    )
    countries = (
        featured.groupby("Country", as_index=False, dropna=False)
        .agg(Sales=("Sales", "sum"))
        .sort_values(["Sales", "Country"], ascending=[False, True], kind="stable")
        .reset_index(drop=True)
    )
    return {"orders": orders, "monthly": monthly, "products": products, "countries": countries}


def _format_table(title: str, frame: pd.DataFrame) -> str:
    display = frame.copy()
    for column in ("Sales", "OrderTotal"):
        if column in display:
            display[column] = display[column].map(lambda value: f"{value:.2f}")
    return f"{title}\n{display.to_string(index=False)}"


def main() -> None:
    parser = argparse.ArgumentParser(description="清洗零售数据并计算第三周基础指标")
    parser.add_argument("--input", required=True, help="本地 CSV 或 Excel 文件路径")
    parser.add_argument("--limit", type=int, default=None, help="只处理前 N 行；默认处理全部")
    parser.add_argument("--top-n", type=int, default=10, help="显示销售额最高的 N 个商品")
    args = parser.parse_args()

    try:
        raw = load_data(args.input, args.limit)
        cleaned, reasons = clean_data(raw)
        featured = add_sales_features(cleaned)
        summaries = summarize_metrics(featured, args.top_n)
    except (FileNotFoundError, ValueError, ImportError, UnicodeError, pd.errors.ParserError) as exc:
        parser.exit(1, f"分析失败：{exc}\n")

    print(f"读取 {len(raw)} 行；清洗后分析 {reasons['total_kept']} 行；订单数 {len(summaries['orders'])}")
    print(_format_table("\n各订单金额：", summaries["orders"]))
    print(_format_table("\n月度销售额：", summaries["monthly"]))
    print(_format_table(f"\n热门商品（按销售额排序，前 {args.top_n}）：", summaries["products"]))
    print(_format_table("\n各国家销售额：", summaries["countries"]))
    if args.limit is not None:
        print(f"\n注意：指定了 --limit {args.limit}，以上指标不代表全量数据。")


if __name__ == "__main__":
    main()

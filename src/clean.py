"""Clean a retail dataset and report which rows were removed and why.

Week 2 scope: detect and drop bad rows (duplicates, missing keys,
cancelled orders, non-positive quantity/price), log the counts for each
reason, and optionally save the cleaned data.

清洗规则（对应九周计划第二周任务 1）：
  1. 重复行        —— 与前面某行完全相同，只保留首条。
  2. 缺失值        —— CustomerID 或 Description 缺失。
  3. 取消订单      —— InvoiceNo 以字母 C 开头（UCI Online Retail 的约定）。
  4. 非正数数量    —— Quantity <= 0。
  5. 非正数价格    —— UnitPrice <= 0。

统计口径：各类问题是**独立统计**的，同一行可能同时命中多类问题；
清洗时只要命中任意一类就移除该行。
"""

from __future__ import annotations

import argparse

import pandas as pd

from .load_data import load_data

# 每种清洗原因的中文说明，供报告和命令行输出复用。
RULE_DESCRIPTIONS: dict[str, str] = {
    "duplicate": "完全重复的行（保留首条）",
    "missing": "CustomerID 或 Description 缺失",
    "cancelled": "取消订单（InvoiceNo 以 C 开头）",
    "nonpositive_quantity": "数量 Quantity <= 0",
    "nonpositive_price": "单价 UnitPrice <= 0",
}


def _issue_masks(frame: pd.DataFrame) -> dict[str, pd.Series]:
    """返回每类问题的布尔掩码，True 表示该行命中此类问题。

    掩码之间允许重叠：例如取消订单通常数量为负，会同时命中
    ``cancelled`` 与 ``nonpositive_quantity``。
    """
    invoice = frame["InvoiceNo"].astype(str)
    quantity = pd.to_numeric(frame["Quantity"], errors="coerce")
    price = pd.to_numeric(frame["UnitPrice"], errors="coerce")

    return {
        "duplicate": frame.duplicated(keep="first"),
        "missing": frame["CustomerID"].isna() | frame["Description"].isna(),
        "cancelled": invoice.str.upper().str.startswith("C"),
        "nonpositive_quantity": quantity <= 0,
        "nonpositive_price": price <= 0,
    }


def clean_data(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """移除脏数据，返回 ``(清洗后的 DataFrame, 各原因命中行数)``。

    返回的 ``reasons`` 字典包含各类问题的独立命中行数（允许重叠），
    以及 ``total_removed``（被移除总行数）和 ``total_kept``（保留总行数）。
    """
    if frame.empty:
        return frame.copy(), {"total_removed": 0, "total_kept": 0}

    masks = _issue_masks(frame)
    reasons = {name: int(mask.sum()) for name, mask in masks.items()}

    keep = pd.Series(True, index=frame.index)
    for mask in masks.values():
        keep &= ~mask

    reasons["total_removed"] = int((~keep).sum())
    reasons["total_kept"] = int(keep.sum())

    cleaned = frame.loc[keep].reset_index(drop=True)
    return cleaned, reasons


def summarize_cleaning(reasons: dict[str, int]) -> str:
    """把清洗统计格式化为可读文本，供命令行输出使用。"""
    total = reasons.get("total_kept", 0) + reasons.get("total_removed", 0)
    lines = [f"清洗前总行数：{total}"]
    for name, desc in RULE_DESCRIPTIONS.items():
        lines.append(f"  {desc}：{reasons.get(name, 0)} 行")
    lines.append(f"清洗后保留行数：{reasons.get('total_kept', 0)}")
    lines.append(f"共移除行数：{reasons.get('total_removed', 0)}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="清洗零售数据并报告每种排除原因")
    parser.add_argument("--input", required=True, help="本地 CSV 或 Excel 文件路径")
    parser.add_argument("--limit", type=int, default=None, help="只处理前 N 行；默认处理全部")
    parser.add_argument("--output", default=None, help="可选：把清洗后的数据写入 CSV")
    args = parser.parse_args()

    try:
        frame = load_data(args.input, args.limit)
    except (FileNotFoundError, ValueError, ImportError, UnicodeError, pd.errors.ParserError) as exc:
        parser.exit(1, f"读取失败：{exc}\n")

    cleaned, reasons = clean_data(frame)
    print(summarize_cleaning(reasons))

    if args.output:
        cleaned.to_csv(args.output, index=False, encoding="utf-8-sig")
        print(f"已把清洗后的 {reasons['total_kept']} 行写到：{args.output}")

    if args.limit is not None:
        print(f"注意：指定了 --limit {args.limit}，以上统计只针对本次读取的行，不代表全量数据。")


if __name__ == "__main__":
    main()

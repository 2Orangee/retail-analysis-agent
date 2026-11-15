"""Read a retail CSV/Excel file and print a basic data-quality overview.

Week 1 scope: inspect only. This module does not clean or change the data.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


SUPPORTED_SUFFIXES = {".csv", ".xlsx", ".xls"}


def load_data(path: str | Path, limit: int | None = None) -> pd.DataFrame:
    """Load a local CSV/Excel file, optionally reading only the first N rows."""
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"找不到文件：{file_path.resolve()}")
    if file_path.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise ValueError("只支持 .csv、.xlsx 或 .xls 文件")
    if limit is not None and limit < 1:
        raise ValueError("--limit 必须是正整数")

    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path, nrows=limit, encoding="utf-8-sig")
    return pd.read_excel(file_path, nrows=limit)


def describe_data(frame: pd.DataFrame) -> str:
    """Return a readable overview without modifying the input frame."""
    lines = [f"本次读取行数：{len(frame)}", f"列数：{len(frame.columns)}", "字段与数据类型："]
    lines.extend(f"  {column}: {frame[column].dtype}" for column in frame.columns)
    lines.append("各列缺失值数量：")
    lines.extend(f"  {column}: {int(frame[column].isna().sum())}" for column in frame.columns)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="读取零售数据并查看基本信息")
    parser.add_argument("--input", required=True, help="本地 CSV 或 Excel 文件路径")
    parser.add_argument("--limit", type=int, default=None, help="只读取前 N 行；默认读取全部")
    args = parser.parse_args()

    try:
        frame = load_data(args.input, args.limit)
    except (FileNotFoundError, ValueError, ImportError, UnicodeError, pd.errors.ParserError) as exc:
        parser.exit(1, f"读取失败：{exc}\n")
    print(describe_data(frame))
    if args.limit is not None:
        print(f"注意：指定了 --limit {args.limit}，以上行数不是文件总行数。")


if __name__ == "__main__":
    main()

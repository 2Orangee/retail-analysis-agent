# 数据说明

## 真实数据

计划使用 UCI Machine Learning Repository 的 [Online Retail 数据集](https://archive.ics.uci.edu/dataset/352/online+retail)。该数据集包含英国一家在线零售商的交易记录，官方页面显示约 54 万条记录。进入页面下载 `Online Retail.xlsx`，放在本项目的 `data/raw/` 目录下。若目录不存在，先创建它。

原始数据不随仓库提交。项目只记录数据来源、处理方法和少量测试样例。后续各周会在代码里写清取消订单、缺失值、非正数数量和价格的处理规则。

## 样例数据

`sample.csv` 是**人工编写的演示数据**，字段名参照 Online Retail；它不来自 UCI，也不能当成真实实验结果。它故意包含一行取消订单、一行缺失 `CustomerID` 和一行非正数价格，供后续清洗代码验证。

## 第一周命令

```powershell
python -m src.load_data --input data/sample.csv
python -m src.load_data --input 'data/raw/Online Retail.xlsx' --limit 5000
```

## 第二周命令

```powershell
python -m src.clean --input data/sample.csv
python -m src.clean --input 'data/raw/Online Retail.xlsx' --limit 5000
python -m src.clean --input data/sample.csv --output data/cleaned.csv
```

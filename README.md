# 零售数据 AI 分析助手

《大模型原理与技术》2026 年课程项目，选择 **06-Data-Processing（数据处理及统计）** 方向。

最终目标：上传零售交易 CSV 后，自动清洗数据、计算销售指标、生成图表、完成一项简单统计检验；本地小模型作为轻量 Agent 选择并调用预设分析工具，再根据工具返回的真实结果输出 Markdown 分析报告。项目按九周逐步开发；**当前已完成第一周（读取）和第二周（清洗）**，还没有指标计算、图表、Agent、报告或网页。

## 已完成内容

- `src/load_data.py`：读取 CSV 或 Excel，显示读取行数、列名、数据类型和各列缺失值数量。
- `src/clean.py`：清洗数据，统计并移除重复、缺失、取消订单、非正数数量/价格五类问题行。
- `tests/test_clean.py`：清洗规则的单元测试。
- `data/sample.csv`：自造的小样例，用于检查脚本，不代表真实实验数据。
- `data/README.md`：真实数据来源和放置方法。
- `progress/week01.md`、`progress/week02.md`：第一、二周进度记录。

## 安装与运行（Windows PowerShell）

先安装 Python 3.10 或更新版本，并确认终端中的 `python --version` 能正常显示版本号。然后在本项目目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.load_data --input data/sample.csv
python -m src.clean --input data/sample.csv
```

如果不使用虚拟环境，也可以先执行 `python -m pip install -r requirements.txt`，再运行最后一条命令。PowerShell 若不允许激活虚拟环境，可直接运行 `.\.venv\Scripts\python.exe -m src.load_data --input data/sample.csv`。

真实数据下载并放入 `data/raw/` 后，可先读取前 5,000 行，避免第一步耗时过长：

```powershell
python -m src.load_data --input 'data/raw/Online Retail.xlsx' --limit 5000
```

`--limit` 显示的是**本次读取行数**，不是整个文件的总行数。读取整个文件时去掉 `--limit`。支持 `.csv`、`.xlsx`、`.xls`，但 `.xls` 可能需要额外依赖；本项目主数据为 `.xlsx`。

## 第二周：清洗脏数据

`src/clean.py` 会按下面五类规则逐行判断，并输出每一类命中的行数、清洗前后总行数：

| 规则 | 判定 |
|---|---|
| 重复行 | 与前面某行完全相同，只保留首条 |
| 缺失值 | `CustomerID` 或 `Description` 缺失 |
| 取消订单 | `InvoiceNo` 以字母 C 开头（大小写不敏感） |
| 非正数数量 | `Quantity <= 0` |
| 非正数价格 | `UnitPrice <= 0` |

各规则是独立统计的（同一行可能同时命中多类，例如取消订单通常数量为负）；清洗时只要命中任意一类就移除该行。运行：

```powershell
python -m src.clean --input data/sample.csv
python -m src.clean --input 'data/raw/Online Retail.xlsx' --limit 5000
python -m src.clean --input data/sample.csv --output data/cleaned.csv
```

加 `--output` 会把清洗后的数据另存为 CSV。运行单元测试：

```powershell
python -m pytest tests/test_clean.py -q
```

真实数据下载后，去掉 `--limit` 可对全量数据清洗；`--limit` 只处理前 N 行，统计结果不代表全量。

## 数据和提交原则

真实数据来自 [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)。下载方法见 [data/README.md](data/README.md)。原始大数据放在 `data/raw/`，该目录被 `.gitignore` 排除，不上传项目仓库。不要把密码、密钥或个人敏感信息提交到公开仓库。

## 九周路线

第 1 周读取数据 → 第 2 周清洗 → 第 3 周指标 → 第 4 周图表与检验 → 第 5 周本地模型报告 → 第 6 周一键流程 → 第 7 周网页 Demo → 第 8 周评估改进 → 第 9 周最终报告。每周任务会在 `progress/` 中留下记录。

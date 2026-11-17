# 零售数据 AI 分析助手

《大模型原理与技术》2026 年课程项目，选择 **06-Data-Processing（数据处理及统计）** 方向。

最终目标：上传零售交易 CSV 后，自动清洗数据、计算销售指标、生成图表、完成一项简单统计检验；本地小模型作为轻量 Agent 选择并调用预设分析工具，再根据工具返回的真实结果输出 Markdown 分析报告。项目按九周逐步开发；**当前已完成前三周（读取、清洗、基础指标）**，还没有图表、Agent、报告或网页。

## 已完成内容

- `src/load_data.py`：读取 CSV 或 Excel，显示读取行数、列名、数据类型和各列缺失值数量。
- `src/clean.py`：清洗数据，统计并移除重复、缺失、取消订单、非正数数量/价格五类问题行。
- `tests/test_clean.py`：清洗规则的单元测试。
- `src/features.py`：计算每行销售额、交易月份和订单金额。
- `src/analyze.py`：汇总订单、月份、热门商品和国家销售额。
- `tests/test_analyze.py`：金额计算与汇总规则的单元测试。
- `data/sample.csv`：自造的小样例，用于检查脚本，不代表真实实验数据。
- `data/README.md`：真实数据来源和放置方法。
- `progress/week01.md`、`progress/week02.md`、`progress/week03.md`：前三周的实际运行记录。

## 安装与运行（Windows PowerShell）

先安装 Python 3.10 或更新版本，并确认终端中的 `python --version` 能正常显示版本号。然后在本项目目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.load_data --input data/sample.csv
python -m src.clean --input data/sample.csv
python -m src.analyze --input data/sample.csv
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

## 第三周：计算基础指标

分析命令会先复用第二周规则清洗数据，再计算和输出以下指标：

| 指标 | 定义 |
|---|---|
| 每行销售额 `Sales` | `Quantity × UnitPrice` |
| 交易月份 `InvoiceMonth` | 从 `InvoiceDate` 提取的 `YYYY-MM` |
| 订单金额 `OrderTotal` | 同一 `InvoiceNo` 下各行销售额之和 |
| 月度销售额 | 同一交易月份的销售额之和 |
| 热门商品 | 按 `StockCode + Description` 汇总，默认按销售额降序取前 10，同时显示销量 |
| 国家销售额 | 同一 `Country` 的销售额之和，按销售额降序 |

运行样例、真实数据和测试：

```powershell
python -m src.analyze --input data/sample.csv
python -m src.analyze --input 'data/raw/Online Retail.xlsx' --limit 5000 --top-n 10
python -m pytest -q
```

`--top-n` 控制显示的热门商品数量。对真实数据使用 `--limit` 时，汇总只代表本次读取的数据；正式全量结果应去掉该参数。

本项目已用真实数据前 5,000 行完成联调：读取 5,000 行，清洗后保留 3,646 行，得到 248 个订单；相关汇总和三条手算核对见 `progress/week03.md`。这些数字是限量调试结果，不应写成全量结论。当前命令会打印所有订单，全量运行时终端内容较长。

## 数据和提交原则

真实数据来自 [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)。下载方法见 [data/README.md](data/README.md)。原始大数据放在 `data/raw/`，该目录被 `.gitignore` 排除，不上传项目仓库。不要把密码、密钥或个人敏感信息提交到公开仓库。

## 九周路线

第 1 周读取数据 → 第 2 周清洗 → 第 3 周指标 → 第 4 周图表与检验 → 第 5 周本地模型报告 → 第 6 周一键流程 → 第 7 周网页 Demo → 第 8 周评估改进 → 第 9 周最终报告。每周任务会在 `progress/` 中留下记录。

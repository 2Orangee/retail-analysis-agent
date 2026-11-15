# 零售数据 AI 分析助手

《大模型原理与技术》2026 年课程项目，选择 **06-Data-Processing（数据处理及统计）** 方向。

最终目标：上传零售交易 CSV 后，自动清洗数据、计算销售指标、生成图表、完成一项简单统计检验；本地小模型作为轻量 Agent 选择并调用预设分析工具，再根据工具返回的真实结果输出 Markdown 分析报告。项目按九周逐步开发；**第一周只实现数据读取与检查**，还没有 Agent、报告或网页。

## 第一周已有内容

- `src/load_data.py`：读取 CSV 或 Excel，显示读取行数、列名、数据类型和各列缺失值数量。
- `data/sample.csv`：自造的小样例，用于检查脚本，不代表真实实验数据。
- `data/README.md`：真实数据来源和放置方法。
- `progress/week01.md`：第一周进度与待实测项目。

## 安装与运行（Windows PowerShell）

先安装 Python 3.10 或更新版本，并确认终端中的 `python --version` 能正常显示版本号。然后在本项目目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.load_data --input data/sample.csv
```

如果不使用虚拟环境，也可以先执行 `python -m pip install -r requirements.txt`，再运行最后一条命令。PowerShell 若不允许激活虚拟环境，可直接运行 `.\.venv\Scripts\python.exe -m src.load_data --input data/sample.csv`。

真实数据下载并放入 `data/raw/` 后，可先读取前 5,000 行，避免第一步耗时过长：

```powershell
python -m src.load_data --input 'data/raw/Online Retail.xlsx' --limit 5000
```

`--limit` 显示的是**本次读取行数**，不是整个文件的总行数。读取整个文件时去掉 `--limit`。支持 `.csv`、`.xlsx`、`.xls`，但 `.xls` 可能需要额外依赖；本项目主数据为 `.xlsx`。

## 数据和提交原则

真实数据来自 [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)。下载方法见 [data/README.md](data/README.md)。原始大数据放在 `data/raw/`，该目录被 `.gitignore` 排除，不上传项目仓库。不要把密码、密钥或个人敏感信息提交到公开仓库。

## 九周路线

第 1 周读取数据 → 第 2 周清洗 → 第 3 周指标 → 第 4 周图表与检验 → 第 5 周本地模型报告 → 第 6 周一键流程 → 第 7 周网页 Demo → 第 8 周评估改进 → 第 9 周最终报告。每周任务会在 `progress/` 中留下记录。

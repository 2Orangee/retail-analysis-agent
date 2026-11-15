# Week 01：项目骨架与数据读取

## 已准备

- 建立项目目录、依赖清单和 Git 忽略规则。
- 编写 CSV/Excel 读取与缺失值检查脚本。
- 添加人工演示样例和 UCI 数据下载说明。

## 等待本人完成

- [ ] 在课程 06 方向对应 Issue 留言报名：`学号+姓名+选题`。报名内容需本人确认后发布。
- [x] 在笔记本安装 Python 3.10+，并运行 `python --version`（已确认安装 Python 3.13.17）。
- [x] 下载真实数据到 `data/raw/Online Retail.xlsx`，并成功读取前 5,000 行。
- [x] 运行 `python -m src.load_data --input data/sample.csv`（使用虚拟环境的 Python，用户已反馈输出）。
- [x] 运行 `.\.venv\Scripts\python.exe -m src.load_data --input 'data/raw/Online Retail.xlsx' --limit 5000`。
- [x] 把已得到的实际输出补充到下方；完整数据尚未读取。

## 本机实测记录（待填写）

- 运行日期：
- Python 版本：3.13.17（安装路径已核对；当前工具终端的 `python` 别名仍指向 WindowsApps）
- 样例数据读取结果：7 行、8 列；`CustomerID` 缺失 1 个，其余列缺失 0 个。与人工样例预期一致。
- 真实数据读取结果：前 5,000 行、8 列；字段为 `InvoiceNo`、`StockCode`、`Description`、`Quantity`、`InvoiceDate`、`UnitPrice`、`CustomerID`、`Country`。`Description` 缺失 12 个，`CustomerID` 缺失 1,205 个，其余字段在这 5,000 行中缺失 0 个。`InvoiceDate` 识别为 `datetime64[ns]`。这些数字仅针对本次读取的前 5,000 行，不代表全量数据。
- 遇到的问题与解决方式：首次在 `C:\Windows\System32` 运行相对路径命令，找不到项目虚拟环境；切换到 `E:\LLM-Course\retail-analysis-agent` 后成功运行。
- Git commit / PR 链接（正式提交后填写）：

## 下一周

制定清洗规则，处理缺失值、取消订单和异常价格/数量，并记录每一步保留或排除的行数。

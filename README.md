## Table Recognition Metric
<p align="left">
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/python->=3.6,<3.12-aff.svg"></a>
    <a href="https://pepy.tech/project/table-recognition-metric"><img src="https://static.pepy.tech/personalized-badge/table-recognition-metric?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
<a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

- 该库用来评测表格识别算法效果，与[表格识别测试集](https://www.modelscope.cn/datasets/liekkas/table_recognition/summary)配套使用。
- 该评测指标目前仅用于评测算法在自己构建数据集上效果，暂无对接已知的公开数据集。
- 不同于论文中用到的公开数据集，这里构建的数据集更有针对性的，用户可根据业务具体需求，自行增删，使得在数据集上的指标更加贴近实际业务场景。
- 这里只是提供一个基准平台，会默认给出一些标注好的数据集。
- 指标计算代码参考：[PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/ppstructure/table/table_metric/table_metric.py) 和 [DAVAR-Lab-OCR](https://github.com/hikopensource/DAVAR-Lab-OCR/blob/main/davarocr/davar_table/utils/metric.py)

### 使用说明：
1. Install package by pypi.
    ```bash
    pip install table_recognition_metric
    ```
2. Run by command line.
   - Usage:
       ```bash
       $ table_recognition_metric -h
       usage: table_recognition_metric [-h] [-gt GT_HTML] [-pred PRED_HTML]

       optional arguments:
       -h, --help            show this help message and exit
       -gt GT_HTML, --gt_html GT_HTML
       -pred PRED_HTML, --pred_html PRED_HTM
       ```
   - Example:
       ```bash
       $ table_recognition_metric -gt '<html><body><table><tr><td>购买方</td><td colspan="5">纳税人识别号地址、电记开户行及账号</td><td>密码区</td><td colspan="4"></td></tr><tr><td colspan="2">货物或应税劳务、服务名称理肤泉清痘旅行装控油祛痘调节水油平衡理肤泉特安舒缓修护乳40ml合计</td><td>规格型号</td><td>单位</td><td>11</td><td colspan="3"></td><td></td><td>税率17%17%</td><td></td></tr><tr><td colspan="2">价税合计（大写）</td><td colspan="9"></td></tr><tr><td>销售方</td><td colspan="5">纳税人识别号地址、电话开户行及账号</td><td>备注</td><td colspan="4"></td></tr></table></body></html>' -pred ''

       # 0.0
       ```
3. Run by script.
    ```python
    from table_recognition_metric import TEDS

    teds = TEDS()

    gt_html = '<html><body><table><tr><td>购买方</td><td colspan="5">纳税人识别号地址、电记开户行及账号</td><td>密码区</td><td colspan="4"></td></tr><tr><td colspan="2">货物或应税劳务、服务名称理肤泉清痘旅行装控油祛痘调节水油平衡理肤泉特安舒缓修护乳40ml合计</td><td>规格型号</td><td>单位</td><td>11</td><td colspan="3"></td><td></td><td>税率17%17%</td><td></td></tr><tr><td colspan="2">价税合计（大写）</td><td colspan="9"></td></tr><tr><td>销售方</td><td colspan="5">纳税人识别号地址、电话开户行及账号</td><td>备注</td><td colspan="4"></td></tr></table></body></html>'
    pred_html = '<html><body><table><tr><td>购买方</td><td colspan="5">纳税人识别号地址、电记开户行及账号</td><td>密码区</td><td colspan="4"></td></tr><tr><td colspan="2">货物或应税劳务、服务名称理肤泉清痘旅行装控油祛痘调节水油平衡理肤泉特安舒缓修护乳40ml合计</td><td>规格型号</td><td>单位</td><td>11</td><td colspan="3"></td><td></td><td>税率17%17%</td><td></td></tr><tr><td colspan="2">价税合计（大写）</td><td colspan="9"></td></tr><tr><td>销售方</td><td colspan="5">纳税人识别号地址、电话开户行及账号</td><td>备注</td><td colspan="4"></td></tr></table></body></html>'

    score = teds(gt_html, pred_html)
    print(score)
    ```

#### 数据集上评测
- 这里以`rapid-table`在表格数据集[liekkas/table_recognition](https://www.modelscope.cn/datasets/liekkas/table_recognition/summary)上的评测代码。大家可以以此类推。
- 安装必要的包
    ```bash
    pip install modelscope==1.5.2
    pip install rapid_table
    ```
- 运行测试
    ```python
    from modelscope.msdatasets import MsDataset
    from rapid_table import RapidTable

    from table_recognition_metric import TEDS

    test_data = MsDataset.load(
        "table_recognition",
        namespace="liekkas",
        subset_name="default",
        split="test",
    )
    table_engine = RapidTable()
    teds = TEDS()

    content = []
    for one_data in test_data:
        img_path = one_data.get("image:FILE")
        gt = one_data.get("label")

        pred_str, _ = table_engine(img_path)
        scores = teds(gt, pred_str)
        content.append(scores)
        print(f"{img_path}\t{scores:.5f}")

    avg = sum(content) / len(content)
    print(avg)
    # 0.5847187558587787
    ```

## Table Recognition Metric
<p align="left">
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/python->=3.6,<3.12-aff.svg"></a>
    <a href="https://pypi.org/project/table_recognition_metric/"><img alt="PyPI" src="https://img.shields.io/pypi/v/table_recognition_metric"></a>
    <a href="https://pepy.tech/project/table-recognition-metric"><img src="https://static.pepy.tech/personalized-badge/table-recognition-metric?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
<a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

- 该库用于计算TEDS指标，用来评测表格识别算法效果。可与[魔搭-表格识别测试集](https://www.modelscope.cn/datasets/liekkas/table_recognition/summary)配套使用。
- TEDS计算代码参考：[PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/ppstructure/table/table_metric/table_metric.py) 和 [DAVAR-Lab-OCR](https://github.com/hikopensource/DAVAR-Lab-OCR/blob/main/davarocr/davar_table/utils/metric.py)

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
- 这里以[`rapid-table`](https://github.com/RapidAI/RapidStructure/blob/main/docs/README_Table.md)在表格数据集[liekkas/table_recognition](https://www.modelscope.cn/datasets/liekkas/table_recognition/summary)上的评测代码，大家可以以此类推。
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

### Tree-EditDistance-based Similarity (TEDS)
- TEDS是IBM在论文《[Image-based table recognition: data, model, and evaluation](https://arxiv.org/pdf/1911.10683)》中提出的。
- 之前提出的评测算法，主要是将一个表格的`ground truth`和`recognition result`各自展平为非空cell两两之间的邻接关系列表。然后通过比较这两个列表，来计算precision, recall和F1-score。该metric主要存在两个明显问题：
    1. 由于它只检查非空单元格之间的直接邻接关系，因此它无法检测由空单元格和超出直接邻居的单元格未对齐引起的错误；
    2. 由于它通过精准匹配来检查关系，因此它没有衡量fine-grained单元格内容识别性能的机制。
- 针对以上问题，TEDS通过以下方法予以解决：
    1. 通过在全局树结构级别检查识别结果，使其能够识别它识别所有类型的结构错误，来解决上述问题1；
    2. 当**tree-edit**的操作是节点替换时，计算对应的字符串编辑距离，来解决上述问题2。
- 计算公式：
  
   $$TEDS(T_{a}, T_{b}) = 1 - \frac{EditDist(T_{a}, T_{b})}{max(|T_{a}|, |T_{b}|)}$$

    其中， $EditDist$指的是**tree-edit distance**, $|T|$ 指的是在 $T$ 中节点的数量。一个表格还原算法在一系列测试集上识别效果可以定义为：测试集中所有样例逐个计算其**ground truth**和**predict result**之间的TEDS，最终对所有样例的TEDS求均值得到最终得分。

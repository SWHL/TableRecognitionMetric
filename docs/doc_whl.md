## table_recognition_metric
<p align="left">
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/python->=3.6,<3.12-aff.svg"></a>
    <a href="https://pepy.tech/project/table-recognition-metric"><img src="https://static.pepy.tech/personalized-badge/table-recognition-metric?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
<a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

### 1. Install package by pypi.
```bash
pip install table_recognition_metric
```
### 2. Run by command line.
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
### 3. Run by script.
```python
teds = TEDS()

gt_html = '<html><body><table><tr><td>购买方</td><td colspan="5">纳税人识别号地址、电记开户行及账号</td><td>密码区</td><td colspan="4"></td></tr><tr><td colspan="2">货物或应税劳务、服务名称理肤泉清痘旅行装控油祛痘调节水油平衡理肤泉特安舒缓修护乳40ml合计</td><td>规格型号</td><td>单位</td><td>11</td><td colspan="3"></td><td></td><td>税率17%17%</td><td></td></tr><tr><td colspan="2">价税合计（大写）</td><td colspan="9"></td></tr><tr><td>销售方</td><td colspan="5">纳税人识别号地址、电话开户行及账号</td><td>备注</td><td colspan="4"></td></tr></table></body></html>'
pred_html = '<html><body><table><tr><td>购买方</td><td colspan="5">纳税人识别号地址、电记开户行及账号</td><td>密码区</td><td colspan="4"></td></tr><tr><td colspan="2">货物或应税劳务、服务名称理肤泉清痘旅行装控油祛痘调节水油平衡理肤泉特安舒缓修护乳40ml合计</td><td>规格型号</td><td>单位</td><td>11</td><td colspan="3"></td><td></td><td>税率17%17%</td><td></td></tr><tr><td colspan="2">价税合计（大写）</td><td colspan="9"></td></tr><tr><td>销售方</td><td colspan="5">纳税人识别号地址、电话开户行及账号</td><td>备注</td><td colspan="4"></td></tr></table></body></html>'

score = teds(gt_html, pred_html)
print(score)
```
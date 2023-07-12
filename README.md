## Table Recognition Metric
<p align="left">
    <a href=""><img src="https://img.shields.io/badge/OS-Linux-pink.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/python->=3.6,<3.12-aff.svg"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

- 该库用来评测表格识别算法效果，与[表格识别测试集](https://www.modelscope.cn/datasets/liekkas/table_recognition/summary)配套使用。
- 该评测指标目前仅用于评测算法在自己构建数据集上效果，暂无对接已知的公开数据集。
- 不同于论文中用到的公开数据集，这里构建的数据集更有针对性的，用户可根据业务具体需求，自行增删，使得在数据集上的指标更加贴近实际业务场景。
- 这里只是提供一个基准平台，会默认给出一些标注好的数据集。
- 指标计算代码参考：[PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/ppstructure/table/table_metric/table_metric.py) 和 [DAVAR-Lab-OCR](https://github.com/hikopensource/DAVAR-Lab-OCR/blob/main/davarocr/davar_table/utils/metric.py)

#### TODO
- [ ] 配置`setup.py`文件
- [ ] 编写单元测试
- [ ] 打包为whl，上传到pypi
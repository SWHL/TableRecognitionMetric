# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from modelscope.msdatasets import MsDataset
from rapid_table import RapidTable

from table_recognition_metric import TEDS

test_data = MsDataset.load(
    'table_recognition', namespace='liekkas', subset_name='default', split='test'
)
table_engine = RapidTable()
teds = TEDS()

content = []
for one_data in test_data:
    img_path = one_data.get('image:FILE')
    gt = one_data.get('label')

    pred_str, _ = table_engine(img_path)

    scores = teds(gt, pred_str)

    print(f'{img_path}\t{scores:.5f}')

    content.append(scores)

avg = sum(content) / len(content)
print(avg)

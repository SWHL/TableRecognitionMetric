# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import numpy as np
from datasets import load_dataset
from rapid_table import RapidTable
from tqdm import tqdm

from table_recognition_metric import TEDS

dataset = load_dataset("SWHL/table_rec_test_dataset")
test_data = dataset["test"]

table_engine = RapidTable()
teds = TEDS(structure_only=True)

content = []
for one_data in tqdm(test_data):
    img = one_data.get("image")
    gt = one_data.get("html")

    pred_str, _, _ = table_engine(np.array(img))

    scores = teds(gt, pred_str)
    content.append(scores)

avg = sum(content) / len(content)
print(f"TEDS: {avg:.5f}")

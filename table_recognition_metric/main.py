# Copyright 2020 IBM
# Author: peter.zhong@au1.ibm.com
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the Apache 2.0 License.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Apache 2.0 License for more details.
import argparse
from collections import deque
from typing import List, Optional, Tuple

from apted import APTED, Config
from apted.helpers import Tree
from Levenshtein import distance
from lxml import etree, html
from lxml.html import HtmlElement


class TEDS:
    """Tree Edit Distance basead Similarity"""

    def __init__(
        self, structure_only: bool = False, ignore_nodes: Optional[str] = None
    ):
        self.structure_only = structure_only
        self.ignore_nodes = ignore_nodes
        self.__tokens__: List[str] = []

    def __call__(self, pred: str, gt: str) -> float:
        """Computes TEDS score between the prediction and the ground truth of a
        given sample

        Args:
            pred (str): The predict html string of the table image.
            gt (str): The ground truth html string of the table image.

        Returns:
            float: TEDS score
        """
        if (not pred) or (not gt):
            return 0.0

        parser = html.HTMLParser(remove_comments=True, encoding="utf-8")
        pred_element: HtmlElement = html.fromstring(pred, parser=parser)
        gt_element: HtmlElement = html.fromstring(gt, parser=parser)

        xpath_ele = "body/table"
        if pred_element.xpath(xpath_ele) and gt_element.xpath(xpath_ele):
            pred_element = pred_element.xpath(xpath_ele)[0]
            gt_element = gt_element.xpath(xpath_ele)[0]

            if self.ignore_nodes:
                etree.strip_tags(pred_element, *self.ignore_nodes)
                etree.strip_tags(gt_element, *self.ignore_nodes)

            tree_pred = self.load_html_tree(pred_element)
            tree_true = self.load_html_tree(gt_element)
            distance = APTED(
                tree_pred, tree_true, CustomConfig()
            ).compute_edit_distance()

            n_nodes_pred = len(pred_element.xpath(".//*"))
            n_nodes_true = len(gt_element.xpath(".//*"))
            n_nodes = max(n_nodes_pred, n_nodes_true)
            return 1.0 - (float(distance) / n_nodes)
        return 0.0

    def tokenize(self, node: HtmlElement):
        """Tokenizes table cells"""
        self.__tokens__.append(f"<{node.tag}>")

        if node.text is not None:
            self.__tokens__ += list(node.text)

        for n in node.getchildren():
            self.tokenize(n)

        if node.tag != "unk":
            self.__tokens__.append(f"</{node.tag}>")

        if node.tag != "td" and node.tail is not None:
            self.__tokens__ += list(node.tail)

    def load_html_tree(
        self, node: HtmlElement, parent: Optional[HtmlElement] = None
    ) -> Optional[HtmlElement]:
        """Converts HTML tree to the format required by apted"""
        global __tokens__
        if node.tag == "td":
            if self.structure_only:
                cell = []
            else:
                self.__tokens__ = []
                self.tokenize(node)
                cell = self.__tokens__[1:-1].copy()

            new_node = TableTree(
                node.tag,
                int(node.attrib.get("colspan", "1")),
                int(node.attrib.get("rowspan", "1")),
                cell,
                *deque(),
            )
        else:
            new_node = TableTree(node.tag, None, None, None, *deque())

        if parent is not None:
            parent.children.append(new_node)

        if node.tag != "td":
            for n in node.getchildren():
                self.load_html_tree(n, new_node)

        if parent is None:
            return new_node
        return None


class TableTree(Tree):
    def __init__(
        self,
        tag: str,
        colspan: Optional[int] = None,
        rowspan: Optional[int] = None,
        content: Optional[List[str]] = None,
        *children: Tuple[Tree],
    ):
        self.tag = tag
        self.colspan = colspan
        self.rowspan = rowspan
        self.content = content
        self.children = list(children)


class CustomConfig(Config):
    @staticmethod
    def maximum(*sequences):
        """Get maximum possible value"""
        return max(map(len, sequences))

    def normalized_distance(self, *sequences):
        """Get distance from 0 to 1"""
        return float(distance(*sequences)) / self.maximum(*sequences)

    def rename(self, node1: TableTree, node2: TableTree) -> float:
        """Compares attributes of trees"""
        if (
            (node1.tag != node2.tag)
            or (node1.colspan != node2.colspan)
            or (node1.rowspan != node2.rowspan)
        ):
            return 1.0

        if node1.tag == "td":
            if node1.content or node2.content:
                return self.normalized_distance(node1.content, node2.content)

        return 0.0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-steds", "--structure_only", action="store_true", default=False
    )
    parser.add_argument("-gt", "--gt_html", type=str, default=None)
    parser.add_argument("-pred", "--pred_html", type=str, default=None)
    args = parser.parse_args()

    if args.gt_html is None:
        raise ValueError("gt_html must be non-empty.")

    if args.pred_html is None:
        raise ValueError("pred_html must be non-empty.")

    teds = TEDS(structure_only=args.structure_only)

    score = teds(args.gt_html, args.pred_html)
    print(score)


if __name__ == "__main__":
    main()

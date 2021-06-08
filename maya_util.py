# -*- coding: utf-8 -*-
# author:yangtao
# time: 2021/04/16

import pymel.core as pm


def get_selection():
    return pm.ls(selection=True)


def get_one_selection():
    selected = get_selection()
    if selected:
        return selected[0]


def get_transform_node():
    return pm.ls(type="transform")


def select_node(node_name):
    if node_name:
        pm.select(node_name, replace=True)
        pm.viewFit()
        #pm.select(hi=True)
        #pm.mel.eval("fitPanel -selected;")


def get_relatives_transform(node):
    return pm.listRelatives(node, allDescendents=True, type="transform")

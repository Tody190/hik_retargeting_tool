# -*- coding: utf-8 -*-
# author:yangtao
# time: 2023/03/05

import os
import sys

current_path = os.path.abspath(r".\hik_retargeting_tool")
if current_path not in sys.path:
    sys.path.append(current_path)

import hik_retargeting_tool
#reload(hik_retargeting_tool.main)

hik_retargeting_tool.main.load_ui()

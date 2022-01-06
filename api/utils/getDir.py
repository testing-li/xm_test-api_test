#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# 获取utils目录
utilsDir = os.path.dirname(__file__)
# 截取项目路径
proDir = os.path.dirname(utilsDir)
# 获取core目录
coreDir = f'{proDir}/core'

print(proDir)
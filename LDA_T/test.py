#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: ake
@software: PyCharm Community Edition
@time: 2016/4/26 10:40
"""
import nltk
import numpy as np
import matplotlib.pyplot as plt
from nltk.corpus import brown
import jieba.posseg as pseg
import webbrowser

import re

noo = [("money", "NN"), ("market", "NN"), ("fund", "NN")]
grammar = r'NP: {<NN>+}'
cp = nltk.RegexpParser(grammar)
print(cp.parse(noo))

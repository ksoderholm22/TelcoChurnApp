#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 12:23:24 2022

@author: disha.dubey
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

#function to load data
def load_data(filename) -> pd.DataFrame:
    dir = Path.cwd().parent
    path = dir/filename
    print(path)
    if filename.split('.')[1]== 'xlsx':
        data = pd.read_excel(path)
    elif filename.split('.')[1]== 'csv':
        data = pd.read_csv(path)
    else:
        'Check file format'
    return data

#rounding function
def myround(x, base):
    return base * round(x/base)

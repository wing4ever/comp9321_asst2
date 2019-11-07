#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 7 21:37:55 2019

@author: blueberry

"""

import pandas as pd
import numpy as np


df = pd.read_csv('Airbnb_Sydney_Calendar.csv')

df.drop("adjusted_price",axis =1,inplace=True)

df['date'] = pd.to_datetime(df['date'])
print(df['date'].head())

end_time = pd.to_datetime('2019-11-01')

df = df[df.date<end_time]
df.fillna(0, inplace=True)


print(df.head().to_string())
print(len(df))

df.to_csv('example.csv')


# -*- coding: UTF-8 -*-
# @Time: 5/12/2022 9:25 AM
# @File: test_demo.py
# @Software: PyCharm
temperature_list = [71.07, 70.32, 70.51, '', '', '', 50.22]
temperature_list_new = []
for temperature in temperature_list:
    if type(temperature) == float:
        temperature_list_new.append(temperature)
print(temperature_list_new)
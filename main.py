#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/5 11:57 AM
# @Author  : sunwenjun
# @File    : main.py
# @brief: test
from read_pdf import extract_text_from_pdf
from esdemo import EsDemo

filename = "./RAG.pdf"
text_list = extract_text_from_pdf(filename=filename, min_line_length=10)


index_name = "test_index"
esdemo = EsDemo(index_name=index_name)

# 往es里添加数据
esdemo.add_data_to_es(text_list)

# 查询
query = "Retrieval"
results = esdemo.search(query, 5)
for res in results:
    print(res)

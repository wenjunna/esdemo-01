#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/4 1:24 PM
# @Author  : sunwenjun
# @File    : esdemo.py
# @brief: esdemo

from keywords import keywords
from elasticsearch import Elasticsearch, helpers


class EsDemo(object):
    def __init__(self, index_name="test_index"):
        # 创建Elasticsearch连接
        self.es = Elasticsearch(
            hosts=['https://localhost:9200'],  # 服务地址与端口
            basic_auth=("elastic", "N-sf6R*O0Ur344otTfzc"),  # 用户名，密码
            ca_certs="/Users/sunwenjun/data/elastic8/http_ca.crt"  # 证书
        )
        self.index_name = index_name  # 定义索引名称

    def add_data_to_es(self, text_list=["text1", "text2"]):
        '''
        建立索引，并往索引里添加数据
        param text_list: [] 需要检索的文本列表
        :return:
        '''

        # 如果索引已存在，删除它
        if self.es.indices.exists(index=self.index_name):
            self.es.indices.delete(index=self.index_name)

        # 创建索引
        self.es.indices.create(index=self.index_name)

        # 灌库指令
        actions = []
        for text in text_list:
            action = {
                "_index": self.index_name,
                "_source": {
                    "keywords": keywords(text),
                    "text": text
                }
            }

            actions.append(action)

        # 文本灌库
        res = helpers.bulk(self.es, actions)
        return res

    def search(self, query="text", top_n=3):
        '''
        查询
        :param query:
        :param top_n:
        :return:
        '''
        search_query = {
            "match":
                {"keywords": keywords(query)}
        }
        search_res = self.es.search(index=self.index_name, query=search_query, size=top_n)
        print('search_res', search_res)

        results = [hit["_source"]["text"] for hit in search_res["hits"]["hits"]]
        print('results', results)
        return results

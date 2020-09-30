#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 @Author Tabuyos
 @Time 2020/9/16 14:00
 @Site www.tabuyos.com
 @Email tabuyos@outlook.com
 @Description
"""
import json


def convert_json_to_python(data):
    return json.loads(data)


def convert_python_to_json(data):
    return json.dumps(data)


class OperateJson:

    def __init__(self, file_path):
        self.file_path = file_path

    def load_json(self):
        with open(self.file_path, 'r', encoding='UTF-8') as file_str:
            data = json.load(file_str)
        return data

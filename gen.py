#!/usr/bin/python
#-*- coding:utf-8 -*-

import os

DIR="./template"
TMP="./tmp"

def find_ydl_project(path):
    # target_path
    # target_pathtarget-path-intf
    # target_path/target-pathr-service
    # 如果满足当前的目录结构 就认为是YDL project
    pass

# cp文件
def cpfile(from,to):
    pass

# 编译内容
def compile_content(dist,content,vars):
    pass

# 获取编译后的名字
def get_real_name(name,vars):
    pass
# gen
def gen():
    for root, dirs, files in os.walk(DIR, False):
        print(files)

if __name__=="__main__":
    gen()

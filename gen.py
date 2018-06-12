#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import shutil
import argparse

DIR = "./template"
TMP = "./tmp"


def parse_ydl_project(path):
    # target_path
    # target_pathtarget-path-intf
    # target_path/target-pathr-service
    # 如果满足当前的目录结构 就认为是YDL project
    name = os.path.realpath(path)
    abs_path = name.split("/")[0:-1]
    identity = name.split("/")[-1]
    project_prefix = "ydl-{}".format(identity.split("-")[0])
    package1 = project_prefix.split("-")[0]
    package2 = project_prefix.split("-")[1]

    interface_path = "/".join(abs_path + [identity, project_prefix, "{}-intf".format(project_prefix)])
    service_path = "/".join(abs_path + [identity, project_prefix, "{}-service".format(project_prefix)])

    intf_facade_path = "{}/{}".format(interface_path, "src/main/java/com/{}/{}/intf/facade".format(package1, package2))
    intf_req_dto_path = "{}/{}".format(interface_path,
                                       "src/main/java/com/{}/{}/intf/dto/request".format(package1, package2))
    intf_resp_dto_path = "{}/{}".format(interface_path,
                                        "src/main/java/com/{}/{}/intf/dto/response".format(package1, package2))
    intf_po_path = "{}/{}".format(interface_path, "src/main/java/com/{}/{}/intf/po".format(package1, package2))

    service_facade_impl_path = "{}/{}".format(service_path,
                                              "src/main/java/com/{}/{}/service/facade".format(package1, package2))
    service_intf_biz_path = "{}/{}".format(service_path,
                                           "src/main/java/com/{}/{}/service/biz".format(package1, package2))
    service_biz_impl_path = "{}/{}".format(service_path,
                                           "src/main/java/com/{}/{}/service/biz/impl".format(package1, package2))
    service_dao_path = "{}/{}".format(service_path, "src/main/java/com/{}/{}/service/dao".format(package1, package2))
    service_sql_xml_path = "{}/{}".format(service_path, "src/main/resources/sqlmap")

    # print("Interface facade path is {}".format(intf_facade_path))
    # print("Interface req dto path is {}".format(intf_req_dto_path))
    # print("Interface resp dto path is {}".format(intf_resp_dto_path))
    # print("Interface po path is {}".format(intf_po_path))
    # print("Service facade impl path is {}".format(service_facade_impl_path))
    # print("Service biz intf  path is {}".format(service_intf_biz_path))
    # print("Service biz impl path is {}".format(service_biz_impl_path))
    # print("Service dao path is {}".format(service_dao_path))
    # print("Service sql xml path is {}".format(service_sql_xml_path))

    d = dict()

    d["intf_facade_path"] = intf_facade_path
    d["intf_req_dto_path"] = intf_req_dto_path
    d["intf_resp_dto_path"] = intf_resp_dto_path
    d["intf_po_path"] = intf_po_path

    d["service_intf_biz_path"] = service_intf_biz_path
    d["service_facade_impl_path"] = service_facade_impl_path
    d["service_biz_impl_path"] = service_biz_impl_path
    d["service_sql_xml_path"] = service_sql_xml_path
    d["service_dao_path"] = service_dao_path

    for id, path in d.iteritems():
        if (not os.path.exists(path)):
            print("请提供正确的ydl project {}".format(path))
            return False

    return d


# cp文件
def safe_cpfile(f, target_path_map, res_name):
    res_name = res_name[0].upper() + res_name[1:]

    if f is None:
        print("Sorry 源文件不存在")
        exit(-1)

    print("-------------------------------------")
    print("开始copy 文件{}".format(f))
    print("-------------------------------------")


    identity = f.split("/")[-1]
    categories_map = dict()
    categories_map["{}Facade.java".format(res_name)] = "intf_facade_path"
    categories_map["{}RespDto.java".format(res_name)] = "intf_resp_dto_path"
    categories_map["{}ReqDto.java".format(res_name)] = "intf_req_dto_path"
    categories_map["{}Mapper.java".format(res_name)] = "service_dao_path"
    categories_map["{}FacadeImpl.java".format(res_name)] = "service_facade_impl_path"
    categories_map["{}Biz.java".format(res_name)] = "service_intf_biz_path"
    categories_map["{}BizImpl.java".format(res_name)] = "service_biz_impl_path"
    categories_map["{}Mapper.xml".format(res_name)] = "service_sql_xml_path"
    categories_map["{}.java".format(res_name)] = "intf_po_path"

    target_path = target_path_map[categories_map[identity]]

    if (not os.path.isdir(target_path)):
        print("目标 {} 不存在".format(target_path))
        exit(-1)


    try:
        shutil.move(f, target_path)
    except Exception as e:

        print("无法移动 [{}] -_-".format(e.message))
        exit(-1)


    print("move 当前的文件{} 到 {}".format(f, target_path))


# 编译内容
def compile_content(compile_table, origin, tmp):

    if not os.path.isdir(tmp):
        os.mkdir(tmp)

    identity = os.path.realpath(origin).split("/")[-1]
    identity = "{}/{}".format(tmp, compile(identity, compile_table))

    with open(origin, "r+") as f:
        body = f.read()

    with open(identity, "w+") as f:
        f.write(compile(body, compile_table))

    print("--------------------------------")
    print("成功编译文件 {} [{}]".format(identity, len(body)))
    print("--------------------------------")
    return identity


# 获取编译后的名字
def compile(body, compile_table):
    for d, v in compile_table.iteritems():
        body = body.replace(d, v)

    return body


# gen
def gen(res_name, look_path):

    clean_tmp()

    res_name = res_name[0].upper() + res_name[1:]

    print("----------------------------------")
    print("你的资源名称为 {}".format(res_name))
    print("----------------------------------")

    PROJECT_TARGET_PATH = parse_ydl_project(look_path)

    if (PROJECT_TARGET_PATH):
        print("解析YDL Project 成功！")
    else:
        print("对不起，你提供的project 无法识别！")
        exit(-1)

    compile_table = dict()
    compile_table['${PLACE}'] = "{}{}".format(res_name[0].upper(), res_name[1:])
    compile_table['${PLACE_VAR}'] = "{}{}".format(res_name[0].lower(), res_name[1:])

    print("--------------------------------------")
    print("编译常量表")
    print("--------------------------------------")

    # 编译文件
    for root, dirs, files in os.walk(DIR, False):
        for file in files:
            if (file[0] == "$"):
                compiled_file = compile_content(compile_table, os.path.join(root, file), TMP)
                safe_cpfile(compiled_file, PROJECT_TARGET_PATH, res_name)


def clean_tmp():
    for root, dirs, files in os.walk(TMP, False):
        for file in files:
            os.remove(os.path.join(root, file))
    print("清空目录 {}".format(TMP))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto create Resource for ydl java project")
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose mode')

    parser.add_argument("resource_name")
    parser.add_argument("project_path")
    args = parser.parse_args()
    project_path = args.project_path
    resource_name = args.resource_name

    gen(resource_name, project_path)

#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import shutil
import argparse
import xml.etree.ElementTree as ET
import re

DIR = os.path.join(".","template")
TMP = os.path.join(".","tmp")
JAR_PATH = os.path.join(".","jar")
MYBATIS_GEN_JAVA_PATH = "{}/java".format(TMP)
PO = ""


def parse_ydl_project(path):
    """
    target_path
    target_pathtarget-path-intf
    target_path/target-pathr-service
    如果满足当前的目录结构 就认为是YDL project
    :param path:
    :return:
    """
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

    service_sql_mybatis_generator_config_path = "{}/{}".format(service_path,
                                                               "src/main/resources/mybatis/generatorConfig.xml")

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
    d["mybatis_config_path"] = service_sql_mybatis_generator_config_path
    d["base_path"] = "/".join(abs_path + [identity, project_prefix])

    for id, path in d.iteritems():
        if (not os.path.exists(path)):
            print("请提供正确的ydl project {}".format(path))
            return False

    return d


# cp文件
def safe_cpfile(f, target_path_map, res_name):
    """
    cp文件到project path

    :param f:
    :param target_path_map:
    :param res_name:
    :return:
    """
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


def is_dto(path):
    return path[-8:] == "Dto.java"


def is_po(res_name, identity):
    """
    检测是否是po

    :param res_name:
    :param identity:
    :return:
    """
    res_name = res_name[0].upper() + res_name[1:]

    print("检测po {}  {}".format(res_name, identity.split("/")[-1]))

    return "{}.java".format(res_name) == identity.split("/")[-1]


def config_mybatis(res_name, table_name, mybatis_config_path):
    """
    重写mybatis generatorConfig

    :param res_name:
    :param table_name:
    :param mybatis_config_path:
    :return:
    """

    print("-----------------------------------------------")
    print("修改 {}".format(mybatis_config_path))
    print("-----------------------------------------------")

    head = """
    <!DOCTYPE generatorConfiguration PUBLIC "-//mybatis.org//DTD MyBatis Generator Configuration 1.0//EN" "http://mybatis.org/dtd/mybatis-generator-config_1_0.dtd">
    """

    root = ET.parse(mybatis_config_path)
    e = ET.Element("table", tableName=table_name, domainObjectName=res_name, enableCountByExample="false",
                   enableDeleteByExample="false", enableSelectByExample="false", enableUpdateByExample="false",
                   selectByExampleQueryId="false")

    classPathEntry = ET.Element("classPathEntry", location="{}/mysql-connector-java-5.1.25.jar".format(JAR_PATH))
    context = root.find("context")

    root.getroot().insert(0, classPathEntry)
    context.append(e)
    po_path = context.find("javaModelGenerator").get("targetPackage")

    java_model_generator = context.find("javaModelGenerator")
    java_model_generator.set("targetProject", "{}/java/".format(TMP))

    tmp_mybatis_path = os.path.join(TMP, "generatorConfig.xml")

    root.write(tmp_mybatis_path, encoding="utf-8")

    with open(tmp_mybatis_path, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(head + content)

    return {"tmp_mybatis_path": tmp_mybatis_path, "po_path": po_path}


def gen_po(res_name, project_target_path):
    """
    生成po 调用mybatis 的generator

    :param res_name:
    :param project_target_path:
    :return:
    """
    mybatis_config_path = project_target_path['mybatis_config_path']

    if (not os.path.exists(mybatis_config_path)):
        print("Mybatis 路径有误")
        exit(-1)

    tables_name = get_table_name(res_name)

    local_mybatis_config = config_mybatis(res_name, tables_name, mybatis_config_path)

    local_mybatis_config_path = local_mybatis_config["tmp_mybatis_path"]

    po_path = "{}/{}".format(MYBATIS_GEN_JAVA_PATH, "/".join(local_mybatis_config["po_path"].split(".")))

    print(po_path)
    gen_po_cmd = """
    java -jar {}/mybatis-generator-core-1.3.6.jar -configfile {}  -overwrite
    """.format(JAR_PATH, local_mybatis_config_path)

    print("----------------------------------------")
    print(gen_po_cmd)
    print("----------------------------------------")
    os.system(gen_po_cmd)

    mybatis_gen_po_path = "{}/{}.java".format(po_path, res_name)

    if (not os.path.exists(mybatis_gen_po_path)):
        print("无法获取到Mybatis 生成的po文件")
        exit(-1)

    with open(mybatis_gen_po_path, "r+") as f:

        po = f.read()

    return po


def compile_content(res_name, compile_table, origin, tmp, project_target_path):
    """
    编译内容

    :param res_name:
    :param compile_table:
    :param origin:
    :param tmp:
    :param project_target_path:
    :return:
    """
    global PO

    res_name = get_res_name(res_name)
    if not os.path.isdir(tmp):
        os.mkdir(tmp)

    identity = os.path.realpath(origin).split("/")[-1]
    identity = "{}/{}".format(tmp, compile(identity, compile_table))

    with open(origin, "r+") as f:
        body = f.read()

    with open(identity, "w+") as f:
        f.write(compile(body, compile_table))

    # 检测如果当前的文件是PO的话，使用mybatis 生成po
    if is_po(res_name, identity):
        print("发现po {}".format(identity))

        with open(identity, "w+") as f:
            po_body = gen_po(res_name, project_target_path)
            PO = po_body
            f.write(po_body)

    print("--------------------------------")
    print("成功编译文件 {} [{}]".format(identity, len(body)))
    print("--------------------------------")

    return identity


def compile(body, compile_table):
    """
    编译

    :param body:
    :param compile_table:
    :return:
    """
    for d, v in compile_table.iteritems():
        body = body.replace(d, v)

    return body


def clean_tmp():
    """
    清空临时目录

    :return:
    """
    if (os.path.isdir(TMP)):
        shutil.rmtree(TMP)

    os.mkdir(TMP)
    os.mkdir(MYBATIS_GEN_JAVA_PATH)

    print("清空目录 {}".format(TMP))


def get_res_name(res_name):
    name = underline2hump(res_name)

    return name[0].upper() + name[1:]


def hump2underline(hunp_str):
    '''
    驼峰形式字符串转成下划线形式
    :param hunp_str: 驼峰形式字符串
    :return: 字母全小写的下划线形式字符串
    '''
    # 匹配正则，匹配小写字母和大写字母的分界位置
    p = re.compile(r'([a-z]|\d)([A-Z])')
    # 这里第二个参数使用了正则分组的后向引用
    sub = re.sub(p, r'\1_\2', hunp_str).lower()
    return sub


def underline2hump(underline_str):
    '''
    下划线形式字符串转成驼峰形式
    :param underline_str: 下划线形式字符串
    :return: 驼峰形式字符串
    '''
    # 这里re.sub()函数第二个替换参数用到了一个匿名回调函数，回调函数的参数x为一个匹配对象，返回值为一个处理后的字符串
    sub = re.sub(r'(_\w)', lambda x: x.group(1)[1].upper(), underline_str)
    return sub


def get_table_name(res_name):
    return hump2underline(res_name)


def run_tests(path):
    c = """
    cd {} && mvn clean test

    """.format(path)
    if os.path.isdir(path) and os.path.exists(os.path.join(path, "pom.xml")):
        os.system(c)


def gen(res_name, look_path):
    global PO
    """
    核心逻辑

    :param res_name:
    :param look_path:
    :return:
    """
    clean_tmp()
    res_name = get_res_name(res_name)
    print("----------------------------------")
    print("你的资源名称为 {}".format(res_name))
    print("----------------------------------")

    PROJECT_TARGET_PATH = parse_ydl_project(look_path)

    print(PROJECT_TARGET_PATH)

    if (PROJECT_TARGET_PATH):
        print("解析YDL Project 成功！")
    else:
        print("对不起，你提供的project 无法识别！")
        exit(-1)

    compile_table = dict()
    compile_table['${PLACE}'] = "{}{}".format(res_name[0].upper(), res_name[1:])
    compile_table['${PLACE_VAR}'] = "{}{}".format(res_name[0].lower(), res_name[1:])

    intf = PROJECT_TARGET_PATH["intf_po_path"]

    # 检索包名
    p = re.compile("[\s\S]*\/(.+)\-intf\/[\s\S]*")

    matches = re.match(p, intf)

    if matches is not None:
        package = matches.group(1)
    else:
        package = ""
        print("抱歉，无法在{} 中解析到包规则".format(look_path))
        exit(-1)

    package_list = package.split("-")
    if len(package_list) != 2:
        print("包解析失败啦~")
        exit(-1)

    package_level1 = package_list[0]
    package_level2 = package_list[1]

    compile_table['${PACKAGE_LEVEL1}'] = "{}".format(package_level1)
    compile_table['${PACKAGE_LEVEL2}'] = "{}".format(package_level2)

    print("--------------------------------------")
    print("编译常量表")
    print("--------------------------------------")
    # 编译文件
    compiled_file_list = []

    print(DIR)
    for root, dirs, files in os.walk(DIR, False):
        for file in files:
            if (file[0] == "$"):
                compiled_file = compile_content(res_name, compile_table, os.path.join(root, file), TMP,
                                                PROJECT_TARGET_PATH)
                compiled_file_list.append(compiled_file)

    matchObj = re.match("[\s\S]+class (\w+) {([\s\S]+)}(.*?)[\s\S]+", PO)

    if (matchObj is not None):
        PO = matchObj.group(2)
        print(PO)
        if PO[-1] != "}":
            PO += "\n    }"

    po_body = PO
    for compiled_file in compiled_file_list:
        if is_dto(compiled_file):
            with open(compiled_file, "r+") as f:
                dto_body = f.read()
                dto_body = dto_body.replace("${PO}", po_body)

            with open(compiled_file, "w+") as f:
                f.write(dto_body)

        safe_cpfile(compiled_file, PROJECT_TARGET_PATH, res_name)

    clean_tmp()

    run_tests(PROJECT_TARGET_PATH["base_path"])

    print("---------------------------------------------")
    print("\033[27;32;40m\t恭喜~~你的工作完成了\033[0m")

    print("---------------------------------------------")


def main():
    print("-------------------------")
    print("Start Building your Resource")
    print("Draw by ghost ")
    print("-------------------------")
    parser = argparse.ArgumentParser(description="Auto create Resource for ydl java project")

    parser.add_argument("resource_name")
    parser.add_argument("project_path")
    args = parser.parse_args()

    project_path = args.project_path
    resource_name = args.resource_name
    gen(resource_name, project_path)


if __name__ == "__main__":
    main()

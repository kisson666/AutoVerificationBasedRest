# coding=utf-8

"""
### 思路：
- 从文件读取信息，文件是json格式的？兼容POSTMAN？文件是excel的？或者做个web页面？直接在web页面上改很方便啊
- 支持各种method，参数该怎么处理，post参数的参数怎么实现？
- 如何与静态文件共存？
- 如何兼容auto refresh？
- 对后台的自动化测试
- 实现单文件
"""
import argparse
import json
import urlparse

import xlrd
from flask import Flask, make_response

app = Flask(__name__)


class Api(object):
    """ This is a api class, resolve xlsx or json to Api class
    """

    def __init__(self, name, url, method, response, param):
        self.name = name
        self.url = url
        self.method = method
        self.response = response
        self.param = param


def parse_json_api(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    raw_api = json.loads(content)
    apis = []
    for i in raw_api['item']:
        try:
            formdata = [j['key'] for j in i['request']['body']['formdata']]
        except KeyError as e:
            formdata = []
        url = i['request']['url']
        if url.startswith("http"):
            rs = urlparse.urlparse(url)
            url = rs.path

        api = Api(name=i['name'], url=url, method=i['request']['method'], response=i['response'],
                  param=formdata)
        apis.append(api)
    return apis


def parse_xls_api(filepath):
    workbook = xlrd.open_workbook(filepath)
    sheet = workbook.sheets()[0]
    nrows = sheet.nrows
    ncols = sheet.ncols
    head = sheet.row_values(0)
    refer = dict(zip(head, range(len(head))))
    result = []
    for i in range(1, nrows):
        row = sheet.row_values(i)
        param = row[refer['param']] if refer.get('param') else None
        try:
            api = Api(row[refer['name']], row[refer['url']], row[refer['method']], row[refer['response']], param)
            result.append(api)
        except KeyError as e:
            print "缺少参数" + str(e)
            exit(1)
    return result


def import_file(filepath):
    """import files"""
    suffix = None
    allows = ['xls', 'xlsx', 'json']
    if "." in filepath:
        suffix = filepath.rsplit(".", 1)[-1].lower()
        if suffix not in allows:
            print "不正确的文件格式，允许" + ", ".join(allows)
            exit(1)
    else:
        print "没有文件后缀名，允许" + ", ".join(allows)
        exit(1)
    if suffix == "json":
        return parse_json_api(filepath)
    else:
        return parse_xls_api(filepath)


def add_route(api):
    """add view route by api"""

    def generate_view_func(response_value):
        def warp():
            response = make_response(response_value)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        return warp

    app.add_url_rule(api.url, api.name, generate_view_func(api.response), methods=[api.method])
    print u"add API %10s %5s %-30s" % (api.name, api.method.upper(), api.url)


def main(port, filepath):
    apis = import_file(filepath)
    if len(apis) > 0:
        for i in apis:
            add_route(i)
    app.run(port=port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto verification based rest")
    parser.add_argument('filepath', help='the path to api file')
    parser.add_argument('-p', "--port", type=int, default=3000, help='the port of server')
    args = parser.parse_args()
    main(args.port, args.filepath)

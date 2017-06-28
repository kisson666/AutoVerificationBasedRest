# coding=utf-8

"""
### 思路：
- 从文件读取信息，文件是json格式的？兼容POSTMAN？文件是excel的？或者做个web页面？直接在web页面上改很方便啊
- 支持各种method，参数该怎么处理，post参数的参数怎么实现？
- 支持跨域
- 如何与静态文件共存？
- 如何兼容auto refresh？
- 对后台的自动化测试
- 对输入参数的解析，click？
- 实现单文件
"""

import json
import urlparse
import click
import sys

from flask import Flask, make_response, jsonify

app = Flask(__name__)


class Api(object):
    """ This is a api class, resolve xlsx or json to Api class
    """

    name = ""
    url = ""
    method = "GET"
    response = ""
    param = []

    def __init__(self, name, url, method, response, param):
        self.name = name
        self.url = url
        self.method = method
        self.response = response
        self.param = param


def import_file(filename):
    """import files"""
    with open(filename, 'r') as f:
        content = f.read()
    return content


def parse_json_api(content):
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


def add_route(api):
    """add view route by api"""

    def generate_view_func(response_value):
        def warp():
            response = make_response(response_value)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        return warp

    app.add_url_rule(api.url, api.name, generate_view_func(api.response), methods=[api.method])


@click.command()
@click.option('-f', '--filename', help='path to json api')
def main(filename):
    content = import_file(filename)
    apis = parse_json_api(content)
    for i in apis:
        add_route(i)
    app.run()


if __name__ == "__main__":
    # main(sys.argv[1:])
    main()

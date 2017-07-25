# 基于REST接口的自动化验证软件

## 环境
Python 2.7版本，不需要任何依赖

## 使用
    python auto.py [-h] [-p PORT] [-m METHOD] url response

其中`-h` `-p` `-m` `--host` 为可选参数

    -h, --help 显示帮助信息
    --host  监听地址
    -p PORT, --port PORT  监听端口
    -m METHOD, --method METHOD 指定API方法，默认为GET

`url` `response` 为必选参数

    url 为api的url地址
    response 为返回值，如果有返回值有空格，请用引号将返回值内容括起来


## 举例

```bash
python auto.py /user/login 登录成功 # url 和 response内容必须要有
python auto.py /user/login {\"code\":0}  #没有空格，但是正常的引号要用 \" 防止被解析
python auto.py /abc "如果中间有空格 要用引号括起来"
python --host 0.0.0.0 -p 80 -m POST /支持中文路径 返回测试  #监听所有网卡地址，端口为80，方法为POST

```
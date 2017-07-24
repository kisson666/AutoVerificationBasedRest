# 基于rest接口的自动化验证软件

## 依赖
- flask
- xlrd

## 使用
`python auto.py [-h] [-p PORT] filepath`

## 文件格式
支持json和excel两种文件格式  
json的格式默认为postman的导出格式  
excel 要求必须要有 name url method response 这四列，且必须有列头  
可以参考示例文件

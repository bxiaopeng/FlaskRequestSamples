#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
from flask import Flask, render_template, request
from flask import jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = "dfdfdffdad"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getstr')
def get_string():
    name = request.args.get('name')  # 获取 ajax get 请求传递过来的数据
    print("ajax 发送来的数据是: {}".format(name))
    return '我是从 /getstr 返回的字符串'


@app.route('/postdatafromajax')
def get_data_from_ajax():
    ajax_data = request.args.get('name')
    print("从 ajax 获取的 data: {}".format(ajax_data))
    return '我是从 ajax 发送来的数据'


@app.route('/getdict', methods=['GET', 'POST'])
def get_dict():
    if request.method == 'POST':
        """测试通过JQuery发送POST"""
        name = request.form['name']
        print("name: {}".format(name))
        desc = request.form['desc']
        print("desc: {}".format(desc))

    # 返回的数据
    response_data = {'name': '小叮当', 'age': 8}
    return jsonify(response_data)


@app.route('/postform', methods=['POST'])
def post_form():
    name = request.form['name']
    age = request.form['age']
    d = {'name': name + ' ', 'age': age}
    return jsonify(d)


@app.route('/myform', methods=['POST'])
def myform():
    print('post')
    a = request.form['FirstName']
    print(a)
    d = {'name': 'xmr', 'age': 18}
    return jsonify(d)


@app.route('/getlist')
def get_list():
    """获取一个列表"""
    a_list = ['xmr', 18]
    print('获取一个列表')
    return json.dumps(a_list)


@app.route('/gettable')
def get_table():
    table = [('id', 'name', 'age', 'score'),
             ('1', 'xiemanrui', '18', '100'),
             ('2', 'yxx', '18', '100'),
             ('3', 'yaoming', '37', '88')]

    print('mytable')
    data = json.dumps(table)
    print(data)
    return data


if __name__ == '__main__':
    app.run(debug=True, port=7777)

# -*- coding:utf-8 -*-

"""
<Description> (form.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Created by bixiaofan <wirelessqa@163.com> on 2018/7/31 at 下午2:13
"""

from wtforms import Form, BooleanField, StringField, validators, DateTimeField


# Form是表单的基类，继承From的子类可以将字段定义为类属性。
class RegistrationForm(Form):
    # 类的属性定义为字段，StringField和BooleanField等都是字段的类型
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])


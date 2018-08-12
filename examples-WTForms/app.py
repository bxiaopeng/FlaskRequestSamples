# -*- coding:utf-8 -*-

"""
<Description> (app.py.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Created by bixiaofan <wirelessqa@163.com> on 2018/7/31 at 上午11:04
"""

from flask import Flask, render_template, request
from wtforms import Form, StringField, PasswordField, validators, ValidationError

app = Flask(__name__)


class UserRegisterForm(Form):
    """用户注册表单验证"""
    username = StringField(
        label="用户名",
        validators=[
            validators.Length(min=4, max=10, message="用户名必须在4-10个字节之间"),
            validators.DataRequired(message='用户名不能为空')
        ]
    )
    email = StringField(
        label="邮箱",
        validators=[
            validators.DataRequired(message='邮件不能为空')
        ]
    )
    password = PasswordField(
        validators=[
            validators.DataRequired(message='密码不能为空')
        ]
    )
    confirm_password = PasswordField(
        validators=[
            validators.DataRequired(message='重复密码不能为空'),
            validators.EqualTo("password")
        ]
    )

    def validate_password(self, field):
        password = field.data
        if password == password.lower() or password == password.upper():
            raise ValidationError('必须同时包含大小写字母')


@app.route('/user/register/', methods=["GET", "POST"])
def register():
    form = UserRegisterForm(request.form)

    if request.method == "POST":
        if form.validate():
            print(form.username.data)
            print(form.email.data)
            print(form.password1.data)
            print(form.password2.data)
            return "感谢你的注册!"
        else:
            # abort(400)
            return render_template("register.html", form=form)
    return render_template("register.html", form=form)


if __name__ == '__main__':
    app.run(debug=True, port=7777)

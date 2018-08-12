# WTForms

WTForms 是一个适用于 Python 的灵活的表单验证和渲染库。



WTForms 是一个灵活的表单验证和渲染库，用于 Python Web开发。 它与框架无关，可以与你选择的任何 Web 框架和模板引擎一起使用。 有各种社区库提供与流行框架更紧密的集成。



## 基本信息（缺）



## 安装

```shell
pip install WTForms
```



## 基本功能

**什么时候开始使用 WTForms?**

当你写了几个页面，想要进行「表单输入处理和验证」的时候，WTForms 就上场了。



**为什么我们要使用 WTForms？**

- 如果你不想每种形式都直接映射到数据库模型

一些 webapp 框架采用将**数据库模型与表单处理相关联**的方法，虽然这对于非常基本的创建/更新视图很方便，但是你也许不想每种形式都直接映射到数据库模型。

- 如果你想自定义表单字段的 HTML 代码和验证

或者你可能已经使用了通用表单处理框架，但是你希望**自定义生成**这些表单字段的 HTML，并定义你自己的验证。

使用 WTForms，你可以在 Python 代码中定义生成表单字段的 HTML，也可以在 HTML 模板中自定义它，这样可以保持代码和展示的分离，并且将那些混乱的参数保留在 Python 代码之外。

因为我们努力实现松耦合，所以你应该能够在你喜欢的任何模板引擎中做到这一点。



## 主要概念

> - [`Forms`](http://wtforms.readthedocs.io/en/stable/forms.html#wtforms.form.Form)  是WTForms的核心容器。 表单(Forms)表示字段(Fields) 的集合，字段(Fields)通过表单的字典形式或者属性形式访问。
> - [`Fields`](http://wtforms.readthedocs.io/en/stable/fields.html#module-wtforms.fields) 做了大部分繁重的工作。 每个字段(field)表示一种数据类型，该字段处理对该数据类型的强制表单输入。 例如，`IntegerField` 和 `StringField` 表示两种不同的数据类型。 除了字段包含的数据之外，字段还包含许多有用的属性，例如标签，说明和验证错误列表。
> - 每个字段都有一个 Widget 实例。Widget 的工作是呈现该字段的 HTML 表示。 可以为每个字段指定窗口Widget 实例，但默认情况下每个字段都有一个有意义。 有些字段只是方便，例如 `TextAreaField` 只是一个 `StringField`，默认 Widget 是一全 [`TextArea`](http://wtforms.readthedocs.io/en/stable/widgets.html#wtforms.widgets.TextArea)。
> - 为了指定验证规则，字段( fields )包含验证器(Validators)列表。



## 官方快速入门教程

### 定义表单

让我们定义第一个表单(Form)：

```python
from wtforms import Form, BooleanField, StringField, validators

# Form是表单的基类，继承From的子类可以将字段定义为类属性。
class RegistrationForm(Form):
    # 类的属性定义为字段，StringField和BooleanField等都是字段的类型
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])
```

STEP 1. 从  wtforms 中导入表单基类(Form)，字段类型(BooleanField，StringField)，验证器(validators)

STEP 2. 自定义表单 RegistrationForm 并继承表单基类 From

STEP 3. 通过定义 RegistrationForm 的类属性来定义表单的字段实例

- StringField 和 BooleanField 等都是字段的类型；
- 字段实例的第 1 个参数，如 'Username' 是字段的标签；
- 字段实例的第 2 个参数，[validators.Length(min=4, max=25)] 是该字段的验证列表；



因为表单(forms)是常规的 Python 类，所以我们可以轻松的扩展它们：

```python
class ProfileForm(Form):
    birthday  = DateTimeField('Your Birthday', format='%m/%d/%y')
    signature = TextAreaField('Forum Signature')

class AdminProfileForm(ProfileForm):
    username = StringField('Username', [validators.Length(max=40)])
    level    = IntegerField('User Level', [validators.NumberRange(min=0, max=10)])
```

通过子类化，AdminProfileForm 获取已在父类 ProfileForm 中定义的所有字段。 这使我们可以轻松地在表单之间共享通用的字段子集，例如上面的示例，我们可以向 ProfileForm 添加 admin-only 字段。

### 使用 Forms

使用表单就像实例化一样简单。 

使用我们之前定义的 RegistrationForm 考虑以下类似 django 的视图：

```python
def register(request):
    # STEP1. 实例化表单
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate(): # STEP2. 验证请求方法和规则
        # STEP3. 创建新用户并将数据保存
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.save()
        redirect('register')
    return render_response('register.html', form=form)
```

STEP 1. 实例化表单，通过 request.POST 提供可用的数据。 

STEP 2. 检查请求是否是使用 POST 进行的，如果是，验证表单，并检查用户是否接受了规则。

STEP 3. 如果成功，创建一个新用户并将验证表单中的数据分配给它，然后保存。



#### 编辑现有的对象

我们之前的注册示例展示了如何接受输入并对新条目进行验证，但是如果我们想要编辑现有对象呢？ 

简单：

```python
def edit_profile(request):
    user = request.current_user
    # 向表单中传入 user 对象
    form = ProfileForm(request.POST, user)
    if request.method == 'POST' and form.validate():
        form.populate_obj(user) # 使用验证过的表单内容重新填译 user 对象
        user.save()
        redirect('edit_profile')
    return render_response('edit_profile.html', form=form)
```

在这里，我们通过向表单提供 request.POST 和 user 对象来实例化表单。 通过这样做，表单将获得来自 user 对象的 post data 中不存在的数据。

我们还使用表单的 **populate_obj** 方法用验证过的表单内容重新填充 user 对象。 提供此方法是为了方便，当字段名称与我们提供 data 的对象上的名称匹配时使用。 通常，我们需要手动分配值，但对于这个简单的情况，它是完美的。 另外它对 CRUD 和管理表单也很有用。

#### 在控制台中探索

WTForms 表单是非常简单的容器对象，也许找出表单中可用内容的最简单方法是在控制台中使用表单：

```shell
>>> from wtforms import Form, StringField, validators
>>> class UsernameForm(Form):
...     username = StringField('Username', [validators.Length(min=5)], default=u'test')
...
>>> form = UsernameForm()
>>> form['username']  # 通过字典样式访问
<wtforms.fields.StringField object at 0x827eccc>
>>> form.username.data  # 通过属性样式访问
u'test'
>>> form.validate()  # 验证表单
False
>>> form.errors  # 验证不通过的错误摘要
{'username': [u'Field must be at least 5 characters long.']}
```

当我们实例化一个表单时，它包含所有字段的实例，可以通过字典样式或属性样式访问它们。 这些字段具有自己的属性，enclosing form 也是如此。

当我们验证表单时，它返回 False，这意味着至少有一个验证器不满足。 [`form.errors`](http://wtforms.readthedocs.io/en/stable/forms.html#wtforms.form.Form.errors)  将为我们提供所有错误的摘要。

```shell
>>> form2 = UsernameForm(username=u'Robert')
>>> form2.data
{'username': u'Robert'}
>>> form2.validate()
True
```

这次，我们在实例化 UserForm 时传递了 username 的新值，并且表单验证通过。

### Forms 如何获取数据

除了使用前两个参数（formdata 和 obj）提供数据之外，我们还可以传递关键字参数来填充表单。 请注意一些参数名是被保留的：formdata，obj 和 prefix。

formdata 优先级高于 obj，obj 优先级高于关键字参数。 

例如：

```python
def change_username(request):
    user = request.current_user
    # request.POST 是 formdata，即从HTML表单传递过来的数据
    # user 是对象
    # username 是传递给表单的关键字参数
    form = ChangeUsernameForm(request.POST, user, username='silly')
    if request.method == 'POST' and form.validate():
        # 这里体现了获取数据的优先级
        user.username = form.username.data
        user.save()
        return redirect('change_username')
    return render_response('change_username.html', form=form)
```

虽然我们几乎从没有在实践中一起使用过这三种获取数据的方法，但本例很好的说明了 WTForms 是如何查找 username 字段的：

1. 如果通过 HTML 提交了表单（request.POST 不为空），则处理表单输入。 即使没有特定字段的表单输入，如果存在任何类型的表单输入，那么我们将处理表单输入。
2. 如果没有表单输入，会按顺序尝试以下操作：

- 检查 user 是否具有名为 username 的属性。
- 检查是否提供了名为 username 的关键字参数。
- 最后，如果其他所有方法都失败，会使用字段提供的默认值（如果有）。

### Validators: 验证器

WTForms 中的验证是通过提供一个字段来完成的，该字段包含一组 Validators，以便在验证包含表单时运行。 

我们通过字段构造函数的第二个参数提供 Validators：

```python
class ChangeEmailForm(Form):
    email = StringField('Email', [validators.Length(min=6, max=120), validators.Email()])
```

您可以为字段提供任意数量的 validators。 

通常，我们需要提供自定义错误消息：

```python
class ChangeEmailForm(Form):
    email = StringField('Email', [
        validators.Length(min=6, message=_(u'Little short for an email address?')),
        validators.Email(message=_(u'That\'s not a valid email address.'))
    ])
```

一般我们最好提供自己定义的消息，因为必要的默认消息是通用的。 这也是提供本地化错误消息的方法。

For a list of all the built-in validators, check the [`Validators Reference`](http://wtforms.readthedocs.io/en/stable/validators.html#module-wtforms.validators)

### Rendering Fields:渲染字段

渲染字段就像将其强制转换为字符串一样简单：

```shell
>>> from wtforms import Form, StringField
>>> class SimpleForm(Form):
...   content = StringField('content')
...
>>> form = SimpleForm(content='foobar')
>>> str(form.content)
'<input id="content" name="content" type="text" value="foobar" />'
>>> unicode(form.content)
u'<input id="content" name="content" type="text" value="foobar" />'
```

然而，真正的力量来自于使用 [`__call__()`](http://wtforms.readthedocs.io/en/stable/fields.html#wtforms.fields.Field.__call__) 方法渲染字段。 通过调用该字段，我们可以提供关键字参数，这些参数将作为输出中的 html 属性注入：

```shell
>>> form.content(style="width: 200px;", class_="bar")
u'<input class="bar" id="content" name="content" style="width: 200px;" type="text" value="foobar" />'
```

现在让我们应用这个功能来渲染 Jinja 模板中的表单。 

首先，我们的表单：

```python
class LoginForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')

form = LoginForm()
```

HTML 模板:

```html
<form method="POST" action="/login">
    <div>{{ form.username.label }}: {{ form.username(class="css_class") }}</div>
    <div>{{ form.password.label }}: {{ form.password() }}</div>
</form>
```

或者，如果你正在使用 Django 模板，那么当你想要传递关键字参数时，可以使用我们在 Django 扩展中提供的form_field 模板标签：

```html
{% load wtforms %}
<form method="POST" action="/login">
    <div>
        {{ form.username.label }}:
        {% form_field form.username class="css_class" %}
    </div>
    <div>
        {{ form.password.label }}:
        {{ form.password }}
    </div>
</form>
```

这些都将输出:

```html
<form method="POST" action="/login">
    <div>
        <label for="username">Username</label>:
        <input class="css_class" id="username" name="username" type="text" value="" />
    </div>
    <div>
        <label for="password">Password</label>:
        <input id="password" name="password" type="password" value="" />
    </div>
</form>
```

WTForms 是模板引擎不可知的，并且可以与任何允许属性访、字符串强制和/或函数调用的东西一起使用。 提供form_field 模板标签是为了方便，因为我们无法在 Django 模板中传递参数。

### 显示 Errors

现在我们有一个表单模板，让我们添加错误消息：

```html
<form method="POST" action="/login">
    <div>{{ form.username.label }}: {{ form.username(class="css_class") }}</div>
    {% if form.username.errors %}
        <ul class="errors">{% for error in form.username.errors %}<li>{{ error }}</li>{% endfor %}</ul>
    {% endif %}

    <div>{{ form.password.label }}: {{ form.password() }}</div>
    {% if form.password.errors %}
        <ul class="errors">{% for error in form.password.errors %}<li>{{ error }}</li>{% endfor %}</ul>
    {% endif %}
</form>
```

如果您更喜欢顶部的一大列错误，这也很容易：

```jinja2
{% if form.errors %}
    <ul class="errors">
        {% for field_name, field_errors in form.errors|dictsort if field_errors %}
            {% for error in field_errors %}
                <li>{{ form[field_name].label }}: {{ error }}</li>
            {% endfor %}
        {% endfor %}
    </ul>
{% endif %}
```

由于错误处理可能会变得相当冗长，因此最好使用 Jinja macros（或 equivalent）来减少模板中的样板。 ([example](http://wtforms.readthedocs.io/en/stable/specific_problems.html#jinja-macros-example))

### 自定义 Validators

有两种方法可以提供自定义验证器。 

通过定义自定义验证器并在字段上使用它：

```python
from wtforms.validators import ValidationError

def is_42(form, field):
    if field.data != 42:
        raise ValidationError('Must be 42')

class FourtyTwoForm(Form):
    num = IntegerField('Number', [is_42])
```

或者在自定义表单中为该表单提供特定的验证器：

```python
class FourtyTwoForm(Form):
    num = IntegerField('Number')

    def validate_num(form, field):
        if field.data != 42:
            raise ValidationError(u'Must be 42')
```

For more complex validators that take parameters, check the [Custom validators](http://wtforms.readthedocs.io/en/stable/validators.html#custom-validators) section.



## 实战教程

### RESTFUL API 应用中使用 WTForms

> 本章来自：[用 WTForms 和装饰器做表单校验](http://liyangliang.me/posts/2015/10/using-wtforms-and-decorator-to-validate-form-in-flask/) ，描述略有调整。

在一个 Web 应用里，不管是为了业务逻辑的正确性，还是系统安全性，做好参数（querystring, form, json）验证都是非常必要的。

[WTForms](https://github.com/wtforms/wtforms) 是一个非常好用而且强大的表单校验和渲染的库，提供 Form 基类用于定义表单结构（类似 ORM），内置了丰富的字段类型和校验方法，可以很方便的用来做校验。

如果应用需要输出 HTML，集成到模板里也很容易。

**对于 RESTFUL API 应用，用不到渲染的功能，但是结构化的表单和校验功能依然非常有用。**



#### 案例描述

以一个注册的应用场景为例，用户输入用户名、邮箱、密码、确认密码，服务程序先检查参数然后处理登录逻辑。这几个字段都是必填的，此外还有一些额外的限制：

- 用户名：长度在 3-20 之间
- 邮箱：合法的邮箱格式，比如 “abc” 就不合法
- 密码：长度在 8-20 之间，必须同时包含大小写字母
- 确认密码：必须与密码一致

如果参数不合法，返回 400；登录逻辑略去不表。

#### 原始的做法

最原始的做法，就是直接在注册的接口里取出每个参数，逐个手动校验。

这种做法可能的代码是：

```python
@app.route('/user/signup/', methods=['POST'])
def register():
    username = request.form.get('username')
    if not username or not (3 <= len(username) <= 20):
        abort(400)
    
    email = request.form.get('email')
    if not email or not re.match(EMAIL_REGEX, email):
        abort(400)
    
    password = request.form.get('password')
    if not password:
        abort(400)
    if password == password.lower() or password == password.upper():
        abort(400)
    
    confirm_password = request.form.get('confirm_password')
    if not confirm_password or confirm_password != password:
        abort(400)
    
    # 处理注册的逻辑
```

有可能是我的写法不太对，但是这样检查参数的合法性，实在不够优雅。检查参数的代码行数甚至超出了注册的逻辑，也有些喧宾夺主的感觉。可以把这些代码移出来，使得业务逻辑代码更加清晰一点。

#### 用 WTForms 来改造

下面先用 WTForms 来改造一下:

```python
from wtforms import Form
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError


class SignupForm(Form):
    username = StringField(validators=[DataRequired(), Length(3, 20)])
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password')])
    
    def validate_password(self, field):
        password = field.data
        if password == password.lower() or password == passowrd.upper():
            raise ValidationError(u'必须同时包含大小写字母')


@app.route('/user/signup/', methods=['POST'])
def register():
    form = SignupForm(formdata=request.form)
    if not form.validate():
        abort(400)
    
    # 处理注册逻辑，参数从 form 对象获取，比如
    username = form.username.data
```

这个版本带来的好处很明显：

1. 参数更加结构化了，所有字段名和类型一目了然
2. 有内置的，语义清晰的校验方法，可以组合使用
3. 还能自定义额外的校验方法，**方法签名是 `def validate_xx(self, field)`，其中 `xx` 是字段名，通过 `field.data` 来获取输入的值**
4. 还有没体现出来的，就是丰富的错误提示信息，既有内置的，也可以自定义

再看原来的 `register` 方法，代码变得更加简洁和清晰，整体的编码质量也得到了提升。

那么再考虑一下更复杂的场景，在一个返回 JSON 的 API 应用里，有很多 API，有不同的参数提交方式（GET 方法通过 query string，POST 方法可能有 form 和 JSON），一样的校验错误处理方式（abort(400) 或其他）。我们依然可以像上面那样处理，但如果再借助装饰器改进一下，又能少写几行“重复”的代码。

需要注意的是，WTForms 的 formdata 支持的是类似 Werkzeug/Django/WebOb 中的 `MultiDict` 的数据结构。Flask 中的 `request.json` 是一个 `dict` 类型，所以需要先包装一下。

继续改造注册的例子：

```python
import functools

from werkzeug.datastructures import MultiDict

# 验证表单
def validate_form(form_class):
    def decorator(view_func):
        @functools.wraps(view_func)
        def inner(*args, **kwargs):
            if request.method == 'GET':
                formdata = request.args
            else:
                if request.json:
                    formdata = MultiDict(request.json)
                else:
                    formdata = request.form
                    
            form = form_class(formdata=formdata)
            if not form.validate():
                return jsonify(code=400, message=form.errors), 400

            g.form = form 
            return view_func(*args, **kwargs)

        return inner

    return decorator


@app.route('/user/signup/', methods=['POST'])
@validate_form(form_class=SignupForm)
def register():
    form = g.form   # 运行到这里，说明表单是合法的

    # 处理注册逻辑，参数从 form 对象获取，比如
    username = form.username.data
```

实现了一个叫 `validate_form` 的装饰器，指定一个 Form 类，处理统一的参数获取、校验和错误处理，如果一切正确，再把 Form 对象保存到全局变量 `g` 里面，这样就可以在 view 函数里取出来用了。现在的 `register` 方法变得更加简洁，甚至都看不到检查参数的那些代码，只需要关心具体的和注册相关的逻辑本身就好。

这个装饰器的可重用性非常好，其他的接口只要定义一个 Form 类，然后调用一下装饰器，再从 `g` 获取 Form 对象。不仅省了很多心思和体力劳动，代码也变得更加清晰优雅和 Pythonic。



### HTML 渲染 WTForms

> 本文来自：[Flask扩展系列(七)–表单](http://www.bjhee.com/flask-ext7.html)，略有修改。

表单Form，在Web应用中无处不在。其实所有的表单项都有共性，比如有文字输入框，单选框，密码输入框等；此外表单的验证也有共性，比如有非空验证，长度限制，类型验证等。

如果有个框架，能把这些共性抽象出来，那就能大量简化我们的工作。Python的 WTForms 就提供了这些功能。



#### 一个简单的表单

这个表单只有一个文字输入框，并且当输入用户名为”admin”时才返回成功。WTForms 让我们在后端代码中定义表单类，并列出表单的字段和相应的验证规则。

现在让我们先定义一个 MyForm 类：

```python
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
 
class MyForm(Form):
    user = StringField('Username', validators=[DataRequired()])
```

表单类 MyForm 定义个了一个字符型字段，也就是一个文字输入框”user”。

StringField 的第一个参数 ”Username” 指定了该字段的显示名，第二个参数指定了验证规则。这是一个列表，也就是你可以对一个字段定义多个验证规则，上例中我们使用了”wtforms.validators.DataRequired”验证，也就是代表了该字段为必填项，表单提交时必须非空。

下一步，我们写个视图函数 login 来使用 MyForm 表单：

```python
from flask import Flask, render_template
app = Flask(__name__)
app.secret_key = '1234567'
 
@app.route('/login', methods=('GET', 'POST'))
def login():
    form = MyForm()
    if form.validate_on_submit():
        # if form.user.data == 'admin':
        if form.data['user'] == 'admin':
            return 'Admin login successfully!'
        else:
            return 'Wrong user!'
    return render_template('login.html', form=form)
```

有了这个 ”form.validate_on_submit()” 方法，我们就不用像之前一样通过请求方法是否为 ”POST” 来判断表单是否提交。

在表单提交后，我们可以用表单对象的 data 属性来获取提交内容，这个 ”form.data” 是一个字典类型。

上例中，它只有一个字段，也就是 ”user”。我们同样也可以用 ”form.user.data” 获取 ”user” 字段的值。

在非提交状态下，我们就渲染模板，并且往模板中传入表单对象。另外注意，这里要设置 ”app.secret_key”，因为表单类中会使用到会话对象 session。



最后让我们写 ”login.html” 模板来显示这个表单：

```html
<form method="POST" action="{{ url_for('login') }}">
    {{ form.hidden_tag() }}
    {{ form.user.label }}: {{ form.user(size=20) }}
    <input type="submit" value="Submit">
</form>
```

表单中，`form.hidden_tag()` 会生成一个隐藏的`<div>`标签，其中会渲染任何隐藏的字段，最主要的是 CSRF 字段。

这个 CSRF（Cross-Site Request Forgery 跨站请求伪造）是一种通过伪装来自受信任用户的请求，来发送恶意攻击的方法，具体内容大家可以在网上搜到。

WTForms 默认开启 CSRF 保护，如果你想关闭它（建议不要这样做），可以在实例化表单时传入参数，比如 `form = MyForm(csrf_enabled=False)`。

`form.user.label` 会输出`user`字段的显示名，即上例中的`Username`；`form.user`会输出一个`text`类型的`<input>`标签，它的参数`size=20`会成为这个`<input>`标签里的属性。

所以上面的模板内容在渲染后，会被转换为下面这段 HTML 代码：

```html
<form method="POST" action="/login">
    <div style="display:none;"><input id="csrf_token" name="csrf_token" type="hidden" value="1458707165##33a1f1384d3c12dca29cce5e8ccf6e4d21f5f28f"></div>
    <label for="user">Username</label>: <input id="user" name="user" size="20" type="text" value="">
    <input type="submit" value="Submit">
</form>
```

让我们运行上面的代码，并且测试下。有没有看到下面的表单？

 ![Simple Form](http://www.bjhee.com/wp-content/uploads/2016/03/simple-form.png) 

当我们输入”admin”时，返回成功；输入其他字符串时，返回失败；而不输入直接提交，会返回表单页。

是不是很神奇？

#### 表单字段类型

上例中的表单只包含了一个字符类型的字段，WTForms 提供了大量内置的字段类型，来便于我们创建表单项，它们都放在”wtforms.fields”包下。下面，我们创建一个用户注册表单类，并将常用的字段类型都包括在其中，为了方便理解，描述就直接写在注释里：

```python
from wtforms.fields import (StringField, PasswordField, DateField, BooleanField,
                            SelectField, SelectMultipleField, TextAreaField,
                            RadioField, IntegerField, DecimalField, SubmitField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
 
class RegisterForm(Form):
    # Text Field类型，文本输入框，必填，用户名长度为4到25之间
    username = StringField('Username', validators=[Length(min=4, max=25)])
 
    # Text Field类型，文本输入框，Email格式
    email = StringField('Email Address', validators=[Email()])
 
    # Text Field类型，密码输入框，必填，必须同confirm字段一致
    password = PasswordField('Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
 
    # Text Field类型，密码输入框
    confirm = PasswordField('Repeat Password')
 
    # Text Field类型，文本输入框，必须输入整型数值，范围在16到70之间
    age = IntegerField('Age', validators=[NumberRange(min=16, max=70)])
 
    # Text Field类型，文本输入框，必须输入数值，显示时保留一位小数
    height = DecimalField('Height (Centimeter)', places=1)
 
    # Text Field类型，文本输入框，必须输入是"年-月-日"格式的日期
    birthday = DateField('Birthday', format='%Y-%m-%d')
 
    # Radio Box类型，单选框，choices里的内容会在ul标签里，里面每个项是(值，显示名)对
    gender = RadioField('Gender', choices=[('m', 'Male'), ('f', 'Female')],
                                  validators=[DataRequired()])
 
    # Select类型，下拉单选框，choices里的内容会在Option里，里面每个项是(值，显示名)对
    job = SelectField('Job', choices=[
        ('teacher', 'Teacher'),
        ('doctor', 'Doctor'),
        ('engineer', 'Engineer'),
        ('lawyer', 'Lawyer')
    ])
 
    # Select类型，多选框，choices里的内容会在Option里，里面每个项是(值，显示名)对
    hobby = SelectMultipleField('Hobby', choices=[
        ('swim', 'Swimming'),
        ('skate', 'Skating'),
        ('hike', 'Hiking')
    ])
 
    # Text Area类型，段落输入框
    description = TextAreaField('Introduction of yourself')
 
    # Checkbox类型，加上default='checked'即默认是选上的
    accept_terms = BooleanField('I accept the Terms of Use', default='checked',
                                validators=[DataRequired()])
 
    # Submit按钮
    submit = SubmitField('Register')
```

每个字段类型的第一个参数都是显示名，而且都接收 ”validator” 参数来传入验证规则。

上例的表单字段上，我们用到了很多验证规则，关于这部分，我们会在下一小节介绍。

对于时间日期字段，如”DateField”或”DateTimeField”，它们都有一个”format”参数来传入可识别的日期格式；

对于选择框，如”RadioField”, “SelectField”或”SelectMultipleField”，它们都有一个”choices”参数来传入可选择项，每个项是一个”(值, 显示名称)”对，同时它们也有一个参数”coerce”参数来强制转换选择项值的类型，比如”coerce=int”。

接下来，让我们编写模板，因为字段比较多，我们先写一个宏来**渲染单个字段**，并存放在模板文件”_field.html”中：

```html
{% macro render_field(field) %}
<tr>
  <td>{{ field.label }}</td>
  <td>{{ field(**kwargs)|safe }}</td>
  <td>{% if field.errors %}
    <ul class=errors>
    {% for error in field.errors %}
      <li>{{ error }}</li>
    {% endfor %}
    </ul>
  {% endif %}
  </td>
</tr>
{% endmacro %}
```

这个”render_field”宏用来渲染表格中的一个行，它有三个列，分别是字段显示名，字段值，和错误信息（如果有错误的话）。

然后，我们写”register.html”模板：

```html
<!doctype html>
<title>Registration Form Sample</title>
<h1>User Registration</h1>
{% from "_field.html" import render_field %}
<form method="POST" action="{{ url_for('register') }}">
  {{ form.hidden_tag() }}
  <table>
    {{ render_field(form.username) }}
    {{ render_field(form.email) }}
    {{ render_field(form.password) }}
    {{ render_field(form.confirm) }}
    {{ render_field(form.age) }}
    {{ render_field(form.height) }}
    {{ render_field(form.gender) }}
    {{ render_field(form.birthday) }}
    {{ render_field(form.job) }}
    {{ render_field(form.hobby) }}
    {{ render_field(form.description) }}
    {{ render_field(form.accept_terms) }}
  </table>
  {{ form.submit }}
</form>
```

模板中导入”render_field”宏，并依次渲染用户注册表单里的每一个字段。最后，我们写个视图函数来显示这个表单：

```python
@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash('User "%s" registered successfully! Please login.' % form.username.data)
        login_form = LoginForm()
        return render_template('login.html', form=login_form)
 
    return render_template('register.html', form=form)
```

打开浏览器，访问”/register”地址，你会看到这样的表单页面：
![Register Form](http://www.bjhee.com/wp-content/uploads/2016/03/register-form.png)
如果你什么都不输入，直接提交，错误信息将会在字段旁显示：
![Register Error Form](http://www.bjhee.com/wp-content/uploads/2016/03/register-error-form.png)

这个页面还很丑陋，你可以通过CSS来美化它，本文就不介绍了。总之，大家已经被WTForms的强大感染到了吧！

Flask-WTF还提供了”RecaptchaField”字段来方便我们生成验证码。可惜，它是基于Google的[Recaptcha API](https://www.google.com/recaptcha/api.js)实现的，如果你的网站用户是天朝内的，千万不要用。对于开发天朝外网站的朋友们，可以参考下[这个示例](https://github.com/lepture/flask-wtf/tree/master/examples/recaptcha)。

完整的字段类型说明可以参阅[WTForms官方的Fields API文档](http://wtforms.readthedocs.org/en/latest/fields.html)，其中也描述了如何自定义字段类型。

#### 验证规则

上一节的例子中其实已经把大部分常用的验证规则validator都用上了，WTForms 同样提供了大量内置的验证规则，它们都放在 ”wtforms.validators” 包下。

这里我们就来列举一下：

| 验证规则     | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| DataRequired | 验证必填项                                                   |
| Email        | 验证邮件地址格式                                             |
| EqualTo      | 验证必须同另一个字段值相同，它需传入另一个字段的名称”fieldname” |
| Length       | 验证输入字符串长度，它有两个参数：”min”最小长度，”max”最大长度，缺省的话就不检查 |
| NumberRange  | 验证输入数值的范围，它有两个参数：”min”最小值，”max”最大值，缺省的话就不检查 |
| URL          | 验证URL格式                                                  |
| IPAddress    | 验证IP地址格式，默认IPV4，你可以传入”ipv6=True”来验证IPV6地址 |
| MacAddress   | 验证Mac地址格式                                              |
| AnyOf        | 传入一个列表作为参数，验证是否匹配列表中的任一值             |
| NoneOf       | 传入一个列表作为参数，验证是否与列表中的所有值都不同         |
| Regexp       | 正则表达式验证，需传入一个正则表达式，它还有一个flags参数，如果你传入”re.IGNORECASE”，就会忽略大小写 |

所有的validator都有一个”message”参数，用来指定当验证失败时抛出的错误消息，不指定的话WTForms就会使用默认错误消息。

完整的验证规则validator说明可以参阅[WTForms官方的Validators API文档](http://wtforms.readthedocs.org/en/latest/validators.html)，其中也描述了如何自定义验证规则。

#### 文件上传

WTForms 本身有一个”FileField”用来处理文件上传功能，Flask-WTF 扩展对其作了封装，使得我们可以更方便的在 Flask 应用中实现文件上传。

现在就让我们来定义一个文件上传的表单类：

```python
class AttachForm(Form):
from flask_wtf.file import FileField, FileAllowed, FileRequired
 
class AttachForm(Form):
    attach = FileField('Your Attachment', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
```

我们引入”flask_wtf.file” 包下的文件上传框 ”FileField”，和两个验证规则”FileRequired”及”FileAllowed”。

”FileRequired”验证表单提交时必须有文件已被指定；

”FileAllowed”验证文件的类型，上例中只接收以”jpg”和”png”为后缀的文件，如果不是会抛出错误消息”Images only!”。

模板文件很简单，只要记得在”<form>”标签里加上属性’enctype=”multipart/form-data”‘即可：

```html
<form method="POST" action="{{ url_for('upload') }}" enctype="multipart/form-data">
    {{ form.hidden_tag() }}
    {{ form.attach.label }} {{ form.attach }}
    <input type="submit" value="Submit">
</form>
```

最后，写上视图函数：

```python
from werkzeug import secure_filename
 
@app.route('/upload', methods=('GET', 'POST'))
def upload():
    form = AttachForm()
    if form.validate_on_submit():
        filename = secure_filename(form.attach.data.filename)
        form.attach.data.save('uploads/' + filename)
        return 'Upload successfully!'
```

“secure_filename”用来确保文件名安全，我们在介绍[Flask文件和流](http://www.bjhee.com/flask-ad5.html)时有提到过。

”form.attach.data”就可以获取文件的内容，它的”save()”方法可以将内容保存到本地文件中去。

上例中，我们把文件保存在本地当前目录下的”uploads”子目录中。

运行下这段程序，你将看到下图这样的表单，你可以试着上传一个文件。 ![Upload Form](http://www.bjhee.com/wp-content/uploads/2016/03/upload-form.png)

####  表单字段国际化

由于表单类是在Flask上下文环境外定义的，对于其字段显示名的国际化，要使用”lazy_gettext”方法。

比如：

```python
from flask_wtf import Form
from flask_babel import lazy_gettext
from wtforms import StringField
from wtforms.validators import DataRequired
 
class MyForm(Form):
    user = StringField(lazy_gettext(u'Username'), validators=[DataRequired()])
```

关于国际化本地化的内容，可参考[本系列第三篇](http://www.bjhee.com/flask-ext3.html)介绍的Babel扩展。



## Forms

https://wtforms.readthedocs.io/en/stable/forms.html

## Fields

https://wtforms.readthedocs.io/en/stable/fields.html



**WTForms 支持的 HTML 标准字段**

| 字段对象            | 说明                                |
| ------------------- | ----------------------------------- |
| StringField         | 文本字段                            |
| TextAreaField       | 多行文本字段                        |
| PasswordField       | 密码文本字段                        |
| HiddenField         | 隐藏文本字段                        |
| DateField           | 文本字段，值为datetime.date格式     |
| DateTimeField       | 文本字段，值为datetime.datetime格式 |
| IntegerField        | 文本字段，值为整数                  |
| DecimalField        | 文本字段，值为decimal.Decimal       |
| FloatField          | 文本字段，值为浮点数                |
| BooleanField        | 复选框，值为True和False             |
| RadioField          | 一组单选框                          |
| SelectField         | 下拉列表                            |
| SelectMultipleField | 下拉列表，可选择多个值              |
| FileField           | 文本上传字段                        |
| SubmitField         | 表单提交按钮                        |
| FormField           | 把表单作为字段嵌入另一个表单        |
| FieldList           | 一组指定类型的字段                  |

 

## Validators

https://wtforms.readthedocs.io/en/stable/validators.html

**WTForms 常用验证函数**

| 验证函数     | 说明                                     |
| ------------ | ---------------------------------------- |
| DataRequired | 确保字段中有数据                         |
| EqualTo      | 比较两个字段的值，常用于比较两次密码输入 |
| Length       | 验证输入的字符串长度                     |
| NumberRange  | 验证输入的值在数字范围内                 |
| URL          | 验证 URL                                 |
| AnyOf        | 验证输入值在可选列表中                   |
| NoneOf       | 验证输入值不在可选列表中                 |

## Widgets

https://wtforms.readthedocs.io/en/stable/widgets.html

## class Meta

https://wtforms.readthedocs.io/en/stable/meta.html

## CSRF Prottection

https://wtforms.readthedocs.io/en/stable/csrf.html

## 扩展





## 学习资料

- [WTForms 官方文档](https://wtforms.readthedocs.io/en/stable/index.html)
- [Github wtforms](https://github.com/wtforms/wtforms)
- [Flask表单：表单数据的验证与处理](https://zhuxin.tech/2017/08/26/Flask%E8%A1%A8%E5%8D%95%EF%BC%9A%E8%A1%A8%E5%8D%95%E6%95%B0%E6%8D%AE%E7%9A%84%E9%AA%8C%E8%AF%81%E4%B8%8E%E5%A4%84%E7%90%86/)
- [Flask扩展系列(七)–表单](http://www.bjhee.com/flask-ext7.html)






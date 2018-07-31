本项目是一些 Flask 中关于请求的示例。


## 环境配置

macOS/Linux:

```shell
$ pip install pipenv
$ export PIPENV_VENV_IN_PROJECT=true
$ pipenv --three
$ pipenv shell
$ pipenv install --skip-lock
```
Windows

```shell
$ pip install pipenv
$ pipenv --three
$ pipenv shell
$ pipenv install --skip-lock
```

## 启动服务

macOS/Linux/Windows：

```shell
$ python request-examples/app.py
```

或

macOS/Linux：

```shell
$ bash run.sh
```

会启动:
```shell
http://127.0.0.1:7777/
```
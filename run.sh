#!/usr/bin/env bash

export  FLASK_APP=samples/app.py  # 指定应用
export FLASK_ENV=development   # 打开调试
flask run --port 7777   # 启动，并指定端口
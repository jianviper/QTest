#!/usr/bin/env python
#coding:utf-8
from app import create_app
from flask_script import Manager, Shell

# app = create_app('default')
app = create_app('production')
manager = Manager(app)


@app.shell_context_processor
def make_shell_context():
    return dict()
manager.add_command('shell',Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()

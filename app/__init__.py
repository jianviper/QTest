#!/usr/bin/env python
#coding:utf-8
'''
Create on 2018
author:linjian
summary:为初始化做准备
'''
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_nav import Nav
from flask_nav.elements import *
from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
nav = Nav()


def create_app(config_name, main_blueprint=None):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    nav.register_element('top', Navbar('Q',
                                       View('Home', 'main.index'),
                                       View('Api Test', 'main.api_test'),
                                       View('数据可视化','main.data_visualization')
                                       ))

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    nav.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

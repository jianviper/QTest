#!/usr/bin/env python
#coding:utf-8
'''
Create on 2018
author:linjian
summary:配置选项
'''
import os

basedir = os.path.dirname(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'QSH_Test'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    HOST = '0.0.0.0'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://myuser:mypassword@192.168.2.2:33306/test_db?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://myuser:mypassword@192.168.2.2:33306/hty?charset=utf8'
    SELLER_IDS = [416, 440, 1601, 1607, 1629, 1667]


class ProductionConfig(Config):
    DEBUG = True
    HOST = '192.168.2.52'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://readonly:mypassword@192.168.2.3:33306/hty?charset=utf8'
    SELLER_IDS = [416, 440, 6716, 8199, 10814, 10819, 12865, 16126, 18405, 24993, 26206, 26210, 29427]


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

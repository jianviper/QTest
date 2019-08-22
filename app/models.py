#!/usr/bin/env python
#coding:utf-8
'''
Create on 2018
author:linjian
summary:创建模型
'''
from . import db


class Order(db.Model):
    __tablename__ = 'tb_order'
    order_id = db.Column(db.BigInteger, primary_key=True)
    order_time = db.Column(db.Date)
    order_status = db.Column(db.Integer)

    def __repr__(self):
        return '<Order %r>' % self.order_id, self.order_time, self.order_status


class OrderSupplier(db.Model):
    __tablename__ = 'tb_order_supplier'
    order_id = db.Column(db.BigInteger, primary_key=True)
    user_id_supplier = db.Column(db.BigInteger)

    def __repr__(self):
        return '<OrderSupplier %r>' % self.order_id, self.user_id_supplier


class UserSeller(db.Model):
    __tablename__ = 'tb_web_user_seller'
    user_id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(60))

    def __repr__(self):
        return '<UserSeller %r>' % self.user_id, self.company

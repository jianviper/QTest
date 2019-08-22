#!/usr/bin/env python
#coding:utf-8
from dateutil.relativedelta import relativedelta
from datetime import datetime
from flask import current_app
from sqlalchemy import and_, func

from ..models import Order, OrderSupplier, UserSeller


class Visualization():
    def sub_query(self, dbsession, dateGet):  #子查询
        startDate = datetime.now() - relativedelta(months=dateGet)
        subQuery = dbsession.query(Order.order_time, OrderSupplier.order_id, UserSeller.company,
                                   OrderSupplier.user_id_supplier).join(
            OrderSupplier, Order.order_id == OrderSupplier.order_id).outerjoin(
            UserSeller, OrderSupplier.user_id_supplier == UserSeller.user_id).filter(
            and_(Order.order_time.between(startDate.strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d')),
                 Order.order_status == 3,
                 OrderSupplier.user_id_supplier.in_(current_app.config['SELLER_IDS']))).subquery()
        return subQuery

    def query_result(self, dbsession, dateGet, dateStep):  #查询结果
        subQuery = self.sub_query(dbsession, dateGet)
        queryResult = dbsession.query(func.DATE_FORMAT(subQuery.c.order_time, dateStep), subQuery.c.company,
                                      subQuery.c.user_id_supplier, func.count(subQuery.c.order_id)).group_by(
            func.DATE_FORMAT(subQuery.c.order_time, dateStep), subQuery.c.company).order_by(
            subQuery.c.order_time)
        return queryResult


'''
subQuery = dbsession.query(Order.order_time, OrderSupplier.order_id, UserSeller.company,
                           OrderSupplier.user_id_supplier).join(
    OrderSupplier, Order.order_id == OrderSupplier.order_id).outerjoin(
    UserSeller, OrderSupplier.user_id_supplier == UserSeller.user_id).filter(
    and_(Order.order_time.between(startDate.strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d')),
         Order.order_status == 3,
         OrderSupplier.user_id_supplier.in_(current_app.config['SELLER_IDS']))).subquery()
resultQuery = dbsession.query(func.DATE_FORMAT(subQuery.c.order_time, dateStepGet), subQuery.c.company,
                              subQuery.c.user_id_supplier, func.count(subQuery.c.order_id)).group_by(
    func.DATE_FORMAT(subQuery.c.order_time, dateStepGet), subQuery.c.company).order_by(
    subQuery.c.order_time)
'''

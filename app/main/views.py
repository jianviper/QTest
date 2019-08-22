#!/usr/bin/env python
#coding:utf-8
'''
Create on 2018
author:linjian
summary:路由和视图函数
'''
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, jsonify, current_app

from .common import Comm
from . import main
from .forms import ApiTestForm, DataVisual
from .. import db
from ..visualization import Visualization as V


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    ip_addr = request.remote_addr
    return render_template('index.html', current_time=datetime.utcnow(), ip=ip_addr)


@main.route('/apiTest', methods=['GET', 'POST'])
def api_test():
    form = ApiTestForm()
    formData = {}
    ip = request.remote_addr.split('.')[-1]
    if form.validate_on_submit():  #表单提交
        print('ip:%s,\r\nform.data:%s' % (request.remote_addr, form.data))
        formData['host'] = form.site.data
        formData['api_name'] = form.api_name.data.strip()
        formData['url'] = form.site.data.split('|')[0] + '/' + form.api_name.data.strip()
        formData['data'] = Comm().str_to_dictRawline(form.api_data.data.strip().replace(' :', ':').replace(': ', ':'))
        formData['check_login'] = form.check_login.data
        formData['check_openid'] = form.check_openid.data
        formData['company'] = form.company.data.strip()
        formData['username'] = form.username.data.strip()
        formData['stock_list'] = form.stock_list.data.strip()
        formData['stock_id'] = form.stock_id.data.strip()
        formData['password'] = form.password.data.strip()
        formData['pwd'] = form.pwd.data.strip()
        formData['cookies'] = {'_s_openid': form.s_openid.data.strip()}
        formData['thread_num'] = form.thread_num.data
        formData['ip'] = ip
        if formData.get('stock_list'):
            formData['stock_name'] = Comm().handle_stock(formData.get('stock_list').strip(), formData.get('stock_id'))
            print('stock_id:%s,stock_name:%s' % (formData['stock_id'], formData['stock_name']))
        if formData.get('check_login') == True and (formData.get('username') == '' or formData.get('password') == ''):
            flash('请输入用户名和密码')
        elif formData.get('check_login') == True and formData.get('host').split('|')[1][0] == 's' and formData.get(
                'company') == '':
            flash('请输入公司编号')
        else:
            print('formData:%s' % (formData))
            Comm().do_test(formData)  #执行测试
            return redirect(url_for('.api_test'))
    resultData = ''
    #print(ResponseText.rcontent)
    if Comm.rcontent.get(ip):
        resultData=''.join(Comm.rcontent[ip])
        print('resultData:%s' % resultData)
    return render_template('apiTest.html', form=form, result=resultData)


@main.route('/dataVisualization', methods=['GET', 'POST'])
def data_visualization():
    form = DataVisual()
    if request.method == 'POST':
        visual_data = []
        try:
            dateGet = int(request.json['dateSelected'])  #时间范围
            dateStepGet = request.json['dateStep']  #时间间隔
            #print(dateStepGet)
            enginer = db.create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
            dbsession = db.Session(bind=enginer)
            resultQuery = V().query_result(dbsession, dateGet, dateStepGet)  #查询结果
            #print(resultQuery)
            query_result = resultQuery.all()
            #print(query_result)
            for i in query_result:
                name = str(i[1]).replace('车辆销售有限公司', '').replace('汽车销售有限公司', '').replace('修车仔连锁（', '').replace('）', '')
                visual_data.append({'date': i[0], 'name': name, 'type': i[2], 'value': str(i[3])})
            print(visual_data.__len__())
            return jsonify({'mydata': visual_data})
        except BaseException as e:
            print(e)
            flash(e)
            return redirect(url_for('.data_visualization'))
    return render_template('dataVisualization.html', form=form)


@main.route('/getStocks', methods=['GET', 'POST'])
def get_stocks():
    if request.method == 'POST':
        print('stockForm:%s' % request.form)
        username = request.form.get('username')
        host = 'http://a.zj-qsh.com:8081|pc'
        if request.form.get('site').split('.')[1] == '8673h':
            host = 'http://www.8673h.com|pc'
        url = host.split('|')[0] + '/Action/QueryStockWriterJson.do'
        data = {'JsonType': 'queryStock', 'login_name': username}
        stock_data = eval(Comm().api_getdata(url, data, ck={}, header=Comm().build_header(host))[0])
        print('stock_data:%s' % stock_data)
        return jsonify(stock_data['data'])
    else:
        return jsonify({})

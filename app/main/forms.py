#!/usr/bin/env python
#coding:utf-8
'''
Create on 2018
author:linjian
summary:表单
'''
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *


class ApiTestForm(FlaskForm):
    site_choices = [('http://a.zj-qsh.com|mm', 'M测试(a.zj-qsh.com)'),
                    ('http://m.8673h.com|mm', 'M正式(m.8673h.com)'),
                    ('http://a.zj-qsh.com|md', '门店APP测试(a.zj-qsh.com)'),
                    ('http://m.8673h.com|md', '门店APP正式(m.8673h.com)'),
                    ('http://a.zj-qsh.com:8081|pc', '进销存测试(a.zj-qsh.com:8081)'),
                    ('http://www.8673h.com|pc', '进销存正式(www.8673h.com)'),
                    ('http://a.zj-qsh.com:8081|pc', 'PC测试(a.zj-qsh.com:8081)'),
                    ('http://www.8673h.com|pc', 'PC正式(www.8673h.com)'),
                    ('http://oa.juzibuluo.cn|sa', 'SGMW-APP测试(oa.juzibuluo.cn)'),
                    ('https://wl.sgmwsales.com|sa', 'SGMW-APP正式(wl.sgmwsales.com)'),
                    ('http://oa.juzibuluo.cn|sp', 'SGMW测试(oa.juzibuluo.cn)'),
                    ('https://wl.sgmwsales.com|sp', 'SGMW正式(wl.sgmwsales.com)'),
                    ('oa.juzibuluo.cn/oa-flow/', '【暂不可用】SGMW测试流程(oa.juzibuluo.cn)'),
                    ('wl.sgmwsales.com/oa-flow/', '【暂不可用】SGMW正式流程(wl.sgmwsales.com)')]
    site = SelectField(label='环境选择', choices=site_choices, render_kw={'onchange': 'checkLogin()'})
    api_name = StringField('接口名，格式：Action/LunBoAction.do', validators=[DataRequired()], render_kw={
        'placeholder': u'请输入接口名', 'onchange': 'inputData()'})
    check_login = BooleanField('是否登录', render_kw={'onclick': 'checkLogin()', 'value': 'unchecked'})
    company = StringField('公司', render_kw={'placeholder': 'SGMW/经销商/服务商'})
    username = StringField('用户名', render_kw={'placeholder': '手机/邮箱/用户名', 'onblur': 'getStock()'})
    password = StringField('密码',render_kw={'onblur': 'encrypt()'})
    stock_list = TextAreaField(label='仓库(点击刷新）', render_kw={'onfocus': 'getStock()'})
    stock_id = StringField(label='选择仓库（输入仓库编号）', render_kw={'placeholder': '请输入仓库编号'})
    check_openid = BooleanField('s_openid', render_kw={'onclick': 'checkOpenid()', 'value': 'unchecked'})
    s_openid = StringField('S_openid')
    pwd=StringField('加密密码')
    api_data = TextAreaField('参数格式：{"car_model_id":13,"year":2013}或page_id:3(换行)ad_id:1或car_model_id:13,year:2013',
                             render_kw={'rows': '16'})
    thread_num = IntegerField('并发数', validators=[NumberRange(1, 5000)], render_kw={'placeholder': '填写并发数', 'value': 1})
    submit = SubmitField('提交', render_kw={'onclick': 'checkUser();'})


class DataVisual(FlaskForm):
    date_choices = [(1, '一个月'), (3, '三个月'), (6, '半年'), (12, '一年')]
    date_step = [('%Y-%m-%d', '按天'), ('%Y年(%m月)第%u周', '按周'), ('%Y年%m月', '按月')]
    date_get = SelectField(label='时间范围', choices=date_choices,
                           render_kw={'v-model': 'selected', 'style': 'width:100%;color:black'})
    date_step_get = SelectField(label='时间间隔', choices=date_step,
                                render_kw={'v-model': 'stepSelected', 'style': 'width:100%;color:black'})
    submit = SubmitField('确定')

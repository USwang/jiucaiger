import time
from datetime import datetime
from flask import Blueprint, request, render_template
from exts import db
from getdatafuns import pageNumber, getjson_stocklist, getjson_stockprice, getjson_stockincome
from models import Stockdata
from utils import restful
import numpy as np

bp = Blueprint("front", __name__, url_prefix='/')


@bp.route('/getdata/',methods=['GET', 'POST'])
def getdata():
    return render_template('front/get_data.html')

@bp.post('/getdatalist/')
def getlist():
    user = request.form.get('user')
    password = request.form.get('password')
    # 更新数据库
    if user == 'wsy' and password == 'mtjb1..':
        print('ok')
        try:
            totolPage = pageNumber()
            for page in range(totolPage):
                list_pages = getjson_stocklist(page + 1)
                for lists_page in list_pages:
                    SECURITY_CODE = lists_page['SECURITY_CODE']
                    print(SECURITY_CODE)
                    SECURITY_NAME_ABBR = lists_page['SECURITY_NAME_ABBR']
                    # 判断是否已经在数据库，
                    li = db.session.query(Stockdata).filter_by(SECURITY_CODE=SECURITY_CODE).first()
                    if not bool(li):
                        # li.SECURITY_CODE = SECURITY_CODE
                        # li.SECURITY_NAME_ABBR = SECURITY_NAME_ABBR
                        # db.session.commit()
                        stockdata = Stockdata(SECURITY_CODE=SECURITY_CODE, SECURITY_NAME_ABBR=SECURITY_NAME_ABBR)
                        db.session.add(stockdata)
                        db.session.commit()
                    # time.sleep(3)
        except Exception as e:
            print(e)
    else:
        return restful.params_error(message='账号或密码错误')
    return restful.ok(message='finished update_list')


@bp.post('/getdataprice/')
def get_price():
    user = request.form.get('user')
    password = request.form.get('password')
    # 更新数据库
    if user == 'wsy' and password == 'mtjb1..':
        print('ok')
        lies = db.session.query(Stockdata).all()
        if bool(lies):
            for li in lies:
                SECURITY_CODE = li.SECURITY_CODE
                da = db.session.query(Stockdata).filter_by(SECURITY_CODE=SECURITY_CODE).first()
                try:
                    pricedatajson = getjson_stockprice(SECURITY_CODE)
                except Exception as e:
                    print(e)
                if da:
                    da.PRICE_datajson = pricedatajson
                    db.session.commit()
                else:
                    stockdata = Stockdata(PRICE_datajson=pricedatajson)
                    db.session.add(stockdata)
                    db.session.commit()
        else:
            return restful.ok(message='no list')
    return restful.ok(message='finished update_list')

@bp.post('/getdataincome/')
def get_income():
    now = datetime.now()
    date_only = now.date()
    # print(date_only)
    username = request.form.get('user')
    # print(username)
    password = request.form.get('password')
    # print(password)
    id_ = request.form.get('id_')
    numbers = [int(n) for n in id_.split(':')]
    Lists = np.arange(numbers[0],numbers[1])
    if username == 'wsy' and password == 'mtjb1..':
        #如果填入了具体ID则单独更新
        if numbers:
            for _id in Lists:
                print(_id)
                lie = db.session.query(Stockdata).get(_id) #获取stock列表
                SECURITY_CODE = lie.SECURITY_CODE
                try:
                    income = getjson_stockincome(SECURITY_CODE)
                except Exception as e:
                    print(SECURITY_CODE, e)
                lie.INCOME_datajson = income
                lie.INCOME_updatetime = date_only
                db.session.commit()
        else:
            lies = db.session.query(Stockdata).all()  # 获取stock列表
            if lies:
                for li in lies:
                    ID = li.id
                    print(ID)
                    INCOME_updatetime = li.INCOME_updatetime
                    SECURITY_CODE = li.SECURITY_CODE
                    if not INCOME_updatetime:
                        try:
                            income = getjson_stockincome(SECURITY_CODE)
                        except Exception as e:
                            print(SECURITY_CODE, e)
                        li.INCOME_datajson = income
                        li.INCOME_updatetime = date_only
                        db.session.commit()
                    elif INCOME_updatetime.date() == date_only:  #如果更新日期和数据库更新日期一致
                        continue
                    else:
                        try:
                            income = getjson_stockincome(SECURITY_CODE)
                        except Exception as e:
                            print(SECURITY_CODE, e)
                        li.INCOME_datajson = income
                        li.INCOME_updatetime = date_only
                        db.session.commit()
    else:
        return restful.permission_error()
    return restful.ok()
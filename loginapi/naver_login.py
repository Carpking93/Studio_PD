from flask import Flask, render_template ,request ,redirect ,session ,url_for, flash
from mysql import Mysql
import config
import pymysql
from datetime import timedelta
from functools import wraps
import requests
from flask_mail import Mail, Message
from random import randint
from flask import Blueprint


mysql = Mysql(password="coramdeo")



bp = Blueprint('naver', __name__, url_prefix='/')




@bp.route("/naver")
def NaverLogin():
    client_id = "xQblil4Y1DlLCIc7nLfa"
    redirect_uri = "https://jyahn.pythonanywhere.com/callback"
    url = f"https://nid.naver.com/oauth2.0/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    return redirect(url)

@bp.route("/callback")
def callback():
    params = request.args.to_dict()
    code = params.get("code")
    client_id = "xQblil4Y1DlLCIc7nLfa"
    client_secret = "tDRlsSv0cz"
    redirect_uri = "https://jyahn.pythonanywhere.com/callback"
    token_request = requests.get(f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}")
    token_json = token_request.json()
    print(token_json)
    access_token = token_json.get("access_token")
    profile_request = requests.get("https://openapi.naver.com/v1/nid/me", headers={"Authorization" : f"Bearer {access_token}"},)
    profile_data = profile_request.json()
    print(profile_data)
    # 네이버 접속 시 유저 정보 전달 받기
    naver_name = profile_data['response']['name']
    naver_email = profile_data['response']['email']
    naver_phone = "naver"
    naver_password = str(randint(1000000, 9999999))
    # print(naver_name)
    # print(naver_email)
    # print(naver_id)
    # user_naver = mysql.naver_insert_user(naver_id, naver_age, naver_gender, naver_email, naver_name)
    # print(user_naver)
    # print(profile_data['response']['email'])
    # 접속한 유저 정보 중 email정보를 통해 가입여부를 확인
    result  = mysql.naver_email_check(naver_name, naver_email, naver_phone, naver_password)
    print(result)

    if len(result) != 0:
        session['is_loged_in'] = True
        session['username'] = naver_name
        session['email'] = naver_email
        session['password'] = naver_password
        return redirect('/')
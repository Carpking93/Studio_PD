from flask import Flask , render_template ,request ,redirect ,session ,url_for, flash
from mysql import Mysql
import pymysql
# from datetime import timedelta
# from functools import wraps
import requests
# from flask_mail import Mail, Message
# from random import randint
from flask import Blueprint



bp = Blueprint('kakao', __name__, url_prefix='/')


mysql = Mysql(password="coramdeo")
class Mytest:
    def __init__(self , host='jyahn.mysql.pythonanywhere-services.com', user='jyahn', db='jyahn$studio', password='coramdeo', charset='utf8'):
            self.host = host
            self.user = user
            self.db = db
            self.password = password
            self.charset = charset

@bp.route('/kakao')
def kakao_sign_in():
    client_id = "1b8666766ab7f094d5853843728f0cd7"
    redirect_uri = "https://jyahn.pythonanywhere.com/oauth"
    # 카카오톡으로 로그인 버튼을 눌렀을 때
    kakao_oauth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    return redirect(kakao_oauth_url)


@bp.route('/oauth')
def callback():
    code = request.args.get("code")
    client_id = "1b8666766ab7f094d5853843728f0cd7"
    client_secret = "jrFDuU4SdW44S8gZVHELiPanjdUAi1OX"
    redirect_uri = "https://jyahn.pythonanywhere.com/oauth"
    token_request = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={code}")
    token_json = token_request.json()
    # print(token_json)
    access_token = token_json.get("access_token")
    profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"},)
    profile_data = profile_request.json()
    print(profile_data)

    # 카카오 로그인 시 유저 정보 전달 받기
    kakao_name = profile_data['kakao_account']['profile']['nickname']
    kakao_email = profile_data['kakao_account']['has_email']
    kakao_email = str(kakao_email)
    kakao_phone = 'kakao'
    kakao_password = profile_data['id']
    print(kakao_name)
    print(kakao_email)
    print(type(kakao_password))
    # user_naver = mysql.naver_insert_user(naver_id, naver_age, naver_gender, naver_email, naver_name)
    # print(user_naver)
    # print(profile_data['response']['email'])
    # 접속한 유저 정보 중 email정보를 통해 가입여부를 확인
    result  = mysql.kakao_email_check(kakao_name, kakao_email, kakao_phone, kakao_password)
    db = pymysql.connect(host='jyahn.mysql.pythonanywhere-services.com', user='jyahn', db='jyahn$studio', password='coramdeo', charset='utf8')
    curs = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from user where password = %s;'
    curs.execute(sql, kakao_password)
    rows = curs.fetchall()
    print(rows)
    if len(result) != 0:
        session['is_loged_in'] = True
        session['username'] = rows[0]['username']
        session['email'] = rows[0]['email']
        session['phone'] = rows[0]['phone']
        session['password'] = rows[0]['password']
    return redirect('/')




from flask import Flask , render_template ,request ,redirect ,session , flash
from mysql import Mysql
# from data import Articles
from loginapi import naver_login, kakao_login
import config
import pymysql
from datetime import timedelta
# print(Articles())
from functools import wraps
from flask_mail import Mail, Message
from random import randint
# import ctypes
# from plyer import notification1

app = Flask(__name__)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=1000)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] ='eungok'

#0828
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bigpiggood@gmail.com'
app.config['MAIL_PASSWORD'] = 'rylatwbfpdykbkoz'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

mysql = Mysql()

def is_loged_in(func):
    @wraps(func)
    def wrap(*args , **kwargs):
        if 'is_loged_in' in session:
            return func(*args , **kwargs)
        else:
            return redirect('/loginst')
    return wrap

@app.route('/' , methods=['GET','POST'])
# @is_loged_in
def index():
    if request.method == "GET":
        os_info = dict(request.headers)
        # print(os_info)
        name = request.args.get("name")
        # print(name)
        hello = request.args.get("hello")
        # print(hello)
        return render_template('indexst.html',header=f'{name}님 {hello}!!' )

    elif request.method == "POST":
        data  = request.form.get("name")
        data_2 = request.form['hello']
        # print(data_2)
        return render_template('indexst.html')
    # print(session['is_loged_in'])
    return render_template('indexst.html')
    # print(session['id'])

@app.route('/registerst', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        number = request.form.get('number')
        phone = request.form.get('phone')
        password = request.form.get('password')
        print(username , email , phone , password)

        db = pymysql.connect(host=mysql.host, user=mysql.user, db=mysql.db, password=mysql.password, charset=mysql.charset)
        curs = db.cursor()

        sql = f'SELECT * FROM user WHERE email = %s;'
        curs.execute(sql , email)

        rows = curs.fetchall()
        print(rows)

        user_otp = session['user_otp']
        user_email = session['user_email']

        if rows:
            flash("이미 가입된 회원입니다.")
            # ctypes.windll.user32.MessageBoxW(0, "이미 가입된 회원입니다.", "알림", 48)
            # notification.notify(
            #     title = 'testing',
            #     message = 'message',
            #     app_icon = None,
            #     timeout = 10,)
            return render_template('registerst.html')

        elif user_otp!=number or user_email!=email:
             flash("인증번호가 일치하지 않습니다")
             return redirect('/registerst')

        else:
            result = mysql.insert_user(username, email ,phone,password )
            flash("회원가입이 완료되었습니다.")
            print(result)
            return redirect('/loginst')

    elif request.method == "GET":
        return render_template('registerst.html')

@app.route('/loginst',  methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('loginst.html')
    elif request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        db = pymysql.connect(host=mysql.host, user=mysql.user, db=mysql.db, password=mysql.password, charset=mysql.charset)
        curs = db.cursor()

        sql = f'SELECT * FROM user WHERE email = %s;'
        curs.execute(sql , email)

        rows = curs.fetchall()
        # print(rows)

        if rows:
            result = mysql.verify_password(password, rows[0][4])
            if result:
                session['is_loged_in'] = True
                session['id'] = rows[0][0]
                session['username'] = rows[0][1]
                session['email'] = rows[0][2]
                session['phone'] = rows[0][3]
                session['password'] = rows[0][4]
                return redirect('/')
                # return render_template('index.html', is_loged_in = session['is_loged_in'] , username=session['username'] )
                print(rows[0][4])
            else:
                flash("회원정보가 틀립니다.")
                # ctypes.windll.user32.MessageBoxW(0, "회원정보가 틀립니다.", "알림", 16)
                return redirect('/loginst')
        else:
            flash("회원정보가 틀립니다.")
            return render_template('loginst.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route("/email", methods=['GET', 'POST'])
def send_email():
    if request.method == 'GET':
        return render_template('email.html')

    elif request.method == 'POST':
        user_mail = request.form['usermail']
        db = pymysql.connect(host=mysql.host, user=mysql.user, db=mysql.db, password=mysql.password, charset=mysql.charset)
        curs = db.cursor()
        sql = f'SELECT * FROM user WHERE email = %s;'
        curs.execute(sql , user_mail)
        rows = curs.fetchall()
        if rows:
           flash("이미 가입된 이메일주소입니다.")
           return redirect('/email')
        else:
            otp = str(randint(100000, 999999))
            session['user_otp'] = otp  # 세션에 인증번호 저장
            usermail = request.form['usermail']
            session['user_email'] = usermail
            msg = Message('studioPD 이메일 인증', sender=config.MAIL_USERNAME, recipients=[usermail])
            msg.body = '안녕하세요. studioPD 입니다.\n인증번호를 입력하여 이메일 인증을 완료해 주세요.\n인증번호 : {}'.format(otp)
            mail.send(msg)
            flash("인증번호를 발송하였습니다")
            return redirect('/registerst')
# 유저 비밀번호 변경 요청
@app.route("/change_password", methods=['GET', 'POST'])
def change_password():
    if request.method == 'GET':
        return render_template('change_password.html')
    if request.method == 'POST':
        user_mail = request.form['user_mail']
        db = pymysql.connect(host=mysql.host, user=mysql.user, db=mysql.db, password=mysql.password, charset=mysql.charset)
        curs = db.cursor()
        sql = f'SELECT * FROM user WHERE email = %s;'
        curs.execute(sql , user_mail)
        rows = curs.fetchall()
        if rows:
            otp = str(randint(100000, 999999))
            session['user_otp'] = otp  # 세션에 인증번호 저장
            session['user_email'] = user_mail
            msg = Message('studioPD 이메일 인증', sender=config.MAIL_USERNAME, recipients=[user_mail])
            msg.body = '안녕하세요. studioPD 입니다.\n인증번호를 입력하여 이메일 인증을 완료해 주세요.\n인증번호 : {}'.format(otp)
            mail.send(msg)
            flash("인증번호를 발송하였습니다")
            return redirect('/update')
        else:
            flash("가입되지 않은 이메일주소입니다.")
            return redirect('/change_password')

# 유저 비밀번호 변경 창으로 이동
@app.route("/update", methods=['GET', 'POST'])
def change():
    if request.method == 'GET':
        return render_template('update.html')
    if request.method == 'POST':
        email = request.form.get('email')
        number = request.form.get('number')
        password = request.form.get('password')
        user_otp = session['user_otp']
        user_email = session['user_email']
        if user_email==email and user_otp==number:
           result = mysql.update_user(password, email)
           flash("비밀번호 변경완료! 다시 로그인해주세요.")
           print(result)
           return redirect('/loginst')
        else:
            flash("인증번호가 일치하지 않습니다.")
            return redirect('/update')

@app.route('/lists', methods=['GET' , 'POST'])
def lists():
    if request.method == "GET":
        result = mysql.get_data()
        print(result)
        return render_template('lists.html', data=result)

    elif request.method =="POST":
        title = request.form['title']
        cont = request.form['cont']
        author = request.form['author']
        result = mysql.insert_list(title , cont , author)
        print(result)
        return redirect('/lists')

@app.route('/create_list')
def create_list():
    return render_template('dashboard.html')

@app.route('/view/<ids>',methods=['GET','POST'])
def view(ids):
    if request.method == 'GET':
        db = pymysql.connect(host=mysql.host, user=mysql.user, db=mysql.db, password=mysql.password, charset=mysql.charset)
        curs = db.cursor()

        sql = f'SELECT * FROM posts WHERE `id` = %s;'
        curs.execute(sql , ids)

        rows = curs.fetchall()
        print(rows)
        db.close()
        return render_template('view.html',data = rows)

    elif request.method == 'POST':
        ids =request.form['ids']
        title = request.form['title']
        cont = request.form['cont']
        author = request.form['author']

        result = mysql.update_list(ids,title,cont,author)
        print(ids)
        return redirect('/lists')

@app.route('/edit/<ids>',methods=['GET','POST'])
def edit(ids):
    print(ids)
    if request.method == 'GET':
        db = pymysql.connect(host=mysql.host, user=mysql.user, db=mysql.db, password=mysql.password, charset=mysql.charset)
        curs = db.cursor()

        sql = f'SELECT * FROM posts WHERE `id` = %s;'
        curs.execute(sql , ids)

        rows = curs.fetchall()
        print(rows)
        # db.close()
        return render_template('list_edit.html',data = rows)

    elif request.method == 'POST':
        ids = request.form['ids']
        title = request.form['title']
        cont = request.form['cont']
        author = request.form['author']
        print(ids)

        result = mysql.update_list(ids,title,cont,author)
        print(result)
        return redirect('/lists')


@app.route('/sub' , methods=['GET','POST'])
def sub():
    if request.method == 'GET':
        datas = mysql.star()
        print(datas)

        for i in datas:
            if i['reviewStar'] == None:
                i['reviewStar'] = 0

            else:
                i['reviewStar'] = i['reviewStar']
        print(datas)

        return render_template('sub.html', data = datas)


# 상세페이지 이동 / 예약 기능 구현중

@app.route('/detail/<id>',  methods=['GET', 'POST'])
def detail(id):
    # Check if the user is_loged_in
    # Continue with the original code
    if request.method == "GET":
        result = mysql.star()
        id = int(id)
        result = result[id]
        result2= mysql.get_reservation(id)
        result3, result4 = mysql.get_review_star()
        print(result)
        print(result2)
        print(result3)
        print(result4)
        print('====***====')

        reivew_list = []
        star_list = []
        for result4_data in result4:
            if result4_data['studio_id'] == id:
               reivew_list.append(result4_data['review'])
               star_list.append(result4_data['reviewStar'])
        #        print(result4_data['studio_id'])
        #        print(result4_data['review'])
        #        print(result4_data['reviewStar'])
        # print(reivew_list)
        # print(star_list)
        result5 = dict(zip(reivew_list, star_list))
        # print(result5)

        # result3({스튜디오아이디 : 평균별점, ...})에 id값이 없을 경우
        if result3.get(id) == None:
            result3 = '등록된 리뷰가 없습니다'

        # result3에 id값이 있을 경우 id를 '키'값으로 하는 '밸류'값 전달
        else:
            result3 = result3.get(id)

        return render_template('detail.html', data=result, data2=result2, data3=result3, data4 = result5)



    elif request.method == "POST":
        if not session.get('is_loged_in'):
                # Redirect the user to the login page
                return redirect('/loginst')
        else:
            result = mysql.star()
            id = int(id)
            result = result[id]
            studio_id = request.form.get('ids')
            studio_name = request.form.get('name')
            studio_date = request.form.get('reservation')
            email = session['email']
            result2= mysql.get_reservation(id)
            check_result = mysql.insert_reservation(studio_id, studio_name, studio_date, email)
            flash("예약완료")
            return redirect(f'/detail/{id}')
@app.route('/master' , methods=['POST','GET'])
def master():
    if request.method == "GET":
        return render_template('master.html')

@app.route('/change_email', methods=['GET'])
def change_email():
    return render_template('change_email.html')


@app.route("/update_email", methods=["POST"])
def update_email():
    password = request.form['password']
    username = request.form["username"]
    new_email = request.form["new_email"]
    phone = request.form["phone"]
    print('뽀뽀잉')
    db = pymysql.connect(host=mysql.host, user=mysql.user, db=mysql.db, password=mysql.password, charset=mysql.charset)
    curs = db.cursor()

    # email을 업데이트
    # sql = "UPDATE user SET email=%s WHERE username=%s"
    # curs.execute(sql, (new_email, username))
    # result = mysql.updates_user(new_email, username)
    result = mysql.updates_user( username,new_email,phone,password)
    db.close()
    print(new_email)
    print(username)
    # session['email'] = session['email']
    session['phone'] = request.form["phone"]
    session.update()
    print(password)
    return redirect('/')


# 스튜디오 예약 취소 (수정됨)
@app.route('/myreservation',  methods=['GET', 'POST'])
def myreservation():
    if request.method == "GET":
        email = session['email']
        result = mysql.cancel_reservation(email)
        print(result)
        return render_template('myreservation.html', data=result)
    if request.method == "POST":
    #  request.form.getlist 는 다중 name값을 리스트형태로 저장해줌.
    #  체크박스 한개만 선택해도 리스트 형식으로 전달됨
    #  cancel_number = request.form.get("number") : 변경 전
       cancel_number = request.form.getlist("number")
       print("============================")
       print(cancel_number)
    # mysql.delete_reservation에 리스트 형태로 값을 전달
       if cancel_number:
           result = mysql.delete_reservation(cancel_number)
           print(result)
           return redirect('/myreservation')
       else:
           flash('하나이상 선택해주세요')
           return redirect('/myreservation')

# 유저 가입정보 확인 및 비밀번호 변경
@app.route('/info',  methods=['GET', 'POST'])
def info():
    if request.method == "GET":
        return render_template('info.html')

    if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            result = mysql.update_user(password, email)
            flash("비밀번호 변경완료! 다시 로그인해주세요.")
            print(result)
            return redirect('/loginst')
            # result = mysql.info_change(username, email, number, password)
            # print(result)


# @app.route('/review',  methods=['GET', 'POST'])
# def review():
#     if request.method == "GET":
#         return render_template('review.html')

#     if request.method == 'POST':
#     #     reviewStar = request.form.get('reviewStar')
#     #     print(reviewStar)
#         return redirect('/myreservation')


# @app.route('/popup',  methods=['GET', 'POST'])
# def popup():
#     print(request.form)
#     if request.method == "GET":
#         studio_number = request.args.get('number')
#         return render_template('popup.html',studio_number=studio_number)

#     if request.method == 'POST':
#         reviewStar = request.form.get('reviewStar')
#         studio_id = request.form.get("number")
#         review = request.form.get("review")
#         print(review)

#         result = mysql.update_reservation(reviewStar,studio_id)
#         print(result)
#         return redirect('/close')

# @app.route('/close')
# def close():
#     return render_template('close.html')



@app.route('/popup/<date>/<name>/<number>/<id>', methods=['GET', 'POST'])
def popup(date, name, number, id):
    if request.method == 'GET':
        result1 = date
        result2 = name
        result3 = number
        result4 = id
        return render_template('popup.html', data1 = result1, data2 = result2, data3 = result3, data4 = result4)

    if request.method == 'POST':
        number = request.form.get('number')
        studio_name = request.form.get('studio_name')
        review = request.form.get('review')
        reviewStar = request.form.get('reviewStar')
        studio_id = request.form.get('studio_id')
        # print(number)
        # print(studio_name)
        # print(review)
        # print(reviewStar)
        # print(studio_id)

        result1 = mysql.insert_reivew(number, studio_name, review, reviewStar, studio_id)
        # print(result1)
        result2 = mysql.delete_reservation(number)
        # print(result2)

        return redirect('/myreservation')


@app.route('/review_list', methods=['GET', 'POST'])
def review_list():
    if request.method == 'GET':
        result = mysql.star()
        return render_template('review_list.html')



# 파일 전송 테스트
@app.route('/test_studio', methods=['GET', 'POST'])
def test_studio():
    if request.method == 'GET':
        return render_template('test_studio.html')

    if request.method == 'POST':
        studio_file = request.form.get('studio_file')
        print(type(studio_file))
        print(studio_file)
        return redirect('/test_studio')

@app.route('/infomation')
def ifmation():
    return render_template('infomation.html')



app.register_blueprint(naver_login.bp)
app.register_blueprint(kakao_login.bp)

if __name__ == '__main__':
    app.run(debug=True)
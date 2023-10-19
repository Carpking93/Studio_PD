import pymysql
# 암호화 알고리즘. 256을 제일 많이 사용한다.
from passlib.hash import pbkdf2_sha256
import pandas as pd

# 원문 비밀번호를, 암호화 하는 함수

def hash_password(original_password):
    salt = 'eungok'
    password = original_password + salt
    password = pbkdf2_sha256.hash(password)
    return password

def check_password(input_password , hashed_password):
    salt= 'eungok'
    password = input_password + salt
    result = pbkdf2_sha256.verify(password , hashed_password)
    return result


class Mysql:
    def __init__(self , host='jyahn.mysql.pythonanywhere-services.com', user='jyahn', db='jyahn$studio', password='coramdeo', charset='utf8'):
        self.host = host
        self.user = user
        self.db = db
        self.password = password
        self.charset = charset

    def get_user(self):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()

        sql = "select * from user";
        curs.execute(sql)

        rows = curs.fetchall()
        # db.commit()
        db.close()
        return rows

    def insert_user(self , username ,password):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()

        sql = '''insert into user (usernamepassword) values(%s,%s)'''
        hashed_password = hash_password(password)
        result = curs.execute(sql,(username,hashed_password))
        print(result)
        db.commit()
        db.close()

        return result

    # 네이버 접속한 유저 정보를 mysql DB와 비교. 가입정보가 있으면 가입x, 없으면 DB에 새로 저장
    def naver_email_check(self, naver_name, naver_email, naver_phone, naver_password):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()
        sql = "select * from user WHERE email = %s";
        curs.execute(sql , (naver_email))
        rows = curs.fetchall()
        for mysql_user_email in rows:
            if naver_email in mysql_user_email:
                return "존재하는 이메일"
        else:
            db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
            curs = db.cursor()
            sql = '''insert into user (username, email, phone, password) values(%s,%s,%s,%s)'''
            # hashed_password = hash_password(password)
            result = curs.execute(sql,(naver_name, naver_email, naver_phone, naver_password))
            print(result)
            db.commit()
            db.close()
        return result


    def insert_user(self , username , email , phone , password):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()

        sql = '''insert into user (username, email, phone, password) values(%s,%s,%s,%s)'''
        hashed_password = hash_password(password)
        result = curs.execute(sql,(username, email, phone,hashed_password))
        print(result)
        db.commit()
        db.close()

        return result

    # 비밀번호 변경 시 유저 데이터 업데이트
    def update_user(self, password, email):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()
        sql = 'update user set password=%s WHERE email=%s;'
        hashed_password = hash_password(password)
        result = curs.execute(sql, (hashed_password, email))
        print(result)
        db.commit()
        db.close()
        return result

    def updates_user(self, username,email,phone,password):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()
        sql = 'update user set username=%s, email=%s, phone=%s WHERE password=%s;'
        result = curs.execute(sql, (username,email,phone,password))
        print(phone)
        db.commit()
        db.close()
        return result

    # 카카오 로그인 유저 정보를 mysql DB와 비교. 가입정보가 있으면 가입x, 없으면 DB에 새로 저장
    def kakao_email_check(self, kakao_name, kakao_email, kakao_phone, kakao_password):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()
        sql = "select * from user WHERE password = %s";
        curs.execute(sql , (kakao_password))
        rows = curs.fetchall()
        if len(rows) != 0:
            for mysql_kakao_names in rows:
                if kakao_name in mysql_kakao_names:
                    return rows
        else:
            db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
            curs = db.cursor()
            sql = '''insert into user (username, email, phone, password) values(%s,%s,%s,%s)'''
            # hashed_password = hash_password(password)
            result = curs.execute(sql,(kakao_name, kakao_email, kakao_phone, kakao_password))
            print(result)
            db.commit()
            db.close()
            return str(result)


    def get_data(self):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()

        sql = "select * from posts";
        curs.execute(sql)

        rows = curs.fetchall()
        # db.commit()
        db.close()
        return rows

    def insert_list(self , title , cont , author):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()

        sql = '''insert into `posts` (`title` , `cont` , `author`) values(%s,%s,%s)'''
        result = curs.execute(sql,[title , cont , author])
        print(result)
        db.commit()
        db.close()

        return result

    # def view_list(self ,id , title , cont , author):
    #     db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
    #     curs = db.cursor()

    #     sql = f'select * from posts WHERE `id`=%s;'
    #     result = curs.execute(sql,[id])
    #     print(result)
    #     db.commit()
    #     db.close()

    #     return result

    def update_list(self ,id , title , cont , author):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()

        sql = f'UPDATE `posts` SET `title`=%s, `cont`=%s, `author`=%s WHERE `id`=%s;'
        result = curs.execute(sql,[title , cont , author , id])
        print(result)
        db.commit()
        db.close()

        return result

    def delete_list(self ,id):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()
        sql = f'DELETE from `posts` WHERE `id`= %s'

        result = curs.execute(sql,[id])
        print(result)
        db.commit()
        db.close()

        return result


    # 스튜디오ID값으로 예약일 가져오기
    def get_reservation(self, id):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()
        sql = "select studio_date from studio_reservation WHERE studio_id= %s";
        curs.execute(sql , [id])
        rows = curs.fetchall()
        print(rows)
        date_result = []
        for x in rows:
            print(x[0].year)
            print(x[0].month)
            print(x[0].day)
            x = str(x[0].year)+'-'+str(x[0].month)+'-'+str(x[0].day)
            print(x)
            date_result.append(x)
        print(date_result)
        db.commit()
        db.close()
        return date_result



    # # 회원 이메일 확인 후 예약취소
    # def cancel_reservation(self, email):
    #     db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
    #     curs = db.cursor()
    #     sql = "select studio_date, studio_name, number, studio_id from studio_reservation WHERE email= %s";
    #     curs.execute(sql , [email])
    #     rows = curs.fetchall()
    #     print(rows)
    #     studio_date = []
    #     studio_name = []
    #     studio_number = []
    #     studio_id = []
    #     for i in rows:
    #         studio_date.append(i[0])
    #         studio_name.append(i[1])
    #         studio_number.append(i[2])
    #         studio_id.append(i[3])
    #         # print(studio_date)
    #         # print(studio_name)
    #         # print(studio_id)
    #     date_result = []
    #     for x in studio_date:
    #         # print(x.year)
    #         # print(x.month)
    #         # print(x.day)
    #         x = str(x.year)+'-'+str(x.month)+'-'+str(x.day)
    #         # print(x)
    #         date_result.append(x)
    #     # print(date_result)
    #     db.commit()
    #     db.close()
    #     # print(date_result)
    #     # print(studio_name)
    #     result = tuple(zip(date_result, studio_name, studio_number, studio_id))
    #     print(result)
    #     return result

    # # 예약일 삭제
    # def delete_reservation(self ,cancel_number):
    #     db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
    #     curs = db.cursor()
    #     # sql = f'DELETE from `studio_reservation` WHERE `number` =  %s;'
    #     # sql = "DELETE from studio_reservation WHERE number in %s)";
    #     #  테이블에서 리스트에 있는 값을 찾아 삭제
    #     sql = f"DELETE from studio_reservation WHERE number = %s";
    #     result = curs.execute(sql,[cancel_number])
    #     print(result)
    #     db.commit()
    #     db.close()
    #     return result

    # 회원 이메일 확인 후 예약취소
    def cancel_reservation(self, email):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()
        # sql = "select studio_date, studio_name, number, studio_id from studio_reservation WHERE email= %s";
        sql = """SELECT studio_date, studio_name, number, studio_id,
                CURDATE(),
                TIMESTAMPDIFF(DAY, studio_reservation.studio_date, CURDATE()) AS diff_day
                FROM studio_reservation
                WHERE email= %s""";

        curs.execute(sql , [email])
        rows = curs.fetchall()
        print(rows)
        studio_date = []
        studio_name = []
        studio_number = []
        studio_id = []
        diff_day = []
        for i in rows:
            studio_date.append(i[0])
            studio_name.append(i[1])
            studio_number.append(i[2])
            studio_id.append(i[3])
            diff_day.append(i[5])
            print(studio_date)
            print(studio_name)
            print(studio_id)
            print(diff_day)

        date_result = []
        for x in studio_date:
            # print(x.year)
            # print(x.month)
            # print(x.day)
            x = str(x.year)+'-'+str(x.month)+'-'+str(x.day)
            # print(x)
            date_result.append(x)
        # print(date_result)
        db.commit()
        db.close()
        # print(date_result)
        # print(studio_name)
        result = tuple(zip(date_result, studio_name, studio_number, studio_id, diff_day))
        print(result)
        return result

    # 예약일 삭제
    def delete_reservation(self ,cancel_number):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()
        # sql = f'DELETE from `studio_reservation` WHERE `number` =  %s;'
        # sql = "DELETE from studio_reservation WHERE number in %s)";
        #  테이블에서 리스트에 있는 값을 찾아 삭제
        sql = f"DELETE from studio_reservation WHERE number = %s";
        result = curs.execute(sql,[cancel_number])
        print(result)
        db.commit()
        db.close()
        return result




     # 예약 일자 테이블에 넣기
    def insert_reservation(self, studio_id, studio_name, studio_date, email):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()
        sql = "select * from studio_reservation WHERE (studio_id= %s) and (studio_name= %s) and (studio_date= %s) and (email= %s)";
        curs.execute(sql , [studio_id, studio_name, studio_date, email])
        rows = curs.fetchall()
        if len(rows) != 0:
            return 0
        else:
            db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
            curs = db.cursor()
            sql = '''insert into `studio_reservation` (`studio_id`, `studio_name`, `studio_date`, `email`) values(%s,%s,%s,%s)'''
            curs.execute(sql , [studio_id, studio_name, studio_date, email])
            rows = curs.fetchall()
            db.commit()
            db.close()
            return rows


    def verify_password(self, password ,hashed_password):
        # db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        # curs = db.cursor()

        # sql = f'SELECT * FROM user WHERE email = %s;'
        # curs.execute(sql , email)

        # rows = curs.fetchall()
        # print(rows)
        # db.commit()
        # db.close()
        # if len(rows) != 0:
        #     hashed_password = rows[0][4]
        #     result = check_password(password , hashed_password)
        #     if result:
        #         print("Welcome to My World!!")
        #     else:
        #         print("MissMatch Password")
        # else:
        #     print("User isnot founded")
        result = check_password(password , hashed_password)
        return result

    def Articles(self):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM studio_lists";
        curs.execute(sql)
        result = curs.fetchall()
        print("*********************************")
        json_data = []
        # for i in result:
        #     if '유형' or 'image' in i:
        #         i['유형'] = eval(i['유형'])
        #         i['image'] = eval(i['image'])
        #         json_data.append(i)
        #     else:s
        #         json_data.append(i)

        # result는 [] 안에 딕셔너리 형태로 들어옴
        # 반복문으로 result안에 있는 딕셔너리(i)자료들을 위에 만들어 놓은 빈 리스트(json_data)에 옮겨 담는데
        # 이때 i['유형'] 과 i['image']같은 경우 value값을 eval()함수를 이용하여
        # 문자열형태'[]' 에서  리스트형태 []로 변경 하여 담는다.
        for i in result:
                i['유형'] = eval(i['유형'])
                i['image'] = eval(i['image'])
                json_data.append(i)

        print(json_data)
        return json_data

    #  기존 app.py에서 data.py를 이용 json파일을 불러오기 위해 호출한 Articles() 함수는
    #  mysql.Articles()로 호출.



    # # mysql 리뷰테이블 별도 생성
    # def insert_reivew(self, number, studio_name, review, reviewStar, studio_id):
    #     db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
    #     curs = db.cursor()

    #     sql = '''insert into `studio_reivew` (`number` , `studio_name` , `review`, `reviewStar`, `studio_id`) values(%s,%s,%s,%s,%s)'''
    #     result = curs.execute(sql,[number, studio_name, review, reviewStar, studio_id])
    #     print(result)
    #     db.commit()
    #     db.close()

    #     return result




    # def get_review_star(self):
    #     db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
    #     curs = db.cursor(pymysql.cursors.DictCursor)
    #     sql = "select * from studio_reivew";
    #     curs.execute(sql)
    #     rows = curs.fetchall()

    #     df = pd.DataFrame(rows)


    #     print(df)
    #     # db.commit()
    #     db.close()
    #     print(rows)
    #     print("=========================================")

    #     return rows




    # mysql 리뷰테이블(studio_review) 별도 생성
    def insert_reivew(self, number, studio_name, review, reviewStar, studio_id):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()

        sql = '''insert into `studio_reivew` (`number` , `studio_name` , `review`, `reviewStar`, `studio_id`) values(%s,%s,%s,%s,%s)'''
        result = curs.execute(sql,[number, studio_name, review, reviewStar, studio_id])
        print(result)
        db.commit()
        db.close()

        return result


    # studio_review테이블에서 별점정보 가져오기
    def get_review_star(self):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        # df = []
        # 딕셔너리 형태로 모든 자료 가져오기
        curs = db.cursor(pymysql.cursors.DictCursor)
        curs_2 = db.cursor(pymysql.cursors.DictCursor)

        sql = "select * from studio_reivew";
        sql_2 = "select studio_id, review, reviewStar from studio_reivew";

        curs.execute(sql)
        curs_2.execute(sql_2)

        rows = curs.fetchall()
        rows_2 = curs_2.fetchall()
        # 판다스 활용, 데이터 프레임으로 변환
        # print(rows)
        # print('******================')
        print(rows_2)


        df = pd.DataFrame(rows)
        # print(df['studio_id'])

        # 별점과 스튜디오 아이디를 컬럼으로 데이터프레임 생성
        df1 = df[['reviewStar', 'studio_id']]
        # 스튜디오 아이디를 기준으로 그룹 후 평균값 계산
        grouped_mean = df1['reviewStar'].groupby(df1['studio_id']).mean()
        print(grouped_mean)
        print(grouped_mean.to_dict())
        # 딕셔너리 형태롤 변환 후 @app.route('/detail/<id>',  methods=['GET', 'POST'])에 값 전달
        result = grouped_mean.to_dict()
        print(df1)
        # db.commit()
        db.close()


        return result, rows_2



    def join(self):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)

        # 딕셔너리 형태로 모든 자료 가져오기
        curs = db.cursor(pymysql.cursors.DictCursor)
        sql = "select * from studio_reivew";
        curs.execute(sql)
        rows = curs.fetchall()



    def star(self):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        # 딕셔너리 형태로 모든 자료 가져오기
        curs = db.cursor(pymysql.cursors.DictCursor)
        sql = """SELECT * FROM studio_lists left join (SELECT studio_lists.studio_id,
              AVG(studio_reivew.reviewStar)
              AS reviewStar
              FROM studio_lists
              left join studio_reivew
              on studio_lists.studio_id = studio_reivew.studio_id
              GROUP BY studio_lists.studio_id) as b on studio_lists.studio_id = b.studio_id""";

        curs.execute(sql)
        result = curs.fetchall()
        print("*********************************")
        json_data = []
        # for i in result:
        #     if '유형' or 'image' in i:
        #         i['유형'] = eval(i['유형'])
        #         i['image'] = eval(i['image'])
        #         json_data.append(i)
        #     else:s
        #         json_data.append(i)

        # result는 [] 안에 딕셔너리 형태로 들어옴
        # 반복문으로 result안에 있는 딕셔너리(i)자료들을 위에 만들어 놓은 빈 리스트(json_data)에 옮겨 담는데
        # 이때 i['유형'] 과 i['image']같은 경우 value값을 eval()함수를 이용하여
        # 문자열형태'[]' 에서  리스트형태 []로 변경 하여 담는다.
        for i in result:
                i['유형'] = eval(i['유형'])
                i['image'] = eval(i['image'])
                json_data.append(i)

        print(json_data)
        return json_data


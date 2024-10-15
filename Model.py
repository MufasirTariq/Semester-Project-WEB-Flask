import pymysql

class Model:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def registerInspector(self, em, nm, pwd, ph, dob, edu, exp, kd, gd, type, fn):
        con = None
        cursor = None
        insert = False

        try:
            con = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                  database=self.database)
            cursor = con.cursor()

            user_sql = 'INSERT INTO User(email,password, type) VALUES(%s,%s,%s)'
            user_args = (em, pwd, type)
            cursor.execute(user_sql, user_args)
            con.commit()

            sql = 'INSERT INTO Inspector(user_id, name, phone, exp, dob, edu, gender, type, image) VALUES(LAST_INSERT_ID(),%s,%s,%s,%s,%s,%s,%s,%s)'
            args = (nm, ph, exp, dob, edu, gd, kd, fn)
            cursor.execute(sql, args)
            con.commit()
            insert = True

        except Exception as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
        return insert

    def registerVictim(self,em, pwd, nm, ph, add, dob, cnic, job, emg, gd, type, img):
        con = None
        cursor = None
        insert = False

        try:
            con = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                  database=self.database)
            cursor = con.cursor()

            user_sql = 'INSERT INTO User(email,password,type) VALUES(%s,%s,%s)'
            user_args = (em, pwd, type)
            cursor.execute(user_sql, user_args)
            con.commit()

            sql = 'INSERT INTO Victim(user_id, name, phone, address, dob, gender, cnic, job, emergency, image) VALUES(LAST_INSERT_ID(),%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            args = (nm, ph, add, dob, gd, cnic, job, emg, img)
            cursor.execute(sql, args)
            con.commit()
            insert = True

        except Exception as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
        return insert


    def loginUser(self, em, pwd):
        con = None
        cursor = None
        profile = []
        table = ""
        try:
            con = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cursor = con.cursor()

            user_sql = 'SELECT user_id FROM User WHERE email=%s and password=%s'
            user_args = (em, pwd)
            res = cursor.execute(user_sql, user_args)
            print(res)
            if res:
                x = cursor.fetchone()
                sql = "SELECT * FROM Inspector WHERE user_id = %s"
                args = (x,)
                res = cursor.execute(sql, args)
                if res:
                    row = cursor.fetchall()
                    for i in row:
                        p = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
                        profile.append(p)
                    table = "Ins"
                else:
                    sql = "SELECT * FROM Victim WHERE user_id = %s"
                    args = (x,)
                    cursor.execute(sql, args)
                    row = cursor.fetchall()
                    if row:
                        for i in row:
                            p = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]]
                            profile.append(p)
                        table = "Vic"
        except Exception as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
        return profile, table



    def UpdateIns_Profile(self, user_id, em, nm, pwd, ph, dob, edu, exp, kd, gd, fn):
        print("MODEL:IN Update Fucntion")
        con = None
        cursor = None
        Flag = False
        try:
            print("MODEL:IN Update Fucntion, TRY:")
            con = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cursor = con.cursor()
            print("Connection done")

            sql = "UPDATE User SET email = %s, password = %s WHERE user_id = %s"
            args = (em, pwd, user_id)
            res = cursor.execute(sql, args)
            if res:
                con.commit()
                print("MODEL:IN Update Function, USer tabel Updated")
                sql = "UPDATE Inspector SET name = %s, phone = %s, exp = %s, dob = %s, edu = %s, gender = %s, type = %s, image = %s WHERE user_id = %s;"
                args = (nm, ph, exp, dob, edu, gd, kd, fn, user_id)
                res = cursor.execute(sql, args)
                if res:
                    Flag = True
                    print("MODEL: Updated Inspector in database")
                    con.commit()
        except Exception as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
            return Flag


    def UpdateVic_Profile(self, user_id, nm, pwd, em, ph, add, dob, cnic, job, emg, gd):
        print("MODEL:IN Update Fucntion")
        con = None
        cursor = None
        Flag = False
        try:
            print("MODEL:IN Update Fucntion, TRY:")
            con = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cursor = con.cursor()
            print("connecction done")
            sql = "UPDATE User SET email = %s, password = %s WHERE user_id = %s"
            args = (em, pwd, user_id)
            res = cursor.execute(sql, args)
            if res:
                print("MODEL:IN Update Function, USer tabel Updated")
                sql = "UPDATE Victim SET name = %s, phone = %s, address = %s, dob = %s, gender = %s, cnic = %s, job = %s, emergency = %s WHERE user_id = %s;"
                args = (nm, ph, add, dob, gd, cnic, job, emg, user_id)
                res = cursor.execute(sql, args)
                if res:
                    Flag = True
                    print("MODEL: Updated Victim in database")
                    con.commit()
        except Exception as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
            return Flag

    def deleteProfile(self, user_id):
        con = None
        cursor = None
        flag = False
        try:
            con = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cursor = con.cursor()

            user_sql = 'DELETE FROM Inspector WHERE user_id=%s'
            user_args = (user_id,)
            res = cursor.execute(user_sql, user_args)
            if res:
                con.commit()
                sql = "DELETE FROM User WHERE user_id=%s"
                args = (user_id,)
                res = cursor.execute(sql, args)
                if res:
                    flag = True
                    con.commit()
            else:
                sql = "DELETE FROM Victim WHERE user_id=%s"
                args = (user_id,)
                res = cursor.execute(sql, args)
                if res:
                    con.commit()
                    sql = "DELETE FROM User WHERE user_id=%s"
                    args = (user_id,)
                    res = cursor.execute(sql, args)
                    if res:
                        flag = True
                        con.commit()
        except Exception as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
        return flag


    def allCriminalRecords(self):
        con = None
        cursor = None
        Criminals = []
        try:
            con = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cursor = con.cursor()

            user_sql = 'SELECT * FROM Criminal'
            res = cursor.execute(user_sql)
            if res:
                row = cursor.fetchall()
                if row:
                    for i in row:
                        p = [i[0], i[1], i[2], i[3], i[4], i[5], i[6]]
                        Criminals.append(p)
        except Exception as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
        return Criminals



    def myrecords(self, name):
        con = None
        cursor = None
        Criminals = []
        try:
            con = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cursor = con.cursor()

            user_sql = 'SELECT * FROM Criminal WHERE Ins_name = %s'
            res = cursor.execute(user_sql, name)
            if res:
                row = cursor.fetchall()
                if row:
                    for i in row:
                        p = [i[0], i[1], i[2], i[3], i[4], i[5], i[6]]
                        Criminals.append(p)
        except Exception as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
        return Criminals



    def addCriminalReocrd(self, nm, add, sex, kind, stt, ins_name):
        con = None
        cursor = None
        insert = False

        try:
            con = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                  database=self.database)
            cursor = con.cursor()

            user_sql = 'INSERT INTO Criminal(Cri_id,name,address,sex,type,status,Ins_name) VALUES(LAST_INSERT_ID(),%s,%s,%s,%s,%s,%s)'
            user_args = (nm, add, sex, kind, stt, ins_name)
            cursor.execute(user_sql, user_args)
            con.commit()
            insert = True
        except Exception as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
        return insert


    def firForm(self, type, date, time, des, wn, dmg, loc, user_id, status):
            con = None
            cursor = None
            insert = False
            try:
                con = pymysql.connect(host=self.host, user=self.user, password=self.password,database=self.database)
                cursor = con.cursor()
                user_sql = 'INSERT INTO FIR(Fir_id, type, date, time, descrip, wit_name, damage, loc, user_id, status) VALUES (LAST_INSERT_ID(), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                user_args = (type, date, time, des, wn, dmg, loc, user_id, status)
                cursor.execute(user_sql, user_args)
                con.commit()
                insert = True
            except Exception as e:
                print(str(e))
            finally:
                if cursor is not None:
                    cursor.close()
                if con is not None:
                    con.close()
            return insert

    def FirRecords(self):
        con = None
        cursor = None
        Firs = []
        try:
            con = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cursor = con.cursor()

            user_sql = 'SELECT * FROM FIR'
            res = cursor.execute(user_sql)
            if res:
                row = cursor.fetchall()
                if row:
                    for i in row:
                        p = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]]
                        Firs.append(p)
                        sql = "SELECT name FROM Victim WHERE user_id=%s"
                        args = (i[8],)
                        res = cursor.execute(sql,args)
                        if res:
                            name = cursor.fetchone()
        except Exception as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
        return Firs,name


    def Report(self,ins_id, ins_name, vic_id, fir_id, type, vic_name, status):
        con = None
        cursor = None
        insert = False
        try:
            con = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cursor = con.cursor()
            user_sql = 'INSERT INTO Report(report_id,ins_id,Ins_name,vic_id,fir_id,crimetype,vic_name) VALUES (LAST_INSERT_ID(), %s, %s, %s, %s, %s, %s)'
            user_args = (ins_id, ins_name, vic_id, fir_id, type, vic_name)
            res = cursor.execute(user_sql, user_args)
            if res:
                con.commit()
                sql = 'UPDATE FIR SET status = %s WHERE Fir_id = %s'
                args = (status, fir_id)
                res2 = cursor.execute(sql,args)
                if res2:
                    con.commit()
                    insert = True
        except Exception as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
        return insert


    def ins_cases(self,ins_id):
        con = None
        cursor = None
        cases = []
        try:
            con = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cursor = con.cursor()

            user_sql = 'SELECT * FROM Report WHERE ins_id = %s'
            args = (ins_id,)
            res = cursor.execute(user_sql,args)
            if res:
                row = cursor.fetchall()
                if row:
                    for i in row:
                        p = [i[0], i[1], i[2], i[3], i[4], i[5], i[6]]
                        cases.append(p)
        except Exception as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
        return cases




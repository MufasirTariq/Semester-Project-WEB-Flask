from flask import Flask, session, render_template, request
from flask_session import Session
from Model import Model

app = Flask(__name__)
app.secret_key = 'encrypted'
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)


@app.route('/')
def route_root():
    return render_template("Home.html")


@app.route('/InspectorForm', methods=['POST'])
def registerInspector():
    em = request.form['email']
    nm = request.form['name']
    pwd = request.form['password']
    ph = request.form['phone']
    dob = request.form['dob']
    edu = request.form['edu']
    exp = request.form['exp']
    kd = request.form['kind']
    gd = request.form['gender']
    type = 'Inspector'
    image = request.files['ins-pic']
    fn = image.filename
    image.save('/home/mufasir/Desktop/Web-Project/static/' + fn)
    path = "/static/" + fn

    con = Model('Localhost', 'root', 'Test@123', 'LCID')
    call = con.registerInspector(em, nm, pwd, ph, dob, edu, exp, kd, gd, type, fn)

    if call:
        return render_template("InspectorProfile.html", name=nm, password=pwd, phone=ph, email=em, dob=dob, edu=edu,
                               exp=exp, type=kd, image_path=path)
    else:
        return render_template("Home.html", msg="Some Error while registration")


@app.route('/VictimForm', methods=['POST'])
def registerVictim():
    nm = request.form['name']
    pwd = request.form['password']
    em = request.form['email']
    ph = request.form['phone']
    add = request.form['address']
    dob = request.form['dob']
    cnic = request.form['cnic']
    job = request.form['job']
    emg = request.form['emergency']
    gd = request.form['gender']
    type = 'Victim'
    img = request.files['vic-pic']
    fn = img.filename
    img.save('/home/mufasir/Desktop/Web-Project/static/' + fn)
    path = "/static/" + fn

    con = Model('Localhost', 'root', 'Test@123', 'LCID')
    call = con.registerVictim(em, pwd, nm, ph, add, dob, cnic, job, emg, gd, type, fn)

    if call:
        return render_template("VictimProfile.html", email=em, name=nm, password=pwd, phone=ph, address=add,
                               dob=dob, cnic=cnic, job=job, emg=emg, gender=gd, img=path)
    else:
        return render_template("Home.html", msg="Some Error while registration")


@app.route('/LoginForm', methods=["POST"])
def LoginForm():
    user_id = None
    em = request.form['email']
    pwd = request.form['password']

    con = Model('Localhost', 'root', 'Test@123', 'LCID')
    call = con.loginUser(em, pwd)

    if call:
        if call[1] == 'Ins':
            for i in call[0]:
                user_id = i[0]
                nm = i[1]
                ph = i[2]
                exp = i[3]
                dob = i[4]
                edu = i[5]
                gd = i[6]
                kd = i[7]
                img = i[8]
                path = "/static/" + img

            session['user_id'] = user_id
            session['name'] = nm
            session['image'] = img
            return render_template("InspectorProfile.html", user_id=user_id, name=nm, password=pwd, phone=ph, email=em, dob=dob, edu=edu, exp=exp, type=kd, gender=gd, image_path=path)
        elif call[1] == 'Vic':
            for i in call[0]:
                user_id = i[0]
                nm = i[1]
                ph = i[2]
                add = i[3]
                dob = i[4]
                gd = i[5]
                cnic = i[6]
                job = i[7]
                emg = i[8]
                img = i[9]
            session['user_id'] = user_id
            session['name'] = nm
            session['image'] = img
            path = "/static/" + img
            return render_template("VictimProfile.html", user_id=user_id, name=nm, phone=ph, email=em, password=pwd, address=add ,
                                   dob=dob, gender=gd, cnic=cnic, job= job, emg=emg, img=path)
    else:
        return render_template("Home.html", msg="Some Error while Signing")


@app.route("/InspectorUpdate", methods=['POST'])
def updateInsForm():
    if session.get("user_id") is not None:
        user_id = session['user_id']
        em = request.form['email']
        nm = request.form['name']
        pwd = request.form['password']
        ph = request.form['phone']
        dob = request.form['dob']
        edu = request.form['edu']
        exp = request.form['exp']
        kd = request.form['kind']
        gd = request.form['gender']
        image = request.files['ins-pic']
        fn = image.filename
        image.save('/home/mufasir/Desktop/Web-Project/static/' + fn)
        path = "/static/" + fn


        con = Model('Localhost', 'root', 'Test@123', 'LCID')
        call = con.UpdateIns_Profile(user_id, em, nm, pwd, ph, dob, edu, exp, kd, gd, fn)

        if call:
            return render_template("InspectorProfile.html", msg="Your profile is updated", user_id=user_id, name=nm,
                                   password=pwd, phone=ph, email=em, dob=dob, edu=edu,
                                   exp=exp, type=kd, gender=gd, image_path=path)
        else:
            return render_template("InspectorProfile.html", msg="Your profile not is updated", name=nm)


@app.route('/deleteprofile')
def deleteprofile():
    if session.get("user_id") is not None:
        user_id = session['user_id']

        con = Model('Localhost', 'root', 'Test@123', 'LCID')
        call = con.deleteProfile(user_id)

        if call:
            return render_template("Home.html", del_msg="Your Profile is successfully deleted")
        else:
            return render_template("Home.html", del_msg="Your Profile is not successfully deleted, Try again Later!")


@app.route("/updateVictim", methods=['POST'])
def updateVicForm():
    if session.get("user_id") is not None:
        user_id = session['user_id']
        nm = request.form['name']
        pwd = request.form['password']
        em = request.form['email']
        ph = request.form['phone']
        add = request.form['address']
        dob = request.form['dob']
        cnic = request.form['cnic']
        job = request.form['job']
        emg = request.form['emg']
        gd = request.form['gender']


        con = Model('Localhost', 'root', 'Test@123', 'LCID')
        call = con.UpdateVic_Profile(user_id, nm, pwd, em, ph, add, dob, cnic, job, emg, gd)
        if call:
            return render_template("VictimProfile.html", msg="Your profile is updated",user_id=user_id, name=nm, phone=ph,
                                   email=em, password=pwd, address=add, dob=dob, gender=gd, cnic=cnic, job= job, emg=emg)
        else:
            return render_template("VictimProfile.html", msg="Your profile not is updated", name=nm)


@app.route('/logout')
def logout():
    session.clear()
    return render_template("Home.html")

@app.route('/CriminalRecords')
def CriminalRecords():
    return render_template("CriminalRecord.html")

@app.route('/allCriminalRecords')
def allCriminalRecords():
    if session.get("user_id") and session.get("name") is not None:
        name = session['name']
        con = Model('Localhost', 'root', 'Test@123', 'LCID')
        call = con.allCriminalRecords()

        if call:
            Criminals = call
            return render_template("CriminalRecord.html", Criminals=Criminals, name=name)
        else:
            return render_template("CriminalRecord.html", msg="You don't have access!")

@app.route('/myrecords')
def myrecords():
    if session.get("user_id") and session.get("name") is not None:
        name = session['name']

        con = Model('Localhost', 'root', 'Test@123', 'LCID')
        call = con.myrecords(name)

        if call:
            Criminals = call
            return render_template("CriminalRecord.html", Criminals=Criminals, name=name)
        else:
            return render_template("CriminalRecord.html", msg="You don't have any Cases!")

@app.route("/addRecord", methods=['POST'])
def addCriminalRecord():
    if session.get("user_id") and session.get("name") is not None:
        user_id = session['user_id']
        ins_name = session['name']
        nm = request.form['name']
        add = request.form['address']
        sex = request.form['gender']
        kind = request.form['type']
        stt = request.form['status']


        con = Model('Localhost', 'root', 'Test@123', 'LCID')
        call = con.addCriminalReocrd(nm, add, sex, kind, stt, ins_name)

        if call:
            return render_template("CriminalRecord.html", msg="New Criminal Record added")
        else:
            return render_template("CriminalRecord.html", msg="New Criminal Record not added")

@app.route("/BackInspectorProfile")
def BackInspectorProfile():
    if session.get('name') is not None:
        name = session['name']
        img = session['image']
        path = "/static/"+img
        return render_template("InspectorProfile.html", name=name, image_path=path)

@app.route("/firform", methods=['POST'])
def firform():
    if session.get("user_id") and session.get('name') and session.get('image') is not None:
        user_id = session["user_id"]
        name = session["name"]
        img = session['image']
        path = "/static/" + img
        type = request.form['type']
        date = request.form['date']
        time = request.form['time']
        des = request.form['desc']
        wn = request.form['witname']
        dmg = request.form['damage']
        loc = request.form['loc']
        status = "Pending"
    con = Model('Localhost', 'root', 'Test@123', 'LCID')
    call = con.firForm(type, date, time, des, wn, dmg, loc, user_id, status)

    if call:
        return render_template("VictimProfile.html", msg="Your FIR has been received", name=name, img=img)
    else:
        return render_template("VictimProfile.html", msg="Your FIR has not been received, Try Again", name=name, img=path)

@app.route('/firRecords')
def firrecords():
    if session.get("user_id") and session.get("name") is not None:
        name = session['name']
        con = Model('Localhost', 'root', 'Test@123', 'LCID')
        call = con.FirRecords()

        if call:
            Firs = call[0]
            for i in call[1]:
                vic_name = i
            return render_template("FirRecord.html", FIR=Firs, name=name, vic_name=vic_name)
        else:
            return render_template("FirRecord.html", msg="Error")


@app.route("/report", methods=['POST'])
def report():
    if session.get("user_id") and session.get("name") and session.get("image") is not None:
        ins_id = session['user_id']
        ins_name = session['name']
        ins_img = session['image']
        path = "/static/"+ins_img

        data = request.form
        fir_id = data.get('id')
        type = data.get('type')
        vic_id = data.get('victimId')
        vic_name = data.get('victimName')
        status = "Accept"
        con = Model('Localhost', 'root', 'Test@123', 'LCID')
        call = con.Report(ins_id,ins_name,vic_id,fir_id,type,vic_name,status)

        if call:
            return render_template("InspectorProfile.html", msg="Case Accepted", name=ins_name, image_path=path)
        else:
            return render_template("InspectorProfile.html", msg="Error in accepted case!", name=ins_name, image_path=path)


@app.route('/ins_cases')
def ins_cases():
    if session.get("user_id") and session.get("name") and session.get("image") is not None:
        ins_id = session['user_id']
        ins_name = session['name']
        ins_img = session['image']
        path = "/static/" + ins_img


        con = Model('Localhost', 'root', 'Test@123', 'LCID')
        call = con.ins_cases(ins_id)

        if call:
            cases = call
            return render_template("InspectorCases.html", FIR=cases, name=ins_name)


if __name__ == "__main__":
    app.run()

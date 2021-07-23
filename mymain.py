from flask import Flask,render_template,request,redirect,url_for,session
from mylib import *
import os
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key="super secret key"
app.config['UPLOAD_FOLDER'] = './static/medicine_photos'

@app.route("/",methods=["GET","POST"])
def welcome():
    if request.method=="POST":
        med_name=request.form["T1"]

        sql="select * from medicine_with_medical where mname LIKE '%"+med_name+"%'"
        cur=make_connection()
        cur.execute(sql)
        n=cur.rowcount
        if(n>0):
            dd=cur.fetchall()
            vgt=[]
            for r in dd:
                mid=r[0]
                photo=check_medicine_photo(mid)
                record=[r[1],r[2],r[3],r[4],r[5],r[6],photo]
                vgt.append(record)

            return render_template("welcome.html",data=vgt)
        else:
            return render_template("welcome.html",msg="No medicine found")
    elif(request.method=="GET"):
        return render_template("welcome.html")
@app.route('/admin_reg',methods=['GET','POST'])
def admin_reg():
    if request.method=='GET':
        print("URL is using Get request ")
        return render_template('loginform.html')
    elif request.method=='POST':
        print("after submit the form")
        name=request.form["T1"]
        address=request.form["T2"]
        contact=request.form["T3"]
        email=request.form["T4"]
        password=request.form["T5"]
        confirm=request.form["T6"]
        usertype = "admin"
        if (password == confirm):
            cur = make_connection()
            s1 = "insert into admindata values('" + name + "','" + address + "','" + contact + "','" + email + "')"
            s2 = "insert into logindata values('" + email + "','" + password + "','" + usertype + "')"

            cur.execute(s1)
            m = cur.rowcount
            cur.execute(s2)
            n = cur.rowcount

            msg = ""
            if (m == 1 and n == 1):
                msg = "Data saved and login created"
            elif (m == 1):
                msg = "Data saved but login not created"
            elif (n == 1):
                msg = "Data not saved but login created"
            else:
                msg = "Data not saved and login not created"

            return render_template("loginform.html", kota=msg)
        else:
            return render_template("loginform.html", kota="Invalid Confirm Password")

    elif (request.method == "GET"):
        return render_template("loginform.html")


@app.route('/show_admins',methods=['GET','POST'])
def show_admin():
    conn=pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="zaid", autocommit=True)
    sql = "select * from admindata"
    print(sql)
    cur=conn.cursor()
    cur.execute(sql)
    n=cur.rowcount

    if n>0:
        dd=cur.fetchall()
        return render_template("showadmin.html",data=dd)
    else:
        return render_template("showadmin.html",msg="No data Found")

@app.route('/medical_reg',methods=['GET','POST'])
def medical_reg():
    if request.method=='GET':
        print("URL is using GET request ")
        return render_template('loginform2.html')
    elif request.method=='POST':
        print("after submit the form")

        name=request.form["t1"]
        lno=request.form["t2"]
        owner=request.form["t3"]
        address=request.form["t4"]
        contact=request.form["t5"]
        email=request.form["t6"]
        password=request.form["t7"]
        confirm=request.form["t8"]

        usertype = "medical"
        if (password == confirm):
            cur = make_connection()
            s1 = "insert into medicaldata values('" + name + "','" + lno + "','" + owner + "','" + address + "','" + contact + "','" + email + "')"
            s2 = "insert into logindata values('" + email + "','" + password + "','" + usertype + "')"

            cur.execute(s1)
            m = cur.rowcount
            cur.execute(s2)
            n = cur.rowcount

            msg = ""
            if (m == 1 and n == 1):
                msg = "Data saved and login created"
            elif (m == 1):
                msg = "Data saved but login not created"
            elif (n == 1):
                msg = "Data not saved but login created"
            else:
                msg = "Data not saved and login not created"

            return render_template("loginform2.html", kota=msg)
        else:
            return render_template("loginform2.html", kota="Invalid Confirm Password")

    elif (request.method == "GET"):
        return render_template("loginform2.html")

@app.route('/medicals')
def medicals():
    conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="zaid", autocommit=True)
    sql = "select * from medicaldata"
    print(sql)
    cur = conn.cursor()
    cur.execute(sql)
    n = cur.rowcount

    if n > 0:
        dd = cur.fetchall()
        return render_template("medicals.html", data=dd)
    else:
        return render_template("medicals.html", msg="No data Found")


@app.route('/show_medicals',methods=['GET','POST'])
def show_medicals():
    if "usertype" in session:
        ut=session["usertype"]
        if ut=="admin":

            sql = "select * from medicaldata"
            print(sql)
            cur = make_connection()
            cur.execute(sql)
            n = cur.rowcount

            if n > 0:
                dd = cur.fetchall()
                return render_template("showmedicals.html", data=dd)
            else:
                return render_template("showmedicals.html", msg="No data Found")

        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form["T1"]
        password=request.form["T2"]

        sql="select * from logindata where email='"+email+"' AND password='"+password+"'"
        cur=make_connection()
        cur.execute(sql)
        n=cur.rowcount
        if(n==1):
            data=cur.fetchone()
            ut=data[2]  #fetch usertype from record
            print(ut)
            session["email"]=email
            session["usertype"]=ut

            if(ut=="admin"):
                return redirect(url_for("adminhome"))
            elif (ut=="medical"):
                return redirect(url_for("medicalhome"))
        else:
            return render_template("LoginFormws.html",msg="Invalid email or password")
    elif request.method=="GET":
        return render_template("LoginFormws.html")

@app.route("/logout")
def logout():
    if "usertype" in session:
        session.pop("usertype",None)
        session.pop("email", None)
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

@app.route("/adminhome")
def adminhome():
    if "usertype" in session:
        ut=session["usertype"]
        if ut=="admin":
            return render_template("AdminHome.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/auth_error")
def auth_error():
    return render_template("AuthorizationError.html")

@app.route("/medicalhome")
def medicalhome():
    if "usertype" in session:
        ut=session["usertype"]
        if ut=="medical":
            return render_template("Medicalhome.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route('/edit_medicals',methods=['GET','POST'])
def edit_medicals():
    if request.method=='POST':
        id=request.form["H1"]
        conn = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="zaid", autocommit=True)
        cur = conn.cursor()
        sql="select * from medicaldata where email='"+ id+ "'"
        cur.execute(sql)
        n=cur.rowcount
        if(n==1):
            dd=cur.fetchone()
            return render_template("Editmedicals.html",data=dd)
        else:
            return render_template("Editmedicals.html",msg="No data found")
    elif(request.method=="GET"):
        return redirect(url_for("show_medicals"))

@app.route('/edit_medicals1',methods=["GET","POST"])
def edit_medicals1():
    if(request.method=='POST'):
        name=request.form["T1"]
        lno=request.form["T2"]
        owner=request.form["T3"]
        address=request.form["T4"]
        contact=request.form["T5"]
        email=request.form["T6"]
        conn = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="zaid", autocommit=True)
        cur = conn.cursor()
        sql = "update medicaldata SET name='"+name+"',lno='"+lno+"',owner='"+owner+"',address='"+address+"',contact='"+contact+"'  where email='"+ email+ "'"
        cur.execute(sql)
        n = cur.rowcount
        if(n==1):
            return render_template("Editmedicals1.html",msg="Data changes are saved successfully")
        else:
            return render_template("Editmedicals1.html", msg="Data changes are not saved")

    elif(request.method=="GET"):
        return redirect(url_for("show_medicals"))

@app.route('/delete_medicals',methods=['GET','POST'])
def delete_medicals():
    if(request.method=="POST"):
        email=request.form["H1"]
        conn = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="zaid", autocommit=True)
        cur = conn.cursor()
        sql = "select * from medicaldata where email='"+ email+ "'"
        cur.execute(sql)
        n = cur.rowcount
        if (n == 1):
            aa = cur.fetchone()
            return render_template('DeleteMedical.html', data=aa)
        else:
            return render_template('DeleteMedical.html', msg="No data found")
    else:
        return redirect(url_for('show_medicals'))

@app.route('/delete_medicals1',methods=['GET','POST'])
def delete_medicals1():
    if(request.method=='POST'):
        email=request.form["H1"]
        conn = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="zaid", autocommit=True)
        cur = conn.cursor()
        sql1 = "delete from medicaldata where email='"+ email+ "'"
        sql2 = "delete from logindata where email='" + email + "'"

        cur.execute(sql1)
        n = cur.rowcount
        cur.execute(sql2)
        m = cur.rowcount
        if (n == 1 and m==1):
            return render_template('Deletemedical1.html',msg="Data Deleted")
        else:
            return render_template('Deletemedical1.html',msg="Data not deleted")
    else:
        return redirect(url_for('show_medicals'))



@app.route("/change_password_admin",methods=["GET","POST"])
def change_password_admin():
    #check existence of the session
    if "usertype" in session:
        #fetch usertype
        ut=session["usertype"]
        if ut=="admin":
            if request.method=="POST":
                oldpass=request.form["T1"]
                newpass = request.form["T2"]
                confirm = request.form["T3"]
                e1=session["email"] #get email of logged-in user
                if (newpass!=confirm):
                    return render_template("ChangePasswordAdmin.html",msg="New and the Confirm Password are not same ")
                else:
                    cur=make_connection()
                    sql="update logindata set password='"+newpass+"' WHERE email='"+e1+"'"" AND password='"+oldpass+"'"
                    cur.execute(sql)
                    n=cur.rowcount
                    if n==1:
                        return render_template("ChangePasswordAdmin.html",msg="password changed successfully")
                    else:
                        return render_template("ChangePasswordAdmin.html",msg="Invalid old password ")
            elif(request.method=="GET"):
                return render_template("ChangePasswordAdmin.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/change_password_medical",methods=["GET","POST"])
def change_password_medical():
    #check existence of the session
    if "usertype" in session:
        #fetch usertype
        ut=session["usertype"]
        if ut=="medical":
            if request.method=="POST":
                oldpass=request.form["T1"]
                newpass = request.form["T2"]
                confirm = request.form["T3"]
                e1=session["email"] #get email of logged-in user
                if (newpass!=confirm):
                    return render_template("ChangePasswordmedical.html",msg="New and the Confirm Password are not same ")
                else:
                    cur=make_connection()
                    sql="update logindata set password='"+newpass+"' WHERE email='"+e1+"'"" AND password='"+oldpass+"'"
                    cur.execute(sql)
                    n=cur.rowcount
                    if n==1:
                        return render_template("ChangePasswordmedical.html",msg="password changed successfully")
                    else:
                        return render_template("ChangePasswordmedical.html",msg="Invalid old password ")
            elif(request.method=="GET"):
                return render_template("ChangePasswordmedical.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/admin_profile")
def admin_profile():
    # check existance of session
    if "usertype" in session:
        # fetch usertype
        ut = session["usertype"]
        if (ut == "admin"):
            e1=session["email"]
            cur=make_connection()
            sql="select * from admindata where email='"+e1+"'"
            cur.execute(sql)
            n=cur.rowcount
            if(n==1):
                data=cur.fetchone()
                return render_template("AdminProfile.html",kota=data)
            else:
                return render_template("AdminProfile.html",msg="No data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/admin_profile1")
def admin_profile1():
    # check existance of session
    if "usertype" in session:
        # fetch usertype
        ut = session["usertype"]
        if (ut == "admin"):
            e1=session["email"]
            cur=make_connection()
            sql="select * from admindata where email='"+e1+"'"
            cur.execute(sql)
            n=cur.rowcount
            if(n==1):
                data=cur.fetchone()
                return render_template("AdminProfile1.html",kota=data)
            else:
                return render_template("AdminProfile1.html",msg="No data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/admin_profile2",methods=["GET","POST"])
def admin_profile2():
    # check existance of session
    if "usertype" in session:
        # fetch usertype
        ut = session["usertype"]
        if (ut == "admin"):
            if(request.method=="POST"):
                name=request.form["T1"]
                address=request.form["T2"]
                contact=request.form["T3"]
                email=session['email']
                cur=make_connection()

                sql="update admindata set name='"+name+"', address='"+address+"', contact='"+contact+"' WHERE email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("AdminProfile2.html",msg="Data changes saved successfully")
                else:
                    return render_template("AdminProfile2.html", msg="Cannot save changes")
            elif(request.method=="GET"):
                return redirect(url_for("admin_profile"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/medical_profile")
def medical_profile():
    # check existance of session
    if "usertype" in session:
        # fetch usertype
        ut = session["usertype"]
        if (ut == "medical"):
            e1=session["email"]
            cur=make_connection()
            sql="select * from medicaldata where email='"+e1+"'"
            cur.execute(sql)
            n=cur.rowcount
            if(n==1):
                data=cur.fetchone()
                return render_template("MedicalProfile.html",kota=data)
            else:
                return render_template("MedicalProfile.html",msg="No data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/medical_profile1")
def medical_profile1():
    # check existance of session
    if "usertype" in session:
        # fetch usertype
        ut = session["usertype"]
        if (ut == "medical"):
            e1=session["email"]
            cur=make_connection()
            sql="select * from medicaldata where email='"+e1+"'"
            cur.execute(sql)
            n=cur.rowcount
            if(n==1):
                data=cur.fetchone()
                return render_template("MedicalProfile1.html",kota=data)
            else:
                return render_template("MedicalProfile1.html",msg="No data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/medical_profile2",methods=["GET","POST"])
def medical_profile2():
    # check existance of session
    if "usertype" in session:
        # fetch usertype
        ut = session["usertype"]
        if (ut == "medical"):
            if(request.method=="POST"):
                name=request.form["T1"]
                lno = request.form["T2"]
                owner = request.form["T3"]
                address=request.form["T4"]
                contact=request.form["T5"]
                email=session['email']
                cur=make_connection()

                sql="update medicaldata set name='"+name+"',lno='"+lno+"',owner='"+owner+"', address='"+address+"', contact='"+contact+"' WHERE email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("MedicalProfile2.html",msg="Data changes saved successfully")
                else:
                    return render_template("MedicalProfile2.html", msg="Cannot save changes")
            elif(request.method=="GET"):
                return redirect(url_for("medical_profile"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/add_medicine",methods=["GET","POST"])
def add_medicine():
    # check existance of session
    if "usertype" in session:
        # fetch usertype
        ut = session["usertype"]
        if (ut == "medical"):
            if(request.method=="POST"):
                name = request.form['T1']
                company = request.form['T2']
                lno = request.form['T3']
                med_type = request.form['T4']
                unit_price = request.form['T5']
                details = request.form['T6']
                medical_email = session["email"]

                cur=make_connection()
                sql="insert into medicinedata(name,company,lno,med_type,unit_price,details,medical_email) values('"+name+"','"+company+"','"+lno+"','"+med_type+"',"+unit_price+",'"+details+"','"+medical_email+"')"
                cur.execute(sql)
                n=cur.rowcount
                msg=""
                if(n==1):
                    msg="Medicine successfully added."
                else:
                    msg="Medicine is not added."
                return render_template("AddMedicine.html",kota=msg)
            else:
                return render_template("AddMedicine.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))
@app.route("/show_medicines")
def show_medicines():
    #check existance of session
    if "usertype" in session:
        #fetch usertype
        ut=session["usertype"]
        if (ut=="medical"):
            cur=make_connection()
            e1=session["email"]
            sql = "select * from medicinedata where medical_email='"+e1+"'"
            cur.execute(sql)
            n = cur.rowcount
            if (n > 0):
                dd = cur.fetchall()
                vgt=[]
                for d in dd:
                    mid=d[0]
                    photo=check_medicine_photo(mid)
                    record=[d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],photo]
                    vgt.append(record)

                return render_template('/ShowMedicines.html', data=vgt)
            else:
                return render_template('/ShowMedicines.html', msg="No data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/edit_medicine",methods=["GET","POST"])
def edit_medicine():
    #check existance of session
    if "usertype" in session:
        #fetch usertype
        ut=session["usertype"]
        if (ut=="medical"):
            if(request.method=="POST"):

                cur=make_connection()
                id=request.form["H1"]
                sql = "select * from medicinedata where med_id=" + id
                cur.execute(sql)
                n = cur.rowcount
                if (n == 1):
                    dd = cur.fetchone()
                    return render_template("Editmedicine.html", data=dd)
                else:
                    return render_template("Editmedicine.html", msg="No data found")
            elif (request.method == "GET"):
                return redirect(url_for("show_medicines"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/edit_medicine1",methods=["GET","POST"])
def edit_medicine1():
    #check existance of session
    if "usertype" in session:
        #fetch usertype
        ut=session["usertype"]
        if (ut=="medical"):
            if(request.method=="POST"):

                cur=make_connection()
                med_id= request.form["T1"]
                name = request.form["T2"]
                company = request.form["T3"]
                lno = request.form["T4"]
                med_type = request.form["T5"]
                unit_price = request.form["T6"]
                details = request.form["T7"]

                sql = "update medicinedata SET name='" + name + "',company='" +company+ "',lno='" + lno + "',med_type='" + med_type + "',unit_price=" + unit_price +unit_price + ",details='"+details+"'  where med_id=" + med_id
                cur.execute(sql)
                n = cur.rowcount
                if (n == 1):
                    return render_template("Editmedicine1.html", msg="Data changes are saved successfully")
                else:
                    return render_template("Editmedicine1.html", msg="Data changes are not saved")

            elif (request.method == "GET"):
                return redirect(url_for("show_medicines"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/delete_medicine",methods=["GET","POST"])
def delete_medicine():
    #check existance of session
    if "usertype" in session:
        #fetch usertype
        ut=session["usertype"]
        if (ut=="medical"):
            if(request.method=="POST"):
                cur=make_connection()
                med_id=request.form["H1"]
                sql = "select * from medicinedata where med_id=" + med_id
                cur.execute(sql)
                n = cur.rowcount
                if (n == 1):
                    aa = cur.fetchone()
                    return render_template('DeleteMedicine.html', data=aa)
                else:
                    return render_template('DeleteMedicine.html', msg="No data found")
            else:
                return redirect(url_for('show_medicines'))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/delete_medicine1",methods=["GET","POST"])
def delete_medicine1():
    #check existance of session
    if "usertype" in session:
        #fetch usertype
        ut=session["usertype"]
        if (ut=="medical"):
            if(request.method=="POST"):
                cur=make_connection()
                med_id=request.form["H1"]
                sql = "delete from medicinedata where med_id=" + med_id
                cur.execute(sql)
                n = cur.rowcount
                if (n == 1):
                    return render_template('DeleteMedicine1.html', msg="Data Deleted")
                else:
                    return render_template('DeleteMedicine1.html', msg="Data not deleted")
            else:
                return redirect(url_for('show_medicines'))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/upload_medicine_photo",methods=["GET","POST"])
def upload_medicine_photo():
    # Check the existance of session
    if ("usertype" in session):
        ut = session["usertype"]
        if (ut == "medical"):

            if request.method == 'POST':
                mid=request.form["H1"]
                file = request.files['F1']
                if file:
                    path = os.path.basename(file.filename)

                    file_ext = os.path.splitext(path)[1][1:]
                    filename = str(int(time.time())) + '.' + file_ext
                    filename = secure_filename(filename)

                    cur=make_connection()
                    sql = "insert into medicine_photo values(" + mid + ",'" + filename + "')"

                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if n == 1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            return render_template('MedicinePhoto.html', result="success")
                        else:
                            return render_template('MedicinePhoto.html', result="failure")
                    except:
                        return render_template('MedicinePhoto.html', result="duplicate")
            else:
                return redirect(url_for("show_medicines"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))



if __name__ == "__main__":
    app.run(debug=True)


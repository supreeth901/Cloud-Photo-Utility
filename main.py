import pymysql
from flask import Flask, render_template, request, session
import hashlib
import os
import datetime
import re
from werkzeug.utils import secure_filename
from flask import Flask, redirect, url_for, request,render_template
import timeit
import hashlib
import random
import csv
import collections
#import pygal
#import boto3
from flask import Flask ,redirect, url_for, request,render_template
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.secret_key=os.urandom(24)

my_con = pymysql.connect(host=hostname, user=usernameCred, passwd=cred, db=database)
cur = my_con.cursor();
print("Database Connected")
Uploadpath = "C:/Users/Supreeth/PycharmProjects/secure/static/stores"
Downloadpath = "/home/ubuntu/Download"

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/')
def hello_world():
    return render_template("index.html")


def getsession():
    if 'username' in session:
        return session['username']
    return 'not logged in!'


@app.route('/signup', methods=['POST'])
def signupuser():
    m = hashlib.sha256()
    userid = request.form['userid'].strip()
    username = request.form['name']
    passw = request.form['passwordsignup']
    group = request.form.getlist('group')
    pattern = re.compile("^[A-z a-z]+[0-9]*$")  # Input validation against regular expression
    print(pattern.match(userid))
    if (pattern.match(userid) and pattern.match(username) and len(passw) > 8 and len(passw) < 12):
        query1 = "select userid from userss where userid ='" + userid + "';"
        cur.execute(query1)
        rowcount = cur.rowcount
        print(rowcount)
        if rowcount:
            return render_template("loginerror.html", msg="User already found try to login")
        else:
            group1, group2, group3, group4 = [''] * 4
            m.update(passw.encode('utf-8'))
            final = m.hexdigest()
            print(m.hexdigest())
            query = "insert into userss values('" + userid + "','" + username + "','" + final + "','" + "');"
            for i in group:
                if i == '1':
                    group1 = 'R'
                if i == '2':
                    group2 = 'R'
                if i == '3':
                    print("grp" + group1 + "  " + group2)
                    group3 = 'R'
                if i == '4':
                    group4 = 'R'
            query1 = "insert into admin values('" + userid + "','" + group1 + "','" + group2 + "','" + group3 + "','" + group4 + "');"
            cur.execute(query)
            cur.execute(query1)
            my_con.commit()
            return render_template("index.html")
    else:
        return render_template("loginerror.html",
                               msg="Invalid input: Shouldn't include any special characters. It should be only alphanumeric EX: user12 valid & Password should be Greater than 8 and less than 12")


@app.route('/login', methods=['POST'])
def loginuser():
    m = hashlib.sha256()
    usernamelog = request.form['usernameLogin']
    session['username'] = usernamelog
    passslog = request.form['passwordLogin']
    pattern = re.compile("^[A-z a-z]+[0-9]*$")  # Input validation against regular expression
    session['username'] = usernamelog
    uuu = usernamelog
    if pattern.match(usernamelog):
        session['user'] = usernamelog
        m.update(passslog.encode('utf-8'))
        final = m.hexdigest()
        query = "select password,admin from userss where userid='" + usernamelog + "';"
        print(query)
        cur.execute(query)
        rr = cur.fetchall()
        if rr:
            val = rr[0]
            if final == val[0]:
                if val[1] == 'Y':
                    queryAdmin = "select * from admin;"
                    cur.execute(queryAdmin)
                    res = cur.fetchall()
                    return render_template("adminApproval.html", res=res)
                else:
                    group1, group2, group3, group4 = ['N'] * 4
                    grpAccess = "select * from grp where userid='" + usernamelog + "';"
                    print(grpAccess)
                    cur.execute(grpAccess)
                    result = cur.fetchall()
                    if result:
                        accessRes = result[0]
                        if accessRes[1] == 'Y':
                            group1 = 'group1'
                        if accessRes[2] == 'Y':
                            group2 = 'group2'
                        if accessRes[3] == 'Y':
                            group3 = 'group3'
                        if accessRes[4] == 'Y':
                            group4 = 'group4'
                        print(group1 + " " + group2 + " " + group2 + " " + group4)
                        view_sql = "select picid,picname,description,createdby,image_path from picss where groupid in('" + group1 + "','" + group2 + "','" + group3 + "','" + group4 + "');"
                        cur.execute(view_sql)
                        result = cur.fetchall()
                        return render_template("View.html", your_list=result)
                    else:
                        return render_template("loginerror.html",
                                               msg="Admin has not approved your signup request yet Please try after some time")
            elif cur.rowcount == 0:
                return render_template("loginerror.html", msg="UserId is not yet signed up.")

            else:
                return render_template("loginerror.html",
                                       msg="User name or Password entered is wrong Please try to login again")
        else:
            return render_template("loginerror.html",
                                   msg="User Not registered yet")
    else:
        return render_template("loginerror.html",
                               msg="Invalid input: Shouldn't include any special characters. It should be only alphanumeric Please Login again for security reasons")


@app.route('/approve', methods=['POST'])
def approve():
    userid = request.form['userid']
    pattern = re.compile("^[A-z a-z]+[0-9]*$")
    if pattern.match(userid):
        group1, group2, group3, group4 = [''] * 4
        query = "select * from admin where userid ='" + userid + "';"
        print(query)
        cur.execute(query)
        res = cur.fetchall()[0]
        if res[1] == 'R':
            group1 = 'Y'
        if res[2] == 'R':
            group2 = 'Y'
        if res[3] == 'R':
            group3 = 'Y'
        if res[4] == 'R':
            group4 = 'Y'
        query1 = "delete from admin where userid ='" + userid + "';"
        cur.execute(query1)
        my_con.commit()
        query2 = "insert into grp values('" + userid + "','" + group1 + "','" + group2 + "','" + group3 + "','" + group4 + "');"
        cur.execute(query2)
        my_con.commit()
        queryAdmin = "select * from admin;"
        cur.execute(queryAdmin)
        res = cur.fetchall()
        return render_template("adminApproval.html", res=res)
    else:
        return render_template("loginerror.html",
                               msg="Invalid input: Shouldn't include any special characters. It should be only alphanumeric Please LOGIN again for security resons")


@app.route('/upload', methods=['POST'])
def upload():
    title = request.form['title']
    image_path = request.form['title'] + ".jpg"
    description = request.form['descp']
    grpupload = int(request.form['grpupload'])
    file = request.files['file']
    pattern = re.compile("^[A-z a-z]+[0-9]*$")  # Input validation against regular expression
    if (pattern.match(title) and pattern.match(description)):
        print(file)
        print(getsession())
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(Uploadpath, filename))
        print(os.path.join(Uploadpath, filename))
        times = "201801202"
        print(times)
        query1 = "select * from grp where userid='" + getsession() + "';"
        print(query1)
        cur.execute(query1)
        ress = cur.fetchall()[0]
        print(ress)
        if ress[grpupload] == 'Y':
            groupid = "group" + str(grpupload)
            query2 = "insert into picss(picname, description, createdate, lastaccessedtime, image_path, userid, groupid, createdby)values('" + title + "','" + description + "','" + times + "','" + times + "','" + os.path.join(
                Uploadpath, filename) + "','" + getsession() + "','" + groupid + "','" + " ');"
            cur.execute(query2)
            my_con.commit()
            group1, group2, group3, group4 = ['N'] * 4
            grpAccess = "select * from grp where userid='" + getsession() + "';"
            cur.execute(grpAccess)
            accessRes = cur.fetchall()[0]
            if accessRes[1] == 'Y':
                group1 = 'group1'
            if accessRes[2] == 'Y':
                group2 = 'group2'
            if accessRes[3] == 'Y':
                group3 = 'group3'
            if accessRes[4] == 'Y':
                group4 = 'group4'
            print(group1 + " " + group2 + " " + group2 + " " + group4)
            view_sql = "select picid,picname,description,createdby,image_path from picss where groupid in('" + group1 + "','" + group2 + "','" + group3 + "','" + group4 + "');"
            cur.execute(view_sql)
            result = cur.fetchall()
            return render_template("View.html", your_list=result)
        else:
            return render_template("loginerror.html",
                                   msg="Your are not in this group. Please LOGIN for security resons")
    else:
        return render_template("loginerror.html",
                               msg="Invalid input: Shouldn't include any special characters. It should be only alphanumeric Please LOGIN again for security resons")


@app.route('/adminview', methods=['POST'])
def adminview():
    view_sql = "select picid,picname,description,createdby,image_path from picss;"
    cur.execute(view_sql)
    result = cur.fetchall()
    return render_template("View.html", your_list=result)


@app.route('/delete', methods=['POST'])
def delete():
    picid = request.form['picid']
    query1 = "select admin from userss where userid ='" + getsession() + "';"
    print(query1)
    query2 = "select userid from picss where picid =" + picid + ";"
    cur.execute(query1)
    res1 = cur.fetchall()[0]
    print(res1)
    cur.execute(query2)
    res2 = cur.fetchall()[0]
    print(res2[0])
    if (res1[0] == 'Y' or res2[0] == getsession()):
        query3 = "delete from picss where picid =" + picid + ";"
        cur.execute(query3)
        my_con.commit()
        print("hellow")
        group1, group2, group3, group4 = ['N'] * 4
        if res2[0] == getsession():
            grpAccess = "select * from grp where userid='" + getsession() + "';"
            print(grpAccess)
            cur.execute(grpAccess)
            accessRes = cur.fetchall()[0]
            if accessRes[1] == 'Y':
                group1 = 'group1'
            if accessRes[2] == 'Y':
                group2 = 'group2'
            if accessRes[3] == 'Y':
                group3 = 'group3'
            if accessRes[4] == 'Y':
                group4 = 'group4'
            print(group1 + " " + group2 + " " + group2 + " " + group4)
            view_sql = "select picid,picname,description,createdby,image_path from picss where groupid in('" + group1 + "','" + group2 + "','" + group3 + "','" + group4 + "');"
            cur.execute(view_sql)
            result = cur.fetchall()
            return render_template("View.html", your_list=result)
        else:
            view_sql = "select picid,picname,description,createdby,image_path from picss;"
            cur.execute(view_sql)
            result = cur.fetchall()
            return render_template("View.html", your_list=result)
    else:
        return render_template("loginerror.html",
                               msg="Your are not in this group. Please LOGIN again for security resons")


@app.route('/logout', methods=['POST'])
def logout():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
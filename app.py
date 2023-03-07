import datetime
import re
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

grades = {'A*': 10, 'A': 10, 'B+': 9, 'B': 8, 'C+': 7, 'C': 6, 'D+': 5, 'D': 4, 'E': 0, 'F': 0}
mth = {1 : ["MTH111", "MTH112"], 2 : ["MTH113", "MTH114"]}
phys = ["PHY112", "PHY113", "PHY114", "PHY115"]
courses = {1 : ["PHY111", "TA111", "CHM112", "CHM113", "ELC11X"], 2 : ["CHM111", "ESC111", "ESC112",  "LIF111"]}
course_credit = {"PHY111" : 3, "TA111" : 9, "CHM112" : 4, "CHM113" : 4, "ELC11X" : 9, "CHM111" : 3, "ESC111" : 7, "ESC112" : 7, "LIF111" : 6, "MTH111" : 6, "MTH112" : 6, "MTH113" : 6, "MTH114" : 6, "PHY112" : 11, "PHY113" : 11, "PHY114" : 11, "PHY115" : 11}
global counts
counts = 0
s_p_i = {}

@app.route('/', methods=["GET","POST"])
def index():

    if request.method == "POST":
        global branch
        branch = request.form.get("branch")
        global semester
        semester = int(request.form.get("semester"))
        global group
        group = int(request.form.get("group"))
        global ind
        global counts
        counts = counts + 1

        if (branch in ["AE", "CE", "CHE", "CHM"] and semester == 1) or (branch in ["BSBE", "ECO", "ES", "ME", "PHY"] and semester == 2):
            ind = 0

        elif (branch in ["EE", "ME", "PHY"] and semester == 1) or (branch in ["CHE", "CHM", "CSE", "MSE"] and semester == 2):
            ind = 1

        elif (branch in ["CSE", "MSE"] and semester == 1) or (branch in ["EE", "MTH", "SDS"] and semester == 2):
            ind = 2

        elif (branch in ["BSBE", "ECO", "MTH", "ES", "SDS"] and semester == 1) or (branch in ["AE", "CE"] and semester == 2):
            ind = 3

        return redirect("/spi")
    
    else:
        ind = 0
        return render_template("index.html")


@app.route('/spi',methods=["GET", "POST"])
def spi():
    if request.method == "POST":
        credit_scored = 0
        global total_credit
        total_credit = 11

        credit_scored += 11 * int(request.form.get(phys[ind]))

        for course in mth[semester]:

            course_get = request.form.get(course)
            if course_get != None:

                total_credit += course_credit[course]
                credit_scored += int(course_get) * course_credit[course]
        for course in courses[group]:
            course_get = request.form.get(course)
            if course_get != None:
                total_credit += course_credit[course]
                credit_scored += int(course_get) * course_credit[course]

        s_p_i[semester] = {total_credit : credit_scored / total_credit}
        return redirect("/submit")
    
    else:
        return render_template("esc.html", phy =phys[ind], semester=semester, group=group, branch=branch, grades=grades, mth=mth, courses=courses)


@app.route('/submit', methods=["GET", "POST"])
def submit():

    total_credit1 = 0
    num = 0

    for sem in s_p_i:
            for creds in s_p_i[sem]:
                total_credit1 += creds
                num += creds * s_p_i[sem][creds]

    cpi = num/ total_credit1
    return render_template("submit.html", spi=s_p_i[semester][total_credit], cpi=cpi,sem=semester % 2 + 1, branch=branch, group=group, counts=counts)


if __name__ == '__main__':
	app.run(debug=True)
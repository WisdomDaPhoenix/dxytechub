from flask import Flask, render_template,flash, request, url_for, send_from_directory, jsonify
from flask_mail import Mail, Message
from MongoOnline import addToMongoDB
import json, os
from dotenv import load_dotenv
import requests

import time
from getlength import lengthData
import pandas as pd
coursesinfo = pd.read_csv("static/coursesinfo.csv",encoding='utf-8',encoding_errors='ignore')

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS")
app.config['MAIL_USE_SSL'] = os.getenv("MAIL_USE_SSL")
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER']=('DXYTECHUB-Trainings','info@dmarketforces.com')


mail = Mail(app)

specials = {'uiux':'UI/UX','nocode':'No-code'}


# clientsdir = 'clientsdata'
# file_path = os.path.join(clientsdir, 'clients.json')  # Full file path

# Ensure the directory exists
# os.makedirs(clientsdir, exist_ok=True)
# if os.path.exists(file_path):
#     with open(file_path, 'r') as file:
#         try:
#             content = json.load(file)
#             open("clientsdata/clients.json").close()
#             if "data" not in content:
#                 content["data"] = []
#         except json.JSONDecodeError as error:
#             content = {"data": []}  # Handle case where JSON is invalid or corrupted, if not, sets content to an array
# else:
#     content = {"data": []} # ensures content is always set to the data array even if file does not exist or if its corrupt

log_file_path = "/tmp/ip_log.txt"
@app.route("/home")
@app.route("/")
def home():
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if client_ip:
        client_ip = client_ip.split(",")[0].strip()  # Get first IP if multiple exist
    with open(log_file_path,"a") as log_file:
        log_file.write(f"{client_ip}\n")
    return render_template("index.html")


@app.route("/clients", methods=["GET"])
def clients():
    url = "https://allclientsfinal.vercel.app/newclient"
    dxyclients = getDXYData(url)
    return jsonify(dxyclients)


@app.route("/course/<string:coursename>",methods=["GET"])
def course(coursename):
    # if coursename.split('-')[0] in specials:
    for key in specials:
        if key in coursename:
            coursename = coursename.replace(key, specials[key]).strip().upper()
    coursename = coursename.replace('-',' ').strip().upper()

    for i in range(len(coursesinfo)):
        careercourse = coursesinfo["Course"][i].strip().upper()
        careertext = coursesinfo["Career Text"][i]
        print(f"{coursename} : {careercourse}")
        if coursename == careercourse:
            careers = coursesinfo["Careers"][i].split('.')
            curriculum = coursesinfo["Curriculum"][i].split('.')
            outcomes = coursesinfo["Learning Outcomes"][i].split('.')
            return render_template("coursetemp.html",
                                   coursename=coursename,
                                   careertext=careertext,
                                   careers=careers,
                                   curriculum=curriculum,
                                   outcomes=outcomes)


            #     return render_template("coursetemp.html",
            #                            coursename=coursename,
            #                            careertext=careertext,
            #                            careers=careers,
            #                            curriculum=curriculum,
            #                            outcomes=outcomes)
            #
            #
            #
            # print(f"{coursename} : {careercourse}")
            # print(f"{len(coursename)} : {len(careercourse)}")
            # if coursename == careercourse:
            #     careers = coursesinfo["Careers"][i].split('.')
            #     curriculum = coursesinfo["Curriculum"][i].split('.')
            #     outcomes = coursesinfo["Learning Outcomes"][i].split('.')


    return f"No Data"


@app.route("/submit", methods=["POST"])
def submitData():
    datasize = lengthData()
    url = "https://allclientsfinal.vercel.app/newclient"
    headers = {"Content-Type": "application/json"}


    name = request.form['name']
    course = request.form['course']
    phone = request.form['phone']
    email = request.form['email']

    ClientName = name
    ClientCourse = course
    ClientPhone = phone
    ClientEmail = email


    body = {"Client ID": datasize+1,
            "Client Name": ClientName,
            "Client Course": ClientCourse,
            "Client Phone": ClientPhone,
            "Client Email": ClientEmail
     }


    try:
        requests.post(url, headers=headers, json=body)

        subject_student = f"Acknowledgement of Course Registration"
        subject_dxy = f"Notification of Student Registration"

        studentmailbody = f""" Thank you {ClientName} for registering your interest in our training course.\n
        Course Name: {ClientCourse} \n\n
        Our courses run 3 times a week \n\n
        Opening Time/Daily Schedule : 10.00am \n\n\n
        Here's a detailed brochure on our fees and course details: \n 
        https://dxytechub.vercel.app/courses. You will be contacted shortly for any further information."""

        dxymailbody = f"""A student registration has been confirmed. See details:  \n\n
                                         Course Name: {ClientCourse} \n\n
                                         Student Name: {ClientName} \n\n
                                         Phone number: {ClientPhone} \n\n
                                         """
        dxymsg = Message(subject_dxy, recipients=["intelligent.unit@yahoo.com","iconsoftwarepoint@tutamail.com"])
        studentmsg = Message(subject_student, recipients=[ClientEmail])
        dxymsg.body = dxymailbody
        studentmsg.body = studentmailbody
        try:
            mail.send(studentmsg)
            successmsg = f"Thanks for your interest! We have sent an acknowledgement email to {ClientEmail}"
            time.sleep(2)
            mail.send(dxymsg)
            studentinfo = {"Client Name": ClientName,
                           "Client Course": ClientCourse,
                           "Client Phone": ClientPhone,
                           "Client Email": ClientEmail}
            resultIDMsg = addToMongoDB(studentinfo)
        except Exception as e:
            return f"Server failure: {e}"
        else:
            flash(f"{resultIDMsg}\n\n")
            flash(f"We are glad for your interest in {ClientCourse}\n\n")
            return render_template("success.html", successmsg=successmsg)  # Render the success page
        finally:
            print(f"Completed processing for {ClientName} and {ClientCourse}")
    except:
        return f"Could not post to API"

    # USING GET TO SEND THE CLIENT DATA TO NEWCLIENT ENDPOINT
        # try:
    #     res = requests.get(f"http://127.0.0.1:5400/newclient?ClientName={ClientName}&ClientCourse={ClientCourse}&ClientPhone={ClientPhone}&ClientEmail={ClientEmail}")
    #     if res.status_code==200:
    #         return f"Sucessfully sent {ClientName}, {ClientCourse},{ClientPhone},{ClientEmail}"
    # except Exception as e:
    #     return f"Assigned successfully only:  {e}"



@app.route("/courses",methods=["GET"])
def courses():
    try:
        return send_from_directory('static','TRAINING BROCHURE.pdf')
    except FileNotFoundError as f:
        return f"Courses not available: {f}"


def getDXYData(apiurl):
    response = requests.get(apiurl)
    data = response.json()
    return data







if __name__ == "__main__":
     app.run(port=5600,debug=True,host="0.0.0.0")


                  

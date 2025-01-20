from flask import Flask, render_template,flash, request, url_for, send_from_directory, jsonify
from flask_mail import Mail, Message
import json, os
import requests
from pprint import pprint
import time
from getlength import lengthData



app = Flask(__name__)

app.config['MAIL_SERVER'] = "mail.dmarketforces.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "wisdom.enefiok@dmarketforces.com"
app.config['MAIL_PASSWORD'] = "12Hallmark1!"
app.config['MAIL_DEFAULT_SENDER']=('DXYDEV-Trainings','wisdom.enefiok@dmarketforces.com')
app.config['SECRET_KEY'] = "Datron24"

mail = Mail(app)

clientsdir = 'clientsdata'
file_path = os.path.join(clientsdir, 'clients.json')  # Full file path

# Ensure the directory exists
os.makedirs(clientsdir, exist_ok=True)
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        try:
            content = json.load(file)
            open("clientsdata/clients.json").close()
            if "data" not in content:
                content["data"] = []
        except json.JSONDecodeError as error:
            content = {"data": []}  # Handle case where JSON is invalid or corrupted, if not, sets content to an array
else:
    content = {"data": []} # ensures content is always set to the data array even if file does not exist or if its corrupt


@app.route("/home")
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/clients", methods=["GET"])
def clients():
    url = "http://127.0.0.1:5400/newclient"
    dxyclients = getDXYData(url)
    return jsonify(dxyclients)



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
        http://127.0.0.1:5000/courses. You will be contacted shortly for any further information."""

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
            time.sleep(4)
            mail.send(dxymsg)
        except Exception as e:
            return f"Server failure: {e}"
        else:
            return render_template("success.html", successmsg=successmsg)
        finally:
            flash(f"We are glad for your interest in {ClientCourse}")
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
     app.run(debug=True,host="0.0.0.0")


                  

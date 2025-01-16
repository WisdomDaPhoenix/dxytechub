from flask import Flask, render_template, request, url_for, send_from_directory
from flask_mail import Mail, Message
import json, os
from pprint import pprint



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


pprint(content)

@app.route("/home")
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submitData():
    name = request.form['name']
    course = request.form['course']
    phone = request.form['phone']
    email = request.form['email']

    d = {"Name": name,
         "Course": course,
         "Phone": phone,
         "Email": email}

    with open('clientsdata/clients.json','w') as file:
        content["data"].append(d)
        json.dump(content, file)
        print(content)

    subject = f"Acknowledgement of Course Registration"
    
    mailbody = f"""Thank you {name} for registering your interest in our training course \n\n 
                   Course Name: {course} \n\n
                   Our courses run 3 times a week \n\n
                   Time: 10.00am \n\n
                   You will be contacted shortly for any further information"""
    successmsg = f"Thanks for your interest! We have sent an acknowledgement email to {email}"
    try:
        msg = Message(subject, recipients=[email])
        msg.body = mailbody
        mail.send(msg)
        return render_template("success.html", successmsg=successmsg)
    except Exception as e:
        return f"Send failure: {e}"

@app.route("/courses",methods=["GET"])
def courses():
    try:
        return send_from_directory('static','TRAINING BROCHURE.pdf')
    except FileNotFoundError as f:
        return f"Courses not available: {f}"


if __name__ == "__main__":
     app.run(debug=True,host="0.0.0.0")


                  

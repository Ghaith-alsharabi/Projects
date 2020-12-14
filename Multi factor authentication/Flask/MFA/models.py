from MFA import db, login_manager, app, account_sid, auth_token
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from otpauth import OtpAuth
import qrcode, random
import base64
import cv2
import numpy as np
from PIL import Image
import io
import face_recognition
from twilio.rest import Client
from datetime import datetime
import geocoder
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage, encoders
from email.mime.base import MIMEBase
import smtplib, ssl
import requests
import os
import string
from flask_socketio import emit




end_point = "https://maps.googleapis.com/maps/api/staticmap?"
port = 587
smtp_server = "smtp.gmail.com"

def randomString(stringLength=255):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    confirmed_email = db.Column(db.Boolean, nullable=False, default=1)
    face_confirmed= db.Column(db.Boolean, nullable=False, default=0)
    qr_confirmed = db.Column(db.Boolean, nullable=False, default=0)
    sms_confirmed = db.Column(db.Boolean, nullable=False, default=0)
    auth_mode = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    authenticated=db.Column(db.Boolean, nullable=False, default=0)
    sms_code = db.Column(db.String(6))
    valid_ip = db.Column(db.String(255))
    rem_token = db.Column(db.String(255))


    check_time = db.Column(db.String(20), nullable=False)
    time_out = db.Column(db.Boolean, nullable=False, default=0)
    oneTime_reg = db.Column(db.Boolean, nullable=False, default=0)




    # Validating link time : 2 minutes
    def create_token(self, expires_sec=120):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return False
        return User.query.get(user_id)

    def create_qr(self):
        id=str(self.id)
        auth = OtpAuth(app.config['SECRET_KEY'] + id)  # a secret string
        email = self.email
        s = auth.to_uri('totp', email, 'Unit963')
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=15,
            border=5,
        )
        qr.add_data(s)
        img = qr.make_image(fill_color="#05528a", back_color="white")
        img.save('./MFA/static/QR/' + id + '.png')


#--------------------------------------------------------------------------------------------
    def send_security_email(self, ip, device, browser, ver):
        g = geocoder.ip(ip)
        userInfo = g.geojson
        address = userInfo['features'][0]['properties']['address']
        city1 = userInfo['features'][0]['properties']['city']
        lat = userInfo['features'][0]['properties']['lat']
        lng = userInfo['features'][0]['properties']['lng']
        zoom = 14
        maptype = "hybrid"
        mapReq = end_point + "center=" + city1 + "&zoom=" + str(zoom) + "&markers=" +str(lat)+"," + str(lng) + "&size=400x400&maptype=" + maptype + "&key=" + os.environ.get("map_token")
        r = requests.get(mapReq)
        f = open("map.png", "wb")
        f.write(r.content)
        f.close()
        receiver_email = self.email
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Security Alert"
        message["From"] = os.environ.get('Unit_UN')
        message["To"] = receiver_email
        now = datetime.now()
        time = now.strftime("%d/%m/%Y %H:%M:%S")

        
        html = """\
        <html>
        <body>
            <b><h1>Security Alert</h1></b>
            <hr> 
            <p>Hey, did you try to login? A login attempt has been made.</br>
            <ul>
            <li>When: <b>{time}</b></li></br>
            <li>Device: <b>{device} - Ver: {ver}</b></li></br>
            <li>Browser: <b>{browser}</b></li></br>
            <li>Near: <b>{address}</b></li></br>
            <li>IP: <b>{ip}</b></li></ul><br>
            If that is you, then you can click <a href="http://127.0.0.1:5000/save_ip/{email}/{token}/{ip}">here</a> to save this location.<br>
            If you suspect that someone else is trying to get into your account please contact our tech center.<br> 
            </p>
        </body>
        </html>
        """.format(ip = ip, token=randomString(), address=address, email=receiver_email,device=device,browser=browser,ver=ver,time=time)
        part1 = MIMEText(html, "html")
        message.attach(part1)


        with open('map.png', 'rb') as f:
            mime = MIMEBase('image', 'png', filename='map.png')
            mime.add_header('Content-Disposition', 'attachment', filename='map.png')
            mime.add_header('X-Attachment-Id', '0')
            mime.add_header('Content-ID', '<0>')
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            message.attach(mime)


        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(os.environ.get('Unit_UN'), os.environ.get('Unit_PW'))
            server.sendmail(os.environ.get('Unit_UN'), receiver_email, message.as_string())


#--------------------------------------------------------------------------------------------






    def verify_qr(self):
        id=str(self.id)
        auth = OtpAuth(app.config['SECRET_KEY'] + id)  # a secret string
        return auth.totp()


    def send_sms(self):
        client = Client(account_sid, auth_token)
        numberList = []
        for i in range(6):
            randomNumber = random.randint(0,9)
            numberList.append(str(randomNumber))
        code = "".join(numberList)
        userTelNumDB = self.phone
        phone = userTelNumDB[1 : : ]
        message = client.messages.create(body="Your Code is:\n" + str(code),
                                            from_='+17044694259',
                                            to='+31'+ phone)
        print(message.sid)
        self.sms_code = code
        db.session.commit()


    def create_photo(self, id, img):
        with open("./MFA/static/profile_pics/"+str(id) +".jpg","wb") as f:      
            f.write(base64.b64decode(img))
            print("done from models")

   
    def send_logo(self,logo):
        with open("C:/Users/Ghais/Desktop/testflask/"+logo+".png", "rb") as imageFile:
                image_byte = base64.b64encode(imageFile.read())
                stringData = image_byte.decode("utf-8")
                b64_src = 'data:image/jpg;base64,'
                stringData = b64_src + stringData
                emit('response_back', stringData) 
   


    def image_processing(self, img):
        id=str(self.id)
        print(id)
        imgdata = base64.b64decode(img)
        image = Image.open(io.BytesIO(imgdata))
        imgRGP = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
     
        known_image = face_recognition.load_image_file("./MFA/static/profile_pics/"+id +".jpg")
        known_face_encodings = face_recognition.face_encodings(known_image)
      
      
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(imgRGP)
        face_encodings = face_recognition.face_encodings(imgRGP, face_locations)

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
           # print(face_encoding) 
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            print(matches)
            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                return True
            elif False in matches:
                return False



    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.phone}')"





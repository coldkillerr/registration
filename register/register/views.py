from django.shortcuts import render
import pyrebase
from django.contrib import auth
config = {
    'apiKey': "AIzaSyC87WZEoXzppPa1OWotrHglyaUX1zXKJf4",
    'authDomain': "regi-a7a96.firebaseapp.com",
    'databaseURL': "https://regi-a7a96-default-rtdb.firebaseio.com",
    'projectId': "regi-a7a96",
    'storageBucket': "regi-a7a96.appspot.com",
    'messagingSenderId': "840385202733",
    'appId': "1:840385202733:web:2e22506b1872bc3cb546a4",
    'measurementId': "G-YEMMTXTW87"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


def signin(request):
    return render(request, "signin.html")


def postsignin(request):
    email = request.POST.get("email")
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        message = "invalid credentials"
        return render(request, "signin.html", {"messg": message})
    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, "postsignin.html", {"e": email})


def logout(request):
    auth.logout(request)
    return render(request, "signin.html")


def signup(request):
    return render(request, "signup.html")


def postsignup(request):
    nroom = request.POST.get('nroom')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    sname = request.POST.get('sname')
    try:
        user = authe.create_user_with_email_and_password(email, passw)
    except:
        message = "unable to create account, try again"
        return render(request, "signup.html", {"messg": message})
    uid = user['localId']
    data = {"nroom": nroom}

    database.child(sname).child("details").set(data)

    return render(request, "signin.html")


def create(request):
    return render(request, "create.html")


def output(request):
    return render(request, "output.html")


def post_create(request):

    import time
    from datetime import datetime, timezone
    import pytz
    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))

    fname = request.POST.get('fname')
    contact1 = request.POST.get('contact1')
    contact2 = request.POST.get('contact2')
    room = request.POST.get('room')
    adhar = request.POST.get('adhar')

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("info "+str(a))
    data = {
        "fname": fname,
        "contact1": contact1,
        "contact2": contact2,
        "room": room,
        "adhar": adhar
    }

    database.child('users').child(millis).child(a).child('reports').set(data)

    return render(request, "postsignin.html")


def webcam(request):
    import cv2
    import time
    import winsound

    frequency = 2800  # Set Frequency To 2500 Hertz
    duration = 1500

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    count = 0
    i = 0

    while i == 0:
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow("img", img)
        faces = face_cascade.detectMultiScale(gray, 1.1, 8)
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 3)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        for (ex, ey, ew, eh) in eyes:
            for (x, y, w, h) in faces:
                cv2.imshow('img', img)
                t = time.strftime("%Y-%m-%d_%H-%M-%S")
                print("Image " + t + "saved")
                file = 'C:/Users/caksh/Desktop/' + t + '.jpg'
                cv2.imwrite(file, img)
                count += 1

                if (x, y, w, h) in faces:
                    cv2.destroyWindow("img")
                    winsound.Beep(frequency, duration)
                    i += 1

    return render(request, "create.html")

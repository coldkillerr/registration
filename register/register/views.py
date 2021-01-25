from django.shortcuts import render,redirect
import pyrebase
from django.contrib import auth
from .forms import  signInForm,signUpForm,createForm
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
    if request.method=='POST':
        form=signInForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
        # print(email,password)
            try:
                user = authe.sign_in_with_email_and_password(email, password)
                print(user['idToken'])
                session_id = user['idToken']
                request.session['uid'] = str(session_id)
                return render(request, "postsignin.html", {"e": email})
            except:
                message = "invalid credentials"
                return render(request, "signin.html", {"messg": message,'form':form})
    form=signInForm()
    return render(request, "signin.html", {"form": form})


# def postsignin(request):
#     email = request.POST.get("email")
#     passw = request.POST.get("pass")
#     form=signInForm()

#     try:
#         user = authe.sign_in_with_email_and_password(email, passw)
#     except:
#         message = "invalid credentials"
#         return render(request, "signin.html", {"messg": message})
        
#     print(user['idToken'])
#     session_id = user['idToken']
#     request.session['uid'] = str(session_id)
#     return render(request, "postsignin.html", {"e": email})


def logout(request):
    auth.logout(request)
    return redirect('/')
    # return render(request, "signin.html", {"form": signInForm()})


def signup(request):
    form=signUpForm()
    if request.method=='POST':
        form=signUpForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            nroom=form.cleaned_data['nroom']
            sname=form.cleaned_data['sname']
   
            try:
                user = authe.create_user_with_email_and_password(email, password)
            except:
                print('error')
                message = "unable to create account, try again"
                return redirect('/')
            uid = user['localId']
            data = {"nroom": nroom}
            database.child(sname).set(data)
            return redirect('/')

    return render(request, "signup.html",{"form":form})


# def postsignup(request):
#     form=signUpForm()
#     if request.method=='POST':
#         form=signUpForm(request.POST)
#         if form.is_valid():
#             email=form.cleaned_data['email']
#             password=form.cleaned_data['password']
#             nroom=form.cleaned_data['nroom']
#             sname=form.cleaned_data['sname']
   
#     try:
#         user = authe.create_user_with_email_and_password(email, password)
#     except:
#         message = "unable to create account, try again"
#         return redirect('/')
#     uid = user['localId']
#     data = {"nroom": nroom}

#     database.child(sname).set(data)
#     return redirect('/')


def create(request):
    import time
    from datetime import datetime, timezone
    import pytz
    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))

    form=createForm()
    if request.method=='POST':
        form=createForm(request.POST)
        if form.is_valid():
            fname=form.cleaned_data['fname']
            contact1=form.cleaned_data['contact1']
            contact2=form.cleaned_data['contact2']
            room=form.cleaned_data['room']
            adhar=form.cleaned_data['adhar']

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
    return render(request,'create.html',{"form":form})


def output(request):
    return render(request, "output.html")


def post_create(request):

    import time
    from datetime import datetime, timezone
    import pytz
    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))

    form=createForm()
    if request.method=='POST':
        form=createForm(request.POST)
        if form.is_valid():
            fname=form.cleaned_data['fname']
            contact1=form.cleaned_data['contact1']
            contact2=form.cleaned_data['contact2']
            room=form.cleaned_data['room']
            adhar=form.cleaned_data['adhar']

            idtoken = request.session['uid']
            a = authe.get_account_info(idtoken)
            a = a['users']
            a = a[0]
            a = a['localId']
            print("info "+str(a))
            data = {
                "fname": fname,
                "contact1": str(contact1),
                "contact2": str(contact2),
                "room": room,
                "adhar": adhar
            }
            database.child('users').child('reports').push(data)
    return render(request,'create.html',{"form":form})


def webcam(request):
    return render(request, "webcam.html")
    # import cv2
    # import time
    # # import winsound

    # frequency = 2800  # Set Frequency To 2500 Hertz
    # duration = 1500

    # face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # count = 0
    # i = 0

    # while i == 0:
    #     img = cap.read()
    #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     cv2.imshow("img", img)
    #     faces = face_cascade.detectMultiScale(gray, 1.1, 8)
    #     eyes = eye_cascade.detectMultiScale(gray, 1.3, 3)
    #     k = cv2.waitKey(30) & 0xff
    #     if k == 27:
    #         break
    #     for (ex, ey, ew, eh) in eyes:
    #         for (x, y, w, h) in faces:
    #             cv2.imshow('img', img)
    #             t = time.strftime("%Y-%m-%d_%H-%M-%S")
    #             print("Image " + t + "saved")
    #             file = 'C:/Users/caksh/Desktop/' + t + '.jpg'
    #             cv2.imwrite(file, img)
    #             count += 1

    #             if (x, y, w, h) in faces:
    #                 cv2.destroyWindow("img")
    #                 winsound.Beep(frequency, duration)
    #                 i += 1

   

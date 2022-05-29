from django.contrib import messages
from datetime import date
from django.contrib.auth import logout
from turtle import home
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf.urls.static import static
from django.contrib.auth import login,authenticate,logout
from web_app.models import StudentData
from web_app import take_train_img
from web_app import trainer
from web_app import take_attendance
import pandas as pd
import json
import time
from time import sleep
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

def takeattendance(request):
    p_list=take_attendance.attendance_taker()
    roll_list, name_list, email_list, present_list, total_days_list=fetch_val()
    increment()
    update(p_list)
    time.sleep(1.5)
    create_pcsv(roll_list, name_list, email_list,  present_list, total_days_list, p_list)
    return render(request, "attendance_cnf.html")

def response(request):
    return HttpResponse("Working Fine!!!")

def login(request):
    return render(request, "login.html")


def landing(request):
    #created just for checking
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
          username = request.POST.get('username')
          password = request.POST.get('password')
          print(username)
          print(password)
          user = authenticate(username=username, password=password)
          if user is not None:
                    #login(request, user)
            #if request.user.is_authenticated :
                    return redirect('/home')

          else:
                    messages.info(request, "Problem Logging in")
                    return redirect('/')
     

def logout_view(request):
    messages.info(request, "Logged out sucessfully")
    logout(request)
    return redirect('Login')

def reg(request):
    return render(request, "register.html")


def train_img(request):
    trainer.train()
    return render(request, "traincnf.html")


def reg_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        roll = request.POST.get('roll')
        course = request.POST.get('course')
        stream = request.POST.get('strm')
        gender = request.POST.get('gender')
        year = request.POST.get('year')


        new_student = StudentData(name=name, email=email, roll=roll, course=course,  stream=stream, gender=gender, year=year)
        new_student.save()
        take_train_img.create_dataset(roll)


        return redirect('landing')


def update(present_list):
    for i in present_list:
        t = StudentData.objects.get(roll=i)
        t.present_days = int(t.present_days) +1
        t.save()

def increment():
    StudentData.objects.update(total_days=F('total_days')+1)


def fetch_val():
    list_roll=StudentData.objects.values_list('roll', flat=True)
    list_name=StudentData.objects.values_list('name', flat=True)
    list_email=StudentData.objects.values_list('email', flat=True)
    list_pdays=StudentData.objects.values_list('present_days', flat=True)
    list_tdays=StudentData.objects.values_list('total_days', flat=True)

    list_roll=list(list_roll)
    list_name=list(list_name)
    list_email=list(list_email)
    list_pdays=list(list_pdays)
    list_tdays=list(list_tdays)

    return list_roll, list_name, list_email, list_pdays, list_tdays


def create_pcsv(list_roll, list_name, list_email, list_pdays, list_tdays, p_list):
    status=[]
    for i in range(0,len(list_roll)):
        status.append("ABSENT")

    print(p_list) 
    for i in range(0,len(list_roll)):
        if (int(list_roll[i]) in p_list):
            status[i]="PRESENT"

    percentagelist = []
    k=0
    while(k < len(list_pdays)):
        a=list_pdays[k]
        b=list_tdays[k]
        percentagelist.insert(k, (100*a/b))
        k+=1

    dict={'Roll': list_roll, 'Name': list_name, 'Email': list_email, "Status": status, "Percentage": percentagelist}
    df = pd.DataFrame(dict)
    today = date.today()
    df.to_csv("Attendance Sheet "+str(today)+".csv")



def Table(request):
    today = date.today()
    df = pd.read_csv("Attendance Sheet "+str(today)+".csv")
    # parsing the DataFrame in json format.
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context = {'d': data}
  
    return render(request, 'table.html', context)


def mail_cnf(request):
    return render(request ,"mail_cnf.html")


def initiate_sendmail(request):
    today = date.today()
    df=pd.read_csv("Attendance Sheet "+str(today)+".csv")
    new_df= df.loc[df['Status'] == "ABSENT"]
    for i in new_df["Email"]:
        send_email_status(i)

    return redirect("mailcnf")

def send_email_status(to_email):
    today = date.today()
    subject= "Attendance Status for "+str(today)
    message = "Dear Student, \n\n You have been marked absent for today's class.\nRegards,\nAttendance Admin"
    try:
        send_mail(subject, message, "info.project211@yahoo.com", [to_email])
    except :
        print("cant send email")
    
    print("DONE")


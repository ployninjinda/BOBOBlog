from django.contrib import auth
from django.shortcuts import render,redirect
from django.contrib import messages 
from django.contrib.auth.models import User #ดึงโมเดลauth_userมาใช้งาน


# Create your views here.
def index(request):
    return render(request,"backend/login_register.html")

def register(request):
    if request.method == "POST" :
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        if username == "" or email == "" or password == "" or repassword == "": #ต้องกรอกให้ครบเท่านั้น
            messages.info(request,"กรุณาป้อนข้อมูลให้ครบ") #ให้ส่งข้อความตอบกลับไปให้user
            return redirect("member") #เมื่อกดsubmitให้กลับมาหน้าสมัครสมาชิกเหมือนเดิม
        else:
            if password == repassword :
                if User.objects.filter(username=username).exists(): #เช็คค่าUserซ้ำกัน
                    messages.info(request,"Usernameนี้มีคนใช้แล้ว")
                    return redirect("member")
                elif User.objects.filter(email=email).exists(): #เช็คค่าEmailซ้ำกัน
                    messages.info(request,"Emailนี้ได้ลงทะเบียนเป็นนักเขียนของเราแล้ว")
                    return redirect("member")
                else :
                    user = User.objects.create_user(
                    username = username,
                    email = email,
                    password = password 
                )
                    user.save() #บันทึกข้อมูลลงฐานข้อมูลได้เลย
                    messages.info(request,"ขอบคุณที่สมัครเป็นนักเขียนของเรา!")
                    return redirect("member")
            else:
                messages.info(request,"กรุณากรอกรหัสผ่านให้ตรงกัน")
                return redirect("member")

def login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = auth.authenticate(username=username,password=password)

    if user is not None:
        auth.login(request,user)
        return redirect("panel")
    else:
        messages.info(request,"ไม่พบบัญชีผู้ใช้งาน")
        return redirect("member")

def logout(request):
    auth.logout(request)
    return redirect('member')
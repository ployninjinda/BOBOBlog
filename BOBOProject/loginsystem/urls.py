from django.urls import path
from .views import index,register,login,logout

urlpatterns = [
    path('member',index,name="member"), #หน้าสมัครใช้งานเรียกใช้ member
    path('register/add',register,name="addUser"), #ส่งข้อมูลเรียกใช้register
    path('login',login,name="login"),
    path('logout',logout,name="logout"),
]
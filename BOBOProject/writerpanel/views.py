from django.shortcuts import render,redirect
from blogs.models import Blogs
from django.db.models import Sum 
from django.contrib.auth.decorators import login_required #บังคับให้login
from django.contrib.auth.models import User,auth
from category.models import Category
from django.core.files.storage import FileSystemStorage #อัพโหลดไฟล์ภาพ
from django.contrib import messages
# Create your views here.

@login_required(login_url="member") #ถ้าไม่ล้อคอินจะไม่สามารถใช้panelของนักเขียนได้ และกลับไปหน้าlogin
def panel(request):
    writer = auth.get_user(request) #ทำให้loginไปด้วยโปรไฟล์นักเขียนคนนั้น
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count() #นับจำนวนบทความอ้างอิงจากชื่อนักเขียน
    total = Blogs.objects.filter(writer=writer).aggregate(Sum("views"))
    return render(request,"backend/index.html" , {"blogs":blogs , "writer":writer , "blogCount":blogCount , "total":total}) #รันหน้าindexนักเขียนขึ้นมา

@login_required(login_url="member")
def displayForm(request):
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    total = Blogs.objects.filter(writer=writer).aggregate(Sum("views"))
    categories = Category.objects.all()
    return render(request,"backend/blogForm.html", {"blogs":blogs , "writer":writer , "blogCount":blogCount , "total":total , "categories":categories})

@login_required(login_url="member")
def insertData(request):
    try:
        if request.method == "POST" and request.FILES["image"] : #เช็คว่ามีการส่งPOSTมาและมีไฟล์ชื่อimageไหม
            datafile = request.FILES["image"]
            #รับค่าจากformนักเขียน
            name = request.POST["name"]
            category = request.POST["category"]
            description = request.POST["description"]
            content = request.POST["content"]
            writer = auth.get_user(request)

            if str(datafile.content_type).startswith("image") : #เช็คว่าไฟล์ที่ส่งมาขึ้นต้นด้วยimageหรือไม่
                #การอัพโหลด
                fs = FileSystemStorage()
                img_url = "blogsImages/"+datafile.name
                filename = fs.save(img_url,datafile)
                #การบันทึกบทความลงในฐานข้อมูล
                blog = Blogs(name=name,category_id=category,description=description,content=content,writer=writer,image=img_url)
                blog.save()
                messages.info(request,"อัพโหลดบทความสำเร็จ!")
                return redirect("displayForm")
            else:
                messages.info(request,"กรุณาอัพโหลดไฟล์ภาพ")
                return redirect("displayForm")
    except:
        return redirect("displayForm")

@login_required(login_url="member")        
def deleteData(request,id):
    try:
        blog = Blogs.objects.get(id=id)
        fs = FileSystemStorage()
        #ลบข้อมูลจากฐานข้อมูล
        blog.delete()
        #ลบภาพจากฐานข้อมูล
        fs.delete(str(blog.image))
        return redirect("panel")
    except:
        return redirect("panel")

@login_required(login_url="member")
def editData(request,id):
    #ข้อมูลพื้นฐาน
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    total = Blogs.objects.filter(writer=writer).aggregate(Sum("views"))
    categories = Category.objects.all()

    blogEdit = Blogs.objects.get(id=id)
    return render(request,"backend/editForm.html",{"blogEdit":blogEdit , "writer":writer , "blogCount":blogCount , "total":total , "categories":categories})

@login_required(login_url="member")
def updateData(request,id):
    try:
        if request.method == "POST" :
            #ดึงข้อมูลบทความเดิมมาใช้งาน
            blog = Blogs.objects.get(id=id)
            #รับค่าจากformนักเขียน
            name = request.POST["name"]
            category = request.POST["category"]
            description = request.POST["description"]
            content = request.POST["content"]

            #อัพเดตข้อมูล
            blog.name = name
            blog.category_id = category
            blog.description = description
            blog.content = content
            blog.save()

            #อัพเดตภาพปก
            if request.FILES["image"]:
                datafile = request.FILES["image"]
                if str(datafile.content_type).startswith("image") :
                    #ลบภาพเก่า
                    fs = FileSystemStorage()
                    fs.delete(str(blog.image))
                    #เพิ่มภาพใหม่
                    img_url = "blogsImages/"+datafile.name
                    filename = fs.save(img_url,datafile)
                    blog.image = img_url
                    blog.save()
            messages.info(request,"อัพเดตข้อมูลสำเร็จ!")
            return redirect("panel")
    except:
        return redirect("panel")
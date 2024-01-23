from django.shortcuts import render
from django.http import HttpResponse
from category.models import Category
from .models import Blogs
from django.core.paginator import Paginator , EmptyPage , InvalidPage

# Create your views here.
def index(request):
    categories= Category.objects.all()
    blogs= Blogs.objects.all() #เรียงจากเก่าไปใหม่
    latest = Blogs.objects.all().order_by('-pk')[:2] #เรียงจากpkมากไปน้อย ทำให้เรียงบทความใหม่ไปเก่า และเอาแค่2บทความล่าสุด
    
    #บทความยอดนิยม
    popular = Blogs.objects.all().order_by('-views')[:3] #เอายอดวิวเยอะที่สุด 3 อันดับแรก

    #บทความแนะนำ
    suggestion = Blogs.objects.all().order_by('views')[:3]

    #pageination
    paginator = Paginator(blogs,2) #การแบ่งหน้าบทความเป็น 2 บทความต่อ 1 หน้า
    try:
       page = int(request.GET.get('page','1'))
    except:
        page = 1
    
    try:
        blogPerpage = paginator.page(page) #จำนวนบทความอ้างอิงจากตัวแปรpageที่ตั้งไว้
    except(EmptyPage , InvalidPage):
        blogPerpage = paginator.page(paginator.num_pages) #เอาช่วงของpageหน้าสุดท้ายมากำหนดในblogPerpage
        
    return render(request,"frontend/index.html",{'categories':categories , 'blogs':blogPerpage , 'latest':latest , 'popular':popular , 'suggestion':suggestion})

def BlogDetail(request,id):
    categories= Category.objects.all()
    #บทความยอดนิยม
    popular = Blogs.objects.all().order_by('-views')[:3] #เอายอดวิวเยอะที่สุด 3 อันดับแรก

    #บทความแนะนำ
    suggestion = Blogs.objects.all().order_by('views')[:3]

    singleBlog = Blogs.objects.get(id=id)
    singleBlog .views = singleBlog.views+1 #ยอดวิวจะเพิ่มขึ้นตามการคลิกเข้าไปอ่านบทความ
    singleBlog.save() #เซฟยอดวิวไว้
    return render(request,"frontend/BlogDetail.html" , {'blog':singleBlog , 'categories':categories , 'popular':popular , 'suggestion':suggestion})

def searchCategory(request,cat_id): #ใช้รหัสหมวดหมู่เป็นตัวอ้างอิง
    blogs = Blogs.objects.filter(category_id=cat_id)
    #บทความยอดนิยม
    popular = Blogs.objects.all().order_by('-views')[:3] #เอายอดวิวเยอะที่สุด 3 อันดับแรก

    #บทความแนะนำ
    suggestion = Blogs.objects.all().order_by('views')[:3]
    categoryName = Category.objects.get(id=cat_id)
    categories= Category.objects.all()
    return render(request,"frontend/searchCategory.html",{"blogs":blogs , 'categories':categories , 'popular':popular , 'suggestion':suggestion , "categoryName":categoryName})

def searchWriter(request,writer):
    blogs = Blogs.objects.filter(writer=writer)
    categories= Category.objects.all()
    suggestion = Blogs.objects.all().order_by('views')[:3]
    popular = Blogs.objects.all().order_by('-views')[:3]
    return render(request,"frontend/searchWriter.html",{"blogs":blogs , 'categories':categories , 'popular':popular , 'suggestion':suggestion , 'writer':writer})
from importlib.resources import contents
from multiprocessing import context
from django.shortcuts import render, redirect
from .models import *
from songline import Sendline
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
# เอาไว้ตรวจสอบว่าต้องล็อคอินก่อนถึงจะเข้าหน้าได้
from django.contrib.auth.decorators import login_required
import uuid # uuid สำหรับ gen รหัส unique
from django.core.files.storage import FileSystemStorage #ให้สามารถเก็บไฟล์ได้


def Home(request):
    allproduct = Product.objects.all()  # SELECT * FROM Product
    context = {'allproduct': allproduct}  # Set context as object
    # render html file with variable
    return render(request, 'company/home.html', context)


def AboutUs(request):
    return render(request, 'company/aboutus.html')


def Contact(request):
    context = {}
    if request.method == "POST":
        data = request.POST.copy()  # copy data from POST to var
        title = data.get('title')  # get key from input name
        description = data.get('description')
        cost = data.get('cost')

        # If user don't fill some var
        if title == '' and description == '':
            context['message'] = "ไม่ได้ใส่ title กับ description มา"
            return render(request, 'company/contact.html', context)

        # Add data to tabel
        newContact = ContactList()  # get Class to var
        newContact.title = title  # set key of model
        newContact.description = description
        newContact.cost = cost
        newContact.save()
        context['message'] = "สำเร็จแล้ว"

        token = 'Pq5nvPFOtfGd1SHQCmBMgJ1sXH3DLuqOxnXQuM3UkdM'
        m = Sendline(token)
        m.sendtext('หัวข้อ: {} \nคำอธิบาย: {}\nราคา: {}'.format(
            title, description, cost))
        # Can do like this
        # Contact(title=title,description=description,cost=cost)
    return render(request, 'company/contact.html', context)


def Login(request):
    context = {}
    if request.method == "POST":
        data = request.POST.copy()  # copy data from POST to var
        username = data.get('username')  # get key from input name
        password = data.get('password')
        try:
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home-page')
        except:
            context['message'] = "รหัสผ่านไม่ถูกต้อง"
    return render(request, 'company/login.html', context)

# ต้องล็อกอินก่อนถึงจะเข้าหน้านี้ได้


@login_required
def Accountant(request):
    # if request.user.profile.usertype != 'accountant': # เฉพาะ accountant เท่านั้นที่เช้าได้
    # หรือจะเขียนแบบนี้ก็ได้
    allowUser = ['accountant', 'admin']
    if request.user.profile.usertype not in allowUser:
        return redirect('home-page')
    # contact = ContactList.objects.all()
    contact = ContactList.objects.all().order_by('-id')  # เรียงตามไอดี จากมากไปน้อย
    context = {'contact': contact}
    return render(request, 'company/accountant.html', context)


def Register(request):
    context = {}
    if request.method == "POST":
        data = request.POST.copy()  # copy data from POST to var
        fullname = data.get('fullname')
        username = data.get('username')  # get key from input name
        password = data.get('password')
        password2 = data.get('password2')
        try:
            # ตรวจสอบว่า username ใน db เท่ากับตัวที่รับมาหรือไม่ ถ้าเท่ากันแสดงว่ามีในระบบแล้ว
            user = User.objects.get(username=username)
            context['warning'] = "มี username : {} นี้ในระบบแล้ว".format(
                username)
            context['fullname'] = fullname  # เอา fullname กลับไปวางในช่อง
            return render(request, 'company/register.html', context)
        except:  # ถ้ายังไม่มีให้สร้างใหม่

            # Check match password
            if password != password2:
                return render(request, 'company/register.html', context)
            newUser = User()
            newUser.first_name = fullname
            newUser.username = username
            newUser.email = username
            newUser.set_password(password)  # จำเป็นต้องกำหนดแบบนี้
            newUser.save()

            u = uuid.uuid1()
            token = str(u)

            newProfile = Profile()
            # get last user in db ที่ใช้การดึงตัวล่าสุดมาเพราะว่า username ตัวแรกโดนใช้ไปตอนสร้าง User แล้ว ไม่สามารถเอามาใช้ร่วมกับการสร้าง profile ได้อีก
            newProfile.user = User.objects.get(username=username)
            newProfile.verified_token = token
            newProfile.save()

            tokenLine = 'Pq5nvPFOtfGd1SHQCmBMgJ1sXH3DLuqOxnXQuM3UkdM'
            m = Sendline(tokenLine)
            m.sendtext(
                'กดลิงค์นี้เพื่อยืนยันอีเมล์: {} ของ {} ที่ลิงค์ http://localhost:8000/verify-email/{}'.format(token, request.user.username,token))
        try:
            user = authenticate(username=username, password=password)
            login(request, user)
        except:
            context['message'] = "รหัสผ่านไม่ถูกต้อง"
    return render(request, 'company/register.html', context)

def VerifySuccess(request,token):
    context = {}
    try:
        tokenProfile = Profile.objects.get(verified_token = token)
        tokenProfile.verified = True
        tokenProfile.save()
    except:
        context['error'] = "ลิงค์สำหรับยืนยัน ไม่ถูกต้อง"
    return render(request,'company/verifyemail.html',context)

@login_required
def ProfileUser(request):
    context = {}
    profileUser = Profile.objects.get(user=request.user)
    context['profile'] = profileUser
    return render(request, 'company/profile.html', context)


def ResetPassword(request):
    context = {}
    if request.method == 'POST':
        data = request.POST.copy()
        username = data.get('username')

        try:
            user = User.objects.get(username=username)
            u = uuid.uuid1()
            token = str(u)
            newReset = ResetPasswordToken()
            newReset.user = user
            newReset.token = token
            newReset.save()
            token = 'Pq5nvPFOtfGd1SHQCmBMgJ1sXH3DLuqOxnXQuM3UkdM'
            m = Sendline(token)
            m.sendtext(
                'กดลิงค์นี้เพื่อรีเซ็ตรหัสผ่าน: {} ของ {}'.format(token, username))
            return redirect('home-page')
        except:
            context['message'] = '1'

    return render(request, 'company/resetpassword.html', context)


def ResetNewPassword(request, token):
    context = {}
    try:
        check = ResetPasswordToken.objects.get(token=token) # get แถวที่มี token ตรงกับ token ที่โยนเข้าไป
        if request.method == 'POST':
            data = request.POST.copy()
            password = data.get('password')
            password2 = data.get('password2')
            if password == password2:
                user = check.user # ดึงเอา field user_id ของ model ResetPasswordToken มา
                user.setpassword(password)
                user.save()
                # loginInformation = authenticate(username=user.username, password=password)
                # login(request,loginInformation)
            else:
                context['error'] = "รหัสผ่านทั้งสองช่องไม่ตรงกัน กรุณากรอกใหม่"
    except:
        context['error'] = "ลิงค์สำหรับ reset รหัสผ่านหมดอายุ หรือลิงค์ไม่ถูกต้อง"

    return render(request, 'company/resetnewpassword.html',context)
def AddProduct(request):
    context = {}
    if request.method == 'POST':
       data = request.POST.copy()
       title = data.get('title')
       description = data.get('description')
       price = data.get('price')
       mobile = data.get('mobile')
       newProduct = Product()
       newProduct.title = title
       newProduct.description = description
       newProduct.price = float(price)
       newProduct.mobile = mobile

       if 'image' in request.FILES: #มี key picture อยู่ใน request.FILES หรือไม่
           file_image = request.FILES['image'] # ตัวนี้คือไฟล์จริงๆ
           file_image_name = file_image.name.replace(' ','') # ดึง name ใน object รูปภาพออกมาพร้อมแทนที่ เว้นวรรค ด้วยค่าว่าง
           fs = FileSystemStorage()   # สำหรับบันทึกข้อมูลลงเครื่อง
           filename = fs.save(file_image_name,file_image) # คำสั่งบันทึกลงเครื่องโดยใส่ชื่อ และรูปภาพ
           upload_file_url = fs.url(filename)
           newProduct.image = upload_file_url[6:]

       if 'file' in request.FILES: #มี key picture อยู่ใน request.FILES หรือไม่
           file_image = request.FILES['file'] # ตัวนี้คือไฟล์จริงๆ
           file_image_name = file_image.name.replace(' ','') # ดึง name ใน object รูปภาพออกมาพร้อมแทนที่ เว้นวรรค ด้วยค่าว่าง
           fs = FileSystemStorage()   # สำหรับบันทึกข้อมูลลงเครื่อง
           filename = fs.save(file_image_name,file_image) # คำสั่งบันทึกลงเครื่องโดยใส่ชื่อ และรูปภาพ
           upload_file_url = fs.url(filename) #ดึง url ออกมาจาก file_name 
           newProduct.file = upload_file_url[6:]
       newProduct.save()
    #    render redirect ('home-page') 
    context['message'] = "เพิ่ม Product สำเร็จแล้ว"
    return render(request,'company/addproduct.html')
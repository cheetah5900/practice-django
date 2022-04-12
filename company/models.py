from django.db import models
from django.contrib.auth.models import User  # user data from Auth

# เก็บข้อมูลส่วนตัวนอกเหนือจากชื่อ นามสกุล
class Profile(models.Model):
    # ถ้ามีการลบ User จากระบบ Profile จะโดนลบไปด้วย
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usertype = models.CharField(max_length=100, default='member')
    point = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    verified_token = models.CharField(max_length=100,default='no token')

    def __str__(self):
        return self.user.username  # เอา username ออกมาจาก object user

# เก็บรายชื่อสินค้า
class Product(models.Model):
    title = models.CharField(max_length=200)
    # blank means blankable on website
    description = models.TextField(null=True, blank=True)
    # decimal_place is how many decinal after dot
    price = models.IntegerField(
        default=0, null=True)
    mobile = models.CharField(max_length=20,null=True,blank=True)
    image = models.ImageField(upload_to='product',null=True,blank=True)
    file = models.FileField(upload_to='specfile',null=True,blank=True)

    def __str__(self):
        return self.title

# เก็บรายชื่อผู้ติดต่อ
class ContactList(models.Model):
    title = models.CharField(max_length=200)
    # blank means blankable on website
    description = models.TextField(null=True, blank=True)
    # decimal_place is how many decinal after dot
    cost = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title

#เก็บข้อมูล Reset Password
class ResetPasswordToken (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class CrudUser(models.Model):
    name = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(blank=True, null=True)
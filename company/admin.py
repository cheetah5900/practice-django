from django.contrib import admin
from .models import *  # import any class in model.py

admin.site.register(Product)  # make admin be able to see database
admin.site.register(Profile)
admin.site.register(ResetPasswordToken)
admin.site.register(CrudUser)

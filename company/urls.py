from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name='home-page'),
    path('about/', AboutUs, name='about-page'),
    path('contact/', Contact,name='contact-page'),
    path('account/', Accountant,name='account-page'),
    path('register/', Register,name='register-page'),
    path('profile/', ProfileUser,name='profile-page'),
    path('reset-password/', ResetPassword,name='reset-page'),
    path('reset-new-password/<str:token>', ResetNewPassword,name='reset-new-page'),
    path('verify-email/<str:token>', VerifySuccess,name='verify-email-page'),
    path('add-product', AddProduct,name='add-product-page'),
    #AJAX Example
    path('crud/',  CrudView.as_view(), name='crud_ajax'),
    path('ajax/crud/create/',  CreateCrudUser.as_view(), name='crud_ajax_create'),
    path('ajax/crud/update/',  UpdateCrudUser.as_view(), name='crud_ajax_update'),
    path('ajax/crud/delete/',  DeleteCrudUser.as_view(), name='crud_ajax_delete'),
]

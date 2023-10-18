from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('total/', views.totalthreeyearsv, name='totalthreeyearsv'),
    path('topprovince/',views.topprovinceratev, name='topprovinceratev'),
    path('hotmajor/',views.hotmajorv, name='hotmajorv'),
    path('hotmajor2/',views.hotmajorvv,name='hotmajorvv'),
    path('kyhotwc/',views.kyhotwc,name='kyhotwc'),
    path('school/',views.school,name='school'),
    path('itkyhotwc/',views.itkyhotwc,name='itkyhotwc'),
    path('',views.index,name='index')
]
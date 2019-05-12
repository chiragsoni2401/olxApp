"""olxApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'olx'

urlpatterns = [
     path('',views.index, name='login_page'),
     #path('<slug>/',views.not_found_page, name='not_found_page'),
     path('login/',views.checkLogin, name='from_login_page'),
     path('logout/',views.logoutFromApp, name='logout_from_app'),
     path('productList',views.product_list, name='product_list'),
     path('createProduct/',views.create_new_product, name='create_product'),
     path('saveProduct/',views.save_new_product, name='save_product'),
     path('thankYou/',views.thank_you, name='thank_you'),
     path('progress-bar-upload/',views.ProgressBarUploadView.as_view(), name='progress_bar_upload'),
     path('deletePhoto/' ,views.deleteUploadedPhoto,name= 'delete_photo'),
     path('deletePhotoFromEdit/' ,views.deleteUploadedPhoto,name= 'delete_photo_from_edit'),
     path('actAndDeact/' ,views.activateAndDeactivatePost,name= 'actAndDact_product'),
     path('markAsSold/' ,views.markAsSold,name= 'markAsSold_product'),
     path('saveFinally/', views.saveProductAndPhoto, name='add_post'),
     path('categories/<slug:category_slug>/',views.product_list, name='product_list_by_category'),
     path('<int:id>/productDetail', views.product_detail, name='product_detail'),
     path('myPost/', views.myPost, name='my_all_post'),
     path('<pk>/editProduct/', views.UpdateProduct.as_view(), name='edit_product'),
   


]



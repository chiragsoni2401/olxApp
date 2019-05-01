from django.contrib import admin
from django.contrib.admin  import AdminSite 
# Register your models here.
from .models import Category, Product,Photo

class CategoryAdmin(admin.ModelAdmin):
      list_display = ['name' , 'slug']
      prepopulated_fields = {'slug':('name',)}
      AdminSite.site_header ='Softvision Olx-Administration'
admin.site.register(Category,CategoryAdmin)


class PhotoAdmin(admin.ModelAdmin):
       #list_display = ['name','slug','price','created','image','updated']  
       list_display = ['photo_type','file']  
       list_filter = ['uploaded_at',]
       
admin.site.register(Photo,PhotoAdmin)


class ProductAdmin(admin.ModelAdmin):
       #list_display = ['name','slug','price','created','image','updated']  
       list_display = ['name','slug','price','created','updated']  
       list_filter = ['created','updated','category'] 
       list_editable = ['price']
       prepopulated_fields = {'slug':('name',)}

      
       
admin.site.register(Product,ProductAdmin)




from django.shortcuts import get_object_or_404, render,redirect
from django.http import  HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.views import View
import time
from itertools import zip_longest
from django.http import JsonResponse
#import ldap
from django.db.models import Q
from .models import Category,Product,Photo,PhotoTemp
from .forms import ProductForm,PhotoTempForm
from django.core.paginator import Paginator
from django.contrib.auth import authenticate,login,logout #Added by chirags
from django.contrib.auth.models import User
from olxApp import settings
from django.db import models
import imghdr
from PIL import Image
from django.views.generic.edit import UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.

def product_list(request, category_slug=None):
    if request.user.is_authenticated:
       request.session['currentPageUrl']=request.path 
       return product_list_fn(request,category_slug)
    else:
       print('session expired') 
       return render(request, 'olx/login.html')

def product_detail(request,id):
    print("inside product_detailllllllll")
    if request.user.is_authenticated:  
      prodphoto = Product.objects.filter(id=id).prefetch_related('photo__set').values('id','name','description','price','contact','status','mark_as_sold','created_by','photo__file','photo__cover_photo_flag')
      return render(request,'olx/product/product_detail.html',{'prodphoto':prodphoto})
    else:
       print('session expired') 
       return render(request, 'olx/login.html')  

#view for creating the new product
def create_new_product(request):
    if request.user.is_authenticated:
       return create_product_fn(request)
    else:
       print('session expired') 
       return render(request, 'olx/login.html')
        
#view for finally saving the product and photo both
def saveProductAndPhoto(request):
    cover_photo_id=request.POST.get('photoSelected')
    print('cover_photo_id:::'+str(cover_photo_id))  
    if request.session['product_and_photo_saved'] == False:  
      product = Product.objects.filter(uploaded_by_id=request.user.id)[0]
      #form here taking photo objects from PhotoTemp table and storing them into Photo table
      all_photos_from_PhotoTemp = PhotoTemp.objects.all().filter(uploaded_by_id=request.user.id).order_by("id")
      for item in all_photos_from_PhotoTemp:
          print("item.id:**"+str(item.id))
          if item.id == int(cover_photo_id):
             print("item.id:::"+str(item.id))
             photo = Photo.objects.create(reference_id=product,cover_photo_flag='yes',photo_type=item.photo_type,uploaded_at=item.uploaded_at,file=item.file,uploaded_by_id = item.uploaded_by_id)
          else:
             photo = Photo.objects.create(reference_id=product,photo_type=item.photo_type,uploaded_at=item.uploaded_at,file=item.file,uploaded_by_id = item.uploaded_by_id)

          photo.save()
        
      PhotoTemp.objects.filter(uploaded_by_id=request.user.id).delete()
      request.session['product_and_photo_saved'] = True
      ProgressBarUploadView.cover_photo = True
      return HttpResponseRedirect(reverse('olx:thank_you'))
def thank_you(request):
    if request.user.is_authenticated:
          return render(request, 'olx/thankyou.html') 
    else:
          return render(request, 'olx/login.html')     
#view for saving the new product from user side
def  save_new_product(request):
 if request.user.is_authenticated:
       
       # If after uploading the images user will refresh the upload page,his photos will be deleted
  

       formToSave = ProductForm(request.POST,request.FILES)
       if formToSave.is_valid():
         product = formToSave.save(commit=False)
         user = request.user
         full_name=request.user.first_name+' '+request.user.last_name
         product.created_by=full_name
         product.uploaded_by_id=request.user.id
         request.session['product_and_photo_saved'] = False
       
         product.save() # Instead of saving it store it in session and save when user clicks on add post
         return saveProductAndPhoto(request)
         request.session['product_details_entered'] = True
            
       else:
          if request.session['product_details_entered'] == False: 

             info='without entering the correct product details you can not save.'
             if request.session['user_has_uploaded_photo'] == True:
                PhotoTemp.objects.filter(uploaded_by_id=request.user.id).delete()
             form = ProductForm()
             return render(request, 'olx/product/create_product.html', {'form': formToSave,'info':info})
           
       ProgressBarUploadView.save_created_product = True
         
 else:
       print('session expired') 
       return render(request, 'olx/login.html') 
def createProductPagination(request,products=None,photos=None):
        paginator = Paginator(products,6)#i.e. show 6 items on each page
        page = request.GET.get('page')
        return paginator.get_page(page)
def create_product_fn(request,info=None):
     if request.session['user_has_uploaded_photo'] == True:
         PhotoTemp.objects.filter(uploaded_by_id=request.user.id).delete()
    
     form = ProductForm()   
     return render(request, 'olx/product/create_product.html', {'form': form,'info':info})
def product_list_fn(request,category_slug=None):
      category = None
      abc = 'hello'
      productPagination = ''
      query = request.GET.get("q")
      
      categories = Category.objects.all()
      #writing logic for getting no. of item in particular category and appending them in a list
      products_count_categorywise = []
      for cat in categories:
          products_count_categorywise.append(Product.objects.all().filter(status=0,category__name=cat.name).count())
      categoriesWithProductsCount = list(zip_longest(categories,products_count_categorywise))    
      prodphoto = Product.objects.filter(Q(photo__cover_photo_flag='yes')|Q(photo__file=None),status=0).distinct().prefetch_related('photo__set').values('id','name','description','price','created_by','contact','mark_as_sold','photo__file','photo__cover_photo_flag')
      if not category_slug and not query :
         productPagination = createProductPagination(request,prodphoto)

      #Fetching products based on search query
      noItem=''
      if query:
          prodphoto = Product.objects.filter(
              Q(name__icontains=query)|
              Q(description__icontains=query)|
              Q(category__name__icontains=query),Q(photo__cover_photo_flag='yes')|Q(photo__file=None),status=0).distinct().prefetch_related('photo__set').values('id','name','description','price','contact','mark_as_sold','photo__file','photo__cover_photo_flag')

          productPagination = createProductPagination(request,prodphoto)
      if category_slug:
        print('category_slug::'+str(category_slug))  
        category = get_object_or_404(Category, slug = category_slug)
        prodphoto = Product.objects.filter(Q(photo__cover_photo_flag='yes')|Q(photo__file=None),category = category,status=0).prefetch_related('photo__set').values('id','name','description','price','contact','mark_as_sold','photo__file','photo__cover_photo_flag')

        productPagination = createProductPagination(request,prodphoto)
      
      return render(request,'olx/product/list.html',{'category':category,'categoriesWithProductsCount':categoriesWithProductsCount,'productPagination':productPagination,'noItem':noItem})     
 #============================================================================================================       


class ProgressBarUploadView(View):

    cover_photo = True
    save_created_product = False
    
    def post(self, request):
        request.session['user_has_uploaded_photo'] = True
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        
        form = PhotoTempForm(self.request.POST, self.request.FILES)
        #form will be valid on uploading any type of file later before saving that file will check type of that file
        if form.is_valid():
            photoTemp = form.save(commit=False)
            
            photoTemp.photo_type = 'product'#photo_type can be 'profile' also going forward
            info = ''
            if not photoTemp.file.url.lower().endswith(('.png', '.jpg', '.jpeg','gif')):
                info = 'This file format is not supported, upload jpg,jpeg,gif,png image format'
                '''else:    
                  if file_extn == 'png':
                  file_to_be_converted = Image.open(photoTemp.file)
                  file_to_rgb = file_to_be_converted.convert('RGBA')
                  file_to_rgb.save(photoTemp.file)
                  file_extn_new = imghdr.what(photoTemp.file)
                  print("file_extn_new::"+str(file_extn_new))'''
                data={'info':info}  
            else:
                  photoTemp.uploaded_by_id = request.user.id      
                  photoTemp.save()#This will permanently save the data
                  #logic for fetchng last record id
                  last_record = PhotoTemp.objects.first()
                  print("last_record.id:::"+str(last_record.id))
                  data = {'is_valid': True,'id':last_record.id, 'name': photoTemp.file.name, 'url': photoTemp.file.url}
                
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
#============================================================================================================
def deleteUploadedPhoto(request):
    if request.method == 'GET':
       if request.path == '/olx/deletePhoto/':#when deleted from Add Post screen
           try:
              photo_id = request.GET['photo_id']
              print('photo_id::'+str(photo_id))
              PhotoTemp.objects.filter(id=photo_id,uploaded_by_id=request.user.id).delete()
              return HttpResponse("success")
           except ConnectionAbortedError:
              print("exception raised")    
       elif request.path == '/olx/deletePhotoFromEdit/':#when deleted from edit product screen
               
        
            selected_photo = request.GET.getlist('favorite[]')
            print("selelcted_phtot"+str(selected_photo))
            for photoId in selected_photo:
                print("photoId:::"+str(photoId))
                if '-uploaded' not in photoId: 
                    photo = Photo.objects.filter(id=photoId,uploaded_by_id=request.user.id)
                    if photo:
                       photo.delete()
                else:
                    print("delting from photoTemp table")
                    photoId_extr = photoId.split('-')[0]
                    photoTemp = PhotoTemp.objects.filter(id=int(photoId_extr),uploaded_by_id=request.user.id)    
                    if photoTemp:
                        photoTemp.delete()
                 
            return HttpResponse("success")
    else:

        return HttpResponse("photo not deleted")
def myPost(request):
    productPagination = myPostData(request)#createProductPagination(request,products,photos)
    return render(request,'olx/product/myPost.html',{'productPagination':productPagination})    
def myPostData(request):
    prodphoto = Product.objects.filter(Q(photo__cover_photo_flag='yes')|Q(photo__file=None)).distinct().prefetch_related('photo__set').values('id','name','description','price','contact','status','mark_as_sold','created_by','photo__file','photo__cover_photo_flag')

    
    productPagination = createProductPagination(request,prodphoto)
    return productPagination;    
def activateAndDeactivatePost(request): 
    photo_reference_id = request.GET['photo_reference_id']
    print("photo_reference_id::"+str(photo_reference_id))
    product = Product.objects.get(id=int(photo_reference_id))
    photos = Photo.objects.all().filter(reference_id=product, uploaded_by_id=request.user.id)
    if product.status == 0:
       product.status = 1 #making product inactive
       product.save()
       for photo in photos:
           photo.status = 1 # making photo inactive
           photo.save()
    elif product.status == 1:
         product.status = 0 #making product active
         product.save()
         for photo in photos:
           photo.status = 0 # making photo active
           photo.save()  
    productPagination = myPostData(request)       
    return render(request,'olx/product/myPostAjax.html',{'productPagination':productPagination}) 
def markAsSold(request):
    mark_as_sold_id = request.GET['mark_as_sold_id']
    print("mark as sold photo_reference_id::"+str(mark_as_sold_id))
    product = Product.objects.get(id=int(mark_as_sold_id))
    if product.mark_as_sold == 0:
       product.mark_as_sold = 1 #making product as sold
       product.save()   
    productPagination = myPostData(request)       
    return render(request,'olx/product/myPostAjax.html',{'productPagination':productPagination})             
class UpdateProduct(UpdateView):
      model = Product
      #fields = ['name','description','price']
      pk_url_kwarg = 'pk'
      form_class = ProductForm
      template_name = 'olx/product/update_product.html'
      context_object_name = 'photo_list'
      
      
      #success_url = 'olx/myPost'
      def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        print("pkkkk66kkkk:"+str(self.kwargs.get(self.pk_url_kwarg)))
        reference_id = self.kwargs.get(self.pk_url_kwarg)
        context['photo_list'] = Photo.objects.all().filter(reference_id=reference_id,uploaded_by_id=self.request.user.id)
        #If user uploads the photo during edit and by mistake refreshes the page, delete those uploaded photos
        PhotoTemp.objects.filter(uploaded_by_id=self.request.user.id).delete()

        return context
      
      def form_valid(self, form):
    
          self.object = form.save(commit=False)
          reference_id = self.kwargs.get(self.pk_url_kwarg)
          print("reference_id-->"+str(reference_id))
          cover_photo_id_edit=self.request.POST.get('photoSelected')
          print('cover_photo_id:::'+str(cover_photo_id_edit))
          
         
          

          if  cover_photo_id_edit and '-uploaded' not in cover_photo_id_edit:
               avl_cover_photo_id = Photo.objects.all().filter(cover_photo_flag='yes',uploaded_by_id=self.request.user.id,reference_id=reference_id)[0]
               if avl_cover_photo_id.id == int(cover_photo_id_edit):
                   pass
               else:
                   avl_cover_photo_id.cover_photo_flag = 0
                   avl_cover_photo_id.save()
                   photo_to_set_cpf = Photo.objects.get(id=int(cover_photo_id_edit))
                   photo_to_set_cpf.cover_photo_flag='yes'
                   photo_to_set_cpf.save()
                   
               all_photos_from_PhotoTemp = PhotoTemp.objects.all().filter(uploaded_by_id=self.request.user.id).order_by("id")
               if all_photos_from_PhotoTemp.count() >0:
                    product = Product.objects.get(id=reference_id)
                    for item in all_photos_from_PhotoTemp:
                         Photo.objects.create(reference_id=product,photo_type=item.photo_type,uploaded_at=item.uploaded_at,file=item.file,uploaded_by_id = item.uploaded_by_id).save()
 
          elif cover_photo_id_edit:
              #extract int part from id
              cover_photo_id_extr = cover_photo_id_edit.split('-')[0]
              product = Product.objects.get(id=reference_id)
              all_photos_from_PhotoTemp = PhotoTemp.objects.all().filter(uploaded_by_id=self.request.user.id).order_by("id")
              for item in all_photos_from_PhotoTemp:
                  print("item.id:**"+str(item.id))
                  if item.id == int(cover_photo_id_extr):
                     print("item.id:::"+str(item.id))
                     #changing cover photo
                     #get already avl cover_photo
                     if Photo.objects.all().filter(uploaded_by_id=self.request.user.id,reference_id=reference_id).exists():
                        avl_cover_photo_id = Photo.objects.all().filter(cover_photo_flag='yes',uploaded_by_id=self.request.user.id,reference_id=reference_id)[0]
                        avl_cover_photo_id.cover_photo_flag = 0
                        avl_cover_photo_id.save()  
                     Photo.objects.create(reference_id=product,cover_photo_flag='yes',photo_type=item.photo_type,uploaded_at=item.uploaded_at,file=item.file,uploaded_by_id = item.uploaded_by_id).save()
                  else:
                     Photo.objects.create(reference_id=product,photo_type=item.photo_type,uploaded_at=item.uploaded_at,file=item.file,uploaded_by_id = item.uploaded_by_id).save()

        

          self.object.save()
          #return super().form_valid(form)
          PhotoTemp.objects.filter(uploaded_by_id=self.request.user.id).delete()
          return HttpResponseRedirect(reverse('olx:my_all_post'))

def index(request):
    return render(request,'olx/login.html')
def  checkLogin(request):     
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,username=username, password=password)
            if user is not None:
            # A backend authenticated the credentials
               login(request,user)#This method is required to add the logged in user to the current session by default Anonymous user will be added
               print('going inside authentication: '+str(request.user.username))
               #From here I am setting some session attributes(03-04-2019)
               request.session['create_product'] = False
               request.session['save_product'] = False
               request.session['product_and_photo_saved'] = True
               request.session['user_has_uploaded_photo'] = False
               request.session['product_details_entered'] = False

               request.session.set_expiry(0)
               return HttpResponseRedirect(reverse('olx:product_list'))
            else:
            # No backend authenticated the credentials
               return render(request, 'olx/login.html', {
           
            'error_message_2': "You entered wrong credentials.",
            })
               

def  logoutFromApp(request):
       logout(request)#Note logout well erase session data
       return render(request, 'olx/login.html')

#Later will use generic views to reduce the code    


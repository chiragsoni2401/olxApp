

  

from django.db import models
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.dispatch import receiver

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 200, db_index = True)
    slug = models.SlugField(max_length = 200, db_index = True, unique = True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        print('inside get_absolute_url')
        return reverse('olx:product_list_by_category', args=[self.slug])  
        #return reverse('olx:product_list') 


class Product(models.Model):
    category = models.ForeignKey(Category ,on_delete=models.CASCADE)
    name = models.CharField(max_length = 200, db_index = True)
    slug = models.SlugField(max_length = 200, db_index = True)     
    """image = models.ImageField( blank = True,width_field="width_field",height_field="height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)"""
    description = models.TextField(blank = True)    
    price = models.DecimalField(max_digits = 10, decimal_places = 2 )#Not used FloatField to avoid rounding issues
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    contact= models.BigIntegerField(default=None,blank=True, null=True)
    created_by = models.CharField(max_length = 200, default=None,blank=True, null=True)
    #created_by = models.CharField(max_length = 200, default=None, blank=True, null=True)
    uploaded_by_id = models.IntegerField(default=0)
    status = models.IntegerField(default=0) # 0-->Active,1-->Inactive
    mark_as_sold = models.IntegerField(default=0) # 0-->not sold,1-->sold

    def get_absolute_url(self):
        return reverse('olx:edit_product', kwargs={'pk': self.pk})



    class Meta:
        ordering = ('-created',)
        index_together = (('id','slug'),)# we want to query product by id and slug using together index to improve performance

    def __str__(self):
        return self.name

    #def get_absolute_url(self):
     #   return reverse('olx:product_detail', args=[self.id, self.slug])  

class Photo(models.Model):
  
    #title = models.CharField(max_length=255, blank=True)
    reference_id = models.ForeignKey(Product, null=True,on_delete=models.CASCADE) 
    photo_type = models.CharField(max_length = 70, db_index = True)
    file = models.FileField(upload_to='photos/',default='NoImage.jpg')
    """
    image = models.ImageField( blank = True,width_field="width_field",height_field="height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    """
    cover_photo_flag = models.CharField(default=0,max_length = 5, db_index = True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by_id = models.IntegerField(default=0)
    status = models.IntegerField(default=0) # 0-->Active,1-->Inactive

    

    class Meta:
        ordering = ('-uploaded_at',)

class PhotoTemp(models.Model):
  
    #title = models.CharField(max_length=255, blank=True)
    reference_id = models.IntegerField(default=0) 
    photo_type = models.CharField(max_length = 70, db_index = True)
    file = models.FileField(upload_to='photos/',default='NoImage.jpg')
    """
    image = models.ImageField( blank = True,width_field="width_field",height_field="height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    """
    cover_photo_flag = models.CharField(default=0,max_length = 5, db_index = True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by_id = models.IntegerField(default=0)


    class Meta:
        ordering = ('-uploaded_at',)    

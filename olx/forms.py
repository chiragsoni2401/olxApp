from django import forms

from .models import Product,Category,Photo,PhotoTemp

#Model form for Product model
class ProductForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Product Name','name':'product-name'})) 
    category = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'form-control','selected':'Select Product Category','name':'product-category'}),queryset=Category.objects.all())
    description = forms.CharField(widget=forms.Textarea(attrs={'cols':15,'rows':3,'class':'form-control','placeholder':'Product Description','name':'product-description'})) 
 
    price =forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Product Price','name':'product-price'}))
    contact =forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Provide your contact no','name':'poster-contact'}))
    
    # this function will be used for the validation 
    def clean(self): 
  
        # data from the form is fetched using super function 
        super(ProductForm, self).clean() 
        print("calling clean funciotn ")  
        # extract the username and text field from the data 
        productName = self.cleaned_data.get('name') 
        description = self.cleaned_data.get('description')
        price = self.cleaned_data.get('price')
        contact = self.cleaned_data.get('contact') 
        print("productName:::"+str(productName)+" product name type: "+str(type(productName)))
        print("description:::"+str(description))
  
        # conditions to be met for the username length 
        if len(productName) > 23: 
            self._errors['name'] = self.error_class([ 
                'Product name is too lengthy'])
        if productName.isdigit(): 
            self._errors['name'] = self.error_class([ 
                'Product name is not valid'])         
        if len(description) <10: 
            self._errors['description'] = self.error_class([ 
                'Post Should Contain minimum 10 characters']) 

        if price <=0 or type(price) is str: 
            self._errors['price'] = self.error_class([ 
                'Invalid price'])         
  
        # return any errors if found 
        return self.cleaned_data 


    class Meta:
        model = Product
        #fields = ('name','category', 'image','description','price')
        fields = ('name','category','description','price','contact')

#Model form for Photo model
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file', )

#Model form for Photo model
class PhotoTempForm(forms.ModelForm):
    class Meta:
        model = PhotoTemp
        fields = ('file', )        
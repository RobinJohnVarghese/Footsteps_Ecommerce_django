from django.db import models
from django.urls import reverse
# from footsteps.adminside.new_var import new_var


# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
            return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
    
    
class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True,null=True)
    real_price = models.IntegerField()
    price           = models.IntegerField(null=False)
    images          = models.ImageField(upload_to='photos/products')
    # stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def __str__(self):
        return self.product_name
    

# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='photos/product_images')

#     def _str_(self):
#         if self.product:
#             return f"Product:{self.product.product_name}, {self.product.category}"
#         else:
#             return "Product: N/A"

# class VariationManager(models.Manager):
#     def colors(self):
#         return super(VariationManager, self).filter(variation_category='color', is_active=True)

#     def sizes(self):
#         return super(VariationManager, self).filter(variation_category='size', is_active=True)

    
# variation_category_choice = (
#     ('color', 'color'),
#     ('size', 'size'),
# )
       
# class Variation(models.Model):
#     # Category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     variation_category = models.CharField(max_length=100, choices=variation_category_choice)
#     variation_value     = models.CharField(max_length=100)
#     is_active           = models.BooleanField(default=True)
#     created_date        = models.DateTimeField(auto_now=True)

#     objects = VariationManager()
    

#     def __unicode__(self):
#         return self.product
    
class ColorVariant(models.Model):
	product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
	color = models.CharField(max_length=50)
	def __str__(self):
		return str(f'{self.product_id} ,{self.color}')

class SizeVariant(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    Color_id = models.ForeignKey(ColorVariant, on_delete=models.CASCADE)
    size = models.CharField(max_length=50)
    real_price = models.IntegerField()
    price = models.IntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return f'{self.Color_id}, {self.size}, {self.price}, {self.stock}'
    
    
class Offer(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    end_date = models.DateField()
    
    def expiry_date(self):
        return str(self.end_date)
    
    
    
    

    

 
    
    
    
 
 
    
 


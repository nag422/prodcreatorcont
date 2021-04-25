from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user_ptr = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    content = models.TextField() 
    address = models.CharField(max_length=300,blank=True)
    postalcode = models.CharField(max_length=100,blank=True)
    city = models.CharField(max_length=100,blank=True)
    country = models.CharField(max_length=100,blank=True)
    phone = models.CharField(max_length=100,blank=True)
    

    def __str__(self):
        return self.content

class Books(models.Model):
    # Example model only
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=True)
    genre = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100)
    count = models.IntegerField(null=True, default=0)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    def __str__(self):
        return self.title

class Product(models.Model):
    author = models.IntegerField(null = True, default =0)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='images/', default='images/default.png')
    thumbnail1 = models.ImageField(upload_to='images/', default='images/default.png')
    thumbnail2 = models.ImageField(upload_to='images/', default='images/default.png')
    thumbnail3 = models.ImageField(upload_to='images/', default='images/default.png')
    videofile =  models.FileField(upload_to='uploads/')
    rights = models.TextField(blank=True)
    castncrew = models.TextField(blank=True)
    price = models.IntegerField(null = True, default =0)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     verbose_name_plural = 'Products'
    #     ordering = ('-created',)

    # def get_absolute_url(self):
    #     return reverse('store:product_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Content(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    rights = models.TextField(blank=True)

    category = models.TextField(blank=True)
    language = models.TextField(blank=True)
    genre = models.TextField(blank=True)
    keywords = models.TextField(blank=True)
    country = models.TextField(blank=True)
    rightsregion = models.TextField(blank=True)
    termsconditions = models.TextField(blank=True)
    runtime = models.TextField(blank=True)
    numbofvideos = models.TextField(blank=True)

    thumbnail = models.ImageField(upload_to='images/', default='images/default.png')
    videofile =  models.FileField(upload_to='uploads/')
    thumbnail1 = models.ImageField(upload_to='images/', default='images/default.png')
    thumbnail2 = models.ImageField(upload_to='images/', default='images/default.png')
    thumbnail3 = models.ImageField(upload_to='images/', default='images/default.png')

    # rights = models.TextField(blank=True)
    # castncrew = models.TextField(blank=True)

    price = models.IntegerField(null = True, default =0)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     verbose_name_plural = 'Products'
    #     ordering = ('-created',)

    # def get_absolute_url(self):
    #     return reverse('store:product_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


    def num_likes(self):
        return self.likedproducts_set.all()    

    def withcontent(self):
        return self.boughtedproducts_set.all()    

    def __str__(self):
        return self.title

class ContentSaveNotifyer(models.Model):
    user = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    sendertype = models.CharField(max_length=255)
    receivertype = models.CharField(max_length=255)
    isviewed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.sender

class ContentNotifyerperuser(models.Model):
    notification = models.ForeignKey(ContentSaveNotifyer, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=255)    
    isviewed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.receiver

class ProductRequest(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)    
    title = models.CharField(max_length=255)    
    category = models.CharField(max_length=255)
    authortype = models.CharField(max_length=255)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     verbose_name_plural = 'Products'
    #     ordering = ('-created',)

    # def get_absolute_url(self):
    #     return reverse('store:product_detail', args=[self.slug])

    

    def __str__(self):
        return self.title

# @receiver(post_save, sender=User)
# def user_is_created(sender, instance, created, **kwargs):
#     try:
#         if created:
#             Profile.objects.create(user_ptr=instance)
#         else:
#             instance.profile.save()
#     except Exception as e:
#         print('instance erro',e)

class ProductGroup(models.Model):
    id=models.AutoField(primary_key=True)
    groupname = models.CharField(max_length=255)
    rule = models.CharField(max_length=255)
    products=models.ManyToManyField(Content, blank=True, related_name='products')
    
    def get_products(self):
        return self.products.all()
    def num_products(self):
        return self.products.all().count()        

    def __str__(self):
        return self.groupname

class AssignedUsersGroup(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.CharField(max_length=255)
    groupid = models.CharField(max_length=255)
    def __str__(self):
        return self.user


class Likedproducts(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Content, on_delete=models.CASCADE)    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}-{self.post}-{self.updated}"

class Boughtedproducts(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Content, on_delete=models.CASCADE)    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


       
    
    def __str__(self):
        return f"{self.user}-{self.post}-{self.updated}"

class ProductAssigns(models.Model):
    users=models.ManyToManyField(User, blank=True, related_name='user')
    products=models.ForeignKey(Content, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.users}--{self.products}"

class MessageInbox(models.Model):
    sender=models.ForeignKey(User, blank=True, related_name='sender', on_delete=models.CASCADE)
    msg=models.TextField()
    category=models.CharField(max_length=255,blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender}"

class ChatMessages(models.Model):
    
    sender = models.CharField(max_length=255,blank=True)
    receiver = models.CharField(max_length=255,blank=True)
    sendertype = models.CharField(max_length=255,blank=True)
    receivertype = models.CharField(max_length=255,blank=True)    
    isgrouped = models.CharField(max_length=255,blank=True)
    msg=models.TextField()
    category=models.CharField(max_length=255,blank=True)    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender}"

class MessageChatter(models.Model):
    
    sender = models.CharField(max_length=255,blank=True)
    receiver = models.CharField(max_length=255,blank=True)
    sendertype = models.CharField(max_length=255,blank=True)
    receivertype = models.CharField(max_length=255,blank=True)    
    isgrouped = models.CharField(max_length=255,blank=True)
    msg=models.TextField()
    msgtype=models.CharField(max_length=255,blank=True)
    category=models.CharField(max_length=255,blank=True)    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender}"
    

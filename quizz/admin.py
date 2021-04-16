from django.contrib import admin
from . import models
from quizz.models import (Profile,Books,Product,ProductAssigns,
Content,ProductRequest,ProductGroup,Likedproducts,Boughtedproducts,AssignedUsersGroup,MessageInbox)

admin.site.register(Profile)
admin.site.register(ProductGroup)
admin.site.register(ProductRequest)
admin.site.register(Likedproducts)
admin.site.register(Boughtedproducts)
admin.site.register(AssignedUsersGroup)
admin.site.register(ProductAssigns)
admin.site.register(MessageInbox)



@admin.register(models.Books)
class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',),}

@admin.register(models.Product)
class ProductAdminn(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',),}

@admin.register(models.Content)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',),}



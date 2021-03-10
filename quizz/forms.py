from django import forms
from .models import Books,Product,Content,ProductRequest,Profile,ProductGroup,AssignedUsersGroup

# forms.form
class AddForm(forms.ModelForm):

    class Meta:
        model = Books
        fields = ('title', 'genre', 'author', 'isbn')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):

    class Meta:
        model = Content
        fields = '__all__'

class ProductRequestForm(forms.ModelForm):
    class Meta:
        model = ProductRequest
        fields = '__all__'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class GroupForm(forms.ModelForm):
    class Meta:
        model = ProductGroup
        fields = '__all__'

class AssignedGroupForm(forms.ModelForm):
    class Meta:
        model = AssignedUsersGroup
        fields = '__all__'


       
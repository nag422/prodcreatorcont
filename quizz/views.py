from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import Profile,Books,Content,ProductGroup,Likedproducts,Boughtedproducts,AssignedUsersGroup
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView,RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView,CreateView,UpdateView
from django.db.models import F
from django.utils import timezone
from .forms import AddForm,ProductForm,ProductRequestForm,GroupForm
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect,csrf_exempt
import json
from authentication.utils import DatabaseDynamic

import uuid

def get_random_code():
    code = str(uuid.uuid4())[:8].replace('-', '').lower()
   
    return code


def quiz(request):
    return render(request,'base.html')
def profile(request):
    data = Profile.objects.all()
    for i in data:
        print(i.user_ptr.is_active)
    context = {
        'data':'i.content'
    }
    return JsonResponse(context)

class Ex2View(TemplateView):
    template_name = "1templateview.html"
    # template_engine = ""
    # get_context_data(**kwargs) is method inherited from ContextMixin

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = Books.objects.all()
        # context['title'] = str(*args['id'])
        print('imhere')
        print(self.request.GET.get('id'))  ##### Working Here
        return context

class SinglePostView(RedirectView):
    url="http://youtube.com/pyplane"
            
class PostPreLoadTaskView(RedirectView):

    # url="http://youtube.com/veryacademy"

    # OR
    
    pattern_name ='quizz:singlepost'

    # Permanent = Http status code returned

    def get_redirect_url(self, *args, **kwargs):
        # Updating page count of a page visited
        # get_object_or_404(post,pk=kwargs['pk'])
        # .save()

        #  OR

        # filter,update
        
        # count = F('count') + 1
        count =0
        print(count)

        return super().get_redirect_url(*args, **kwargs)
# DetailView nosupports pagination, noform,no return update delete
class BookDetailView(DetailView):
    model = Books
    # upto now is enough if placed templatefile here quizz/books_detail.html

    # overriting
    template_name = 'book-detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = Books.objects.filter(slug=self.kwargs.get('slug'))
        post.update(count=F('count')+1)
        context['time'] = timezone.now()
        return context
        # refer django singleobjectmixin for this view


# listview supports pagination, but noform,no return update delete

class BookListView(ListView):
    model = Books
    template_name = "home.html"
    context_object_name = "books"
    paginate_by = 2
    # upto here is enough
    # queryset = Books.objects.all()[:2]

    def get_queryset(self, *args, **kwargs):
        # return Books.objects.all()[:2]
        return Books.objects.filter(genre__icontains=self.kwargs.get('genre'))
# Multipleobjectmixin

# Formview not displaying a form page, saving data to a database

class AddBookView(FormView):
    template_name = 'add.html'
    form_class = AddForm
    success_url = '/g/add/form/'
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
# formmixin

# Createview dont supplort forms

class AddBookViewcreate(CreateView):
    model = Books
    form_class = AddForm
    # we can use initial

    # fields = ['title']

    template_name = 'add.html'
    success_url = '/g/add/form/'
    # the below get_initial is optional 
    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        initial['title'] = 'Enter Title'
        return initial
# form saves automatically without extracode
class AddEditView(UpdateView):
    model = Books
    form_class = AddForm
    template_name = 'add.html'
    success_url = '/books/'
# in update view get_object rertrieves the data
# in createview get_object = None

def movieplex(request):
    return render(request,'index.html')

'''
# Context processor
# get_absolute_url()
# Multiple Model Managers (get_query_set)

'''

def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty= producty_qty)

        basketqty = basket.__len__()
        response = JsonResponse({'qty':basketqty})
        return response

def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response


# Product Save
@csrf_exempt
def save_product(request):
    message = ''
    status = ''
    error = ''
    from django.template.defaultfilters import slugify
    request.POST._mutable = True
    user_ptr = get_object_or_404(User, id=1)
    if request.method == 'POST':
        slug = slugify(request.POST.get('title'))
        request.POST.update(author=user_ptr,slug=slug)
        ProductFormResponse = ProductForm(request.POST,request.FILES)
                
        # title = request.POST.get('title')
        # slug = request.POST.get('title')
        # description = request.POST.get('description')
        # thumbnail = request.FILES['thumbnail']
        # videofile =  request.FILES['videofile']
        # rights = request.POST.get('rights')
        # castncrew = request.POST.get('castncrew')
        # price = int(request.POST.get('price'))
        
        
        if ProductFormResponse.is_valid():
            ProductFormResponse.save()
            message = "Successfully saved"
            status= 200
            return JsonResponse({'message':message,'status':status,'error':error})
        else:
            message = "Something Went Wrong or Check with your data"
            status= 400
            print(ProductFormResponse.errors)
            return JsonResponse({'message':message,'status':status,'error':error})
    else:
        status= 403
        message = "Method is not Allowed"
        
        return JsonResponse({'message':message,'status':status,'error':error})

@csrf_exempt
def requestsaveproduct(request):
    message = ''
    status = ''
    error = ''
    request.POST._mutable = True
    user_ptr = get_object_or_404(User, id=1)
    if request.method == 'POST':
        request.POST.update(author=user_ptr)
        ProductFormResponse = ProductRequestForm(request.POST)
        
        if ProductFormResponse.is_valid():
            ProductFormResponse.save()
            message = "Successfully saved"
            status= 200
            return JsonResponse({'message':message,'status':status,'error':error})
        else:
            message = "Something Went Wrong or Check with your data"
            status= 400
            print(ProductFormResponse.errors)
            return JsonResponse({'message':message,'status':status,'error':error})
    else:
        status= 403
        message = "Method is not Allowed"
        
        return JsonResponse({'message':message,'status':status,'error':error})

@csrf_exempt
def getProductsall(request):
    product = []
    error=False,
    status=200
    allobjects = (Content.objects.all().values())

    
    for i in allobjects:
        dt = Likedproducts.objects.filter(post=i['id']).exists()
        df = Boughtedproducts.objects.filter(post=i['id']).exists()
        
        i['isliked'] = dt
        i['isfavored'] = df
        product.append(i)
    
    response = {
        'obs':(product),
        'status':200,
        'error':error
    }
    return JsonResponse(response)

@csrf_exempt
def getProductsallliked(request):
    product = []
    error=False,
    status=200
    allobjects = (Likedproducts.objects.all())

    
    for i in allobjects.values():        
        df = Content.objects.filter(id=i['post_id'])
        for every in df.values():
            product.append(every)
    
    response = {
        'obs':(product),
        'status':200,
        'error':error
    }
    return JsonResponse(response)

@csrf_exempt
def getProductsallbagged(request):
    product = []
    error=False,
    status=200
    allobjects = (Boughtedproducts.objects.all())

    
    for i in allobjects.values():        
        df = Content.objects.filter(id=i['post_id'])
        for every in df.values():
            product.append(every)


    response = {
        'obs':(product),
        'status':200,
        'error':error
    }
    return JsonResponse(response)

@csrf_exempt
def createGroup(request):
    group = []
    error =False
    message=''
    status=200
    dataresp = request.POST

    form = GroupForm(dataresp)
    if form.is_valid:
        # instance = form.save(commit=False)
        # grp = ProductGroup(groupname=dataresp['groupname'],rule=dataresp['rule'])
        # grp.save()
        databaseDynamic = DatabaseDynamic(request)
        
        grplastid = ProductGroup.objects.last()

        if grplastid is not None:
            primaryid = grplastid.id + 1
        else:
            primaryid = 1
        
        
        thisdict = {'groupname':dataresp['groupname'],'rule':dataresp['rule'],'id':primaryid}
        groupid = databaseDynamic.insertrecordtodb(catname='quizz_productgroup',thisdict=thisdict)
        if (groupid):
            status = 200
        else:
            status = 400
        

    response = {
        'error':error,
        'message':message,
        'status':status
    }
    return JsonResponse(response)

    

@csrf_exempt
def assignedtogroup(request):
    group = []
    error =False
    message=''
    status=0
    dataresp = request.POST

    itemlist = (request.POST.get('itemlist')).split(',')    
    if itemlist is not None:
        for items in itemlist:
            try:
                AssignedUsersGroup.objects.get(user=int(items),groupid=dataresp.get('groupname')).delete()
            except Exception as e:
                if item is not None and dataresp.get('groupname') is not None:

                    AssignedUsersGroup(user=int(items),groupid=dataresp.get('groupname')).save()

                    message = 'Success'
                    status=200

                message = 'Failed'
                status=400
            
            

    
    
        
            
            
    else:
        error =True
        message = 'Something is went wrong'
        status=400        

        

    response = {
        'error':error,
        'message':message,
        'status':status
    }
    return JsonResponse(response)

@csrf_exempt
def getAllgroups(request):
    groups = []
    error =False
    message=''
    status=200

    grps = ProductGroup.objects.all()

    for every in grps.values():
        # every['_id'] = str(every['_id'])
        groups.append(every)

    context = {
        'error' : False,
        'message':'Successfully groups loaded',
        'status':200,
        'groups':groups
    }
    return JsonResponse(context)

@csrf_exempt
def addliketoproduct(request):
    postid = request.POST.get('id')
    status = 200
    message = ""
    
    try:
        dt = Likedproducts.objects.filter(post=int(postid)).first()
        dt.delete()
        message = "unliked"
    except:
        Likedproducts.objects.create(post=Content.objects.get(id=int(postid)),user=User.objects.get(id=1))
        message = "liked"
    context = {
        'status':status,
        'message':message
    }
    
    return JsonResponse(context)


@csrf_exempt
def addboughtproduct(request):
    postid = request.POST.get('id')
    status = 200
    message = ""
    
    try:
        dt = Boughtedproducts.objects.filter(post=int(postid)).first()
        dt.delete()
        message = "removedbuy"
    except:
        Boughtedproducts.objects.create(post=Content.objects.get(id=int(postid)),user=User.objects.get(id=1))
        message = "addedbuy"
    context = {
        'status':status,
        'message':message
    }
    
    return JsonResponse(context)

@csrf_exempt
def productstatus(request):
    postid = request.POST.get('id')
    action = request.POST.get('action')
    status = 200
    message = ""
    error = ""
    print(postid,action)
    try:
        instance = Content.objects.get(id=int(postid))
        if action == 'instock':
            instance.in_stock = False if instance.in_stock else True
            instance.save()
            print('saved')
            
        elif action == 'isactive':    
            instance.is_active = False if instance.is_active else True
            isactive = instance.save()
    except Exception as e:
        status = 400
        message = "Something is Went Wrong"
        error = str(e)
        print(e)

        
    context = {
        'status':status,
        'message':message,
        'error':error
    }        
    return JsonResponse(context)        




@csrf_exempt
def getProductswithlikes(request):
    dos = []
    dt =""
    val = Content.objects.all()
    
    for i in val.values():
        try:
            dt = Likedproducts.objects.filter(post=i['id']).first()
            print(dt.id)
        except:
            print('someork')
         
    return HttpResponse('done') 


    
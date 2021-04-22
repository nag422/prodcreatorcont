from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.middleware.csrf import get_token
from quizz.models import Profile,Books,Content,ProductGroup,Likedproducts,Boughtedproducts,AssignedUsersGroup,ProductAssigns,MessageInbox
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView,RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView,CreateView,UpdateView
from django.db.models import F
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import AddForm,ProductForm,ProductRequestForm,GroupForm,MessageInboxForm
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect,csrf_exempt
import json
from authentication.utils import DatabaseDynamic
from .serializers import ProductsSerializer,ProductAssignsSerializer,ProductGroupSerializer,MessageInboxSerializer
from authentication.serializers import CustomUserSerializer
import uuid
from rest_framework.decorators import api_view, schema,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response

def get_random_code():
    code = str(uuid.uuid4())[:8].replace('-', '').lower()   
    return code
@ensure_csrf_cookie
def get_csrf(request):
    response = JsonResponse({"Info": "Success - Set CSRF cookie"})
    response["X-CSRFToken"] = get_token(request)
    return response


def quiz(request):
    return render(request,'index.html')
    
    
def profile(request):
    data = Profile.objects.all()
    for i in data:
        print(i.user_ptr.is_active)
    context = {
        'data':'i.content'
    }
    # return JsonResponse(context)
    return render(request,'index.html')

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def dashboardView(request):
    sellers = 0
    buyers=0
    enquiries=0
    leads=0
    error=""
    try:
        sellers = Profile.objects.filter(content="creator").count()    
        buyers = Profile.objects.filter(content="producer").count()  
        enquiries = MessageInbox.objects.all().count()
        leads = 0
    except Exception as e:
        error = str(e)

    context = {
        'sellers':sellers,
        'buyers':buyers,
        'enquiries':enquiries,
        'leads':leads,
        'error':error


    }
    # return JsonResponse(context)
    return Response(context)


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
@ensure_csrf_cookie
def movieplex(request):
    return render(request,'index.html')


def movieplex2(request):
    print(request.POST)
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


# Backend
# Product Save


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def test_case(request):
    message = request.user.username
    status = 200
    error = False
    return Response({'message':message,'status':status,'error':error})


@api_view(['POST'])
@permission_classes([AllowAny,])
def save_product(request):
    message = ''
    status = ''
    error = ''
    from django.template.defaultfilters import slugify
    request.POST._mutable = True
    user_ptr = get_object_or_404(User, id=request.user.id)
    print('trigged productsave')
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
            return Response({'message':message,'status':status,'error':error})
        else:
            message = "Something Went Wrong or Check with your data"
            status= 400
            print(ProductFormResponse.errors)
            return Response({'message':message,'status':status,'error':error})

    else:
        status= 403
        message = "Method is not Allowed"
        
        return Response({'message':message,'status':status,'error':error})

@api_view(['POST'])
@permission_classes([AllowAny,])
def editProductSave(request):
    message = ''
    status = ''
    error = ''

    from django.template.defaultfilters import slugify
    request.POST._mutable = True
    user_ptr = get_object_or_404(User, id=request.user.id)


    if request.method == "POST":
        slug = slugify(request.POST.get('title'))
        request.POST.update(author=user_ptr,slug=slug)
        instance = Content.objects.get(id=int(39))
        ProductFormResponse = ProductForm(request.POST or None,request.FILES or None, instance=instance)

        print((request.FILES))

        if ProductFormResponse.is_valid():
            ProductFormResponse.save()
            message = "Successfully saved"
            status= 200
            return Response({'message':message,'status':status,'error':error})
        else:
            message = "Something Went Wrong or Check with your data"
            status= 400
            print(ProductFormResponse.errors)
            return Response({'message':message,'status':status,'error':error})
    
    else:
        status= 403
        message = "Method is not Allowed"
        
        return Response({'message':message,'status':status,'error':error})

@csrf_exempt
@api_view(['GET','POST'])
# @ Buyer Accept
def requestsaveproduct(request):
    message = ''
    status = ''
    error = ''
    request.POST._mutable = True
    user_ptr = get_object_or_404(User, id=request.user.id)
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
    try:
        pageno = request.GET['page']
        
    except:
        pageno = 0
    # allobjects = Content.objects.filter(is_active=True)[int(pageno):2]
    allobjects = Content.objects.filter(is_active=True)
    
    
    for i in allobjects.values():
        dt = Likedproducts.objects.filter(post=i['id']).exists()
        df = Boughtedproducts.objects.filter(post=i['id']).exists()
        
        i['isliked'] = dt
        i['isfavored'] = df
        i['customauthor'] = (User.objects.get(pk=i['author_id']).username).capitalize()
        
        product.append(i)
    
    response = {
        'obs':(product),
        'status':200,
        'error':error
    }
    return JsonResponse(response)

@csrf_exempt
# @api_view(['POST'])
# @permission_classes([AllowAny,])
def getProductById(request):
    product = []
    error=False,
    status=200
    try:
        data = json.loads(request.body)        
    except:
        data = {}
    # allobjects = Content.objects.filter(is_active=True)[int(pageno):2]
    allobjects = Content.objects.filter(id=int(data.get('productid')),is_active=True)
    
    
    for i in allobjects.values():
        dt = Likedproducts.objects.filter(post=i['id']).exists()
        df = Boughtedproducts.objects.filter(post=i['id']).exists()
        
        i['isliked'] = dt
        i['isfavored'] = df
        i['customauthor'] = (User.objects.get(pk=i['author_id']).username).capitalize()
        
        product.append(i)
    
    response = {
        'obs':(product),
        'status':200,
        'error':error,
        'user':str(request.user)
    }
    return JsonResponse(response)

@csrf_exempt
def getProductsallbyGroups(request):
    product = []
    error=False,
    status=200

    allobjects = Content.objects.filter(is_active=True).values()

    
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
@api_view(['GET','POST'])
def getProductsallbyUsers(request):
    product = []
    error=False,
    status=200

    groupbyProducts = ProductAssigns.objects.filter(users__in=[int(request.user.id)])
    # print(groupbyProducts.get_products())
    serializer = ProductAssignsSerializer(groupbyProducts,many=True)
    # print(serializer.data)
    for i in serializer.data:
        contentvalues = Content.objects.filter(id=i['products'])
        for j in contentvalues.values():          

            dt = Likedproducts.objects.filter(post=j['id']).exists()
            df = Boughtedproducts.objects.filter(post=j['id']).exists()
            
            j['isliked'] = dt
            j['isfavored'] = df
            product.append(dict(j))
    
    response = {
        'obs':(product),
        'status':200,
        'error':error
    }
    return JsonResponse(response)
# Admin Copy
@csrf_exempt
def getProductsallbyUsersbyid(request):
    product = []
    error=False,
    status=200
    userid = request.GET.get('id')
    pagenumber = request.GET.get('page')

    # df = Content.objects.filter(id=i['post_id'])
    #     for every in df.values():
    
    groupbyProducts = ProductAssigns.objects.filter(users__in=[int(userid)])
    # print(groupbyProducts.get_products())
    serializer = ProductAssignsSerializer(groupbyProducts,many=True)
    # print(serializer.data)
    for i in serializer.data:
        contentvalues = Content.objects.filter(id=i['products'])
        for j in contentvalues.values():          

            dt = Likedproducts.objects.filter(post=j['id']).exists()
            df = Boughtedproducts.objects.filter(post=j['id']).exists()
            
            j['isliked'] = dt
            j['isfavored'] = df
            product.append(dict(j))
    
    response = {
        'obs':(product),
        'status':200,
        'error':error
    }
    return JsonResponse(response)


@csrf_exempt
def getUploadsallbyusersbyid(request):
    product = []
    error=False,
    status=200
    userid = request.GET.get('id')
    pagenumber = request.GET.get('page')

    # df = Content.objects.filter(id=i['post_id'])
    #     for every in df.values():
    
    userUploads = Content.objects.filter(author=int(userid))
    # print(groupbyProducts.get_products())
    serializer = ProductsSerializer(userUploads,many=True)
    # print(serializer.data)
    for i in serializer.data:
        # contentvalues = Content.objects.filter(id=i['products'])
        # for j in contentvalues.values():          

        #     dt = Likedproducts.objects.filter(post=j['id']).exists()
        #     df = Boughtedproducts.objects.filter(post=j['id']).exists()
            
        #     j['isliked'] = dt
        #     j['isfavored'] = df
        product.append(dict(i))
    
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
    allobjects = Likedproducts.objects.all()

    
    for i in allobjects.values():        
        df = Content.objects.filter(id=i['post_id'])
        for every in df.values():
            every['customauthor'] = User.objects.get(id=int(every['author_id'])).username
            every['likedby'] = i['user_id']
            every['likedbyname'] = User.objects.get(id=int(i['user_id'])).username
            product.append(every)
    
    response = {
        'obs':(product),
        'status':200,
        'error':error
    }
    return JsonResponse(response)

# Admin likedproducts
@csrf_exempt
def getProductsalllikedbyuserid(request):
    product = []
    error=False,
    status=200
    userid = request.GET.get('id')
    pagenumber = request.GET.get('page')

    allobjects = Likedproducts.objects.filter(user = int(userid))

    
    for i in allobjects.values():        
        df = Content.objects.filter(id=i['post_id'])
        for every in df.values():
            every['customauthor'] = User.objects.get(id=int(every['author_id'])).username
            every['likedby'] = i['user_id']
            every['likedbyname'] = User.objects.get(id=int(i['user_id'])).username
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
            every['customauthor'] = User.objects.get(id=int(every['author_id'])).username
            every['likedby'] = i['user_id']
            every['likedbyname'] = User.objects.get(id=int(i['user_id'])).username
            product.append(every)


    response = {
        'obs':(product),
        'status':200,
        'error':error
    }
    return JsonResponse(response)

# Admin baggedproducts
@csrf_exempt
def getProductsallbaggedbyuserid(request):
    product = []
    error=False,
    status=200
    userid = request.GET.get('id')
    pagenumber = request.GET.get('page')
    allobjects = (Boughtedproducts.objects.filter(user=int(userid)))

    
    for i in allobjects.values():        
        df = Content.objects.filter(id=i['post_id'])
        for every in df.values():
            every['customauthor'] = User.objects.get(id=int(every['author_id'])).username
            every['likedby'] = i['user_id']
            every['likedbyname'] = User.objects.get(id=int(i['user_id'])).username
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
@api_view(['GET','POST'])
# @ Admin Access
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
                if items is not None and dataresp.get('groupname') is not None:

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
        totalusers = AssignedUsersGroup.objects.filter(groupid=int(every['id'])).count()
        every['users'] = totalusers
        groups.append(every)

    context = {
        'error' : False,
        'message':'Successfully groups loaded',
        'status':200,
        'groups':groups
    }
    return JsonResponse(context)


@csrf_exempt
@api_view(['POST','GET'])
# @ Admin Access
def deleteGroups(request):
    error=False
    message=''
    user_id=''
    itemlist = (request.POST.get('itemlist')).split(',')    
    if itemlist is not None:
        ProductGroup.objects.filter(id__in=itemlist).delete()
    response={
            'error':error,
            'message':message,
            'user_id':user_id
            }
    return JsonResponse(response)

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


@csrf_exempt
def getProductChip(request):
    status = 0
    message = ""
    products =[]
    action = request.POST.get('action').strip()
    if action == "getproduct":
        title = str(request.POST.get('value').strip())
        if len(title) >0:
            
            productinstance = Content.objects.filter(title__icontains = (title))
            
            serializer = ProductsSerializer(productinstance,many=True)
            products = (serializer.data)
            
            status = 200
        else:
            message = True
            status = 400
 
    context = {
        "products":products,
        "message":message,
        "status":status,
        "action":action
    }
    return JsonResponse(context)

@csrf_exempt
@api_view(['POST','GET'])
# @ Admin Access
def UserProductSave(request):
    status = 0
    message = "suucess fully parsed"
    products =[]
    action = request.POST.get('action').strip()
    userdata = request.POST.getlist('userdata')
    productdata = request.POST.getlist('productdata')
    

    if action == 'saveuserproducts':
        for productid in (productdata[0].split(',')):

            producttemp = Content.objects.get(pk=int(productid))
            
            productinstance = ProductAssigns.objects.filter(products=producttemp)
            
            if len(productinstance) == 0:
                productsave = ProductAssigns(products=producttemp)
                productsave.save()       
                status = 200
                message = "Successfully Created and Assigned"
                for userid in (userdata[0].split(',')):
                    usertemp = User.objects.get(pk=int(userid))
                    productsave.users.add(usertemp)
            else:
                status = 200
                message = "Successfully Assigned"
                for userid in (userdata[0].split(',')):
                    usertemp = User.objects.get(pk=int(userid))
                    for iproduct in productinstance:
                        iproduct.users.add(usertemp)
    else:
        for productid in (productdata[0].split(',')):

            producttemp = Content.objects.get(pk=int(productid))
            
            productinstance = ProductAssigns.objects.filter(products=producttemp)
            
            if len(productinstance) >= 0:
                status = 200
                message = "Successfully DeAssigned"
                for userid in (userdata[0].split(',')):
                    usertemp = User.objects.get(pk=int(userid))
                    for iproduct in productinstance:
                        iproduct.users.remove(usertemp)
            else:
                status = 400
                message = "Product is not Exist"
                


    # print(userdata,productdata)

    context = {
        "message":message,
        "status":status,
        "action":action
    }
    return JsonResponse(context)

@csrf_exempt
def GroupProductSave(request):
    status = 200
    message = "suucess fully parsed"
    products =[]
    action = request.POST.get('action').strip()
    groupdata = request.POST.get('groupdata')
    productdata = request.POST.getlist('productdata')
    
    

    grouptemp = ProductGroup.objects.get(pk=int(groupdata))
    
  
    for productid in (productdata[0].split(',')):
        prodtemp = Content.objects.get(pk=int(productid))
        grouptemp.products.add(prodtemp)
  

    # print(userdata,productdata)

    context = {
        "message":message,
        "status":status,
        "action":action
    }
    return JsonResponse(context)    


@api_view(['POST','GET'])
@permission_classes([AllowAny,])
def MessageChatusers(request):
    message = "Success"
    status=200
    users = User.objects.all()
    serailizer = CustomUserSerializer(users,many=True)
    context = {
        'users':serailizer.data,
        'message':message,
        'status':status
    }
    return Response(context)

@csrf_exempt
@api_view(['POST','GET'])
@permission_classes([AllowAny,])
def MessageChatMessages(request):
    message = "Success"
    status=200
    if request.method == "POST":
        request.POST._mutable = True
        request.POST.update({'sender':request.user})
        msgform = MessageInboxForm(request.POST)
        if msgform.is_valid():
            msgform.save()
        else:
            message = msgform.errors

        context = {            
            'message':message,
            'status':status
        }
    if request.method == "GET":
        messagesinstance = MessageInbox.objects.all()
        serailizer = MessageInboxSerializer(messagesinstance,many=True)
        
        context = {
            'mesgs':serailizer.data,
            'message':message,
            'status':status
        }
    return Response(context)
    

# @api_view(['POST','GET'])
# @permission_classes([AllowAny,])
# def MessageChatMessagesBulk(request):
#     message = "Success"
#     status=200
#     if request.method == "POST":
#         category = request.POST.get('category','creator')    
#         itemlist = (request.POST.get('data')).split(',')    
#         for i in itemlist:
#         MessageInbox(sender=request.user,category=category)
#         MessageInbox.save()

#         if msgform.is_valid():
#             msgform.save()
#         else:
#             message = msgform.errors

#         context = {            
#             'message':message,
#             'status':status
#         }
#     return Response(context)
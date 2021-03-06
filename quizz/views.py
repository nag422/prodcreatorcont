from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.middleware.csrf import get_token
from quizz.models import Profile,Books,Content,ProductGroup,Likedproducts,Boughtedproducts,AssignedUsersGroup,ProductAssigns,MessageInbox,ContentSaveNotifyer,MessageChatter,MessageRequest,ProductRequest,Contentcategorynumbertoname
from django.contrib.auth.models import User, Group, Permission
from django.views.generic.base import TemplateView,RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView,CreateView,UpdateView
from django.db.models import F
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import AddForm,ProductForm,ProductRequestForm,GroupForm,MessageInboxForm,MessageChatterForm
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect,csrf_exempt
import json
from authentication.utils import DatabaseDynamic
from .serializers import ProductsSerializer,ProductAssignsSerializer,ProductGroupSerializer,MessageInboxSerializer,MessageChatterSerializer,ContentSaveNotifyerSerializer,ProductRequestSerializer,LikedproductsSerializer,BoughtedproductsSerializer
from authentication.serializers import CustomUserSerializer
import uuid
import math
from rest_framework.decorators import api_view, schema,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

import datetime
from dateutil.relativedelta import relativedelta

from .utils import Util,MassMail

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
    likedcount = 0
    interestcount =0
    messagecount=0
    usersarray =[]
    contentarray=[]
    weekdays = []


    try:
        if request.user.is_superuser:
            sellers = Profile.objects.filter(content="creator").count()    
            buyers = Profile.objects.filter(content="producer").count()  
            sellerenquiries = MessageChatter.objects.filter(sendertype="creator").count()
            buyerenquiries = MessageChatter.objects.filter(sendertype="producer").count()

            monthsnamearray = ['','Jan','Feb','Mar','April','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

            for dates in range(1,7):
                # usercount = 0
                # productcount=0
                weekdaysexplorer = datetime.datetime.today() - relativedelta(days=int(dates))
                usercount = User.objects.filter(date_joined = datetime.datetime(weekdaysexplorer.year, weekdaysexplorer.month, weekdaysexplorer.day)).count()
                usersarray.append(int(usercount))

                productcount = Content.objects.filter(created = datetime.date(weekdaysexplorer.year, weekdaysexplorer.month, weekdaysexplorer.day)).count()
                contentarray.append(int(productcount))

                weekdays.append((str(weekdaysexplorer.day) + str(monthsnamearray[weekdaysexplorer.month])))
        else:
            sellerenquiries = MessageChatter.objects.filter(sender=request.user.id).count()
            likedcount = Likedproducts.objects.filter(user=request.user.id).count()
            interestcount = Boughtedproducts.objects.filter(user=request.user.id).count()
            
        
        
        

            
            
 
    except Exception as e:
        error = str(e)

    context = {
        'sellers':sellers,
        'buyers':buyers,
        'sellerenquiries':sellerenquiries,
        'buyerenquiries':buyerenquiries,
        'likedcount':likedcount,
        'interestcount':interestcount,
        'usersarray':usersarray,
        'contentarray':contentarray,
        'weekdays':weekdays,
        'messagecount':messagecount,
        'error':error
        


    }
    # return JsonResponse(context)
    return Response(context)



@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def dashboardviewsellerView(request):
    sellers = 0
    buyers=0
    enquiries=0
    leads=0
    error=""
    likedcount = 0
    interestcount =0


    try:
        
        # sellers = Profile.objects.filter(content="creator").count()    
        # buyers = Profile.objects.filter(content="producer").count()  
        totaluploads = Content.objects.filter(author = request.user.id).count()
        sellerenquiries = MessageChatter.objects.filter(sendertype="creator").count()
        likedcount = Likedproducts.objects.filter(user=request.user.id).count()
        interestcount = Boughtedproducts.objects.filter(user=request.user.id).count()
        
    
    except Exception as e:
        error = str(e)

    context = {
        'totaluploads':totaluploads,
        'sellerenquiries':sellerenquiries,        
        'likedcount':likedcount,
        'interestcount':interestcount,
        'error':error


    }
    # return JsonResponse(context)
    return Response(context)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])

def dashboardviewbuyerView(request):
    sellers = 0
    buyers=0
    enquiries=0
    leads=0
    error=""
    likedcount = 0
    interestcount =0


    try:
        
        # sellers = Profile.objects.filter(content="creator").count()    
        # buyers = Profile.objects.filter(content="producer").count()  
        # totaluploads = Content.objects.filter(author = request.user.id).count()
        buyerenquiries = MessageChatter.objects.filter(sendertype="producer").count()
        likedcount = Likedproducts.objects.filter(user=request.user).count()
        interestcount = Boughtedproducts.objects.filter(user=request.user).count()
        
    
    except Exception as e:
        error = str(e)

    context = {
        # 'totaluploads':totaluploads,
        'sellerenquiries':buyerenquiries,        
        'likedcount':likedcount,
        'interestcount':interestcount,
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
            prodid = ProductFormResponse.save()
            message = "Successfully saved"
            status= 200
            ContentSaveNotifyer.objects.create(user=user_ptr,sender=request.user,receiver='buyer',productid=prodid.id,
            sendertype='seller',receivertype='buyer')
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
        instance = Content.objects.get(id=int(request.POST.get('id')))
        ProductFormResponse = ProductForm(request.POST or None,request.FILES or None, instance=instance)

        # print((request.FILES))

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
@api_view(['GET','POST'])
def getProductsall(request):
    product = []
    error=False,
    status=200
    totalrecords=0

    paginator = PageNumberPagination()
    paginator.page_size = 8
    paginator.page_query_param = 'page'

    # try:
    #     pageno = request.GET['page']
        
    # except:
    #     pageno = 0
    # allobjects = Content.objects.filter(is_active=True)[int(pageno):2]
    totalrecords = Content.objects.filter(is_active=True).count()
    allobjects = Content.objects.filter(is_active=True)
    contentinstance = paginator.paginate_queryset(allobjects, request)
    
    serializer = ProductsSerializer(contentinstance,many=True)

    for i in serializer.data:
        dt = Likedproducts.objects.filter(post=i['id'],user=request.user).exists()
        df = Boughtedproducts.objects.filter(post=i['id'],user=request.user).exists()
        
        i['isliked'] = dt
        i['isfavored'] = df
        i['customauthor'] = (User.objects.get(pk=i['author']).username).capitalize()
        
        product.append(i)
    
    response = {
        'obs':(product),
        'status':200,
        'error':error,
        'totalrecords':totalrecords
    }
    return JsonResponse(response)

@csrf_exempt
@api_view(['GET','POST'])
def getProductsofcreator(request):
    product = []
    error=False,
    status=200
    totalrecords=0

    paginator = PageNumberPagination()
    paginator.page_size = 8
    paginator.page_query_param = 'page'
    # try:
    #     pageno = request.GET['page']
        
    # except:
    #     pageno = 0
    # allobjects = Content.objects.filter(is_active=True)[int(pageno):2]
    totalrecords = Content.objects.filter(author=request.user).count()
    allobjects = Content.objects.filter(author=request.user)    
    contentinstance = paginator.paginate_queryset(allobjects, request)

    serializer = ProductsSerializer(contentinstance,many=True)
    
    for i in serializer.data:
        dt = Likedproducts.objects.filter(post=i['id']).exists()
        df = Boughtedproducts.objects.filter(post=i['id']).exists()
        
        i['isliked'] = dt
        i['isfavored'] = df
        i['customauthor'] = (User.objects.get(pk=i['author']).username).capitalize()
        
        product.append(i)
    
    response = {
        'obs':(product),
        'status':200,
        'error':error,
        'totalrecords':totalrecords
    }
    return JsonResponse(response)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny,])
def getProductById(request):
    product = []
    error=False,
    status=200
    try:
        data = json.loads(request.body)        
    except:
        data = {}
    # allobjects = Content.objects.filter(is_active=True)[int(pageno):2]
    allobjects = Content.objects.filter(id=int(data.get('productid')))
    
    
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
    totalrecords=0

    paginator = PageNumberPagination()
    paginator.page_size = 8
    paginator.page_query_param = 'page'

    totalrecords = ProductAssigns.objects.filter(users__in=[int(request.user.id)]).count()
    groupbyProducts = ProductAssigns.objects.filter(users__in=[int(request.user.id)])
    # print(groupbyProducts.get_products())
    contentinstance = paginator.paginate_queryset(groupbyProducts, request)
    serializer = ProductAssignsSerializer(contentinstance,many=True)
    # print(serializer.data)
    for i in serializer.data:
        contentvalues = Content.objects.filter(id=i['products'])
        for j in contentvalues.values():          

            dt = Likedproducts.objects.filter(post=j['id'],user=request.user).exists()
            df = Boughtedproducts.objects.filter(post=j['id'],user=request.user).exists()
            
            j['isliked'] = dt
            j['isfavored'] = df
            product.append(dict(j))
    
    response = {
        'obs':(product) if len(product) > 0  else [],
        'status':200,
        'error':error,
        'totalrecords':totalrecords
    }
    return JsonResponse(response)

@csrf_exempt
@api_view(['GET','POST'])
def getgroupProductsallbyUsers(request):
    product = []
    error=False,
    status=200
    totalrecords=0
    gorupgrabbder = []

    paginator = PageNumberPagination()
    paginator.page_size = 8
    paginator.page_query_param = 'page'

    get_usergroup_of_user = list(request.user.groups.values_list(flat=True))

    for i in get_usergroup_of_user:
        gorupgrabbder.append(i)

    totalrecords = ProductGroup.products.through.objects.filter(productgroup__id__in=gorupgrabbder).count()
    groupbyProducts = ProductGroup.products.through.objects.filter(productgroup__id__in=gorupgrabbder)
    # print(groupbyProducts.get_products())
    contentinstance = paginator.paginate_queryset(groupbyProducts, request)
    # serializer = ProductGroupSerializer(contentinstance,many=True)
    # print(serializer.data)
    for i in contentinstance:
        contentvalues = Content.objects.filter(id=i.content_id)
        for j in contentvalues.values():          

            dt = Likedproducts.objects.filter(post=j['id'],user=request.user).exists()
            df = Boughtedproducts.objects.filter(post=j['id'],user=request.user).exists()
            
            j['isliked'] = dt
            j['isfavored'] = df
            product.append(dict(j))
    
    response = {
        'obs':(product) if len(product) > 0  else [],
        'status':200,
        'error':error,
        'totalrecords':totalrecords
    }
    return JsonResponse(response)


# Admin Copy
@csrf_exempt
@api_view(['GET','POST'])
def getProductsallbyUsersbyid(request):
    product = []
    error=False,
    status=200
    totalrecords=0
    userid = request.GET.get('id')  

    paginator = PageNumberPagination()
    paginator.page_size = 8
    paginator.page_query_param = 'page'

    # df = Content.objects.filter(id=i['post_id'])
    #     for every in df.values():
    totalrecords = ProductAssigns.objects.filter(users__in=[int(userid)]).count()
    groupbyProducts = ProductAssigns.objects.filter(users__in=[int(userid)])
    # print(groupbyProducts.get_products())
    contentinstance = paginator.paginate_queryset(groupbyProducts, request)
    serializer = ProductAssignsSerializer(contentinstance,many=True)
    # print(serializer.data)
    for i in serializer.data:
        contentvalues = Content.objects.filter(id=int(i['products']))
        for j in contentvalues.values():          

            dt = Likedproducts.objects.filter(post=j['id']).exists()
            df = Boughtedproducts.objects.filter(post=j['id']).exists()
            
            j['isliked'] = dt
            j['isfavored'] = df
            product.append(dict(j))
    
    response = {
        'obs':(product) if len(product) > 0 else [],
        'status':status,
        'error':error,
        'totalrecords':totalrecords
    }
    return JsonResponse(response)


@csrf_exempt
@api_view(['GET','POST'])
def getUploadsallbyusersbyid(request):
    product = []
    error=False,
    status=200
    totalrecords=0
    userid = request.GET.get('id')
    
    paginator = PageNumberPagination()
    paginator.page_size = 8
    paginator.page_query_param = 'page'

    # df = Content.objects.filter(id=i['post_id'])
    #     for every in df.values():
    totalrecords = Content.objects.filter(author=int(userid)).count()
    userUploads = Content.objects.filter(author=int(userid))
    # print(groupbyProducts.get_products())
    contentinstance = paginator.paginate_queryset(userUploads, request)

    serializer = ProductsSerializer(contentinstance,many=True)
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
        'obs':(product) if len(product) > 0 else [],
        'status':status,
        'error':error,
        'totalrecords':totalrecords
    }
    return JsonResponse(response)

@csrf_exempt
@api_view(['GET','POST'])
def getProductsallliked(request):
    product = []
    error=False,
    status=200
    totalrecords=0

    paginator = PageNumberPagination()
    paginator.page_size = 8
    paginator.page_query_param = 'page'

    if request.user.is_superuser:
        totalrecords = Likedproducts.objects.all().count()
        allobjects = Likedproducts.objects.all()
    else:
        totalrecords = Likedproducts.objects.filter(user=request.user).count()
        allobjects = Likedproducts.objects.filter(user=request.user)

    contentinstance = paginator.paginate_queryset(allobjects, request)
    serializer = LikedproductsSerializer(contentinstance,many=True)

    for i in serializer.data:        
        df = Content.objects.filter(id=i['post'])
        for every in df.values():
            if request.user.is_superuser:
                dt = Likedproducts.objects.filter(post=every['id']).exists()
                df = Boughtedproducts.objects.filter(post=every['id']).exists()
                every['isliked'] = dt
                every['isfavored'] = df

                every['likedby'] = i['user_id']           

                every['likedbyname'] = User.objects.get(id=int(i['user_id'])).username
            else:
                every['isliked'] = True
                every['isfavored'] = True
                every['likedby'] = request.user.id
                every['likedbyname'] = request.user.username



            every['customauthor'] = User.objects.get(id=int(every['author_id'])).username
            
            product.append(every)


    
    response = {
        'obs':(product) if len(product) > 0 else [],
        'status':status,
        'error':error,
        'totalrecords':totalrecords
    }
    return JsonResponse(response)

# Admin likedproducts
@csrf_exempt
@api_view(['GET','POST'])
def getProductsalllikedbyuserid(request):
    product = []
    error=False,
    status=200
    totalrecords=0
    userid = request.GET.get('id')

    paginator = PageNumberPagination()
    paginator.page_size = 8
    paginator.page_query_param = 'page'

    totalrecords = Likedproducts.objects.filter(user = int(userid)).count()
    allobjects = Likedproducts.objects.filter(user = int(userid))

    contentinstance = paginator.paginate_queryset(allobjects, request)
    serializer = LikedproductsSerializer(contentinstance,many=True)
    
    for i in serializer.data:        
        df = Content.objects.filter(id=i['post'])
        for every in df.values():
            # every['customauthor'] = User.objects.get(id=int(every['author_id'])).username
            # every['likedby'] = i['user_id']
            # every['likedbyname'] = User.objects.get(id=int(i['user_id'])).username
            product.append(every)
    
    response = {
        'obs':(product) if len(product) > 0 else [],
        'status':status,
        'error':error,
        'totalrecords':totalrecords
    }
    return JsonResponse(response)


@csrf_exempt
@api_view(['GET','POST'])
def getProductsallbagged(request):
    product = []
    error=False,
    status=200
    totalrecords=0

    paginator = PageNumberPagination()
    paginator.page_size = 8
    paginator.page_query_param = 'page'


    

    if request.user.is_superuser:
        totalrecords = Boughtedproducts.objects.all().count()
        allobjects = Boughtedproducts.objects.all()
    else:
        totalrecords = Boughtedproducts.objects.filter(user=request.user).count()
        allobjects = Boughtedproducts.objects.filter(user=request.user)

    contentinstance = paginator.paginate_queryset(allobjects, request)
    serializer = BoughtedproductsSerializer(contentinstance,many=True)
    
    for i in serializer.data:        
        df = Content.objects.filter(id=i['post'])
        for every in df.values():
            if request.user.is_superuser:
                dt = Likedproducts.objects.filter(post=every['id']).exists()
                df = Boughtedproducts.objects.filter(post=every['id']).exists()
                every['isliked'] = dt
                every['isfavored'] = df
                every['likedby'] = i['user']
                every['likedbyname'] = User.objects.get(id=int(i['user'])).username
            else:
                every['isliked'] = True
                every['isfavored'] = True
                every['likedby'] = request.user.id
                every['likedbyname'] = request.user.username
            
            every['customauthor'] = User.objects.get(id=int(every['author_id'])).username
            
            product.append(every)


    response = {
        'obs':(product) if len(product) > 0  else [],
        'status':status,
        'error':error,
        'totalrecords':totalrecords
    }
    return JsonResponse(response)

# Admin baggedproducts
@csrf_exempt
@api_view(['GET','POST'])
def getProductsallbaggedbyuserid(request):
    product = []
    error=False,
    status=200
    totalrecords=0

    userid = request.GET.get('id')
    
    paginator = PageNumberPagination()
    paginator.page_size = 8
    paginator.page_query_param = 'page'

    totalrecords = Boughtedproducts.objects.filter(user=int(userid)).count()
    allobjects = Boughtedproducts.objects.filter(user=int(userid))

    contentinstance = paginator.paginate_queryset(allobjects, request)
    serializer = BoughtedproductsSerializer(contentinstance,many=True)

    
    for i in serializer.data:        
        df = Content.objects.filter(id=i['post'])
        for every in df.values():
            # every['customauthor'] = User.objects.get(id=int(every['author_id'])).username
            # every['likedby'] = i['user']
            # every['likedbyname'] = User.objects.get(id=int(i['user'])).username
            product.append(every)


    response = {
        'obs':(product) if len(product) > 0 else [],
        'status':status,
        'error':error,
        'totalrecords':totalrecords
    }
    return JsonResponse(response)

# @csrf_exempt
# def createGroup(request):
#     group = []
#     error =False
#     message=''
#     status=200
#     dataresp = request.POST

#     form = GroupForm(dataresp)
#     if form.is_valid:
#         # instance = form.save(commit=False)
#         # grp = ProductGroup(groupname=dataresp['groupname'],rule=dataresp['rule'])
#         # grp.save()
#         databaseDynamic = DatabaseDynamic(request)
        
#         grplastid = ProductGroup.objects.last()

#         if grplastid is not None:
#             primaryid = grplastid.id + 1
#         else:
#             primaryid = 1
        
        
#         thisdict = {'groupname':dataresp['groupname'],'rule':dataresp['rule'],'id':primaryid}
#         groupid = databaseDynamic.insertrecordtodb(catname='quizz_productgroup',thisdict=thisdict)
#         if (groupid):
#             status = 200
#         else:
#             status = 400
        

#     response = {
#         'error':error,
#         'message':message,
#         'status':status
#     }
#     return JsonResponse(response)

@csrf_exempt
def createGroup(request):
    group = []
    error =False
    message=''
    status=200    
    groupname = request.POST.get('groupname')    
    
    new_group, created = Group.objects.get_or_create(name = groupname)

    if created:
        message = "Success! group created" + str(groupname)
        
    else:
        error = True
        status=400
        message = "Error! group is already existed" + str(groupname)

    # user = User.objects.get(username = "nagkum")
    # # us = user.groups.values_list('name',flat = True)
    # us = user.groups.all()

    # for i in  (us):
    #     print(i.id)
    #     print(i.name)
        


    response = {

        'error':error,
        'message':message,
        'status':status
    }
    return JsonResponse(response)

# @csrf_exempt
# @api_view(['GET','POST'])
# # @ Admin Access
# def assignedtogroup(request):
#     group = []
#     error =False
#     message=''
#     status=0
#     dataresp = request.POST

#     itemlist = (request.POST.get('itemlist')).split(',')    
#     if itemlist is not None:
#         for items in itemlist:
#             try:
#                 AssignedUsersGroup.objects.get(user=int(items),groupid=dataresp.get('groupname')).delete()
#             except Exception as e:
#                 if items is not None and dataresp.get('groupname') is not None:

#                     AssignedUsersGroup(user=int(items),groupid=dataresp.get('groupname')).save()

#                     message = 'Success'
#                     status=200

#                 message = 'Failed'
#                 status=400
            
                    
            
#     else:
#         error =True
#         message = 'Something is went wrong'
#         status=400        

        

#     response = {
#         'error':error,
#         'message':message,
#         'status':status
#     }
#     return JsonResponse(response)

@csrf_exempt
@api_view(['GET','POST'])
# @ Admin Access
def assignedtogroup(request):
    group = []
    error =False
    message=''
    status=0
    failcounter = 0
    successcounter = 0
    dataresp = request.POST

    itemlist = (request.POST.get('itemlist')).split(',')    
    if itemlist is not None:
        for items in itemlist:
            user = User.objects.get(pk=int(items))
            group = Group.objects.get(pk=dataresp.get('groupname'))
            isexist = user.groups.filter(name = group).exists()

            if isexist:
                user.groups.remove(group)
                failcounter += 1
            else:
                user.groups.add(group)
                successcounter += 1

            

        message = 'Successfully Assigned'
        status=200

         
    else:
        error =True
        message = 'Something is went wrong'
        status=400        

        

    response = {
        'error':error,
        'message':message,
        'status':status,
        'successcounter':successcounter,
        'failcounter':failcounter
    }
    return JsonResponse(response)    

@csrf_exempt
def getAllgroups(request):
    groups = []
    error =False
    message=''
    status=200
    
    
    grps = Group.objects.all()

    print(grps)
    
    for every in grps.values():
        # every['_id'] = str(every['_id'])
        totalusers = AssignedUsersGroup.objects.filter(groupid=int(every['id'])).count()
        every['users'] = totalusers
        groups.append(every)

    context = {
        'error' : error,
        'message':'Successfully groups loaded',
        'status':200,
        'groups':groups,
        'totalrecords': Group.objects.all().count()
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
        Group.objects.filter(id__in=itemlist).delete()
    response={
            'error':error,
            'message':message,
            'user_id':user_id
            }
    return JsonResponse(response)

@csrf_exempt
@api_view(['GET','POST'])
def addliketoproduct(request):
    postid = request.POST.get('id')
    status = 200
    message = ""
    
    try:
        dt = Likedproducts.objects.filter(post=int(postid),user=request.user).first()
        dt.delete()
        message = "unliked"
    except:
        Likedproducts.objects.create(post=Content.objects.get(id=int(postid)),user=request.user)
        message = "liked"
    context = {
        'status':status,
        'message':message
    }
    
    return JsonResponse(context)


@csrf_exempt
@api_view(['GET','POST'])
def addboughtproduct(request):
    postid = request.POST.get('id')
    status = 200
    message = ""
    
    try:
        dt = Boughtedproducts.objects.filter(post=int(postid),user=request.user).first()
        dt.delete()
        message = "removedbuy"
    except:
        Boughtedproducts.objects.create(post=Content.objects.get(id=int(postid)),user=request.user)
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
@api_view(['POST'])
def deleteproduct(request):
    postid = request.POST.get('id')
    status = 200
    message = ""
    
    try:
        if request.user.is_superuser:
            dt = Content.objects.filter(id=int(postid))
        else:
            dt = Content.objects.filter(id=int(postid),author=request.user)

        dt.delete()
        message = "Deleted"
        try:
            dn = ContentSaveNotifyer.objects.filter(productid=int(postid))
            if dn:
                dn.delete()
        except:
            message = "Deleted but notification is not exist"
    except:        
        message = "Something is went wrong"
        status = 400
    context = {
        'status':status,
        'message':message
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



@api_view(['POST'])
@permission_classes([AllowAny,])
def save_product_by_admin(request):
    message = ''
    status = ''
    error = ''
    from django.template.defaultfilters import slugify
    request.POST._mutable = True
   
    # print('trigged productsave')
    if request.method == 'POST':
        slug = slugify(request.POST.get('title'))
        user_ptr = get_object_or_404(User, username=request.POST.get('user'))
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
            prodid = ProductFormResponse.save()
            message = "Successfully saved"
            status= 200            
            ContentSaveNotifyer.objects.create(user=user_ptr,sender=request.user,receiver='buyer',productid=prodid.id,
            sendertype='seller',receivertype='buyer')

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

@api_view(['POST','GET'])
@permission_classes([AllowAny,])
def NotifyGetter(request):
    message = ''
    status = 200
    error = False
    notifications = []
    data = ContentSaveNotifyer.objects.order_by('-id')[:10]
    serializer = ContentSaveNotifyerSerializer(data,many=True)
    serializerdata = serializer.data
    for proid in serializerdata:
        try:
            productname = Content.objects.get(id=int(proid['productid']))
            prodtitle = productname.title
            proid['productname'] = prodtitle
            
            dt = Likedproducts.objects.filter(post=productname.id,user=request.user.id).exists()
            df = Boughtedproducts.objects.filter(post=productname.id,user=request.user.id).exists()
            
            proid['isliked'] = dt
            proid['isfavored'] = df
            notifications.append(proid)
        except Exception as e:
            message = str(e)
            status = 400
            prodtitle='---Title not Available---'

        
        
    
    context = {
        'message':message,
        'status': status,
        'error':error,
        'notificationdata':notifications if len(notifications) > 0 else []
    }
    return Response(context)


@csrf_exempt
def GroupProductSave(request):
    status = 200
    message = "suucess fully parsed"
    products =[]
    action = request.POST.get('action').strip()
    groupdata = request.POST.get('groupdata')
    productdata = request.POST.get('productdata')
    splittedproduct = productdata.split(',')
    splittedgroup = groupdata.split(',')
    fialprod=[]
    if len(splittedgroup) > 0 :
        for everygroup in splittedgroup:

            grouptemp = Group.objects.get(pk=int(everygroup))
            
        
            for productid in splittedproduct:
                if action == "assign":
                    prodtemp = Content.objects.get(pk=int(productid))
                    new_productgroup, created = ProductGroup.objects.get_or_create(groupname=grouptemp.name,rule=grouptemp.id)
                    if created:
                        createprod = ProductGroup.objects.get(groupname = new_productgroup)
                        createprod.products.add(prodtemp)
                    else:
                        try:
                            new_productgroup.products.add(prodtemp)
                        except:
                            fialprod.append(prodtemp.id)

                else:
                    prodtemp = Content.objects.get(pk=int(productid))
                    ProductGroup.products.remove(prodtemp)

  

    # print(userdata,productdata)

    context = {
        "message":message,
        "status":status,
        "action":action,
        "assignfailed":(fialprod)
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
@csrf_exempt
@api_view(['POST','GET'])
@permission_classes([AllowAny,])
def GetAdminMessages(request):
    message = "Success"
    status=200
    totalrecords=0
    msgs = []

    

    if request.method == "POST":

        msgormail = request.POST.get('mailormessage')

        request.POST._mutable = True
        request.POST.pop('mailormessage')

        

        if msgormail != 'email':
            request.POST.update({'sender':request.user.id,'receiver':0,'sendertype':'superuser','msgtype':'send',
            'receivertype':request.POST.get('to'),'isgrouped':'yes','msg':request.POST.get('message'),'category':'superuser'})
            msgform = MessageChatterForm(request.POST)
            

            if msgform.is_valid():
                msgform.save()
            else:
                message = msgform.errors
        
        if request.POST.get('to') == "creator":
            togrop = "creator"
        else:
            togrop="producer"

        if msgormail == "emailandmessage":   
            users = Profile.objects.filter(content = str(togrop)).values()
            datalist = []
            end = math.ceil(len(users)/25)
            for i in range(end):
                data = (users[i*25:i*25+25])
                MassMail.send_emails(str(request.POST.get('message')),data)
        elif msgormail == "email":
            users = Profile.objects.filter(content = str(togrop)).values()
            datalist = []
            end = math.ceil(len(users)/25)
            for i in range(end):
                data = (users[i*25:i*25+25])
                MassMail.send_emails(str(request.POST.get('message')),data)
                   


        context = {            
            'message':message,
            'status':status
        }

    if request.method == "GET":
        request_query = request.GET.get('q')

        paginator = PageNumberPagination()

        paginator.page_size = int(request.GET.get('perpages',5))
        paginator.page_query_param = 'currentpage'

        if request_query == "all":
            totalrecords = MessageChatter.objects.filter(isgrouped='yes').count()
            messagesinstance1 = MessageChatter.objects.filter(isgrouped='yes')
            messagesinstance = paginator.paginate_queryset(messagesinstance1, request)
            serializer = MessageChatterSerializer(messagesinstance,many=True)
        
        elif request_query == "groupmessages":
            totalrecords = MessageChatter.objects.filter(isgrouped='yes',receivertype='usergroup').count()
            messagesinstance1 = MessageChatter.objects.filter(isgrouped='yes',receivertype='usergroup')
            messagesinstance = paginator.paginate_queryset(messagesinstance1, request)
            serializer = MessageChatterSerializer(messagesinstance,many=True)            

        elif request_query == "requests":
            totalrecords = ProductRequest.objects.all().count()
            requestproductdata1 = ProductRequest.objects.all()
            requestproductdata = paginator.paginate_queryset(requestproductdata1, request)
            serializer = ProductRequestSerializer(requestproductdata,many=True) 

            for every in serializer.data:
                try:
                    every['sendername'] = str(User.objects.get(id=int(every['author'])).username)+" ( "+str(every['authortype'])+" )"
                except:
                    every['sendername'] = '----------'               
            

                every['receivername'] = 'superuser'
                every['msg'] = str(every['title']) + '---' + str(Contentcategorynumbertoname.objects.get(numberval = str(every['category'])))
                msgs.append(dict(every)) 

        else:
            totalrecords = MessageChatter.objects.filter(sendertype=request_query).count()
            messagesinstance1 = MessageChatter.objects.filter(sendertype=request_query)
            messagesinstance = paginator.paginate_queryset(messagesinstance1, request)

            serializer = MessageChatterSerializer(messagesinstance,many=True)
        
        if request_query != "requests":
            for every in serializer.data:
                sendername = User.objects.get(id=int(every['sender'])).username
                try:
                    if request_query == "groupmessages":
                        receiverrname = every['category']
                    else:
                        receiverrname = User.objects.get(id=int(every['receiver'])).username
                except:
                    receiverrname = "----"

                every['sendername'] = str(sendername)
                every['receivername'] = receiverrname
                msgs.append(dict(every))

        context = {
            'mesgs':msgs,
            'message':message,
            'status':status,
            'totalrecords':totalrecords
        }
    return Response(context)

@csrf_exempt
@api_view(['POST','GET'])
@permission_classes([AllowAny,])
def GetAdminMessagesReply(request):
    message = "Success"
    status=200
    msgs = []

    if request.method == "POST":
        request.POST._mutable = True
        
        itemlist = (request.POST.get('itemlist')).split(',')   

        if itemlist is not None:

            for items in itemlist:
                
                msgormail = request.POST.get('mailormessage')

                request.POST._mutable = True
                request.POST.pop('mailormessage')
                receiverdata = MessageChatter.objects.get(id=int(items))
                
                if msgormail != 'email':
                    request.POST.update({'sender':request.user.id,'receiver':int(items),'sendertype':'superuser','msgtype':'reply',
                    'receivertype':receiverdata.receivertype,'isgrouped':'no','msg':request.POST.get('message'),'category':'superuser'})


                    msgform = MessageChatterForm(request.POST)

                    if msgform.is_valid():
                        msgform.save()
                    else:
                        message = msgform.errors
                

                if msgormail == "emailandmessage":   
                    user = User.objects.get(pk=int(items.sender))
                    data = {'email_body': str(request.POST.get('message')), 'to_email': user.email,
                    'email_subject': 'ContentBond - info'}         
                    Util.send_email(data)
                elif msgormail == "email":
                    user = User.objects.get(pk=int(items.sender))
                    data = {'email_body': str(request.POST.get('message')), 'to_email': user.email,
                    'email_subject': 'ContentBond - info'}         
                    Util.send_email(data)

        context = {            
            'message':message,
            'status':status
        }
        return Response(context)

@csrf_exempt
@api_view(['POST','GET'])
@permission_classes([AllowAny,])
def DeleteMessages(request):
    message = "Success"
    status=200
    msgs = []
    query_word_get = request.POST.get('q')

    if request.method == "POST":
        itemlist = (request.POST.get('itemlist')).split(',')   
        if request.user.is_superuser:
            if itemlist is not None:
                for items in itemlist:
                    try:
                        if query_word_get != "requests":
                            MessageChatter.objects.get(id=int(items)).delete()
                        else:
                            ProductRequest.objects.get(id=int(items)).delete()                            
                    except Exception as e:
                        status=400
        elif request.user.is_authenticated:
            if itemlist is not None:
                for items in itemlist:
                    try:
                        if query_word_get != "requests":
                            MessageChatter.objects.get(id=int(items),sender=request.user.id).delete()
                        else:
                            ProductRequest.objects.get(id=int(items),author=request.user).delete()
                        status=200
                    except Exception as e:
                        status=400

        

    context = {            
            'message':message,
            'status':status
        }
    return Response(context)
                



@csrf_exempt
@api_view(['POST','GET'])
@permission_classes([AllowAny,])
def getsellermessages(request):
    message = "Success"
    status=200
    msgs = []
    totalrecords=0

    if request.method == "POST":
        request.POST._mutable = True
        request.POST.update({'sender':request.user.id,'receiver':0,'sendertype':'creator','msgtype':'send',
        'receivertype':request.POST.get('to'),'isgrouped':'no','msg':request.POST.get('message'),'category':'creator'})
        msgform = MessageChatterForm(request.POST)
        if msgform.is_valid():
            msgform.save()
        else:
            message = msgform.errors

        context = {            
            'message':message,
            'status':status
        }

    if request.method == "GET":
        request_query = request.GET.get('q')

        paginator = PageNumberPagination()

        paginator.page_size = int(request.GET.get('perpages',5))
        paginator.page_query_param = 'currentpage'

        if request_query == "all":
            totalrecords = MessageChatter.objects.filter(isgrouped='yes',receivertype='creator').count()
            messagesinstance1 = MessageChatter.objects.filter(isgrouped='yes',receivertype='creator')
            messagesinstance = paginator.paginate_queryset(messagesinstance1, request)
            serializer = MessageChatterSerializer(messagesinstance,many=True)
        if request_query == "groupmessages":
            msggrabber = []
            get_usergroup_of_user = list(request.user.groups.values_list('name',flat=True))
            for thing in get_usergroup_of_user:
                msggrabber.append(thing)

            if len(msggrabber) > 0:
                totalrecords = MessageChatter.objects.filter(isgrouped='yes',receivertype='usergroup',category__in=msggrabber).count()
                messagesinstance1 = MessageChatter.objects.filter(isgrouped='yes',receivertype='usergroup',category__in=msggrabber)
            else:
                totalrecords = MessageChatter.objects.filter(isgrouped='yes',receivertype='creator').count()
                messagesinstance1 = MessageChatter.objects.filter(isgrouped='yes',receivertype='creator')

            messagesinstance = paginator.paginate_queryset(messagesinstance1, request)
            serializer = MessageChatterSerializer(messagesinstance,many=True)    
        elif request_query == "inbox":
           
            # paginator.page = (int(request.GET.get('currentpage',1)))+1
            totalrecords = MessageChatter.objects.filter(sender=request.user.id).count()

            messagesinstance1 = MessageChatter.objects.filter(sender=request.user.id)    

            messagesinstance = paginator.paginate_queryset(messagesinstance1, request)
            serializer = MessageChatterSerializer(messagesinstance,many=True)

        elif request_query == "requests":

            totalrecords = ProductRequest.objects.filter(author=request.user).count()
            requestproductdata1 = ProductRequest.objects.filter(author=request.user)
            requestproductdata = paginator.paginate_queryset(requestproductdata1, request)
            serializer = ProductRequestSerializer(requestproductdata,many=True) 

            for every in serializer.data:
                every['msg'] = str(every['title']) + '---' + str(every['category'])
                msgs.append(dict(every)) 
            
        else:
            totalrecords = MessageChatter.objects.filter(receiver=str(request.user.id)).count()
            messagesinstance1 = MessageChatter.objects.filter(receiver=str(request.user.id))
            messagesinstance = paginator.paginate_queryset(messagesinstance1, request)

            serializer = MessageChatterSerializer(messagesinstance,many=True)
        
        if request_query != "requests":
            for every in serializer.data:
                sendername = User.objects.get(id=int(every['sender'])).username
                try:
                    if request_query == "groupmessages":
                        receiverrname = every['category']
                    else:
                        receiverrname = User.objects.get(id=int(every['receiver'])).username
                except:
                    receiverrname = "----"

                every['sendername'] = str(sendername)
                every['receivername'] = receiverrname
                msgs.append(dict(every))

        context = {
            'mesgs':msgs,
            'message':message,
            'status':status,
            'totalrecords':totalrecords
        }
    return Response(context)



@csrf_exempt
@api_view(['POST','GET'])
@permission_classes([AllowAny,])
def getbuyermessages(request):
    message = "Success"
    status=200
    msgs = []
    totalrecords=0

    if request.method == "POST":
        request.POST._mutable = True
        request.POST.update({'sender':request.user.id,'receiver':0,'sendertype':'producer','msgtype':'send',
        'receivertype':request.POST.get('to'),'isgrouped':'no','msg':request.POST.get('message'),'category':'producer'})
        msgform = MessageChatterForm(request.POST)
        if msgform.is_valid():
            msgform.save()
        else:
            message = msgform.errors

        context = {            
            'message':message,
            'status':status
        }

    if request.method == "GET":
        request_query = request.GET.get('q')
        msggrabber = []

        paginator = PageNumberPagination()

        paginator.page_size = int(request.GET.get('perpages',5))
        paginator.page_query_param = 'currentpage'


        if request_query == "all":
            totalrecords = MessageChatter.objects.filter(isgrouped='yes',receivertype='producer').count()
            messagesinstance1 = MessageChatter.objects.filter(isgrouped='yes',receivertype='producer')
            messagesinstance = paginator.paginate_queryset(messagesinstance1, request)
            serializer = MessageChatterSerializer(messagesinstance,many=True)    
        
        if request_query == "groupmessages":
            msggrabber = []
            get_usergroup_of_user = list(request.user.groups.values_list('name',flat=True))
            for thing in get_usergroup_of_user:
                msggrabber.append(thing)

            if len(msggrabber) > 0:
                totalrecords = MessageChatter.objects.filter(isgrouped='yes',receivertype='usergroup',category__in=msggrabber).count()
                messagesinstance1 = MessageChatter.objects.filter(isgrouped='yes',receivertype='usergroup',category__in=msggrabber)
            else:
                totalrecords = MessageChatter.objects.filter(isgrouped='yes',receivertype='producer').count()
                messagesinstance1 = MessageChatter.objects.filter(isgrouped='yes',receivertype='producer')

            messagesinstance = paginator.paginate_queryset(messagesinstance1, request)
            serializer = MessageChatterSerializer(messagesinstance,many=True)    

        elif request_query == "inbox":
           
            # paginator.page = (int(request.GET.get('currentpage',1)))+1
            totalrecords = MessageChatter.objects.filter(sender=request.user.id).count()

            messagesinstance1 = MessageChatter.objects.filter(sender=request.user.id)    

            messagesinstance = paginator.paginate_queryset(messagesinstance1, request)
            serializer = MessageChatterSerializer(messagesinstance,many=True)

        elif request_query == "requests":

            totalrecords = ProductRequest.objects.filter(author=request.user).count()
            requestproductdata1 = ProductRequest.objects.filter(author=request.user)
            requestproductdata = paginator.paginate_queryset(requestproductdata1, request)
            serializer = ProductRequestSerializer(requestproductdata,many=True) 

            for every in serializer.data:
                every['msg'] = str(every['title']) + '---' + str(every['category'])
                msgs.append(dict(every)) 

        else:
            totalrecords = MessageChatter.objects.filter(receiver=request.user.id,isgrouped='no').count()
            messagesinstance1 = MessageChatter.objects.filter(receiver=request.user.id,isgrouped='no')
            messagesinstance = paginator.paginate_queryset(messagesinstance1, request)

            serializer = MessageChatterSerializer(messagesinstance,many=True)
        
        if request_query != "requests":
            for every in serializer.data:
                sendername = User.objects.get(id=int(every['sender'])).username
                try:
                    if request_query == "groupmessages":
                        receiverrname = every['category']
                    else:
                        receiverrname = User.objects.get(id=int(every['receiver'])).username
                except:
                    receiverrname = "----"

                every['sendername'] = str(sendername)
                every['receivername'] = receiverrname
                msgs.append(dict(every))

        context = {
            'mesgs':msgs if len(msgs) > 0  else [],
            'message':message,
            'status':status,
            'totalrecords':totalrecords
        }
    return Response(context)

# @csrf_exempt
# @api_view(['POST','GET'])
# @permission_classes([AllowAny,])            
# def GetMessageRequest(request):
#     message = "Success"
#     status=200
#     msgs = []

#     if request.method == "POST":
#         request.POST._mutable = True
#         request.POST.update({'sender':request.user.id,'receiver':'superuser','sendertype':'producer','msgtype':'send',
#         'receivertype':request.POST.get('to'),'isgrouped':'no','msg':request.POST.get('message'),'category':'producer'})
#         msgform = MessageChatterForm(request.POST)
#         if msgform.is_valid():
#             msgform.save()
#         else:
#             message = msgform.errors

#         context = {            
#             'message':message,
#             'status':status
#         }

#     return Response(context)

# Group Messages
@csrf_exempt
@api_view(['POST','GET'])
@permission_classes([AllowAny,])
def GetgroupMessages(request):
    message = "Success"
    status=200
    msgs = []
    totalrecords=0

    if request.method == "POST":
        request.POST._mutable = True
        message = (request.POST.get('message'))
        mailormsg = (request.POST.get('mailormessage'))
        to = (request.POST.get('to')).split(',')
        for everygroup in to:
            grpname = Group.objects.get(pk=int(everygroup))            
            request.POST.update({'sender':request.user.id,'receiver':0,'sendertype':'superuser','msgtype':'send',
            'receivertype':'usergroup','isgrouped':'yes','msg':message,'category':grpname})
            msgform = MessageChatterForm(request.POST)
            if msgform.is_valid():
                msgform.save()
            else:
                message = msgform.errors
                status = 200

        context = {            
            'message':message,
            'status':status
        }
        return JsonResponse(context)    

@api_view(['POST','GET'])
@permission_classes([AllowAny,])
def testpurpose(request):
    # val = ProductGroup.related.objects.all()
    # print(val)
    # all_categories = Content.objects.filter(
    # id__in=ProductGroup.products.through.objects.all(
    #     # productgroup__in=[2]
    # ).values()
    
    # )
    paginator = PageNumberPagination()

    paginator.page_size = int(request.GET.get('perpages',1))
    paginator.page_query_param = 'currentpage'

    user = User.objects.get(username="nagendra")
    get_usergroup_of_user = list(user.groups.values_list(flat=True))
    gorupgrabbder = []
    for i in get_usergroup_of_user:
        gorupgrabbder.append(i)

    # all_categories = ProductGroup.products.through.objects.all()
    # messagesinstance = paginator.paginate_queryset(all_categories, request)
    # cnt = ProductGroup.products.through.objects.filter(productgroup__id__in=[1]).count()
    # print(messagesinstance)

    totalrecords = ProductGroup.products.through.objects.filter(productgroup__id__in=gorupgrabbder).count()
    groupbyProducts = ProductGroup.products.through.objects.filter(productgroup__id__in=gorupgrabbder)
    # print(groupbyProducts.get_products())
    # contentinstance = paginator.paginate_queryset(groupbyProducts, request)
    print(groupbyProducts)
    
    return Response({'done':'cnt'})
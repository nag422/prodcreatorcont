'''
# from django.contrib.auth import load_backend, login


# def login_user(request, user):
#     """Log in a user without requiring credentials with user object"""
#     if not hasattr(user, 'backend'):
#         for backend in settings.AUTHENTICATION_BACKENDS:
#             if user == load_backend(backend).get_user(user.pk):
#                 user.backend = backend
#                 break
#     if hasattr(user, 'backend'):
#         return login(request, user)

'''
from django.shortcuts import render,redirect,get_object_or_404
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import connection
from .forms import RegistrationForm, UserEditForm
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect,csrf_exempt
from .utils import DatabaseDynamic
from quizz.models import Profile,AssignedUsersGroup,ProductGroup

def account_register(request):
    if request.user.is_authenticated:
        return redirect('/admin')
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit = False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            # SetUp Email
            current_site = get_current_site(request)
            subject = 'Activate your Account - MoviePlex'
            message = render_to_string('account/account_activation_email.html',{
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_b64encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            user.email_user(subject=subject,message=message,from_email=settings.EMAIL_HOST_USER)
    else:
        return redirect('/admin')

def account_activate(request,uidb64,token):
    try:
        uid =force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request,user)
            return redirect('quizz:quiz')
        else:
            return JsonResponse(request,{error:'Account Activation is failed'})
    except Exception as e:
        return JsonResponse(request,{error:str(e)})


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'account/user/edit_details.html', {'user_form': user_form})


@login_required
def delete_user(request):
    user = User.objects.get(username=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')

# Admin Block

@csrf_exempt
def authRegistervalidation(request):
    status = 0
    message = ""
    action = request.POST.get('action')
    if action == "username":
        username = str(request.POST.get('value'))
        message = User.objects.filter(username = (username).lower()).exists()
        status = 200
    elif action == "email":
        email = request.POST.get('value')
        message = User.objects.filter(email = (email).lower()).exists()
        status = 200  
    

    
   
    context = {
        "message":message,
        "status":status,
        "action":action
    }
    return JsonResponse(context)
@csrf_exempt
def authRegisteraccount(request):

    status = 0
    message = ""
    
    first_name = request.POST.get('first_name','')
    last_name = request.POST.get('last_name','')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    phone = request.POST.get('phone')
    category = request.POST.get('category')
    

    registeruser=User.objects.create_user(
        username=username.lower(),is_active=True,password=password,
        first_name=first_name.lower(),last_name=last_name.lower())
    
    user_id = registeruser.id
    try:
        if user_id > 0:
            Profile.objects.create(user_ptr=User.objects.get(id=int(user_id)),content=category,phone=phone)
            message = "Successfully Registered"
            status = 200
            
    except Exception as e:
        print(e)

    context = {
        "message":message,
        "status":status
    }
    return JsonResponse(context)


@csrf_exempt
def saveUser(request):
    error=False
    message=''
    user_id=''
    posts=''
    GETmethodData = []
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        usertype=request.POST['usertype']
        category=request.POST['usercategory']
        
        if str(usertype) == "user":
            user_admin=User.objects.create_user(username=username.lower(),is_active=True,password=password)
        elif str(usertype) == "admin":
            user_admin=User.objects.create_superuser(username=username.lower(),is_active=True,is_staff=True,password=password)
        elif str(usertype) == "superuser":
            user_admin=User.objects.create_user(username=username.lower(),is_active=True,is_staff=True,password=password,is_superuser=True)
        try:
            user_id = user_admin.id
            print(user_admin)
            print(user_id)
            if user_id > 0:
                databaseDynamic = DatabaseDynamic(request)
                thisdict = {'user_ptr_id':user_id,'content':category,'id':user_id}
                profileid = databaseDynamic.insertrecordtodb(catname='quizz_profile',thisdict=thisdict)

        except Exception as e:
            print('error',e)
            user_id=0
        
        
    else:
          
        try:
            posts = User.objects.all()
        except Exception as e:
            pass
            print(e)    


        for i in posts.values():
            try:
                userinstance=Profile.objects.get(user_ptr=i['id'])    
                try:
                    grp = AssignedUsersGroup.objects.get(user=i['id'])
                    productinstance = ProductGroup.objects.filter(id=grp.groupid).first()
                    i.update({'content':userinstance.content,'user_ptr':userinstance.user_ptr_id,'group':productinstance.groupname})
                    # print('grop find')
                except:
                    # print(userinstance.user_ptr_id)
                    i.update({'content':userinstance.content,'user_ptr':userinstance.user_ptr_id})
            except:
                pass
            GETmethodData.append(i)
        response={
                'error':error,
                'message':message,
                'user_id':user_id,
                'GETmethodData':GETmethodData
             }
        return JsonResponse(response)
        

    response={
                'error':error,
                'message':message,
                'user_id':user_id,
                'GETmethodData':GETmethodData
             }
    return JsonResponse(response)

def getsingleUser(request):
    isquery = request.GET.get('username')
    error=False
    message=''
    user_id=''
    posts=''
    GETmethodData = []
    if isquery is not None:

        try:
            posts = User.objects.filter(username__contains=str(isquery)).all()
        except Exception as e:
            pass
            print(e)
        for i in posts.values():
            try:
                userinstance=Profile.objects.get(user_ptr=i['id'])            
                i.update({'content':userinstance.content,'user_ptr':userinstance.user_ptr_id})
            except:
                pass
            GETmethodData.append(i)
    response={
            'error':error,
            'message':message,
            'user_id':user_id,
            'GETmethodData':GETmethodData
            }
    return JsonResponse(response)

@csrf_exempt
def deleteUsers(request):
    error=False
    message=''
    user_id=''
    itemlist = (request.POST.get('itemlist')).split(',')    
    if itemlist is not None:
        User.objects.filter(id__in=itemlist).delete()
    response={
            'error':error,
            'message':message,
            'user_id':user_id
            }
    return JsonResponse(response)


@csrf_exempt
def updateUser(request):    
    error=False
    message=''
    user_id=''
    status = 0

    userid = request.POST.get('id')
    usertype = request.POST.get('role')
    usercategory = request.POST.get('category')
    useraction = request.POST.get('action')

    userinstance = User.objects.get(id=int(userid))
    if userinstance is not None:
        Profile.objects.filter(user_ptr=userinstance.id).update(content=usercategory)
        if str(usertype) == "user":
            userinstance.is_superuser = False
            userinstance.is_staff= False
            userinstance.is_active= True
            userinstance.save()

                
        elif str(usertype) == "admin":
            userinstance.is_superuser = False
            userinstance.is_staff= True
            userinstance.is_active= True
            userinstance.save()
        elif str(usertype) == "superuser":
            userinstance.is_superuser = True
            userinstance.is_staff= True
            userinstance.is_active= True
            userinstance.save()
        message="Successfully User Changed"
        status = 200
    else:
        message="Something is went wrong"
        status = 400

            
    response={
            'error':error,
            'message':message,
            'status':status
            }
    return JsonResponse(response)
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

import json

from django.shortcuts import render,redirect,get_object_or_404
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string,get_template
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import connection
from .forms import RegistrationForm, UserEditForm,PwdResetConfirmForm
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect,csrf_exempt
from .utils import DatabaseDynamic,SessionHandle
from quizz.models import Profile,AssignedUsersGroup,ProductGroup,MessageChatter,ContentSaveNotifyer
from .serializers import ProfileSerializer,UserSerializer,CustomUserSerializer
from rest_framework import permissions
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework.decorators import api_view, schema,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny

from .tokens import account_activation_token

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
    error = "error"
    try:
        uid =force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if user is not None and user.is_active:
            return redirect('authentication:ResetPasswordMailerComplete')

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request,user)
            return redirect('authentication:ResetPasswordMailerComplete')
        else:
            return render(request, 'account/resetpassworderror.html')
    except Exception as e:
        return render(request, 'account/resetpassworderror.html')


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

@method_decorator(csrf_exempt, name='dispatch')
class loginView(APIView):
    permission_classes = (permissions.AllowAny, )
    
    # def post(self, request, format=None):
    #     data = self.request.data
    #     print(data)
    #     return JsonResponse({ 'error': 'Something went wrong when logging in' })

    def post(self,request,format=None):
        data = json.loads(request.body)
        
        status = 0
        message = ""
        
        username = data.get("username").strip()
        password = data.get("password").strip()

        if username is None or password is None:
            status = 400
            message = "Invalid Credentials"
            return JsonResponse({"status":status,"message":message})
        user = authenticate(username=username,password=password)
        if user is None:
            status = 400
            message = "Invalid Credentials"
            return JsonResponse({"status":status,"message":message})
        login(request,user)

        instance = Profile.objects.filter(user_ptr=request.user.id).first()    
        serializer = ProfileSerializer(instance)
        response = serializer.data
        token, created = Token.objects.get_or_create(user=request.user)
        response['access_token'] = token.key
        status = 200
        message = "Successfully Authenticated"
        
        return JsonResponse({"status":status,"message":message,"response":response})


@csrf_exempt
@api_view(['POST','GET'])
def WhoAmi(request):
    # sessionhandle = SessionHandle(request)
    status =200
    message ="success"
    response = []
    try:
        data = json.loads(request.body)
    except:
        data = {'action':'errortrue'}
    
    if data.get('action') == 'get':
        try:
            instance = Profile.objects.filter(user_ptr=request.user.id).first()    
            serializer = ProfileSerializer(instance)
            response = serializer.data
            token, created = Token.objects.get_or_create(user=request.user)
            response['access_token'] = token.key

            if request.user.is_superuser:
                notifycount = ContentSaveNotifyer.objects.all().count()
                messagecount = MessageChatter.objects.all().count()
                response['notificationcount'] = notifycount
                
            elif request.user.is_staff:
                notifycount = ContentSaveNotifyer.objects.all().count()
                messagecount = MessageChatter.objects.all().count()
                response['notificationcount'] = notifycount

            elif Profile.objects.filter(user_ptr=request.user,content="creator").exists():
                messagecount = MessageChatter.objects.filter(receivertype='creator',receiver=str(request.user.id)).count()
                response['notificationcount'] = 0
            elif Profile.objects.filter(user_ptr=request.user,content="producer").exists():
                notifycount = ContentSaveNotifyer.objects.all()[:10]
                messagecount = MessageChatter.objects.filter(receivertype='producer',receiver=str(request.user.id)).count()
                response['notificationcount'] = len(notifycount)

            response['messagecount'] = messagecount

        except Exception as e:
            response['access_token'] = str(e)
        # Dummy
        # username = "nagendra"
        
        # if username=="nagendra":
        #     response = ({'is_Authenticated':True,'username':'nagendra',
        #     'is_superuser':True,'is_staff':True,'is_active':True,
        #     'email':'nagendrakumar422@gmail.com'
        #     })
        # elif username=="trisha":
        #     response = ({'is_Authenticated':True,'username':'trisha',
        #     'is_superuser':False,'is_staff':True,'is_active':True,
        #     'email':'trishanarayan@yopmail.com','category':'producer'
        #     })
        # else:
        #     response = ({'is_Authenticated':True,'username':'testing',
        #     'is_superuser':False,'is_staff':True,'is_active':True,
        #     'email':'testing@yopmail.com','category':'creator'
        #     })
        # Dummy

        # print('trigging getprofile')
        


    if data.get('action') == 'update':
        instance = User.objects.filter(id=request.user.id).first()  
        ser = (data.get('user')) 
        serializerdata = {'first_name':ser.get('first_name',''),'last_name':ser.get('last_name',''),'email':ser.get('email','')} 
        
        serializer = CustomUserSerializer(instance, data=dict(serializerdata))
        try:
            if True:
                response = serializer.update(instance, dict(serializerdata))
                # response = serializer.save()
            else:
                # print('seri not valid')
                status =400
        except Exception as e:
            # print('serial not valid')
            # print(e)
            status =400
        
        # print(response)
    if data.get('action') == 'profileupdate':
        instance = Profile.objects.filter(user_ptr=request.user.id).first()  
        ser = (data.get('user')) 
        serializerdata = {'address':ser.get('address',''),
        'postalcode':ser.get('postalcode',''),'phone':ser.get('phone',''),
        'city':ser.get('city',''),'country':ser.get('country','')
        } 
        
        serializer = ProfileSerializer(instance, data=dict(serializerdata))
        try:
            if True:
                response = serializer.update(instance, dict(serializerdata))
                # response = serializer.save()
            else:
                # print('seri not valid')
                status =400
        except Exception as e:
            # print('serial not valid')
            # print(e)
            status =400
        
        # print(response)
    
    context = {

        'status':status,
        'message':message,
        'response':response
    }

    return Response(context)

@csrf_exempt

def aboutmebyid(request):
    
    status =200
    message ="success"
    response = []
    
    data = request.GET
    if data.get('action') == 'get':
        instance = Profile.objects.filter(user_ptr=int(data.get('profileid'))).first()    
        serializer = ProfileSerializer(instance)
        response = serializer.data


    context = {

        'status':status,
        'message':message,
        'response':response
    }

    return JsonResponse(context)

@csrf_exempt
@api_view(['POST','GET'])
# @ Access Admin
def WhoamiProfileUpdate(request):
    status =200
    message ="success"
    response = []
    if data.get('action') == 'update':
        instance = User.objects.filter(id=int(data.get('profileid'))).first()  
        ser = (data.get('user')) 
        serializerdata = {'first_name':ser.get('first_name',''),'last_name':ser.get('last_name',''),'email':ser.get('email','')} 
        
        serializer = CustomUserSerializer(instance, data=dict(serializerdata))
        try:
            if True:
                response = serializer.update(instance, dict(serializerdata))
                # response = serializer.save()
            else:
                # print('seri not valid')
                status =400
        except Exception as e:
            # print('serial not valid')
            # print(e)
            status =400
        
        # print(response)
    if data.get('action') == 'profileupdate':
        instance = Profile.objects.filter(user_ptr=int(data.get('profileid'))).first()  
        ser = (data.get('user')) 
        serializerdata = {'address':ser.get('address',''),
        'postalcode':ser.get('postalcode',''),'phone':ser.get('phone',''),
        'city':ser.get('city',''),'country':ser.get('country','')
        } 
        
        serializer = ProfileSerializer(instance, data=dict(serializerdata))
        try:
            if True:
                response = serializer.update(instance, dict(serializerdata))
                # response = serializer.save()
            else:
                # print('seri not valid')
                status =400
        except Exception as e:
            # print('serial not valid')
            # print(e)
            status =400
    context = {

        'status':status,
        'message':message,
        'response':response
    }

    return JsonResponse(context)

@csrf_exempt
@require_POST
def logoutView(request):
    sessionhandle = SessionHandle(request)
    logout(request)
    sessionhandle.clear()
    print(sessionhandle.__len__())
    context = {
        "message":"Successfully logout",
        "status":200
    }
    return JsonResponse(context)


@csrf_exempt
def authRegistervalidation(request):
    status = 0
    message = ""
    action = request.POST.get('action').strip()
    if action == "username":
        username = str(request.POST.get('value').strip())
        if len(username) >=5:
            message = User.objects.filter(username = (username).lower()).exists()
            status = 200
        else:
            message = True
            status = 400
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
def authChipUserGet(request):
    status = 0
    message = ""
    users =[]
    action = request.POST.get('action').strip()
    if action == "Getusername":
        username = str(request.POST.get('value').strip())
        if len(username) >0:
            print('im printing')
            userinstance = User.objects.filter(username__contains = (username).lower())
            serializer = UserSerializer(userinstance,many=True)
            users = (serializer.data)
            status = 200
        else:
            message = True
            status = 400
    elif action == "email":
        email = request.POST.get('value')
        message = User.objects.filter(email = (email).lower()).exists()
        status = 200  
    

    context = {
        "users":users,
        "message":message,
        "status":status,
        "action":action
    }
    return JsonResponse(context)



@csrf_exempt
def authRegisteraccount(request):

    status = 200
    message = ""
    
    first_name = (request.POST.get('first_name','')).strip()
    last_name = request.POST.get('last_name','').strip()
    username = request.POST.get('username').strip()
    email = request.POST.get('email').strip()
    password = request.POST.get('password').strip()
    phone = request.POST.get('phone').strip()
    category = request.POST.get('category').strip()


     
    if User.objects.filter(username=username.lower()).exists():
        status = 400
        message = "user is already exists"
        context = {
        "message":message,
        "status":status
        }
        return JsonResponse(context)
    

    registeruser=User.objects.create_user(
        username=username.lower(),is_active=False,password=password,email=email,
        first_name=first_name.lower(),last_name=last_name.lower())    

    user_id = registeruser.id
    try:
        if user_id > 0:
            user = User.objects.get(id=int(user_id))
            Profile.objects.create(user_ptr=user,content=category,phone=phone)
            message = "Successfully Registered"
            status = 200


            # Sending Email

            current_site = get_current_site(request)           

            ctx = {
                                    
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
                
            }
            subject = "Activate account - Contentbond"
            message = get_template('account/account_activation_email.html').render(ctx)
            msg = EmailMessage(
                    subject,
                    message,
                    'ContentBond <'+settings.EMAIL_HOST_USER+'>',
                    [email],
            )
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()


            # Sending Email
            
    except Exception as e:
        print(e)
        status = 200
        message = 'something is went wrong'

    context = {
        "message":message,
        "status":status
    }
    return JsonResponse(context)


@csrf_exempt
@api_view(['POST','GET'])
# @Admin Access
@permission_classes((AllowAny,))
def saveUser(request):
    error=False
    message=''
    user_id=''
    posts=''
    GETmethodData = []
    gropsarray = []
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        phone=request.POST['phone']
        usertype=request.POST['usertype']
        category=request.POST['usercategory']
        email=request.POST['email']
        
        if str(usertype) == "user":
            user_admin=User.objects.create_user(username=username.lower(),is_active=True,password=password,email=email)
        elif str(usertype) == "admin":
            user_admin=User.objects.create_superuser(username=username.lower(),is_active=True,is_staff=True,password=password,email=email)
        elif str(usertype) == "superuser":
            user_admin=User.objects.create_user(username=username.lower(),is_active=True,is_staff=True,password=password,is_superuser=True,email=email)
        try:
            user_id = user_admin.id
            print(user_admin)
            print(user_id)
            if user_id > 0:
                databaseDynamic = DatabaseDynamic(request)
                thisdict = {'user_ptr_id':user_id,'content':category,'phone':phone,'id':user_id}
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
                    
                    requser = User.objects.get(id=i['id'])
                    requsergroups = requser.groups.all()
                    for every in requsergroups:
                        gropsarray.append(every.name)
                    

                    

                    # productinstance = ProductGroup.objects.filter(id=grp.groupid).first()
                    i.update({'content':userinstance.content,'user_ptr':userinstance.user_ptr_id,'group':gropsarray})
                    # print('grop find')
                except:
                    # print(userinstance.user_ptr_id)
                    i.update({'content':userinstance.content,'user_ptr':userinstance.user_ptr_id})
            except:
                pass
            GETmethodData.append(i)
            gropsarray = []
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

@api_view(['POST','GET'])
def getsingleUser(request):
    isquery = request.GET.get('username')
    isUsertype = request.GET.get('usertype')
    isUsercontent = request.GET.get('usercontent')

    error=False
    message=''
    user_id=''
    posts=[]
    place =""
    GETmethodData = []


    # return JsonResponse({'query':len(isquery)})

    if len(isquery) > 0:
        place = 1
        posts = User.objects.filter(username__contains=str(isquery)).all()
        # if isUsertype == "all" and isUsercontent =="all":
        #     try:
        #         posts = User.objects.filter(username__contains=str(isquery)).all()
        #     except Exception as e:
        #         pass
                
        #     for i in posts.values():
        #         try:
        #             userinstance=Profile.objects.get(user_ptr=i['id'])            
        #             i.update({'content':userinstance.content,'user_ptr':userinstance.user_ptr_id})
        #         except:
        #             pass
        #         GETmethodData.append(i)
        
        # elif isUsertype !="all":
        #     try:
        #         if str(usertype) == "user":
        #             posts=User.objects.filter(username__contains=username.lower()).all()
        #         elif str(usertype) == "admin":
        #             posts=User.objects.filter(username__contains=username.lower(),is_staff=True).all()
        #         elif str(usertype) == "superuser":
        #             posts=User.objects.filter(username__contains=username.lower(),is_superuser=True).all()
                
        #     except Exception as e:
        #         pass
                
        #     for i in posts.values():
        #         try:
        #             userinstance=Profile.objects.get(user_ptr=i['id'])            
        #             i.update({'content':userinstance.content,'user_ptr':userinstance.user_ptr_id})
        #         except:
        #             pass
        #         GETmethodData.append(i)
        
        # elif isUsercontent !="all":
        #     try:
        #         posts=User.objects.filter(username__contains=username.lower()).all()                
                
        #     except Exception as e:
        #         pass
                
        #     for i in posts.values():
        #         try:
        #             userinstance=Profile.objects.get(user_ptr=i['id'],content=str(isUsercontent))            
        #             i.update({'content':userinstance.content,'user_ptr':userinstance.user_ptr_id})
        #         except:
        #             pass
        #         GETmethodData.append(i)
        # else:
        for i in posts.values():
            try:
                userinstance=Profile.objects.get(user_ptr=i['id'])            
                i.update({'content':userinstance.content,'user_ptr':userinstance.user_ptr_id})
            except:
                pass
            GETmethodData.append(i)


    elif len(isquery) <= 0:
        place = 2
        # return JsonResponse({"level":'is none' if isUsertype == "undefined" else 'no none' })
        if isUsertype == "all" and isUsercontent =="all":
            place = 3
            try:
                posts = User.objects.all()
            except Exception as e:
                pass
                
            for i in posts.values():
                try:
                    userinstance=Profile.objects.get(user_ptr=i['id'])            
                    i.update({'content':userinstance.content,'user_ptr':userinstance.user_ptr_id})
                    GETmethodData.append(i)
                except:
                    pass
                
        
        elif isUsertype !="all" and isUsertype != "undefined":
            place = 4
            try:
                if str(isUsertype) == "user":
                    posts=User.objects.all()
                elif str(isUsertype) == "admin":
                    posts=User.objects.filter(is_staff=True,is_superuser=False)
                elif str(isUsertype) == "superuser":
                    posts=User.objects.filter(is_superuser=True)
                
            except Exception as e:
                pass
                
            for i in posts.values():
                try:
                    userinstance=Profile.objects.get(user_ptr=i['id'])            
                    i.update({'content':userinstance.content,'user_ptr':userinstance.user_ptr_id})
                    GETmethodData.append(i)
                except:
                    pass
                
        
        elif isUsercontent !="all" and isUsercontent != "undefined":
            place = 5
            posts = User.objects.all()
            for i in posts.values():
                try:
                    userinstance=Profile.objects.get(user_ptr=i['id'],content=str(isUsercontent))            
                    i.update({'content':userinstance.content,'user_ptr':userinstance.user_ptr_id})
                    GETmethodData.append(i)
                except:
                    pass
                


    response={
        "place":place,
        'posts':str(posts),
        'isquery':isquery,
        'isUsertype':isUsertype,
        'isUsercontent':isUsercontent,
        'error':error,
        'message':message,
        'user_id':user_id,
        'GETmethodData':GETmethodData
            }
    return JsonResponse(response)

@csrf_exempt
@api_view(['POST','GET'])
# @ Admin Access
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
@api_view(['POST','GET'])
# @Admin Access
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

@csrf_exempt
@api_view(['POST'])
def UserUpdateActivate_Deactivate(request):
    error=False
    message=''
    user_id=''
    status = request.POST.get('status')
    itemlist = (request.POST.get('itemlist')).split(',')    
    if itemlist is not None:
        instanceuser = User.objects.filter(id__in=itemlist).update(is_active = True if status == 'activate' else False)
        
    response={
            'error':error,
            'message':message,
            'user_id':user_id
            }
    return Response(response)

@csrf_exempt
# @api_view(['POST','GET'])
# @permission_classes([AllowAny,])
def ResetPasswordMailer(request):
    # Sending Email
    # print(request.POST.get('email'))
    
    status = 200
    message = ''
    try:
        current_site = get_current_site(request)
        user = User.objects.get(email=request.POST.get('email'))
        
        subject = "Reset your Password"
        ctx = {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            }
        
        # user.email_user(subject=subject, message=message)

        message = get_template('account/resetpassword.html').render(ctx)
        msg = EmailMessage(
                subject,
                message,
                'Content Bond <'+settings.EMAIL_HOST_USER+'>',
                [request.POST.get('email')],
        )
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()

        context = {
            'token':account_activation_token.make_token(user),
            'status':status,
            'message':'Mail has been sent! Check your email'
        }
    except Exception as e:
        status = 400
        context = {
            'token':'',
            'status':status,
            'message':str(e)
        }

    return JsonResponse(context)

def ResetPasswordMailerConfirm(request,uidb64,token):
    error = ""
    if request.method == 'GET':
        try:
            # print(urlsafe_base64_decode(uidb64).decode())            
            uid =force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)   
            if user is not None and account_activation_token.check_token(user, token):
                           
                context = {
                    
                    'uidb64':uidb64,
                    'token':token,
                    'uid':uid,
                    'email':user.email
                }
                return render(request,'account/user/password_reset_form.html',context)
        except Exception as e:
            context = {
                'error':str(e)
            }
            return JsonResponse(context,safe=False)
    if request.method == 'POST':
        import re
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        request.POST._mutable = True
        finval = request.POST
        resetForm = PwdResetConfirmForm(request.POST)
        try:
            if resetForm.is_valid():
                
                
                user_email = resetForm.cleaned_data['user_email']
                user_password1 = resetForm.cleaned_data['new_password1']
                user_password2 = resetForm.cleaned_data['new_password2']

                if str(user_password1) == str(user_password2):                    
                    if (len(user_password1) >= 8):                        
                        if(regex.search(user_password1) == None):
                            messages.error(request, 'Should be include a special character')                            
                        else:
                            
                            current_site = get_current_site(request)
                            uid =force_text(urlsafe_base64_decode(uidb64))
                            user = User.objects.get(pk=uid,email=str(user_email))
                            if user is not None and account_activation_token.check_token(user, token):

                                user.set_password(user_password1)     
                                user.save()
                                ctx = {
                                    
                                    "user": user,
                                    "domain": current_site.domain
                                    
                                }
                                subject = "Successfully Password is Changed"
                                message = get_template('account/resetpasswordcompleted.html').render(ctx)
                                msg = EmailMessage(
                                        subject,
                                        message,
                                        'ContentBond <'+settings.EMAIL_HOST_USER+'>',
                                        [user_email],
                                )
                                msg.content_subtype = "html"  # Main content is now text/html
                                msg.send()
                                return redirect('authentication:ResetPasswordMailerComplete')
                    else:
                        messages.error(request, 'Password is should be minimum 8 characters length')

                else:
                    messages.error(request, 'Passwords are not same')    


                fialurl = '/auth/password_reset_confirm/{}/{}'.format(uidb64,token)
                return redirect(fialurl)
            else:
                return redirect(fialurl)
        except Exception as e:
            error = str(e)
        return JsonResponse({'error':error})


def ResetPasswordMailerComplete(request):
    return render(request,"PasswordChangedStatus.html")
def verifysendinblue(request):
    return render(request,'21f1efc09ed4fb65eaa4896bca0f323e.html')
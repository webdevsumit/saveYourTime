from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import (authenticate,login,logout)
import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token



from .models import (
    Logos,
    Images,
    ServicesCatagory,
    SearchName,
    Service,
    Feedbacks,
    Profile,
    UserProfile,
    ServiceFeedback,
    Plans,
    FrontPageFeedback,
    Messages,
    MessageBox,
    GroupMessages,
    FAQ,
    InterestedService,
)

from .serializers import (
    UserSerializer,
    LogosSerializer,
    ImagesSerializer,
    ServicesCatagorySerializer,
    SearchNameSerializer,
    ServiceSerializer,
    FeedbacksSerializer,
    ProfileSerializer,
    UserProfileSerializer,
    ServiceFeedbackSerializer,
    PlansSerializer,
    FrontPageFeedbackSerializer,
    MessagesSerializer,
    MessagesBoxSerializer,
    GroupMessagesSerializer,
    FAQSerializer,
    InterestedServiceSerializer,
)


def fetchingMessages(username,msgMan):
    ''' this function filter the data and sort it acording to id.'''
    data1 = Messages.objects.filter(SendBy = username,
    RecievedBy = msgMan)
    
    data2 = Messages.objects.filter(SendBy = msgMan,
    RecievedBy = username)

    data = []

    i=0
    j=0
    while (i<len(data1) and j<len(data2)):
        if data1[i].id<data2[j].id:
            data.append(data1[i])
            i+=1
        else:
            data.append(data2[j])
            j+=1

    while i<len(data1):
        data.append(data1[i])
        i+=1

    while j<len(data2):
        data.append(data2[j])
        j+=1
    
    return data




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logo(request):
    if request.method=='GET':
        data=LogosSerializer(Logos.objects.filter(active=True), 
        many=True, context={'request':request}).data
        return Response(data)

        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mainPageData(request):
    if request.method=='POST':
        data = {}
        data['ServiceCatagories']=ServicesCatagorySerializer(ServicesCatagory.objects.all(),
        many=True, context={'request':request}).data
        
        data['Plans']=PlansSerializer(Plans.objects.filter(Open=True),
        many=True, context={'request':request}).data
        
        data['FrontPageFeedback']=FrontPageFeedbackSerializer(FrontPageFeedback.objects.filter(Type='Good'),
        many=True, context={'request':request}).data


        if InterestedService.objects.filter(User__username=request.data['user']).exists():
        
            data['InterestedService']=InterestedServiceSerializer(InterestedService.objects.get(User__username=request.data['user']),
                    context={'request':request}).data

        else:
            data['InterestedService']={}
        
        return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FAQData(request):
    if request.method=='GET':
    
        data = FAQSerializer(FAQ.objects.all(),many=True).data

        return Response(data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def messageBox(request):
    if request.method=='POST':
        data = MessageBox.objects.filter(Username = request.data['Username'])
        return Response(MessagesBoxSerializer(data, many=True, context={'request':request}).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def messages(request):
    if request.method=='POST':
        
        updataData = MessageBox.objects.get(Username=request.data['Username'],
        MessagePartner=request.data['MessagePartner'])
        updataData.UnreadMessages=False
        updataData.save()

        data = fetchingMessages(request.data['Username'],request.data['MessagePartner'])
        
        return Response(MessagesSerializer(data, many=True, context={'request':request}).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addMessages(request):
    if request.method=='POST':
    
        dataToAdd = MessagesSerializer(data=request.data)
        if dataToAdd.is_valid():
            dataToAdd.create(dataToAdd.validated_data)
        
        data = fetchingMessages(request.data['SendBy'],request.data['RecievedBy'])

        updataData = MessageBox.objects.get(Username=request.data['RecievedBy'],
        MessagePartner=request.data['SendBy'])
        updataData.UnreadMessages=True
        updataData.save()
        
        return Response(MessagesSerializer(data, many=True, context={'request':request}).data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addNewSmsBox(request):
    if request.method=='POST':
    
        msg,created = MessageBox.objects.get_or_create(Username=request.data['user'],
        MessagePartner=request.data['provider'])
        msg.UnreadMessages=False
        msg.save()

        msg2,created2 = MessageBox.objects.get_or_create(Username=request.data['provider'],
        MessagePartner=request.data['user'])
        msg2.UnreadMessages=True
        msg2.save()

        return Response({'msg':'done'})



@api_view(['POST'])
def signup(request):
    if request.method=='POST':
        
        user_exist = User.objects.filter(username=request.data['username']).exists()
        if user_exist:
            return Response({'error':'Username already exist.'})

        serialized_data = UserSerializer(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            user = serialized_data.create(serialized_data.validated_data)
            user.set_password(request.data['password'])
            user.save()
            img_ = request.FILES.get('image')
            
            Profile_Image=Images.objects.create(Image=img_)
            Profile_Image.save()
            
            userprofile = UserProfile.objects.create(User=user,Image=Profile_Image,Address=request.data['Address'])
            userprofile.save()
            
            

            user_ = authenticate(serialized_data.validated_data)
            if user_ is not None:
                user_.last_login = datetime.datetime.now()
                user_.save()
                login(request,user_)
                            
            token, _  = Token.objects.get_or_create(user_id=user.id)
            return Response({"token": token.key})


@api_view(['POST'])
def signupAsProvider(request):
    if request.method=='POST':
        
        user_exist = User.objects.filter(username=request.data['username']).exists()
        if user_exist:
            return Response({'error':'Username already exist.'})

        user_data = UserSerializer(data=request.data)
        if user_data.is_valid(raise_exception=True):
            user = user_data.create(user_data.validated_data)

            img_ = request.FILES.get('image')
            
            Profile_Image=Images.objects.create(Image=img_)
            Profile_Image.save()
            

            profile = Profile.objects.create(User=user,
                                            Address=request.data['Address'],
                                            MobileNo=request.data['MobileNo'],
                                            Image=Profile_Image
                                            )
            profile.save()

            user_ = authenticate(user_data.validated_data)
            if user_ is not None:
                user.last_login = datetime.datetime.now()
                user.save()
                login(request,user_)
            
            token, _  = Token.objects.get_or_create(user_id=user.id)
            return Response({"token": token.key})

            

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.method=='GET':
        print('loging out!')
        return Response({'msg':'logout successfully.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addFeedback(request):
    if request.method=='POST':
        username = request.data['username']
        msg = request.data['msg']

        try:
            profile = Profile.objects.get(User__username=username)
        except:
            profile = UserProfile.objects.get(User__username=username)

        new_feed = Feedbacks.objects.create(User=username,Message=msg,Image=profile.Image)
        front_feed = FrontPageFeedback.objects.create(Feedback=new_feed)
        
        new_feed.save()
        front_feed.save()
        
        data = {}
        data['FrontPageFeedback']=FrontPageFeedbackSerializer(FrontPageFeedback.objects.filter(Type='Good'),
        many=True, context={'request':request}).data

        return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def account(request):
    if request.method=='POST':
        data={}

        try:
            profile = Profile.objects.get(User__username=request.data['username'])
            data['profile'] = ProfileSerializer(profile, context={'request':request}).data
            
        except:
            profile = UserProfile.objects.get(User__username=request.data['username'])
            data['profile'] = UserProfileSerializer(profile, 
                                context={'request':request}).data

        return Response(data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setFirstname(request):
    if request.method=='POST':
        user = User.objects.get(username=request.data['username'])


        user.first_name = request.data['firstname']
        user.save()


        data={}
        
        try:
            profile = Profile.objects.get(User__username=request.data['username'])
            data['profile'] = ProfileSerializer(profile, context={'request':request}).data
                    
        except:
            profile = UserProfile.objects.get(User__username=request.data['username'])
            data['profile'] = UserProfileSerializer(profile, 
                                        context={'request':request}).data
        return Response(data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setLastname(request):
    if request.method=='POST':
        user = User.objects.get(username=request.data['username'])


        user.last_name = request.data['lastname']
        user.save()


        data={}
        
        try:
            profile = Profile.objects.get(User__username=request.data['username'])
            data['profile'] = ProfileSerializer(profile, context={'request':request}).data
                    
        except:
            profile = UserProfile.objects.get(User__username=request.data['username'])
            data['profile'] = UserProfileSerializer(profile, 
                                        context={'request':request}).data
        return Response(data)
        
 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setEmail(request):
    if request.method=='POST':
        user = User.objects.get(username=request.data['username'])


        user.email = request.data['email']
        user.save()


        data={}
        
        try:
            profile = Profile.objects.get(User__username=request.data['username'])
            data['profile'] = ProfileSerializer(profile, context={'request':request}).data
                    
        except:
            profile = UserProfile.objects.get(User__username=request.data['username'])
            data['profile'] = UserProfileSerializer(profile, 
                                        context={'request':request}).data
        return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setMyAddr(request):
    if request.method=='POST':
        data={}

        try:
            profile = Profile.objects.get(User__username=request.data['username'])
            profile.Address = request.data['Address']
            profile.save()
            data['profile'] = ProfileSerializer(profile, context={'request':request}).data
            
        except:
            profile = UserProfile.objects.get(User__username=request.data['username'])
            profile.Address = request.data['Address']
            profile.save()
            data['profile'] = UserProfileSerializer(profile, 
                                context={'request':request}).data

        return Response(data)
        




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setMyNo(request):
    if request.method=='POST':
        data={}

        try:
            profile = Profile.objects.get(User__username=request.data['username'])
            profile.MobileNo = request.data['MobileNo']
            profile.save()
            data['profile'] = ProfileSerializer(profile, context={'request':request}).data
            
        except:
            profile = UserProfile.objects.get(User__username=request.data['username'])
            profile.MobileNo = request.data['MobileNo']
            profile.save()
            data['profile'] = UserProfileSerializer(profile, 
                                context={'request':request}).data

        return Response(data)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setShopName(request):
    if request.method=='POST':
        service = Service.objects.get(id=request.data['id'])


        service.ShopName = request.data['ShopName']
        service.VStatus = False
        service.save()


        data={}
        
        profile = Profile.objects.get(User__username=request.data['username'])
        data['profile'] = ProfileSerializer(profile, context={'request':request}).data
                    
        return Response(data)
        
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ShopCatagories(request):
    if request.method=='GET':

        data = {}
        data['data']=ServicesCatagorySerializer(ServicesCatagory.objects.all(), 
        many=True,context={'request':request}).data

        return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateShopCatagory(request):
    if request.method=='POST':
        service = Service.objects.get(id=request.data['serviceId'])
        service.VStatus = False

        serviceCatagory = ServicesCatagory.objects.get(id=request.data['catagoryId'])

        service.Type=serviceCatagory
        service.save()

        data={}
                
        profile = Profile.objects.get(User__username=request.data['username'])
        data['profile'] = ProfileSerializer(profile, context={'request':request}).data
                            
        return Response(data)
        


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateMainImage(request):
    if request.method=='POST':
    
        service = Service.objects.get(id=request.data['id'])

        service.MainImage = request.FILES.get('image')
        service.save()

        data={}
                
        profile = Profile.objects.get(User__username=request.data['username'])
        data['profile'] = ProfileSerializer(profile, context={'request':request}).data
                            
        return Response(data)
        



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateImage(request):
    if request.method=='POST':
    
        img = Images.objects.get(id=request.data['id'])

        img.Image = request.FILES.get('image')
        img.save()

        data={}
                
        profile = Profile.objects.get(User__username=request.data['username'])
        data['profile'] = ProfileSerializer(profile, context={'request':request}).data
                            
        return Response(data)
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addNewImage(request):
    if request.method=='POST':
    
        service = Service.objects.get(id=request.data['id'])

        img = Images.objects.create(Image=request.FILES.get('image'))

        service.ServiceImages.add(img)

        service.save()
        img.save()


        data = {}

        profile = Profile.objects.get(User__username=request.data['username'])
        data['profile'] = ProfileSerializer(profile, context={'request':request}).data

        return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setOpenTime(request):
    if request.method=='POST':
    
        service = Service.objects.get(id=request.data['id'])

        service.OpenTime = request.data['openTime']
        service.save()

        data={}
                
        profile = Profile.objects.get(User__username=request.data['username'])
        data['profile'] = ProfileSerializer(profile, context={'request':request}).data
                            
        return Response(data)
        


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setCloseTime(request):
    if request.method=='POST':
    
        service = Service.objects.get(id=request.data['id'])

        service.closeTime = request.data['closeTime']
        service.save()

        data={}
                
        profile = Profile.objects.get(User__username=request.data['username'])
        data['profile'] = ProfileSerializer(profile, context={'request':request}).data
                            
        return Response(data)
        


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setPriceType(request):
    if request.method=='POST':
    
        service = Service.objects.get(id=request.data['id'])

        service.PriceType = request.data['priceType']
        service.save()

        data={}
                
        profile = Profile.objects.get(User__username=request.data['username'])
        data['profile'] = ProfileSerializer(profile, context={'request':request}).data
                            
        return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteSearchName(request):
    if request.method=='POST':
    
        searchName = SearchName.objects.get(id=request.data['id'])
        searchName.delete()

        data={}
            
        profile = Profile.objects.get(User__username=request.data['username'])
        data['profile'] = ProfileSerializer(profile, context={'request':request}).data
                            
        return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteImage(request):
    if request.method=='POST':
    
        img = Images.objects.get(id=request.data['id'])
        img.delete()

        data={}
                
        profile = Profile.objects.get(User__username=request.data['username'])
        data['profile'] = ProfileSerializer(profile, context={'request':request}).data
        return Response(data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addSearchName(request):
    if request.method=='POST':
    
        searchName = SearchName.objects.create(Name=request.data['searchName'].upper())
        service = Service.objects.get(id=request.data['serviceId'])
        service.SearchNames.add(searchName)
        searchName.save()
        service.save()

        data={}
                
        profile = Profile.objects.get(User__username=request.data['username'])
        data['profile'] = ProfileSerializer(profile, context={'request':request}).data

        return Response(data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addNewService(request):
    if request.method=='POST':
    
        catagory = ServicesCatagory.objects.get(id=request.data['catagoryId'])
        
        service = Service.objects.create(
                MainImage=request.FILES.get('MainImage'),
                ShopName=request.data['ShopName'],
                Type=catagory,
                OpenTime=request.data['OpenTime'],
                closeTime=request.data['CloseTime'],
                PriceType=request.data['PriceType']
        )
        service.save()

        data={}
                
        profile = Profile.objects.get(User__username=request.data['username'])
        profile.Service.add(service)
        data['profile'] = ProfileSerializer(profile, context={'request':request}).data
        profile.save()
                            
        return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search(request):
    searchName = request.data['searchName'].upper()

    s_data = {}
    
    s_data['data'] = ServiceSerializer(Service.objects.filter(SearchNames__Name=searchName), many=True, 
    context={'request':request}).data

    return Response(s_data)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def productData(request):

    data={}
    service = Service.objects.get(id=request.data['productId'])
    data['data']=ServiceSerializer(service,
    context={'request':request}).data

    data['providerDetail']=ProfileSerializer(Profile.objects.get(
        Service__id=request.data['productId']
    ), context={'request':request}).data

    user = User.objects.get(username=request.data['Username'])
    
    IService = InterestedService.objects.filter(User__username=request.data['Username']).exists()
    if IService:
        IService1 = InterestedService.objects.get(User__username=request.data['Username'])

    else:
        IService1 = InterestedService.objects.create(User=user)

    IService1.Services.add(service)
    IService1.save()
    
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def giveRating(request):
    if request.method=='POST':

        service_exist = Service.objects.filter(RatedBy__username=request.data['user']).exists()

        if service_exist:
            return Response({'msg':'You have already rated that.'})

        service = Service.objects.get(id=request.data['productId'])
        user = User.objects.get(username=request.data['user'])

        service.Rating = ( service.Rating + (int(request.data['rating']))/10)/2

        
        service.RatedBy.add(user)
        service.save()


        data={}
        data['data']=ServiceSerializer(Service.objects.get(id=request.data['productId']),
        context={'request':request}).data
        
        data['providerDetail']=ProfileSerializer(Profile.objects.get(
            Service__id=request.data['productId']
        ), context={'request':request}).data

        return Response(data)
        


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addServiceFeed(request):
    if request.method=='POST':


        feed = ServiceFeedback.objects.create(
            Username=request.data['user'],
            Message=request.data['feed']
        )

        service = Service.objects.get(id=request.data['productId'])

        service.ServiceFeedback.add(feed)
        service.save()
        feed.save()



        data={}
        data['data']=ServiceSerializer(Service.objects.get(id=request.data['productId']),
        context={'request':request}).data
                
        data['providerDetail']=ProfileSerializer(Profile.objects.get(
            Service__id=request.data['productId']
        ), context={'request':request}).data
        
        return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateDesc(request):
    if request.method=='POST':


        service = Service.objects.get(id=request.data['serviceId'])
        service.VStatus = False
        
        service.Description = request.data['desc']
        service.save()
        
        data={}
                        
        profile = Profile.objects.get(User__username=request.data['username'])
        data['profile'] = ProfileSerializer(profile, context={'request':request}).data
                                    
        return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def removeItem(request):
    if request.method=='POST':


        service = Service.objects.get(id=request.data['id'])

        IService = InterestedService.objects.get(User__username=request.data['user'])

        IService.Services.remove(service)

        IService.save()

        data ={}

        data['InterestedService']=InterestedServiceSerializer(IService,
            context={'request':request}).data

        return Response(data)







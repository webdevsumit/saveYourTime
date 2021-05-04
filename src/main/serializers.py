from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import (
    Logos,
    Images,
    ServicesCatagory,
    SearchName,
    PostCommentsReplies,
    PostComments,
    Post,
    Service,
    Feedbacks,
    Profile,
    ServiceFeedback,
    Plans,
    FrontPageFeedback,
    Messages,
    MessageBox,
    GroupMessages,
    FAQ,
    InterestedService,
    TotalHits,
    TotalHitsPerPersonPerDay,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        )
        extra_kwargs={
            'password':{'write_only':True}
        }

        def create(self, data):
            v_password = data['password']
            user = super().create(data)
            user.set_password(v_password)
            print('password is here --',v_password)
            user.save()
            return user

        def update(self, instance, data):
            user = super().update(instance, data)
            try:
                user.set_password(data['password'])
                user.save()
            except:
                pass
            return user



class LogosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logos
        fields = '__all__'

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'


class ServicesCatagorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicesCatagory
        fields = ('id','Name','Image','Description')


class SearchNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchName
        fields = '__all__'

class FeedbacksSerializer(serializers.ModelSerializer):
    Image = ImagesSerializer()
    class Meta:
        model = Feedbacks
        fields = '__all__'

class ServiceFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFeedback
        fields = '__all__'

class PostCommentsRepliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCommentsReplies
        fields = ('id', 'Username', 'Reply')

class PostCommentsSerializer(serializers.ModelSerializer):
    Replies = PostCommentsRepliesSerializer(many=True)
    class Meta:
        model = PostComments
        fields = ('id', 'Username', 'Comment', 'Replies')

class PostSerializer(serializers.ModelSerializer):
    Comments = PostCommentsSerializer(many=True)
    LikedBy = UserSerializer(many=True)
    class Meta:
        model = Post
        fields = ('id', 'Image', 'HasImage', 'Tittle', 'Media', 'Text', 'TotalLikes', 'LikedBy',
                    'Comments', 'Activated')


class ServiceSerializer(serializers.ModelSerializer):
    RatedBy = UserSerializer(many=True)
    ServiceImages = ImagesSerializer(many=True)
    Type = ServicesCatagorySerializer()
    SearchNames = SearchNameSerializer(many=True)
    ServiceFeedback = ServiceFeedbackSerializer(many=True)
    Posts = PostSerializer(many=True)
    class Meta:
        model = Service
        fields = '__all__'


class ServiceSerializerForMainPage(serializers.ModelSerializer):
    Type = ServicesCatagorySerializer()
    class Meta:
        model = Service
        fields = ('id','Rating', 'Type', 'MainImage', 'ShopName', 'PriceType',
                 'OpenTime', 'closeTime','VStatus','RentalStatus')


class ServiceSerializerForPost(serializers.ModelSerializer):
    Posts = PostSerializer(many=True)
    class Meta:
        model = Service
        fields = ('id', 'ShopName','VStatus','Posts','RentalStatus')



class ProfileSerializer(serializers.ModelSerializer):
    User = UserSerializer()
    Image = ImagesSerializer()
    Service = ServiceSerializer(many=True)
    LastCategory = ServicesCatagorySerializer()
    LastProductTags = SearchNameSerializer(many=True)
    SavedServices = ServiceSerializer(many=True)
    class Meta:
        model = Profile
        fields = '__all__'


class InterestedServiceSerializer(serializers.ModelSerializer):
    User = UserSerializer()
    Services = ServiceSerializerForMainPage(many=True)
    class Meta:
        model = InterestedService
        fields = '__all__'
    

class PlansSerializer(serializers.ModelSerializer):
    PlanServices = ServiceSerializerForMainPage(many=True)
    class Meta:
        model = Plans
        fields = ( 'PlanName', 'Description', 'Rate', 'Open', 'PlanServices')

class FrontPageFeedbackSerializer(serializers.ModelSerializer):
    Feedback = FeedbacksSerializer()
    class Meta:
        model = FrontPageFeedback
        fields = '__all__'


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'

        def create(self,validated_data):
            Messages.object.create(request.data)
            Message.save()

class MessagesBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageBox
        fields = '__all__'
        

class GroupMessagesSerializer(serializers.ModelSerializer):
    Messages = MessagesSerializer(many=True)
    class Meta:
        model = GroupMessages
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class TotalHitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TotalHits
        fields = '__all__'

class TotalHitsPerPersonPerDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TotalHitsPerPersonPerDay
        fields = '__all__'











from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings


# Create your models here.

class Images(models.Model):
    Image = models.ImageField(upload_to='images')


class ServicesCatagory(models.Model):
    Name = models.CharField(max_length = 300)
    Image = models.ImageField(upload_to='catagoryImages')
    Description = models.TextField()

    def __str__(self):
        return self.Name

        
class SearchName(models.Model):
    Name = models.CharField(max_length=2000)

    def __str__(self):
        return self.Name


class Feedbacks(models.Model):
    User  = models.CharField(max_length=1000)
    Message = models.TextField()
    Date = models.DateField(auto_now=True)
    Image = models.ForeignKey(Images, on_delete=models.CASCADE,blank=True, 
                                                    null=True, unique=False)

    def __str__(self):
        return self.User


class ServiceFeedback(models.Model):
    Username = models.CharField(max_length=900)
    Message = models.TextField()
    Date = models.DateField(auto_now=True)

    def __str__(self):
        return self.Username
        

class PostCommentsReplies(models.Model):
    Username = models.CharField(max_length=1000)
    Reply = models.TextField()

    def __str__(self):
        return self.Username

class PostComments(models.Model):
    Username = models.CharField(max_length=1000)
    Comment = models.TextField()
    Replies = models.ManyToManyField(PostCommentsReplies, blank=True)

    def __str__(self):
        return self.Username

class Post(models.Model):
    Image = models.ImageField(upload_to='postImages', null=True, blank=True)
    HasImage = models.BooleanField()
    Tittle = models.TextField()
    Media = models.FileField(upload_to='Posts', blank = True)
    Text = models.TextField()
    TotalLikes = models.IntegerField(default=0)
    LikedBy = models.ManyToManyField(User, blank=True)
    Comments = models.ManyToManyField(PostComments, blank=True)
    Activated = models.BooleanField(default=True)

    def __str__(self):
        return self.Tittle


class Service(models.Model):
    Rating = models.FloatField(default=3)
    RatedBy = models.ManyToManyField(User, blank=True)
    ServiceImages = models.ManyToManyField(Images, blank=True)
    MainImage = models.ImageField(upload_to='serviceMainImages')
    ShopName = models.CharField(max_length = 3000)
    Type = models.ForeignKey(ServicesCatagory, on_delete=models.CASCADE)
    PriceType = models.CharField(max_length = 300)
    SearchNames = models.ManyToManyField(SearchName, blank=True)
    OpenTime = models.CharField(max_length = 300)
    closeTime = models.CharField(max_length = 300)
    ServiceFeedback = models.ManyToManyField(ServiceFeedback, blank=True)
    Description = models.TextField(default='Description box is empty.')
    VStatus = models.BooleanField(default=False)
    RentalStatus = models.BooleanField(default=True)
    NoOfItems = models.IntegerField(default=1)
    Address = models.TextField(default='0')
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)

    Posts = models.ManyToManyField(Post, blank=True)
    Activated = models.BooleanField(default=True)
            
    def __str__(self):
        return self.ShopName


class Profile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    Image = models.OneToOneField(Images, on_delete=models.CASCADE,blank=True, null=True)
    Address = models.TextField()
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    MobileNo = models.CharField(max_length=20)
    
    LastCategory = models.ForeignKey(ServicesCatagory, on_delete=models.SET_NULL,blank=True, null=True,
             primary_key=False, unique=False)
    LastSearcheTag = models.TextField(default='RENTYUG')
    LastProductTags = models.ManyToManyField(SearchName,blank=True)
    LastSearchNotFound = models.TextField(default='RENTYUG')
    SavedServices = models.ManyToManyField(Service, blank=True, 
        related_name = 'SavedServices+')

    Service = models.ManyToManyField(Service, blank=True)
    

    def __str__(self):
        return self.User.username


class InterestedService(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    Services = models.ManyToManyField(Service, blank=True)

    def __str__(self):
        return self.User.username



class Plans(models.Model):
    PlanName = models.CharField(max_length=900)
    Description = models.TextField()
    Rate = models.CharField(max_length=500)
    Open = models.BooleanField(default=False)
    PlanServices = models.ManyToManyField(Service, blank=True)

    def __str__(self):
        return self.PlanName


class FrontPageFeedback(models.Model):
    Type = models.CharField(max_length=100, default='Normal')
    Feedback = models.OneToOneField(Feedbacks, on_delete=models.CASCADE)

    def __str__(self):
        return self.Type

class Messages(models.Model):
    SendBy = models.CharField(max_length=2000)
    Message = models.TextField()
    RecievedBy = models.CharField(max_length=2000)
    DateTime = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.SendBy

class MessageBox(models.Model):
    Username = models.CharField(max_length=2000)
    MessagePartner = models.CharField(max_length=2000)
    UnreadMessages = models.BooleanField(default=True)

    def __str__(self):
        return self.Username
    

class FAQ(models.Model):
    Q = models.TextField()
    A = models.TextField()

    def __str__(self):
        return self.Q

        

class TotalHits(models.Model):
    Hits = models.IntegerField(default=0)

    def __str__(self):
        return str(self.Hits)


class TotalHitsPerPersonPerDay(models.Model):
    Username = models.CharField(max_length=1000)
    Hits = models.IntegerField(default=0)
    Date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.Date )+'     -->'+str(self.Hits)

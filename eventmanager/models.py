from django.db import models
from django.core.mail import send_mail
import datetime

class User(models.Model):
  email=models.EmailField(primary_key=True)
  first_name=models.CharField(max_length=255,null=True,blank=True)
  last_name=models.CharField(max_length=255,null=True,blank=True)
  profile_image=models.ImageField(upload_to="users/",null=True,blank=True)
  phone=models.CharField(max_length=20,null=True,blank=True)
  
  def __str__(self):
      return self.email

class Login(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    password=models.CharField(max_length=255)

    def __str__(self):
      return self.user.email

class Event(models.Model):
    title=models.TextField()
    time_posted=models.DateTimeField(auto_now=True)
    event_date=models.DateTimeField(default=datetime.datetime.now)
    description=models.TextField()
    cover_photo=models.ImageField(upload_to='events/',null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.ManyToManyField("EventCategories",null=True)
    subcategory=models.ManyToManyField("EventSubcategories",null=True)

    def __str__(self):
      return self.title

class EventCategories(models.Model):
       name=models.CharField(max_length=255)
       description=models.TextField(null=True,blank=True)

       def __str__(self):
        return self.name

class EventSubcategories(models.Model):
    name=models.CharField(max_length=255)
    categrory=models.ManyToManyField(EventCategories)

    def __str__(self):
      return self.name

class UserEvents(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    def __str__(self):
      return self.event.user.email

class Advertisements(models.Model):
   title=models.TextField(blank=True,null=True)
   description=models.TextField(blank=True,null=True)
   image=models.ImageField(upload_to="advertisements/")
 
class Messages(models.Model):
   user=models.ForeignKey(User,on_delete=models.CASCADE)
   date=models.DateField(auto_now=True)
   message=models.TextField()


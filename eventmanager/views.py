from django.core.checks import messages
from django.db.models.expressions import F
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render
from .models import Advertisements, User,Login,Event,EventCategories,EventSubcategories, UserEvents,Messages
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
from django.conf import settings
def homeView(request):
    categories=EventCategories.objects.all()
    mainslider_images=Event.objects.all()
    adverts=Advertisements.objects.all()
    # sports=
   
    return render(request,"eventmanager/home.html",{"categories":categories,"mainslider_images":mainslider_images,"adverts":adverts,})

def login(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")

        if email and password:
            try:
                u=User.objects.get(email=email)
                try:
                  l=Login.objects.get(user=u,password=password)
                  return HttpResponseRedirect(reverse("eventmanager:dashboard",args=(email,)))
                except Login.DoesNotExist:
                  error_message="Email or Password incorrect. Try Again using Valid Credentials" 
                  return render(request,"eventmanager/login.html",{"error":error_message,}) 
            except User.DoesNotExist:
                error_message="Not Such User Exists. Try Again Using Valid Credentials."
                return render(request,"eventmanager/login.html",{"error":error_message,})

    return render(request,"eventmanager/login.html")

def signup(request):
    if request.method=="POST":
        email=request.POST.get("email")
        passrd=request.POST.get("password")
        print(email,passrd)
        try:
            u=User.objects.get(email=email)
            if u:
                error_message="user already exists, reset passowrd or create a new account with another email"
                return render(request,"eventmanager/signup.html",{"error":error_message,})
        except:
      
            try:
               u=User(email=email)
               u.save()
               l=Login(user=u,password=passrd)
               l.save()
               
               sendMail(request,"alexmuthini3@gmail.com",email,"Account Creation",'''Dear Customer We appreciate registering With
                our platform. Use it to post your events to reach your intended Audience and to reach more people.'''
                  )
               return HttpResponseRedirect(reverse("eventmanager:dashboard",args=(email,)))
            except:
                error_message="Error creating account, try again registring and make sure to use valid email"
                return render(request,"eventmanager/signup.html",{"error":error_message,})

    return render(request,"eventmanager/signup.html")

def dashboard(request,user_email):
   
    try:
      user=User.objects.get(email=user_email)
      categories=EventCategories.objects.all()
      subcategories=EventSubcategories.objects.all()
      messages=Messages.objects.filter(user=user)
      # planningToAttend=UserEvents.objects.filter(user=user)
      # yourEvenBookings=UserEvents.objects.filter(event__user__email=user_email)
      eventcategories={}
      for c in categories:
        eventcategories[c.name]=c.event_set.all()

      planningToAttend={}
      for c in EventCategories.objects.all():
        planningToAttend[c.name]=UserEvents.objects.filter(user=user)
      yourEvenBookings={}
      for c in EventCategories.objects.all():
        yourEvenBookings[c.name]=UserEvents.objects.filter(event__user=user)
      userevents={}
      for c in EventCategories.objects.all():
          userevents[c.name]=c.event_set.filter(user=user)   
      try:
        profile_image=user.profile_image.url
        return render(request,"eventmanager/dashboard.html",
        {"user":user,"profile_image":profile_image,"userevents":userevents,
        "categories":categories,"subcategories":subcategories,"planningtoattend":planningToAttend,
        "youreventbookings":yourEvenBookings,"eventcategories":eventcategories,"messages":messages,})
      except:
        return render(request,"eventmanager/dashboard.html",
        {"user":user,"userevents":userevents,"categories":categories,
        "subcategories":subcategories,"planningtoattend":planningToAttend,"youreventbookings":yourEvenBookings,"eventcategories":eventcategories,"messages":messages,})

    except User.DoesNotExist:
      return render(request,"eventmanager/dashboard.html")
    
    return render(request,"eventmanager/dashboard.html")

def updateProfile(request,user_email):
  if request.method=="POST":
     firsName=request.POST.get("first_name")
     lastname=request.POST.get("last_name")
     email=request.POST.get("email")
     phone=request.POST.get("phone")
     profile_image=request.FILES.get("profile_image")
    
     try:
        u=User(first_name=firsName,last_name=lastname,email=email,phone=phone,profile_image=profile_image)
        u.save()
        m=Messages(user=u,message="Successfully Updated your profile details.")
        m.save()
        return HttpResponseRedirect(reverse("eventmanager:dashboard",args=(email,)))
     except :
       error="Error updating your account. Try again!"
       return render(request,"eventmanager/dashboard.html",{"error":error,})
       
  return render(request,"eventmanager/dashboard.html")
   


def sendMail(request,sender_email,recepients_emails,subject,message):
  try:
    sender=User.objects.get(email=sender_email)
    recepients=recepients_emails.split(",")
    print("send mail func")
    print(sender,recepients,subject,message)
    try:
      send_mail(subject,message,sender,recepients,fail_silently=False)
      return JsonResponse({"message":"send successfully"},safe=False)
    except:
      return JsonResponse({"message":"not send successfully"},safe=False)
    

  except User.DoesNotExist:
    print("not send")
    return HttpResponse("Not send")

def uploadEvent(request,user_email):
    if request.method=="POST":
        
        title=request.POST.get("title")
        description=request.POST.get("description")
        category=request.POST.getlist("category")
        subcategory=request.POST.getlist("subcategory")
        coverphoto=request.FILES.get("cover_photo")
        print("cover_photo",coverphoto)
        try: 
          coverphoto=request.FILES["cover_photo"]
        except:
          coverphoto=None
        try:
          u=User.objects.get(email=user_email)
          categories=EventCategories.objects.all()
          subcategories=EventSubcategories.objects.all()
          planningToAttend=UserEvents.objects.filter(user=u)
          yourEvenBookings=UserEvents.objects.filter(event__user__email=user_email)
          event=Event(title=title,description=description,cover_photo=coverphoto,user=u)
          event.save()
          m=Messages(user=u,message="Uploaded a new Event.")
          m.save()
          for ck in category:
            c=EventCategories.objects.get(pk=ck)
            event.category.add(c)
         
          for sk in subcategory:
             sb=EventSubcategories.objects.get(pk=sk)
             event.subcategory.add(sb)
          userevents={}
          for c in EventCategories.objects.all():
             userevents[c.name]=c.event_set.filter(user=u)   
          try:
            profile_image=u.profile_image.url
            return HttpResponseRedirect(reverse("eventmanager:dashboard",args=(user_email,)))
            # return render(request,"eventmanager/dashboard.html",{"user":u,"profile_image":profile_image,"userevents":userevents,"categories":categories,"subcategories":subcategories,"planningtoattend":planningToAttend,"youreventbookings":yourEvenBookings,})
          except:
            return HttpResponseRedirect(reverse("eventmanager:dashboard",args=(user_email,)))
            #  return render(request,"eventmanager/dashboard.html",{"user":u,"userevents":userevents,"categories":categories,"subcategories":subcategories,"planningtoattend":planningToAttend,"youreventbookings":yourEvenBookings,})


        except User.DoesNotExist:
           return render(request,"eventmanager/home.html")
        return render(request,"eventmanager/dashboard.html",{"user":u,})

def deletePost(request):
     eventId=request.POST.get("event_id")
     try:
       e=Event.objects.get(pk=eventId)
       e.delete()
      
       return JsonResponse({"data":"deleted Successfully"})
     except:
       return JsonResponse({"data":"Could not delete the requested event. Try again"})

def updatePost(request):
   eventId=request.POST.get("event_id")
   eventTitle=request.POST.get("event_title")
   eventDescription=request.POST.get("event_description")
   eventDate=request.POST.get("event_date")
   eventCategory=request.POST.get("event_category").split(",")
   eventSubcategory=request.POST.get("event_subcategory").split(",")
  #  coverphoto=request.FILES.get("cover_photo")
   print("event_id:",eventId,"title: ",eventTitle,"eventDesc: ",eventDescription,"eventDate: ",eventDate)
   try: 
     print("getting Event: ")
     event=Event.objects.get(pk=eventId)
     print("Event: ",event)
     event.title=eventTitle
     event.description=eventDescription
     event.event_date=eventDate
     event.save()
     for c in eventCategory:
        ca=EventCategories.objects.get(pk=c)
        print("category: ",ca)
        event.category.add(ca)
     for c in eventSubcategory:
        ca=EventSubcategories.objects.get(pk=c)
        print("subcategory: ",ca)
        event.subcategory.add(ca)
     print("new Event: ",event)
     return JsonResponse({"data":True})
   except:
    return JsonResponse({"data":False})

def getCategories(request):
   categories=[[c.pk,c.name] for c in EventCategories.objects.all()]
  
   return JsonResponse({"data":categories},safe=False)

def getSubCategories(request):
   subcategories=[[c.pk,c.name] for c in EventSubcategories.objects.all()]
   return JsonResponse({"data":subcategories},safe=False)

def getEventImage(request):
  eventId=request.GET.get("event_id")
  try:
    event=Event.objects.get(pk=eventId)
    imageurl=event.cover_photo.url
    return JsonResponse({"data":imageurl},safe=False)
  except:
    return JsonResponse({"data":"Not Found"})


def deleteMessage(request):
   messageId=request.POST["message_id"]
   try:
      msg=Messages.objects.get(pk=messageId)
      msg.delete()
      return JsonResponse({"data":"Deleted Message Successfully.."})
   except:
     return JsonResponse({"data":"Could not delete the message."})

def bookEvent(request):
  eventId=request.POST.get("event_id")
  userEmail=request.POST.get("user_email")
  print("event_id: ",eventId," useremail: ",userEmail)
  try:
    e=Event.objects.get(pk=eventId)
    u=User.objects.get(email=userEmail)
    ue=UserEvents(user=u,event=e)
    ue.save()
    m=Messages(user=u,message="Booked to attent an event.")
    m.save()
    return JsonResponse({"data":"Successfully added {0} to be held on {1} to your event list".format(e.title,e.event_date)})
  except:
    return JsonResponse({"data":"unable to add the requested event to your event list. Try Again."})

def testMail(request):
  if request.method == "POST":
      sendMail(request,request.POST.get("sender"),request.POST.get("user_emails"),request.POST.get("subject"),request.POST.get("message"))
      return JsonResponse({"success":True},safe=False)

  return JsonResponse({"success":False},safe=False)
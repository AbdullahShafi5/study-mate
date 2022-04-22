from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model): # a topic can have multiple room but a room can only have one topic
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


#room section
class Room(models.Model):
    host= models.ForeignKey(User, on_delete=models.SET_NULL, null =True) 
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null =True) 
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User,related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) # difference between auto_now_add and auto_now is  auto_now 
    # something else                                  # update every time we make some changes but auto_now_add only take a span shot of the time when it has created
    class Meta:
        ordering = ['-updated','-created'] #this is for showing the latest post


    def __str__(self):
        return self.name

# Everything below(including Topic class from the top) is the part of the main class Room and this is something what we call relationa Database


#message section
class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering= ['-updated','-created']

    def __str__(self):
        return self.body[0:50] #returning only the first 50 character of the body


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
import shortuuid
# Create your models here.

class User(AbstractUser):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True, max_length=254)
    full_name = models.CharField(max_length=100 , null=True , blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) :
        return self.username
    # WHAT HAPPEND HERE ***********************************************
    def save(self, *args , **kwargs):
        email_username , mobile = self.email.split("@")
        if self.full_name == "" or self.full_name == None:
            self.full_name = email_username
        if self.username == "" or self.username == None:
            self.username == email_username
        super(User, self).save(*args, **kwargs)
    # END WHAT HAPPEND HERE ***********************************************

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="image", default="default/default-user.jpg",null=True,blank=True)
    full_name = models.CharField(max_length=50,null=True,blank=True)
    bio = models.CharField(max_length=100 ,null=True,blank=True)
    about = models.CharField(max_length=100 ,null=True,blank=True)
    auther = models.BooleanField(default=False)
    country = models.CharField(max_length=100 ,null=True,blank=True)
    facebook = models.CharField(max_length=100 ,null=True,blank=True)
    twitter = models.CharField(max_length=100 ,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    def save(self, *args , **kwargs):
        if self.full_name == "" or self.full_name == None:
            self.full_name = self.user.full_name
        super(Profile, self).save(*args , **kwargs)



# WHAT HAPPEND HERE ***********************************************
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_use_profile(sender,instance,**kwargs):
    instance.profile.save()
    
post_save.connect(create_user_profile,sender=User)
post_save.connect(save_use_profile,sender=User)
# END WHAT HAPPEND HERE ***********************************************
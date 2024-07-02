from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from api import models as api_models

############################### Need Explain

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls,user):

        token = super().get_token(user)
        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username
        
        return token
############################# To Here

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True , required = True , validators=[validate_password])
    password2 = serializers.CharField(write_only = True , required = True , validators=[validate_password])

    class Meta:
        model = api_models.User
        fields = ['full_name','email','password','password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Password fields didn't match."})
        return attrs

    ############################### Need Explain
    def create(self ,validated_data):
        user = api_models.User.objects.create(
            full_name = validated_data['full_name'],
            email = validated_data['email']
        )
        email_username , mobile = user.email.split("@")
        user.username = email_username
        user.set_password(validated_data['password'])
        user.save()
        
        return user
    ############################# To Here

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.User
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Profile
        fields ='__all__'


    ######################## Need Explain

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['user'] = UserSerializer(instance.user).data
    #     return response

    ######################## To Here

class CategorySerialize(serializers.ModelSerializer):

    #################### Need explation
    def get_post_count(self,category):
        return category.posts.count()
    ################### To Here
    class Meta:
        model = api_models.Category
        fields = ['id','title','image','slug','post_count']

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = api_models.Comment
        fields = '__all__'

    ##################### need explain
    def __init__(self,*args, **kwargs):
        super(CommentSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1
    ######################## to here




class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = api_models.Post
        fields = '__all__'

    ##################### need explain
    def __init__(self,*args, **kwargs):
        super(PostSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1
    ######################## to here


class BookmarkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = api_models.Bookmark
        fields = '__all__'

    ##################### need explain
    def __init__(self,*args, **kwargs):
        super(BookmarkSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1
    ######################## to here



class NotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = api_models.Notification
        fields = '__all__'

    ##################### need explain
    def __init__(self,*args, **kwargs):
        super(NotificationSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1
    ######################## to here

class AutherSerializer(serializers.Serializer):

    views = serializers.IntegerField(default = 0 )
    posts = serializers.IntegerField(default = 0 )
    likes = serializers.IntegerField(default = 0 )
    bookmarks = serializers.IntegerField(default = 0 )
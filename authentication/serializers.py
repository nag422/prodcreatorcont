from rest_framework import serializers
from quizz.models import Profile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"
    def update(self,instance,validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()

class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.EmailField(required=True)
    last_name = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)
        # extra_kwargs = {'password': {'write_only': True}}
    def update(self,instance,validated_data):
        instance.email = validated_data.get("email")
        instance.first_name = validated_data.get("first_name")
        instance.last_name = validated_data.get("last_name")        
        instance.save()

class ProfileSerializer(serializers.ModelSerializer):
    user_ptr = UserSerializer()
    class Meta:
        model = Profile
        fields = ('user_ptr','content','address','postalcode','city','country','phone')
    def update(self,instance,validated_data):
        # instance = self.Meta.model(**validated_data)
        instance.content = validated_data.get("content")
        instance.address = validated_data.get("address")
        instance.postalcode = validated_data.get("postalcode")  
        instance.city = validated_data.get("city")
        instance.country = validated_data.get("country")
        instance.save()
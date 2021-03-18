from rest_framework import serializers
from quizz.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ('content','address','postalcode','city','country','phone')
    def update(self,instance,validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
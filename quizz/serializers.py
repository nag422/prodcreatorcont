from rest_framework import serializers
from quizz.models import Profile,Content


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Content
        fields="__all__"
        # extra_kwargs = {'password': {'write_only': True}}
    def update(self,instance,validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
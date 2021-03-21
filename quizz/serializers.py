from rest_framework import serializers
from quizz.models import Profile,Content,ProductAssigns


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Content
        fields="__all__"
        # extra_kwargs = {'password': {'write_only': True}}
    def update(self,instance,validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
class ProductAssignsSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductAssigns
        fields="__all__"
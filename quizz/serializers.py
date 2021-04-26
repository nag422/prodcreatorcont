from rest_framework import serializers
from quizz.models import Profile,Content,ProductAssigns,ProductGroup,MessageInbox,MessageChatter,ContentSaveNotifyer


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

class ProductGroupSerializer(serializers.ModelSerializer):
    products = ProductsSerializer(many=True)
    class Meta:
        model=ProductGroup
        fields=["id","groupname","rule","products"]
        depth = 2

class MessageInboxSerializer(serializers.ModelSerializer):
    class Meta:
        model=MessageInbox
        fields="__all__"
class MessageChatterSerializer(serializers.ModelSerializer):
    class Meta:
        model=MessageChatter
        fields="__all__"

class ContentSaveNotifyerSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContentSaveNotifyer
        fields="__all__"
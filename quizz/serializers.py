from rest_framework import serializers
from quizz.models import Profile,Content,ProductAssigns,ProductGroup,MessageInbox,MessageChatter,ContentSaveNotifyer,MessageRequest,ProductRequest,Likedproducts,Boughtedproducts


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
    # products = ProductsSerializer(many=True)
    class Meta:
        model=ProductGroup
        # fields=["id","groupname","rule","products"]
        # depth = 2
        fields="__all__"

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

class MessageRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=MessageRequest
        fields="__all__"

class ProductRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductRequest
        fields="__all__"

class LikedproductsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Likedproducts
        fields="__all__"

class BoughtedproductsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Boughtedproducts
        fields="__all__"


        
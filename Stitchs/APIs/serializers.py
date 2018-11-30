from rest_framework import serializers
from trello import models

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StitchBoard
        fields = '__all__'

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StitchList
        fields = '__all__'

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StitchCard
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Members
        fields = "__all__"


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Label
        fields = "__all__"
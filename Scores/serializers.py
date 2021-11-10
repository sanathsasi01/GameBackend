from rest_framework import serializers
from .models import *


class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scores
        fields = '__all__'
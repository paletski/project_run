from rest_framework import serializers
from .models import Run
from django.contrib.auth.models import User


class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name')


class RunSerializer(serializers.ModelSerializer):
    athlete = AthleteSerializer(read_only=True)
    class Meta:
        model = Run
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'date_joined', 'username', 'last_name',
                  'first_name', 'type')

    def get_type(self, obj):
        if obj.is_staff:
            return 'coach'
        else:
            return 'athlete'





from rest_framework import serializers
from .models import Run, AthleteInfo, Challenge, Position
from django.contrib.auth.models import User


class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name')


class RunSerializer(serializers.ModelSerializer):
    athlete_data = AthleteSerializer(read_only=True, source='athlete')
    class Meta:
        model = Run
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    runs_finished = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'date_joined', 'username', 'last_name',
                  'first_name', 'type', 'runs_finished',)

    def get_type(self, obj):
        if obj.is_staff:
            return 'coach'
        else:
            return 'athlete'

    def get_runs_finished(self, obj):
         return  obj.runs.filter(status='finished').count() # получить по
         # обратной связи количество завершенных забегов атлета


class AthleteInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AthleteInfo
        #fields = '__all__'
        fields = ('weight', 'goals',  'user_id')


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ('athlete', 'full_name')


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('latitude', 'longitude', 'run')
    # изобретем велосипед
    def validate_latitude(self, value):
        # пока без try - делаем скелетик
        fvalue = f"{value:.4f}"
        fvalue = float(fvalue)
        #print(f'latitude = {fvalue}')
        if fvalue < -90.0000 or fvalue > 90.0000:
            # кинет 400 ошибку
            raise serializers.ValidationError(
                f'latitude должно быть в диапазоне от -90.0000 до 90.0000')
        return fvalue
    def validate_longitude(self, value):
        # пока без try - делаем скелетик
        fvalue = f"{value:.4f}"
        fvalue = float(fvalue)
        #print(f'longitude = {fvalue}')
        if fvalue < -180.0000 or fvalue > 180.0000:
            # кинет 400 ошибку
            raise serializers.ValidationError(
                f'longitude должно быть в диапазоне от -180.0000 до 180.0000')
        return fvalue


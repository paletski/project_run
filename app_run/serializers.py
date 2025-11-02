from rest_framework import serializers
from .models import Run, AthleteInfo, Challenge, Position, CollectibleItem
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

    run_time_seconds = serializers.IntegerField(allow_null=True, default=0)


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    #runs_finished = serializers.SerializerMethodField()
    runs_finished = serializers.ReadOnlyField()
    class Meta:
        model = User
        fields = ('id', 'date_joined', 'username', 'last_name',
         'first_name', 'type', 'runs_finished',)


    def get_type(self, obj):
        if obj.is_staff:
            return 'coach'
        else:
            return 'athlete'

    #def get_runs_finished(self, obj):
         #return  obj.runs.filter(status='finished').count() # получить по
         # обратной связи количество завершенных забегов атлета


class UserSerializerCollItems(UserSerializer):
    items = serializers.SerializerMethodField()
    class Meta(UserSerializer.Meta):
        model = User
        fields = UserSerializer.Meta.fields + ('items',)


    def get_items(self, obj):
        # проверить на n+1 !!!!! см видео коммент 18.4
        users = User.objects.get(id=obj.id)
        items = users.collectibleitems.all() # это QuerySet а не json

        # сконвертим его в json!
        serializer = CollectibleItemSerializer(items, many=True)
        return serializer.data


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
        fields = ('id', 'latitude', 'longitude', 'run', 'date_time',
                  'distance', 'speed')
    date_time = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%f')

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

class CollectibleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectibleItem
        fields = ('id', 'name', 'uid', 'latitude', 'longitude', 'picture', 'value')

    value = serializers.IntegerField()
    picture = serializers.URLField()

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


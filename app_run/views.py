from rest_framework.decorators import api_view
from rest_framework import viewsets

from django.conf import settings

from .models import Run, AthleteInfo
from .serializers import RunSerializer, UserSerializer, AthleteInfoSerializer
from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination


# Create your views here.

@api_view(['GET'])
def company_description_view(request):
    return Response({'company_name': settings.COMPANY_NAME,
                    'slogan': settings.SLOGAN,
                    'contacts': settings.CONTACTS}
                    )

class RunPagination(PageNumberPagination):
    page_size_query_param = 'size'


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer
    pagination_class = RunPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'athlete'] # фильтруем
    ordering_fields = ['created_at']         # сортируем

class UserPagination(PageNumberPagination):
    page_size_query_param = 'size'


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = RunPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    search_fields = ['first_name', 'last_name',]
    ordering_fields = ['date_joined']

    def get_queryset(self):
        qs = self.queryset
        runs_finished = self.request.query_params.get('runs_finished', None)
        type = self.request.query_params.get('type', None)
        if type:
            if type == 'coach':
                qs = qs.filter(is_staff=True, is_superuser=False)
            elif type == 'athlete':
                qs = qs.filter(is_staff=False, is_superuser=False)
            else:
                qs = qs.filter(is_superuser=False)
        return qs.filter(is_superuser=False)


class RunStartViewSet(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        #print(f'view start {run}')
        if run.status == 'init':
            run.status = 'in_progress'
            run.save()
            data = {'message': f'POST запрос обработан 3'}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'message': f'POST запрос не обработан 2'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class RunStopViewSet(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        #print(f'view stop {run}')
        if run.status == 'in_progress':
            run.status = 'finished'
            run.save()
            data = {'message': f'POST запрос обработан 32'}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'message': f'POST запрос не обработан 22'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class AthleteInfoViewSet(APIView):
    queryset = AthleteInfo.objects.all()
    serializer_class = AthleteInfoSerializer
    def get(self, request, user_id):
        #True создан, False найден
        if not User.objects.filter(id=user_id).exists():
            message = {'message': 'пользователь не найден'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        # юзер есть в User
        # значит достаем данные по нему из AthleteInfo или создаем запись в AthleteInfo
        athlete, created = AthleteInfo.objects.get_or_create(user_id_id=user_id)
        serializer = AthleteInfoSerializer(athlete)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        # True создан,  False обновлен
        if not User.objects.filter(id=user_id).exists():
            message = {'message': 'пользователь не найден'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        athlete, created = AthleteInfo.objects.update_or_create(user_id_id=user_id)
        data = request.data
        if 'goals' in data:
            print('goals in data')
            athlete.goals = data['goals']
        if 'weight' in data:
            try:
                weight = int(data['weight'])  # пока без try
                if weight <= 0 or weight > 900:
                    message = {'msg': 'вес не в диапазоне 1-900'}
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
            # проскочили проверку, в диапазоне и число (помним про try)
            except ValueError:
                message = {'msg': 'вес должен быть числом в диапазоне 1-899'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            athlete.weight = weight
            athlete.save()
            serializer = AthleteInfoSerializer(athlete)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from django.conf import settings

from .models import Run
from .serializers import RunSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

@api_view(['GET'])
def company_description_view(request):
    return Response({'company_name': settings.COMPANY_NAME,
                    'slogan': settings.SLOGAN,
                    'contacts': settings.CONTACTS}
                    )

class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name',]

    def get_queryset(self):
        qs = self.queryset
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
        qs = Run.objects.filter(id=run_id)
        if not qs.exists():
            data = {'message': f'POST запрос не обработан 1'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        if qs.exists():
            if qs[0].status in ['in_progress','finished']:
                data = {'message': f'POST запрос не обработан 2'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            if qs[0].status == 'init':
                qs.update(status='in_progress')
                data = {'message': f'POST запрос обработан 3'}
                return Response(data, status=status.HTTP_200_OK)
        data = {'message': f'POST запрос не обработан, получено странное '
                           f'значение статуса {qs[0].status}'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class RunStopViewSet(APIView):
    def post(self, request, run_id):
        qs = Run.objects.filter(id=run_id)
        if not qs.exists():
            data = {'message': f'POST запрос не обработан 21'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        if qs.exists():
            if qs[0].status in ['init','finished']:
                data = {'message': f'POST запрос не обработан 22'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            if qs[0].status == 'in_progress':
                qs.update(status='finished')
                data = {'message': f'POST запрос обработан 23'}
                return Response(data, status=status.HTTP_200_OK)
        data = {'message': f'POST запрос не обработан, получено странное '
                           f'значение статуса {qs[0].status}'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

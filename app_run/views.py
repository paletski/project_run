from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from django.conf import settings

from .models import Run
from .serializers import RunSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter

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

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.response import Response
import json
from .models import Country
from .serializers import LoginSerializer
from rest_framework.mixins import CreateModelMixin
from django.shortcuts import render

from rest_framework.viewsets import GenericViewSet
from .serializers import UserSerializer
from .serializers import RegisterSerializer
from core_viewsets.custom_viewsets import CreateViewSet
from core_viewsets.custom_viewsets import ListViewSet
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.views import View


class CountryTableView(View): 
    def get(self, request, *args, **kwargs):
        countries = Country.objects.all()
        return render(request, 'templates/users/country_table.html', {'countries': countries})


def import_data():
    with open('dataset_world_population_by_country_name.json') as f:
        data = json.load(f)

    for entry in data:
        entry['place'] = entry.get('place', 0)
        entry['pop1980'] = entry.get('pop1980', 0)
        entry['pop2000'] = entry.get('pop2000', 0)
        entry['pop2010'] = entry.get('pop2010', 0)
        entry['pop2022'] = entry.get('pop2022', 0)
        entry['pop2023'] = entry.get('pop2023', 0)
        entry['pop2030'] = entry.get('pop2030', 0)
        entry['pop2050'] = entry.get('pop2050', 0)
        entry['area'] = entry.get('area', 0)
        entry['landAreaKm'] = entry.get('landAreaKm', 0.0)
        entry['cca2'] = entry.get('cca2', "")
        entry['cca3'] = entry.get('cca3', "")
        entry['netChange'] = entry.get('netChange', 0.0)
        entry['growthRate'] = entry.get('growthRate', 0.0)
        entry['worldPercentage'] = entry.get('worldPercentage', 0.0)
        entry['density'] = entry.get('density', 0.0)
        entry['densityMi'] = entry.get('densityMi', 0.0)
        entry['rank'] = entry.get('rank', 0)

        Country.objects.create(**entry)



class RegisterViewSet(CreateModelMixin, GenericViewSet):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterSerializer 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        first_name = serializer.validated_data.get('first_name')
        last_name = serializer.validated_data.get('last_name')
        password = serializer.validated_data.get('password', None)
        phone_number = serializer.validated_data.get('phone_number')

        try:
            # Use create_user method from the custom user model
            user = get_user_model().objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number
            )
        except IntegrityError as e:
            raise ValueError('The Email field must be unique') from e

        return Response(
            {'code': status.HTTP_201_CREATED, 'message': 'success', 'user_id': user.id},
            status=status.HTTP_201_CREATED
        )
class LoginViewSet(CreateViewSet):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(request, email=email, password=password)

        if user is not None:
           

            user.last_login = timezone.now()
            user.save()

            return Response(
                {
                    'code': 200,
                    'message': 'success',
                    'access_token': '',
                    'refresh_token': 'refresh_token',
                    'user_id': user.pk,
                    'name': user.first_name,
                    'email': user.email,
                    'last_login': user.last_login,
                },
            )
        else:
            # Authentication failed
            return Response(
                {'code': 401, 'message': 'Authentication failed'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class MeViewSet(ListViewSet):
    authentication_classes = () 
    permission_classes = ()
    serializer_class = UserSerializer 
    queryset = get_user_model().objects.all()

    def get(self, request, *args, **kwargs):
        user = request.user  
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
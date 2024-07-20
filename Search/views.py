from django.db.models import Q
from django.shortcuts import render
from django.urls import path
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from Search.GetApiYandex.requestnow import RequestWeather
# Create your views here.
from Search.models import City
from rest_framework import generics
from Search.serializers import CitySerializer


class ProductList(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_queryset(self):
        query_params = self.request.query_params
        print(query_params)

        # Получаем все заголовки запроса
        # Далее извлекаем необходимые параметры из headers и используем их для фильтрации queryset
        # Например, если в заголовках есть параметр X-Filter, можно использовать его для фильтрации
        # x_filter_value = headers.get('HTTP_CITY')  # Пример чтения значения из заголовка
        if query_params:
            results = City.objects.filter(
                Q(name__contains=query_params['city']) | Q(subject__contains=query_params['city']))
            return results
        return super().get_queryset()  # Если нет параметров в заголовках, возвращаем исходный queryset


class CitySearchWeather(APIView):
    def get(self, request):
        idCity = request.query_params['IdCity']
        results = City.objects.filter(id=idCity)
        serializer = CitySerializer(results, many=True).data[0]
        weather = RequestWeather().PerDay(lat=serializer['lat'],lon=serializer['lon'])
        return Response({'name':serializer['name'], 'subject' : serializer['subject'] ,'weather': weather})


class HomePage(View):
    http_method_names = ['get']

    def get(self, request):
        return render(request, 'home.html')

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
                  Q(subject__contains=query_params['city']) | Q(name__contains=query_params['city']))
            return results
        return super().get_queryset()  # Если нет параметров в заголовках, возвращаем исходный queryset


class CitySearchWeather(APIView):
    def get(self, request):

        OneCity = request.query_params['OneCity']
        CityTwo = request.query_params['CityTwo']
        CityThree = request.query_params['CityThree']
        Arr = [OneCity, CityTwo, CityThree]
        ListCity= []
        for i in Arr:
            if i != 'null':
                results = City.objects.filter(id=i)
                serializer = CitySerializer(results, many=True).data[0]
                weather = RequestWeather().PerDay(lat=serializer['lat'], lon=serializer['lon'])
                ListCity.append({'name': serializer['name'], 'subject': serializer['subject'], 'weather': weather})
        return Response(ListCity)


class HomePage(View):
    http_method_names = ['get']

    def get(self, request):
        return render(request, 'home.html')

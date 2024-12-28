from django.shortcuts import render
from rest_framework.decorators import api_view
from django.core.cache import cache
from rest_framework.response import Response
from django.conf import settings
import requests
from .serializers import HolidaysSerializer
# Create your views here.
def index(request):
    return render(request,"holidays/index.html")

@api_view(['GET'])
def all_holidays(request,country,year):
    key = country + "_" + str(year)

    cache_data = cache.get(key)

    if cache_data:
        return Response(cache_data)

    api_url = "https://calendarific.com/api/v2/holidays"
    params = {
        'api_key' : settings.CALENDARIFIC_API_KEY,
        'country' : country,
        'year' : year
    }
    response = requests.get(api_url, params=params)

    print("helloo")
    if response.status_code == 200:
        data = response.json()
        response_data = data.get("response", {})
        holidays = response_data.get("holidays",[])

        serializer = HolidaysSerializer(holidays, many=True)

        cache.set(key,holidays, timeout = 86400)

        holiday_details = serializer.data

        return Response(holiday_details)
    else:
        return Response({"detail" : "Sorry, data fetching failed"})

@api_view(["GET"])
def search_holiday(request):
    print("helloo")
    name = request.query_params.get("name", None)

    if not name:
        return Response({"detail":"Name is required"})

    holidays = cache.get("all_holidays")
    final_holidays = []

    if not holidays:
        api_url = "https://calendarific.com/api/v2/holidays"
        params = {
            'api_key' : settings.CALENDARIFIC_API_KEY,
        }


        response = requests.get(api_url,params=params)
        if response.status_code == 200:
            data = response.json()
            response_data = data.get("response", {})
            holidays = response_data.get("holidays", [])

            cache.set("all_holidays", holidays, timeout=86400)
        else:
            return Response({"detail": "Sorry, fetching data failed."})
    for holiday in holidays:
        if name.lower() in holiday['name'].lower():
            final_holidays.append(holiday)
    return Response(final_holidays)



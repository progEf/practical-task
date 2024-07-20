import requests

from datetime import datetime


class RequestWeather:
    def __init__(self):
        access_key = "33e0a914-fc01-4484-8600-562be354ff1d"
        self.headers = {
            "X-Yandex-Weather-Key": access_key
        }

    def InTenDays(self, lat, lon, days):
        limit = days
        query = """{{
              weatherByPoint(request: {{ lat: {}, lon: {} }}) {{
                forecast {{
                  days(limit: {} ) {{
                    time
                    sunriseTime
                    sunsetTime
                    parts {{
                      morning {{
                        avgTemperature
                      }}
                      day {{
                        avgTemperature
                      }}
                      evening {{
                        avgTemperature
                      }}
                      night {{
                        avgTemperature
                      }}
                    }}
                  }}
                }}
              }}
            }}
            """.format(lat, lon, limit)

        response = requests.post('https://api.weather.yandex.ru/graphql/query', headers=self.headers,
                                 json={'query': query})
        ArrWeather = response.json()['data']['weatherByPoint']['forecast']['days']
        for i in ArrWeather:
            parsed_time = datetime.fromisoformat(i['time'])
            formatted_time = parsed_time.strftime('%d.%m')
            i['time'] = formatted_time
        return ArrWeather

    def PerDay(self, lat, lon):
        query = f"""
        {{
          weatherByPoint(request: {{ lat: {lat}, lon: {lon} }}) {{
            forecast {{
              days(limit: 1) {{
                hours {{
                  time
                  temperature
                  humidity
                  pressure
                  windSpeed
                  windDirection
                }}
              }} 
            }}
          }}
        }}
        """
        response = requests.post('https://api.weather.yandex.ru/graphql/query', headers=self.headers,
                                 json={'query': query})
        ArrWeather = response.json()['data']['weatherByPoint']['forecast']['days'][0]['hours']
        TimeNow = []
        for i in ArrWeather:
            parsed_time = datetime.fromisoformat(i['time'])
            formatted_time = parsed_time.strftime('%H.%M')
            i['time'] = formatted_time
            if datetime.now().strftime('%H') == parsed_time.strftime('%H'):
                TimeNow.append(i)
        return {'ArrWeather' : ArrWeather, 'DatetimeNow':TimeNow[0]}

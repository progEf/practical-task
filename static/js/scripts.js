$(document).ready(function () {
    $('#find-city').on('input', function () {
        const cityName = $(this).val();
        if (cityName.trim() !== '') {
            $('#Hints').append('<div id="suggestions"></div>')
            searchCity(cityName);
        } else {
            $('#Hints').html("");
        }
    });
    const myDiv = document.getElementById('main-input');

// Добавляем обработчик события клика на весь документ
    document.addEventListener('click', function (event) { // Убираем подсказки при потере фокуса
        // Проверяем, является ли цель клика дочерним элементом вашего div
        if (!myDiv.contains(event.target)) {
            $('#Hints').html("");
        }
    });
    var json;

    function searchCity(cityName) {
        fetch('/products?city=' + cityName)
            .then(response => response.json())
            .then(data => {
                $('#Hints').html("");
                $('#Hints').append('<div id="suggestions"></div>')
                const suggestionsDiv = $('#suggestions');
                if (data.length === 0) {
                    const suggestion = $('<div>').addClass('city-list').text('Нету');
                    suggestionsDiv.append(suggestion);
                }
                data.forEach(city => {
                    const suggestion = $('<div>').addClass('city-list').text(city.name).attr('id', city.id).text(city.name);
                    ;
                    suggestionsDiv.append(suggestion);
                    document.getElementById(city.id).addEventListener('click', function () {
                        var id_city = localStorage.getItem("id_city")
                        var arr_city;
                        if (id_city === null) {
                            arr_city = [{'one': city.id, 'two': null, 'three': null}]
                            localStorage.setItem("id_city", JSON.stringify(arr_city));
                        } else {
                            var storedNames1 = JSON.parse(localStorage.getItem("id_city"));
                            if (storedNames1[0]['two'] === null) {
                                arr_city = [{'one': city.id, 'two': storedNames1[0]['one'], 'three': null}]
                                localStorage.setItem("id_city", JSON.stringify(arr_city))
                            } else {
                                arr_city = [{
                                    'one': city.id,
                                    'two': storedNames1[0]['one'],
                                    'three': storedNames1[0]['two']
                                }]
                                localStorage.setItem("id_city", JSON.stringify(arr_city))
                            }
                        }
                        GetWeatherCityId()
                        $('#Hints').html("");

                    })
                });
            })
            .catch(error => {
                console.error('Ошибка при выполнении запроса:', error);
            });
    }

    GetWeatherCityId()

    function GetWeatherCityId() {
        var city_storage = localStorage.getItem("id_city")
        if (city_storage === null) {
            var city_id_arr = [{'one': 615, 'two': 841, 'three': 172}]
            localStorage.setItem("id_city", JSON.stringify(city_id_arr))
            var city_id = city_id_arr[0]
        } else {
            var city_id = JSON.parse(city_storage)[0]

        }

        $.getJSON('/citySearch/?OneCity=' + city_id['one'] + '&CityTwo=' + city_id['two'] + '&CityThree=' + city_id['three'], function (data) {
            for (var i = 0; i < data.length; i++) {
                console.log(data[i])
                var city = data[i]['name']
                var subject = data[i]['subject']
                var weather = data[i]['weather']
                $('#Title-' + i).html("");
                $('#temperature-' + i).html("");
                $('#content-' + i).html("");
                $('#Title-' + i).append('<h1 class="city-title">' + city + '</h1><h2 class="city-subject">' + subject + '</h2>')
                $('#temperature-' + i).append('<h1 id="city-temperature-' + i + '" class="city-temperature">' + weather['DatetimeNow']['temperature'] + '</h1>')
                $('#temperature-' + i).append('<div class="circle"></div>')
                $('#container-days-' + i).html("")

                for (var ij = 0; ij < weather['ArrWeather'].length; ij++) {
                    console.log(i)
                    $('#container-days-' + i).append('<div class="container-hour"><div id="container-' + i + '-weather-' + ij + '" class="weather-past-temp"></div><div id="container-' + i + '-time-' + ij + '" ></div></div>')
                    $('#container-' + i + '-weather-' + ij).append('<h1 class="temp-hour">' + weather['ArrWeather'][ij]['temperature'] + '</h1><div class="circle"></div>')
                    $('#container-' + i + '-time-' + ij).append('<h2 class="time-for-hour">' + weather['ArrWeather'][ij]['time'] + '</h2>')
                }
            }
        })
    }

});


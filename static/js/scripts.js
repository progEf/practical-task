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

    $('#find-city').on('blur', function () {
        $('#Hints').html("");
        // Убираем подсказки при потере фокуса
    });

    function searchCity(cityName) {
        fetch('/products?city=' + cityName)
            .then(response => response.json())
            .then(data => {
                $('#Hints').html("");
                $('#Hints').append('<div id="suggestions"></div>')
                const suggestionsDiv = $('#suggestions');
                console.log(data.length)
                if (data.length === 0) {
                    const suggestion = $('<div>').addClass('city-list').text('Нету');
                    suggestionsDiv.append(suggestion);
                }
                data.forEach(city => {
                    const suggestion = $('<div>').addClass('city-list').text(city.name);
                    suggestionsDiv.append(suggestion);
                });
            })
            .catch(error => {
                console.error('Ошибка при выполнении запроса:', error);
            });
    }
});


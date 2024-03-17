import datetime

BASE_URL1 = "http://api.openweathermap.org/data/2.5/weather?"
BASE_URL2 = "https://api.open-meteo.com/v1/forecast?"

HTML_FORM = """
<html>
    <head>
        <title>Check Weather</title>
    </head>
    <body>
        <h1>Check Weather by City</h1>
        <form action="/weather" method="post">
            <label for="city">Enter city name:</label><br>
            <input type="text" id="city" name="city"><br>
            <label for="start_date">Enter start date:</label><br>
            <input type="date" id="start_date" name="start_date" value="{start_date}"><br>
            <label for="end_date">Enter end date:</label><br>
            <input type="date" id="end_date" name="end_date" value="{end_date}"><br>
            <label for="password">Enter password:</label><br>
            <input type="password" id="password" name="password"><br>
            <input type="submit" value="Check Weather">
        </form>
    </body>
</html>
""".format(
    start_date=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
    end_date=datetime.datetime.now().strftime("%Y-%m-%d")
)


HTML_TEMPLATE = """
<html>
    <head>
        <title>Weather Report</title>
    </head>
    <body>
        <h1>Weather in {city}</h1>
        <p>Current Temperature: {temperature_current_celsius:.2f} °C</p>
        <p>Current Humidity: {humidity_current}%</p>
        <p>Average Historical Temperature: {average_temperature:.2f} °C</p>
        <div>
            {html_plot}
        </div>
    </body>
</html>
"""

from datetime import datetime, timedelta
from influxdb import InfluxDBClient

temperatures = []
humidities = []
living_room_temperature = 0
credentials = ['host_name', '10.0.0.12', 8086, 'bme280monitor', 'Subaru15', 'bme280']

def pull_last_message():
    global temperatures
    """Instantiate a connection to the InfluxDB."""
    host = '10.0.0.12'
    port = 8086
    user = 'bme280monitor'
    password = 'Subaru15'
    dbname = 'bme280'
    query = 'SELECT last("message_text"), message_host, message_time FROM "text_message" WHERE time > now() - 30d  GROUP BY message_host;'
    last_message = ""
    message_time = 0

    client = InfluxDBClient(host, port, user, password, dbname)

    # print("Querying data: " + query)
    results = client.query(query)
    points = results.get_points()
    for item in points:
        host = item['message_host']
        last_message= item['last']
        message_time = item['message_time']
    #        print(item['host'])
    #        print(item['last'])
    #    print(temperatures)
    return last_message, message_time, host

def pull_last_internet_speeds():
    global temperatures
    """Instantiate a connection to the InfluxDB."""
    host = '10.0.0.12'
    port = 8086
    user = 'speedmonitor'
    password = 'Subaru15'
    dbname = 'internetspeed'
    query = 'SELECT last("download"), upload, ping, host FROM "internet_speed" WHERE time > now() - 1d  GROUP BY host;'
    download_speeds = []
    upload_speeds = []
    pings = []
    host_names = []
    times = []
    client = InfluxDBClient(host, port, user, password, dbname)

    # print("Querying data: " + query)
    results = client.query(query)
    points = results.get_points()
    for item in points:
        host_names.append(item['host'])
        download_speeds.append(item['last'])
        upload_speeds.append(item['upload'])
        pings.append(item['ping'])
        times.append(item['time'])
    #        print(item['host'])
    #        print(item['last'])
    #    print(temperatures)
    return host_names, download_speeds, upload_speeds, pings, times


def pull_last_public_ip():
    global temperatures
    """Instantiate a connection to the InfluxDB."""
    host = '10.0.0.12'
    port = 8086
    user = 'closetmonitor'
    password = 'Subaru15'
    dbname = 'closetstats'
    query = 'SELECT last("public_ip"), host FROM "closetstats" WHERE time > now() - 1d  GROUP BY host;'
    public_ip_address = []
    host_names = []
    client = InfluxDBClient(host, port, user, password, dbname)

    # print("Querying data: " + query)
    results = client.query(query)
    points = results.get_points()
    for item in points:
        host_names.append(item['host'])
        public_ip_address.append(item['last'])
    #        print(item['host'])
    #        print(item['last'])
    #    print(temperatures)
    return host_names, public_ip_address


def pull_everything_from_influx(influx_credentials):
    """Instantiate a connection to the InfluxDB."""
    host = '10.0.0.12'
    port = 8086
    user = 'bme280monitor'
    password = 'Subaru15'
    dbname = 'bme280'
    query = 'SELECT * FROM "bme280" WHERE time > now() - 1d  GROUP BY host;'

    client = InfluxDBClient(host, port, user, password, dbname)

    #   print("Querying data: " + query)
    results = client.query(query)
    #  print(results)
    points = results.get_points(tags={'host': 'RaspiTest'})
    # for point in points:


#       print("Time: %s, Temperature: %i" % (point['time'], point['temperature']))


def pull_last_influx():
    global temperatures
    """Instantiate a connection to the InfluxDB."""
    host = '10.0.0.12'
    port = 8086
    user = 'bme280monitor'
    password = 'Subaru15'
    dbname = 'bme280'
    query = 'SELECT last(temperature), host, humidity FROM "bme280" WHERE time > now() - 1d  GROUP BY host;'
    temperatures = []
    humidities = []
    host_names = []
    client = InfluxDBClient(host, port, user, password, dbname)

    # print("Querying data: " + query)
    results = client.query(query)
    # print(results)
    points = results.get_points()
    for item in points:
        #   print(item['host'])
        #   print(item['last'])
        host_names.append(item['host'])
        temperatures.append(item['last'])
        humidities.append(item['humidity'])
    #        print(item['host'])
    #        print(item['last'])
    #    print(temperatures)
    return host_names, temperatures, humidities


def pull_last_24h_influx():
    global temperatures
    """Instantiate a connection to the InfluxDB."""
    host = '10.0.0.12'
    port = 8086
    user = 'bme280monitor'
    password = 'Subaru15'
    dbname = 'bme280'
    query = 'SELECT temperature, host, time FROM "bme280" WHERE time > now() - 24h  GROUP BY host;'
    temperatures = []
    host_names = []
    time_list = []
    client = InfluxDBClient(host, port, user, password, dbname)

    # print("Querying data: " + query)
    results = client.query(query)
    # print(results)
    points = results.get_points()
    for item in points:
        #   print(item['host'])
        #   print(item['last'])
        host_names.append(item['host'])
        temperatures.append(item['temperature'])
        time_list.append(item['time'])
        # print(item['host'])
        # print(item['temperature'])
    # print(temperatures)
    return host_names, temperatures, time_list


def pull_last_influx_living_room():
    global temperatures, living_room_temperature
    """Instantiate a connection to the InfluxDB."""
    host = '10.0.0.12'
    port = 8086
    user = 'bme280monitor'
    password = 'Subaru15'
    dbname = 'bme280'
    query = 'SELECT last(temperature), host FROM "bme280" WHERE time > now() - 1d  GROUP BY host;'
    temperatures = []
    host_names = []
    client = InfluxDBClient(host, port, user, password, dbname)

    # print("Querying data: " + query)
    results = client.query(query)
    # print(results)
    points = results.get_points()
    for item in points:
        #   print(item['host'])
        #   print(item['last'])
        host_names.append(item['host'])
        temperatures.append(item['last'])
        #        print(item['host'])
        #        print(item['last'])
        if item['host'] == 'RetroPie':
            living_room_temperature = item['last']
        else:
            pass
    #    print(temperatures)

    return living_room_temperature


def pull_last_influx_living_room_humidity():
    global temperatures, living_room_temperature
    """Instantiate a connection to the InfluxDB."""
    host = '10.0.0.12'
    port = 8086
    user = 'bme280monitor'
    password = 'Subaru15'
    dbname = 'bme280'
    query = 'SELECT last(humidity), host FROM "bme280" WHERE time > now() - 1d  GROUP BY host;'
    temperatures = []
    host_names = []
    client = InfluxDBClient(host, port, user, password, dbname)

    # print("Querying data: " + query)
    results = client.query(query)
    # print(results)
    points = results.get_points()
    for item in points:
        #   print(item['host'])
        #   print(item['last'])
        host_names.append(item['host'])
        temperatures.append(item['last'])
        # print(item['host'])
        # print(item['last'])
        if item['host'] == 'RetroPie':
            living_room_humidity = item['last']
        else:
            pass
    # print(humidities)

    return living_room_humidity


def pull_OMV_weather():
    global temperatures
    """Instantiate a connection to the InfluxDB."""
    host = '10.0.0.12'
    port = 8086
    user = 'bme280monitor'
    password = 'Subaru15'
    dbname = 'bme280'
    query = 'SELECT last(outside_temperature), host, outside_humidity, outside_pressure, weather_description FROM "OpenWeatherMap" WHERE time > now() - 1d;'
    outside_temperatures = []
    outside_humidities = []
    outside_pressure = []
    weather_description = ""
    host_names = []
    client = InfluxDBClient(host, port, user, password, dbname)

    # print("Querying data: " + query)
    results = client.query(query)
    #    print(results)
    points = results.get_points()
    for item in points:
        #   print(item['host'])
        #   print(item['last'])
        host_names.append(item['host'])
        outside_temperature = item['last']
        outside_humidity = item['outside_humidity']
        outside_pressure = item['outside_pressure']
        weather_description = item['weather_description']
        # print(item['host'])
        # print(item['last'])
        # print(outside_humidity)
        # print(outside_pressure)
        # print(weather_description)
        return outside_temperature, outside_humidity, outside_pressure, weather_description


def main():
    pull_OMV_weather()


if __name__ == '__main__':
    main()

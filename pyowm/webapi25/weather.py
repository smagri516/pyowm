#!/usr/bin/env python

"""
Module containing weather data classes and data structures.
"""

import json
from pyowm.utils import converter, xmlutils


class Weather(object):
    """
    A class encapsulating raw weather data.
    A reference about OWM weather codes and icons can be found at:
    http://bugs.openweathermap.org/projects/api/wiki/Weather_Condition_Codes

    :param reference_time: GMT UNIX time of weather measurement
    :type reference_time: long
    :param sunset_time: GMT UNIX time of sunset
    :type sunset_time: long
    :param sunrise_time: GMT UNIX time of sunrise
    :type sunrise_time: long
    :param clouds: cloud coverage percentage
    :type clouds: int
    :param rain: precipitation info
    :type rain: dict
    :param snow: snow info
    :type snow: dict
    :param wind: wind info
    :type wind: dict
    :param humidity: atmospheric humidity percentage
    :type humidity: int
    :param pressure: atmospheric pressure info
    :type pressure: dict
    :param temperature: temperature info
    :type temperature: dict
    :param status: short weather status
    :type status: Unicode
    :param detailed_status: detailed weather status
    :type detailed_status: Unicode
    :param weather_code: OWM weather condition code
    :type weather_code: int
    :param weather_icon_name: weather-related icon name
    :type weather_icon_name: Unicode
    :returns:  a *Weather* instance
    :raises: *ValueError* when negative values are provided

    """

    def __init__(self, reference_time, sunset_time, sunrise_time, clouds, rain,
                 snow, wind, humidity, pressure, temperature, status,
                 detailed_status, weather_code, weather_icon_name):
        if long(reference_time) < 0:
            raise ValueError("'reference_time' must be greater than 0")
        self._reference_time = long(reference_time)
        if long(sunset_time) < 0:
            raise ValueError("'sunset_time' must be greatear than 0")
        self._sunset_time = long(sunset_time)
        if long(sunrise_time) < 0:
            raise ValueError("'sunrise_time' must be greatear than 0")
        self._sunrise_time = long(sunrise_time)
        if clouds < 0:
            raise ValueError("'clouds' must be greater than 0")
        self._clouds = clouds
        self._rain = rain
        self._snow = snow
        self._wind = wind
        if humidity < 0:
            raise ValueError("'humidity' must be greatear than 0")
        self._humidity = humidity
        self._pressure = pressure
        self._temperature = temperature
        self._status = status
        self._detailed_status = detailed_status
        self._weather_code = weather_code
        self._weather_icon_name = weather_icon_name

    def get_reference_time(self, timeformat='unix'):
        """Returns the GMT time telling when the weather was measured

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time or '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00``
        :type timeformat: str
        :returns: a long or a str
        :raises: ValueError when negative values are provided

        """
        if timeformat == 'unix':
            return self._reference_time
        elif timeformat == 'iso':
            return converter.UNIXtime_to_ISO8601(self._reference_time)
        else:
            raise ValueError("Invalid value for parameter 'format'")

    def get_sunset_time(self, timeformat='unix'):
        """Returns the GMT time of sunset

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time or '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00``
        :type timeformat: str
        :returns: a long or a str
        :raises: ValueError

        """
        if timeformat == 'unix':
            return self._sunset_time
        elif timeformat == 'iso':
            return converter.UNIXtime_to_ISO8601(self._sunset_time)
        else:
            raise ValueError("Invalid value for parameter 'format'")

    def get_sunrise_time(self, timeformat='unix'):
        """Returns the GMT time of sunrise

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time or '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00``
        :type timeformat: str
        :returns: a long or a str
        :raises: ValueError

        """
        if timeformat == 'unix':
            return self._sunrise_time
        elif timeformat == 'iso':
            return converter.UNIXtime_to_ISO8601(self._sunrise_time)
        else:
            raise ValueError("Invalid value for parameter 'format'")

    def get_clouds(self):
        """Returns the cloud coverage percentage as an int

        :returns: the cloud coverage percentage

        """
        return self._clouds

    def get_rain(self):
        """Returns a dict containing precipitation info

        :returns: a dict containing rain info

        """
        return self._rain

    def get_snow(self):
        """Returns a dict containing snow info

        :returns: a dict containing snow info

        """
        return self._snow

    def get_wind(self):
        """Returns a dict containing wind info

        :returns: a dict containing wind info

        """
        return self._wind

    def get_humidity(self):
        """Returns the atmospheric humidity as an int

        :returns: the humidity

        """
        return self._humidity

    def get_pressure(self):
        """Returns a dict containing atmospheric pressure info

        :returns: a dict containing pressure info

        """
        return self._pressure

    def get_temperature(self, unit='kelvin'):
        """Returns a dict with temperature info

        :param unit: the unit of measure for the temperature values. May be:
            '*kelvin*' (default), '*celsius*' or '*fahrenheit*'
        :type unit: str
        :returns: a dict containing temperature values.
        :raises: ValueError

        """
        if unit == 'kelvin':
            return self._temperature
        elif unit == 'celsius':
            helper = lambda x: converter.kelvin_to_celsius(x) if x > 0.0 else x
            return dict((item, helper(self._temperature[item]))
                for item in self._temperature)
        elif unit == 'fahrenheit':
            helper = lambda x: converter.kelvin_to_fahrenheit(x) \
                if x > 0.0 else x
            return dict((item, helper(self._temperature[item]))
                for item in self._temperature)
        else:
            raise ValueError("Invalid value for parameter 'unit'")

    def get_status(self):
        """Returns the short weather status as a Unicode string

        :returns: the short weather status

        """
        return self._status

    def get_detailed_status(self):
        """Returns the detailed weather status as a Unicode string

        :returns: the detailed weather status

        """
        return self._detailed_status

    def get_weather_code(self):
        """Returns the OWM weather condition code as an int

        :returns: the OWM weather condition code

        """
        return self._weather_code

    def get_weather_icon_name(self):
        """Returns weather-related icon name as a Unicode string.

        :returns: the icon name.

        """
        return self._weather_icon_name

    def to_JSON(self):
        """Dumps object fields into a JSON formatted string

        :returns: the JSON string

        """
        return json.dumps({'reference_time': self._reference_time,
                           'sunset_time': self._sunset_time,
                           'sunrise_time': self._sunrise_time,
                           'clouds': self._clouds,
                           'rain': self._rain, 'snow': self._snow,
                           'wind': self._wind,
                           'humidity': self._humidity,
                           'pressure': self._pressure,
                           'temperature': self._temperature,
                           'status': self._status,
                           'detailed_status': self._detailed_status,
                           'weather_code': self._weather_code,
                           'weather_icon_name': self._weather_icon_name})

    def to_XML(self):
        """Dumps object fields into a XML formatted string

        :returns:  the XML string

        """
        return '<Weather><status>%s</status><weather_code>%s</weather_code>' \
               '<rain>%s</rain><snow>%s</snow><pressure>%s</pressure>' \
               '<sunrise_time>%s</sunrise_time><weather_icon_name>%s' \
               '</weather_icon_name><clouds>%s</clouds><temperature>%s' \
               '</temperature><detailed_status>%s</detailed_status>' \
               '<reference_time>%s</reference_time><sunset_time>%s' \
               '</sunset_time><humidity>%s</humidity><wind>%s</wind>' \
               '</Weather>' % (self._status, self._weather_code,
                               xmlutils.dict_to_XML(self._rain),
                               xmlutils.dict_to_XML(self._snow),
                               xmlutils.dict_to_XML(self._pressure),
                               self._sunrise_time, self._weather_icon_name,
                               self._clouds,
                               xmlutils.dict_to_XML(self._temperature),
                               self._detailed_status,
                               self._reference_time,
                               self._sunset_time,
                               self._humidity,
                               xmlutils.dict_to_XML(self._wind))

    def __repr__(self):
        return "<%s.%s - reference time=%s, status=%s>" % (__name__, \
              self.__class__.__name__, self.get_reference_time('iso'),
              self._status)


def weather_from_dictionary(d):
    """
    Builds a *Weather* object out of a data dictionary. Only certain
    properties of the dictionary are used: if these properties are not
    found or cannot be read, an error is issued.

    :param d: a data dictionary
    :type d: dict
    :returns: a *Weather* instance
    :raises: *KeyError* if it is impossible to find or read the data
        needed to build the instance

    """
    # -- times
    reference_time = d['dt']
    if 'sys' in d and 'sunset' in d['sys']:
        sunset_time = d['sys']['sunset']
    else:
        sunset_time = 0L
    if 'sys' in d and 'sunrise' in d['sys']:
        sunrise_time = d['sys']['sunrise']
    else:
        sunrise_time = 0L
    # -- clouds
    if 'clouds' in d:
        if isinstance(d['clouds'], int) or isinstance(d['clouds'], float):
            clouds = d['clouds']
        elif 'all' in d['clouds']:
            clouds = d['clouds']['all']
        else:
            clouds = 0
    else:
        clouds = 0
    # -- rain
    if 'rain' in d:
        if isinstance(d['rain'], int) or isinstance(d['rain'], float):
            rain = {'all': d['rain']}
        else:
            rain = d['rain'].copy()
    else:
        rain = {}
    # -- wind
    if 'wind' in d:
        wind = d['wind'].copy()
    else:
        wind = {}
    # -- humidity
    if 'humidity' in d:
        humidity = d['humidity']
    elif 'main' in d and 'humidity' in d['main']:
        humidity = d['main']['humidity']
    else:
        humidity = 0
    # -- snow
    if 'snow' in d:
        if isinstance(d['snow'], int) or isinstance(d['snow'], float):
            snow = {'all': d['snow']}
        else:
            snow = d['snow'].copy()
    else:
        snow = {}
    # -- pressure
    if 'pressure' in d:
        atm_press = d['pressure']
    elif 'main' in d and 'pressure' in d['main']:
        atm_press = d['main']['pressure']
    else:
        atm_press = None
    if 'main' in d and 'sea_level' in d['main']:
        sea_level_press = d['main']['sea_level']
    else:
        sea_level_press = None
    pressure = {'press': atm_press, 'sea_level': sea_level_press}
    # -- temperature
    if 'temp' in d:
        temperature = d['temp'].copy()
    elif 'main' in d and 'temp' in d['main']:
        temp = d['main']['temp']
        if 'temp_kf' in d['main']:
            temp_kf = d['main']['temp_kf']
        else:
            temp_kf = None
        temp_max = d['main']['temp_max']
        temp_min = d['main']['temp_min']
        temperature = {'temp': temp,
                       'temp_kf': temp_kf,
                       'temp_max': temp_max,
                       'temp_min': temp_min
                       }
    else:
        temperature = {}
    # -- weather status info
    if 'weather' in d:
        # Sometimes provided with a leading upper case!
        status = d['weather'][0]['main'].lower()
        detailed_status = d['weather'][0]['description'].lower()
        weather_code = d['weather'][0]['id']
        weather_icon_name = d['weather'][0]['icon']
    else:
        status = u''
        detailed_status = u''
        weather_code = 0
        weather_icon_name = u''

    return Weather(reference_time, sunset_time, sunrise_time, clouds,
                rain, snow, wind, humidity, pressure, temperature,
                status, detailed_status, weather_code,
                weather_icon_name)

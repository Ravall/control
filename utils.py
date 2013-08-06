# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from md5 import md5
from django.core.cache import cache
from django.conf import settings



def api_request(url):
    """
    обращаемся по апи к sancta_py
    вынесен отдельно, т.к разные проекты могут использовать его
    требуется установка в настройках
        CACHE_API_TIMEOUT (время сохранения кэша)
        API_URL базовый урл до api
        и настроек кэширования
    """
    url = '{0}/api/{1}'.format(settings.API_URL, url)
    cache_key = md5(url).hexdigest()
    try:
        request = requests.get(url)
        request.raise_for_status()
        result = request.content
        if not cache.get(cache_key):
            # если кэш вышел - сохраним вновь.
            # кэш нужен на случай, если что-то сломается
            cache.set(cache_key, result, settings.CACHE_API_TIMEOUT)
    except requests.exceptions.RequestException:
        # если произошла ошибка - берем из Кэша
        result = cache.get(cache_key, '')
    return result

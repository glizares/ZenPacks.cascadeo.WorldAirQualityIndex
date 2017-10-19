"""Models stations using the World Air Quality Index API."""

import json
import urllib

from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.web.client import getPage

from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin

class Stations(PythonPlugin):

    relname = 'worldAirQualityStations'
    modname = 'ZenPacks.cascadeo.WorldAirQualityIndex.WorldAirQualityIndexStation'

    requiredProperties = (
        'zWorldAirQualityIndexAPIKey',
        'zWorldAirQualityIndexLocations'
    )

    deviceProperties = PythonPlugin.deviceProperties + requiredProperties

    @inlineCallbacks
    def collect(self, device, log):
        
        apiKey = getattr(device, 'zWorldAirQualityIndexAPIKey', None)

        if not apiKey:
            returnValue(None)
        
        locations = getattr(device, 'zWorldAirQualityIndexLocations', None)
        if not locations:
            returnValue(None)
        
        rm = self.relMap()

        for location in locations:
            try:
                stationURLTemplate = 'https://api.waqi.info/search/?token={key}&keyword={keyword}'
                locationEscaped = urllib.quote(location)
                stationURL = stationURLTemplate.format(key=apiKey, keyword=locationEscaped)
                response = yield getPage(stationURL)

                responseJSON = json.loads(response)

            except Exception, e:
                returnValue(None)
            
            if responseJSON['status'] != 'ok':
                returnValue(None)

            for result in responseJSON['data']:
                om = self.objectMap({
                    'id': self.prepId(result['uid']),
                    'title': result['station']['name'],
                    'url': result['station']['url']
                })

                rm.append(om)
        
        returnValue(rm)
    
    def process(self, device, results, log):
        return results
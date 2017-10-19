"""Monitors air quality index using World Air Quality Index API"""

import logging
LOG = logging.getLogger('zen.WorldAirQualityIndex')

import json
import time
import urllib

from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.web.client import getPage

from ZenPacks.zenoss.PythonCollector.datasources.PythonDataSource import PythonDataSourcePlugin

class AirQualityInformation(PythonDataSourcePlugin):
    """World Air Quality Index Air Quality Data Source using API"""

    @classmethod
    def config_key(cls, datasource, context):
        return (
            context.device().id,
            datasource.getCycleTime(context),
            context.id,
            'world-air-quality-index-air-quality-info'
        )
    
    @classmethod
    def params(cls, datasource, context):
        return {
            'apiKey': context.zWorldAirQualityIndexAPIKey,
            'stationName': context.title            
        }

    @inlineCallbacks
    def collect(self, config):
        data = self.new_data()

        for datasource in config.datasources:
            try:
                apiKey = datasource.params['apiKey']
                stationName = datasource.params['stationName']
                stationURLTemplate = 'https://api.waqi.info/search/?token={key}&keyword={keyword}'
                stationNameEscaped = urllib.quote(stationName)
                stationURL = stationURLTemplate.format(key=apiKey, keyword=stationNameEscaped)

                response = yield getPage(stationURL)

                responseJSON = json.loads(response)
            except Exception:
                LOG.exception("%s: failed to get conditions for %s", config.id, stationName)
                continue

            if responseJSON['status'] != 'ok':
                continue

            # loop over datapoints inside datasource
            currentObservation = responseJSON['data']
            # data points as are defined in zenpack.yaml and easier if named matching the response JSON
            for datapointID in (x.id for x in datasource.points):
                if datapointID not in currentObservation:
                    continue;

                dpName = '_'.join((datasource.datasource, datapointID))
                value = float(currentObservation[datapointID])
                LOG.info("Writing value %f", value)

                data['values'][datasource.component][dpName] = (value, 'N')
        
        returnValue(data)
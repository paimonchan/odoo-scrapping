# -*- coding: utf-8 -*-

import json
import logging
import requests

from odoo import models
from werkzeug import urls

logger = logging.getLogger(__name__)

class Request(models.AbstractModel):
    _name = 'paimon.request'

    def POST(self, endpoint, data, header):
        default_headers = {
            'Content-Type': 'application/json', 
            'Accept': 'application/json', 
            'Catch-Control': 'no-cache'
        }
        header = {**default_headers, **header}
        try:
            response = requests.post(
                endpoint, data=data, headers=header)
            return response.json()
        except requests.exceptions.Timeout:
            logger.error("request post timeout for url %s", endpoint)
            raise
        except Exception:
            logger.error("request post bad request response")
            raise
    
    def GET(self, endpoint, params = dict(), header = dict()):
        default_headers = {
            'Content-Type': 'application/json', 
            'Accept': 'application/json', 
            'Catch-Control': 'no-cache'
        }
        header = {**default_headers, **header}
        print(str(header))
        try:
            response = requests.get(
                endpoint, params=params, headers=header)
            return response.text
        except requests.exceptions.Timeout:
            logger.error("request get timeout for url %s", endpoint)
            raise
        except Exception:
            logger.error("request get bad request response")
            raise
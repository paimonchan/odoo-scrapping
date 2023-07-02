import re
import json
import logging
import requests

from odoo import models, fields
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)

class Scrapping(models.AbstractModel):
    _inherit = 'scrapping'

    def _get_ucis_status_per_number(self, receipt_number):
        url = 'https://egov.uscis.gov/csol-api/case-statuses/{}'.format(receipt_number)
        header = {
            'Content-Type': 'application/json', 
            'Accept': 'application/json', 
            'Catch-Control': 'no-cache'
        }
        params = dict()
        try:
            response = requests.get(url, params=params, headers=header)
            return response.json()
        except requests.exceptions.Timeout:
            logger.error("request get timeout for url %s", url)
            raise
        except Exception:
            logger.error("request get bad request response")
            raise

    def get_uscis_status(self, receipt_numbers = False):
        receipt_numbers = receipt_numbers or []

        result = []
        for receipt_number in receipt_numbers:
            response = self._get_ucis_status_per_number(receipt_number)
            case_status_response = response.get('CaseStatusResponse') or dict()
            number = case_status_response.get('receiptNumber') or str()
            detail_eng = case_status_response.get('detailsEng') or dict()
            status = detail_eng.get('actionCodeText') or str()
            result.append(dict(
                number = number,
                status = status,
            ))
        return result

    def get_uscis_by_config(self, starter_receipt_number = False, interval = 5, limit = 10):
        if not starter_receipt_number:
            raise UserError('receipt number is required')
        if not len(starter_receipt_number) == 13:
            raise UserError('receipt number is invalid (must be 13 digit)')

        receipt_numbers = [starter_receipt_number]
        number = int(starter_receipt_number[-10:])
        code = starter_receipt_number[:3]

        for num in range(1, limit):
            next_sequence = num * interval
            next_number = number + next_sequence
            receipt_number = '{}{}'.format(code, next_number)
            receipt_numbers.append(receipt_number)

        result = self.get_uscis_status(receipt_numbers)
        return result
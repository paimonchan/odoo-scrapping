from odoo.http import Controller, Response, route, request
from odoo.http import request

class ScrappingUcis(Controller):
    def _get_error(self, message):
        return dict(
            status_code     = 500,
            message         = message,
            payload         = dict()
        )

    def _get_csv(self, results):
        csv = str()
        if results:
            csv += ','.join(key for key in results[0].keys())
        csv = csv.rstrip(',')
        csv += '\n'
        for result in results:
            for key, value in result.items():
                csv += '{},'.format(value)
            csv = csv.rstrip(',')
            csv += '\n'
        return csv
        
    @route('/api/ucis', type='json', auth='public', methods=['GET'])
    def get_ucis(self):
        kwargs = request.jsonrequest
        receipt_number = kwargs.get('receipt_number') or False
        increament = kwargs.get('increment') or 1
        limit = kwargs.get('limit') or 1

        if not receipt_number:
            return self._get_error('receipt number is required')
        if not len(receipt_number) == 13:
            return self._get_error('receipt number must be 13 digit')

        results = request.env['scrapping'].get_uscis_by_config(receipt_number, increament, limit)

        csv = self._get_csv(results)
        Response.headers = [
            ('Content-Disposition', 'attachment; filename="report.csv"'),
            ('Content-Type', 'text/csv;charset=utf8')
        ]
        return dict(
            status_code     = 200,
            payload         = csv
        )

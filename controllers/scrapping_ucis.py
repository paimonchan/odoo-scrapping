from odoo.http import Controller, Response, route, request

class ScrappingUcis(Controller):
    def _get_error(self, message):
        return dict(
            status_code     = 500,
            message         = message,
            payload         = dict()
        )
        
    @route('/ucis', type='json', auth='public', methods=['GET'])
    def get_ucis(self):
        kwargs = response = request.jsonrequest
        receipt_number = kwargs.get('receipt_number') or False
        increament = kwargs.get('increamet') or 1
        limit = kwargs.get('limit') or 1

        if not receipt_number:
            return self._get_error('receipt number is required')
        if not len(receipt_number) == 13:
            return self._get_error('receipt number must be 13 digit')

        results = request.env['scrapping'].get_uscis_by_config(receipt_number, increament, limit)
        return dict(
            status_code     = 200,
            payload         = results
        )

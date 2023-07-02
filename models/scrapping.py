import re
import json
import logging
import requests

from odoo import models, fields
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)

class Scrapping(models.AbstractModel):
    _name = 'scrapping'
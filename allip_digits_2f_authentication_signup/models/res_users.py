# -*- coding: utf-8 -*-
# 1 : imports of python lib
import logging
_logger = logging.getLogger(__name__)
# 2 :  imports of odoo
from openerp import api, fields, models, modules, SUPERUSER_ID, _
from openerp.http import request
from openerp import http
# 3 :  imports from odoo modules

class ResUsers(models.Model):
    _inherit = 'res.users'

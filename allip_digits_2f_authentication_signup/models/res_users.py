# -*- coding: utf-8 -*-
# 1 : imports of python lib
import logging
_logger = logging.getLogger(__name__)
# 2 :  imports of odoo
from odoo import api, fields, models, modules, SUPERUSER_ID, _
from odoo.http import request
from odoo import http
# 3 :  imports from odoo modules

class ResUsers(models.Model):
    _inherit = 'res.users'

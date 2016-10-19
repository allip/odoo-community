# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import MissingError
from odoo.http import request
from odoo import http

class ResPartner(models.Model):
    _inherit = 'res.partner'
  
    @api.multi
    def write(self, vals):
        if 'mobile' in vals:
            userInfo = http.request.env['res.users'].search([('partner_id','=',self.id)])
            if userInfo:
                if not vals['mobile']:
                    user_2f_enable_status = userInfo[0].user_2f_enable_status
                    if user_2f_enable_status:
                        raise  MissingError("Please disable 2FA for the user before removing Mobile Number.")
                userInfo.write({'digits_access_token':''})   
        return super(ResPartner, self).write(vals)
        
        
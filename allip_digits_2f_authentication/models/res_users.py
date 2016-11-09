# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.http import request
from odoo import api, http, SUPERUSER_ID, _
from odoo import registry as registry_get

class ResUsers(models.Model):
    _inherit = 'res.users'
  
    SELF_WRITEABLE_FIELDS = ['user_2f_enable_status', 'digits_access_token']
    
    digits_access_token = fields.Char('Digits Access Token')
    user_2f_enable_status = fields.Boolean('Enable 2FA Login')

    @api.onchange('user_2f_enable_status') # if these fields are changed, call method
    def checkMobileNumber(self):
        if self.user_2f_enable_status:
            if not self._origin.mobile:
                self.user_2f_enable_status = False
                return {'warning': {'title': _('Warning'),'message': _('Please set a valid Mobile Number before enabling 2FA.')}}
            
    @api.multi
    def write(self, vals):
        if 'user_2f_enable_status' in vals:
            if not vals['user_2f_enable_status']:
                vals['digits_access_token'] = ''
        return super(ResUsers, self).write(vals)
            
    def digit_authenticate(self,data):
           user_num = data['phone_number'][-10:]
           dbname = request.session.db
           key = request.session.loginKey
           del request.session['loginKey']
           registry = registry_get(dbname)
           with registry.cursor() as cr:
               env = api.Environment(cr, SUPERUSER_ID, {})       
               user_ids = env['res.users'].sudo().search([("partner_id.mobile","ilike",user_num)])
               if not user_ids:    
                   return False
               else: 
                   for userData in user_ids:
                       if request.session.user_identity == userData.id:
                           if userData.digits_access_token:
                                 if userData.digits_access_token==data['access_token']:
                                      return (dbname, userData.login, key)
                                 else: return False
                           else: 
                                    updatedUserId = userData.write({'digits_access_token':data['access_token'],'user_2f_enable_status':True})
                                    cr.commit()
                                    return (dbname, userData.login, key)    
    
        
    
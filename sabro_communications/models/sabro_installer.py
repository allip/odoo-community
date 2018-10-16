# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, modules, _
from odoo.exceptions import AccessError, UserError, ValidationError, MissingError
from odoo.http import request
import odoorpc
import random
import logging
import string
import random
from datetime import datetime
import requests
_logger = logging.getLogger(__name__)

def id_generator(size=32, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

class SabroInstaller(models.Model):
    
    _name= "sabro_installer"
    
    name= fields.Char("Company Name")
    admin_name= fields.Char("SaBRO Administrator Name")
    mobile= fields.Char()
    phone= fields.Char()
    node_api_username= fields.Char('Email/Login')
    sub_domain= fields.Char()
    node_url= fields.Char()
    otp_pending = fields.Boolean(default=False)
    country_id= fields.Many2one('res.country', 'Country')
    
    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id:
#             if self.mobile:
#                 mobile= str(self.mobile)
#                 if '+' not in str(mobile)[0]:
#                     mobile='+' + mobile
#                 if '+'+ str(self.country_id.phone_code) not in mobile[:len(str('+'+str(self.country_id.phone_code)))]:
#                     mobile= '+'+ str(self.country_id.phone_code) + mobile[len(str('+'+str(self.country_id.phone_code))):]
#                 self.mobile= mobile
#             else:
#             if not self.mobile:
                if self.country_id.phone_code and self.country_id.phone_code != 0:
                    self.mobile = '+'+ str(self.country_id.phone_code)
                    
    def CheckValidationBeforeSignup(self, vals, isCreate= True):
        error = ''
        if not isCreate:
            vals= {
                    'name': self.name if 'name' not in vals.keys() else vals['name'],
                    'admin_name': self.admin_name if 'admin_name' not in vals.keys() else vals['admin_name'],
                    'node_api_username': self.node_api_username if 'node_api_username' not in vals.keys() else vals['node_api_username'],
                    'country_id': (self.country_id.id if self.country_id else False) if 'country_id' not in vals.keys() else vals['country_id'],
                    'mobile': self.mobile if 'mobile' not in vals.keys() else vals['mobile'],
                    'sub_domain': self.sub_domain if 'sub_domain' not in vals.keys() else vals['sub_domain'],
                   }
        if 'name' in vals.keys():
            if not vals['name']:
                raise ValidationError(_('Please enter a valid Company Name.'))
        else:
            raise ValidationError(_('Please enter a valid Company Name.'))
        if 'admin_name' in vals.keys():
            if not vals['admin_name']:
                raise ValidationError(_('Please enter a valid SaBRO Administrator Name.'))
        else:
            raise ValidationError(_('Please enter a valid SaBRO Administrator Name.'))
        if 'node_api_username' in vals.keys():
            if not vals['node_api_username']:
                raise ValidationError(_('Please enter a valid Login Email.'))
        else:
            raise ValidationError(_('Please enter a valid Login Email.'))
        if not vals.get('country_id', False):
            raise ValidationError(_('Please select a country.'))
        if 'mobile' in vals.keys():
            countryObj= self.env['res.country'].sudo().browse(vals['country_id'])
            countryCode= '+'+str(countryObj.phone_code)
            if countryObj.phone_code and countryObj.phone_code != 0 and countryCode not in str(vals['mobile'])[:len(countryCode)]:
                raise ValidationError(_('Please enter a valid mobile number in the format {}*********.'.format(countryCode)))
        else:
            raise ValidationError(_('Please enter a valid mobile number in the format +44*********.'))
        if 'sub_domain' in vals.keys():
            if not vals['sub_domain'] or any(c for c in vals['sub_domain'] if c.isupper()) or ' ' in str(vals['sub_domain']):
                raise ValidationError(_('Please enter a valid Sub Domain. Only small letters, numbers and hyphens "-" are allowed!'))
        else:
            raise ValidationError(_('Please enter a valid Sub Domain.'))
        vals['otp_pending'] = True 

#         setupMenu = self.env['ir.ui.menu'].sudo().search([('name', '=', 'SaBRO Setup')])
#         if setupMenu:
#             veriftOtpAction = self.env['ir.actions.server'].sudo().search([('name', '=', 'SaBRO Installation Verification')])
#             if veriftOtpAction:
#                 setupMenu[0].action = str('ir.actions.server,')+str(veriftOtpAction[0].id)
        masterNodeBaseURL= 'www.allipcloud.com'
        params={
                  'node_api_username': str(vals['node_api_username']),
                  'mobile': str(vals['mobile']),
                  'sub_domain': str(vals['sub_domain']),
                  'masternode_url': masterNodeBaseURL
               }
        res= requests.get('https://{}/sabro/signup/validate/contacts/information'.format(masterNodeBaseURL), params=params).json()
        _logger.debug('sabro for odoo res' + str(res))
        _logger.debug('sabro for odoo res' + str(type(res)))
        if (not res.get('success', False)) and str(res.get('code', False)) == '785':
            raise MissingError('This email address is already associated with another account.')
        elif (not res.get('success', False)) and str(res.get('code', False)) == '786':
            raise ValidationError('This mobile number is already associated with another account.')
        elif (not res.get('success', False)) and str(res.get('code', False)) == '787':
            raise MissingError('This sub-domain is already associated with another account.')
        return True
                
    @api.model
    def create(self, vals):
        self.CheckValidationBeforeSignup(vals)
        return super(SabroInstaller, self).create(vals)
    
    @api.multi
    def write(self, vals):
        self.CheckValidationBeforeSignup(vals, False)
        return super(SabroInstaller, self).write(vals)
    
            
#     def verify_otp(self):
#         view = self.env.ref('sabro_communications.view_sabro_installer_verification_form')
#         return {
#                 'name': "Enter OTP",
#                 'type': 'ir.actions.server',
#                 'res_model': 'sabro_installer_verification',
#                 'view_type': 'form',
#                 'view_mode': 'form',
#                 'view_id': view.id,
#                 'target': 'new',
#             }


class SabroInstallerVerification(models.Model):
    
    _name= "sabro_installer_verification"
    
    otp= fields.Char("Verification Code")
    setup_complete= fields.Boolean(default=False)
    call_again_button = fields.Boolean('Call Again')

    @api.onchange('call_again_button')
    def onchange_call_again_button(self):
        self.callAgainForOTP()
        return {}

    @api.model
    def create(self, vals):
#         try:
#             odooRPCObj= self.env['allip_base_config'].sudo().getOdooAuthentication()
#             nodeUserName= self.env['allip_base_config'].sudo().search([])[0].login
#             saasSignupResponse = odooRPCObj.env['core.base.configuration'].createNode('self', nodeUserName, vals['sub_domain'], vals['mobile'], vals['name'], vals['admin_name'], vals['node_api_username'])
#             if saasSignupResponse:
#                 if saasSignupResponse['success']:
#                     return super(sabroMasternodeChildrenNodes, self).create(vals)
#         except Exception, e:
#             error = e
#             _logger.debug(e)
        sabroInstallerObj= self.env['sabro_installer'].sudo().search([])
        if sabroInstallerObj:
            params= {
                        'entered_otp': str(vals['otp']),
                        'sub_domain': sabroInstallerObj[0].sub_domain,
                        'mobile': sabroInstallerObj[0].mobile,
                        'name': sabroInstallerObj[0].name,
                        'admin_name': sabroInstallerObj[0].admin_name,
                        'node_api_username': sabroInstallerObj[0].node_api_username,
                        'country_iso_code': sabroInstallerObj[0].country_id.code if sabroInstallerObj[0].country_id and sabroInstallerObj[0].country_id.code else 'GB',
                        'raw_country_code': sabroInstallerObj[0].country_id.phone_code if sabroInstallerObj[0].country_id and sabroInstallerObj[0].country_id.phone_code else '44',
                        'currency_iso': sabroInstallerObj[0].country_id.currency_id.name if sabroInstallerObj[0].country_id and sabroInstallerObj[0].country_id.currency_id and sabroInstallerObj[0].country_id.currency_id.name else 'GBP'
                    }
            res= requests.get('https://www.allipcloud.com/sabro/signup/otp/verify', params=params).json()
            if (not res.get('success', False)) and res.get('code', False) == 687:
                raise ValidationError(_('You have entered incorrect OTP.'))
            elif (not res.get('success', False)) and res.get('code', False) == 500:
                raise ValidationError(_('Something went wrong.'))
            self.env['sabro_auth'].sudo().create({
                                          "name": res['company_name'],
                                          "node_web_url": res['node_url'],
                                          "node_host": res['node_url'].replace('https://', '').replace('http://', '').strip('/'),
                                          "protocol": 'jsonrpc+ssl',
                                          "port": 443,
                                          "timeout": 600,
                                          "login": res['username'],
                                          "password": res['password'],
                                          "centrex_sip_registration_url": res['centrex_sip_registration_url'],
                                          "sabro_customer_id": res['customer_ref_id'],
                                        })
            vals['setup_complete'] = True
        return super(SabroInstallerVerification, self).create(vals)
    
    def callAgainForOTP(self):
        obj= self.env['sabro_installer'].sudo().search([], limit=1)
        if obj:
            res= requests.get('https://www.allipcloud.com/sabro/signup/otp/initiate', params={'number_for_otp_verification': str(obj.mobile), 'email_address': str(obj.node_api_username)}).json()
            if (not res.get('success', False)) and str(res.get('code', False)) == '431':
                raise ValidationError('You have exceeded the maximum number of attempts.')
            elif not res.get('success', False):
                raise MissingError('Unable to process your request, Please try again later.')
    
    
    def finish_setup(self):
        setupMenu = self.env['ir.ui.menu'].sudo().search([('name', '=', 'SaBRO Setup')])
        if setupMenu:
            setupMenu[0].unlink()
        menu = self.env['ir.ui.menu'].search([('parent_id', '=', False)])[:1]
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            'params': {'menu_id': menu.id},
        }      
        
class BaseModuleUpgrade(models.TransientModel):
    _inherit = "base.module.upgrade"  
    
    @api.multi
    def upgrade_module(self):
        ctx = dict(self.env.context)
        obj= super(BaseModuleUpgrade, self).upgrade_module()
        if ctx and self.env['ir.module.module'].sudo().search([('name', '=', 'sabro_communications'),('id', '=', ctx.get('active_id', 0))]):
            menu = self.env['ir.ui.menu'].search([('parent_id', '=', False)])[:1]
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
                'params': {'menu_id': menu.id},
            }
        return obj
# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, modules, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.http import request
import odoorpc
import random
import logging
import string
import random
from datetime import datetime
_logger = logging.getLogger(__name__)

def id_generator(size=32, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

class SabroAuth(models.Model):
    _name = 'sabro_auth'
    name = fields.Char('Company Name', required= True)
    node_web_url = fields.Char('SaBRO URL')
    node_host= fields.Char('SaBRO API Host')
    protocol = fields.Selection([('jsonrpc+ssl', 'jsonrpc+ssl'),('jsonrpc', 'jsonrpc')], string='SaBRO API Protocol', default='jsonrpc+ssl', required= True)
    port= fields.Integer('SaBRO API Port', default=443, required= True)
    timeout= fields.Integer('SaBRO API Timeout', default=600, required= True)
    login= fields.Char(required= True)
    password= fields.Char(required= True)
    centrex_sip_registration_url = fields.Char('Centrex Registration URL')
    sabro_customer_id = fields.Char('SaBRO Customer ID', required= True)
    
    
    _sql_constraints = [
                         ('sabro_customer_id', 
                          'UNIQUE(sabro_customer_id)',
                          'SaBRO Customer ID has to be unique!')
                        ]
    _rec_name='name'
    
    @api.model
    def create(self, vals):
        createObj = super(SabroAuth, self).create(vals)
        self.env['sabro_users'].getSabroUsers()
        return createObj
    
# Function for creating Odoo RPC object
# Return parameter : OdooRPC object    
    def getNodeAuthentication(self, uid = False):
        searchConfigurationObj= self.search([])
        if not searchConfigurationObj:
            raise ValidationError(_('SaBRO NODE API Credentials Not Set.'))
        else:
            data = {'login':False, 'password':False}
            if uid:
                userObj = self.env['res.users'].sudo().browse(uid)
                data['login'] = userObj.login
                data['password'] = userObj.sabro_user.odoo_auth_key
            else:
                data['login'] = searchConfigurationObj[0].login
                data['password'] = searchConfigurationObj[0].password
            data.update({
                    'node_host': searchConfigurationObj[0].node_host, 
                    'node_web_url': searchConfigurationObj[0].node_web_url, 
                    'protocol': searchConfigurationObj[0].protocol, 
                    'port': searchConfigurationObj[0].port, 
                    'timeout': searchConfigurationObj[0].timeout, 
                    })
            if 'node_host' in data.keys() and data['login'] and data['password']:
                odoorpcResponse= odoorpc.ODOO(data['node_host'],protocol=data['protocol'],port=data['port'],timeout=data['timeout'])
                odoorpcResponse.login(data['node_host'], data['login'], data['password'])
                return odoorpcResponse
            else:
                raise ValidationError(_('SaBRO NODE API Details Not Set.'))
    
class SabroUsers(models.Model):
    _name = 'sabro_users'
    name = fields.Char(compute='_compute_name', store=True)
    node_user_name = fields.Char('User Name')
    node_user_id = fields.Integer('NODE User ID')
    odoo_auth_key = fields.Char('Auth Key')
    node_user_extension = fields.Integer('NODE User Extension')
    access_level = fields.Selection([('group_cs_user', 'SaBRO User'),('group_cs_admin', 'SaBRO Admin'),('group_node_admin', 'SaBRO System Admin')], string='Access Level')

    _sql_constraints = [
                         ('node_user_id', 
                          'UNIQUE(node_user_id)',
                          'NODE User ID has to be unique!')
                        ]
    _rec_name = 'name'

    @api.multi
    @api.depends('node_user_name', 'node_user_extension')
    def _compute_name(self):
        for record in self:
            if record.node_user_name and record.node_user_extension:
                record.name = record.node_user_name + (' [' + str(record.node_user_extension)+ ']')
            else:
                record.name = False

    @api.multi            
    def write(self, vals):
        if 'access_level' in vals.keys():
            RPCobject= self.env['sabro_auth'].sudo().getNodeAuthentication()
            sabroResponse = RPCobject.env['sabro_odoo'].updateSabroUserAccess('self', self.node_user_id, vals['access_level'])
            if sabroResponse:
                return super(SabroUsers, self).write(vals)
            raise UserError(_("An error occured in updating access level."))
        return super(SabroUsers, self).write(vals)
 
    def getSabroUsers(self):
        RPCobject= self.env['sabro_auth'].sudo().getNodeAuthentication()
        sabroUserList = RPCobject.env['sabro_odoo'].getSabroUsers('self')
        _logger.info(sabroUserList)
        for sabroUser in sabroUserList:
            localSabroUserObj = self.sudo().search([('node_user_id', '=', sabroUser['node_user_id'])])
            if localSabroUserObj:
                localSabroUserObj.write(sabroUser)
            else:
                self.sudo().create(sabroUser)
        return True

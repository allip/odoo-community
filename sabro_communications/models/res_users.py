# -*- coding: utf-8 -*-
import odoo
from odoo import api, fields, models, _
import random, string
from odoo.http import request
from odoo.exceptions import AccessDenied, ValidationError, AccessError, MissingError, Warning, UserError
import logging
_logger=logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    sabro_enabled = fields.Boolean('Enable SaBRO Communications', default = False)
    sabro_user_remapped = fields.Boolean('Existing SaBRO User?', default = False)
    sabro_user = fields.Many2one('sabro_users', 'SaBRO User')
    sabro_login = fields.Text('Manage SaBRO Account', compute='_compute_sabro_login')
    sabro_admin_login = fields.Text('Manage SaBRO Account', compute='_compute_sabro_admin_login')

    def __init__(self, pool, cr):
        """ Override of __init__ to add access rights on sabro_user
            fields. Access rights are disabled by default, but allowed
            on some specific fields defined in self.SELF_{READ/WRITE}ABLE_FIELDS.
        """
        init_res = super(ResUsers, self).__init__(pool, cr)
        # duplicate list to avoid modifying the original reference
        type(self).SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        type(self).SELF_WRITEABLE_FIELDS.extend(['sabro_enabled']) # TO BE REMOVED
        type(self).SELF_WRITEABLE_FIELDS.extend(['sabro_user_remapped']) # TO BE REMOVED
        type(self).SELF_WRITEABLE_FIELDS.extend(['sabro_user']) # TO BE REMOVED
        # duplicate list to avoid modifying the original reference
        type(self).SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        type(self).SELF_READABLE_FIELDS.extend(['sabro_enabled'])
        type(self).SELF_READABLE_FIELDS.extend(['sabro_user_remapped'])
        type(self).SELF_READABLE_FIELDS.extend(['sabro_user'])
        type(self).SELF_READABLE_FIELDS.extend(['sabro_login'])
        return init_res

    @api.model            
    def create(self, vals):
        if 'sabro_enabled' in vals.keys():
            if vals['sabro_enabled']:
                if not (vals['sabro_user'] if 'sabro_user' in vals.keys() else False):
                    name = vals['name'] if 'name' in vals.keys() else False
                    login = vals['login'] if 'login' in vals.keys() else False
                    if '@' not in str(login) or not login or not name:
                        raise ValidationError(_("Please make sure that Email/Login for the user is valid"))
                    RPCobject= self.env['sabro_auth'].sudo().getNodeAuthentication()
                    sabroResponse = RPCobject.env['sabro_odoo'].createSabroUser('self', name, login, '', '')
                    if sabroResponse:
                        sabroUserObj = self.env['sabro_users'].sudo().create(sabroResponse)
                        if sabroUserObj:
                            vals['sabro_user'] = sabroUserObj.id
                    else:
                        raise UserError(_("An error occured in enabling SaBRO for user."))
        return super(ResUsers, self).create(vals)

    @api.multi            
    def write(self, vals):
        if 'sabro_enabled' in vals.keys():
            if vals['sabro_enabled']:
                sabro_user = vals['sabro_user'] if 'sabro_user' in vals.keys() else self.sabro_user
                if not sabro_user:
                    name = vals['name'] if 'name' in vals.keys() else self.name
                    login = vals['login'] if 'login' in vals.keys() else self.login
                    if '@' not in str(login) or not login or not name:
                        raise ValidationError(_("Please make sure that Email/Login for the user is valid"))
                    RPCobject= self.env['sabro_auth'].sudo().getNodeAuthentication()
                    sabroResponse = RPCobject.env['sabro_odoo'].createSabroUser('self', name, login, self.mobile, self.phone)
                    if sabroResponse:
                        sabroUserObj = self.env['sabro_users'].sudo().create(sabroResponse)
                        if sabroUserObj:
                            vals['sabro_user'] = sabroUserObj.id
                    else:
                        raise UserError(_("An error occured in enabling SaBRO for user."))
        return super(ResUsers, self).write(vals)

    @api.multi
    @api.depends('sabro_user')
    def _compute_sabro_login(self):
        sabroConfigurationObj = self.env['sabro_auth'].sudo().search([])
        if sabroConfigurationObj:
            sabroBaseUrl = sabroConfigurationObj[0].node_web_url
            for eachRecord in self:
                if eachRecord.sabro_user:
                    if eachRecord.sabro_user.odoo_auth_key:
                        eachRecord.sabro_login = """<table><tr>
                        <td style='padding:5px;'>
                        <form target='_blank' action='"""+str(sabroBaseUrl)+"""/odoo/web/auth' method="post">
                        <input type='hidden' id=login' name='login' value='"""+str(eachRecord.login)+"""' />
                        <input type='hidden' id=password' name='password' value='"""+str(eachRecord.sabro_user.odoo_auth_key)+"""' />
                        <input type='hidden' id=odoo_login' name='odoo_login' value='true' />
                        <input type='hidden' id=mode' name='mode' value='user-settings' />
                        <input type='hidden' id=sabro_user_id' name='sabro_user_id' value='"""+str(eachRecord.sabro_user.node_user_id)+"""' />
                        <input type='submit' value='Access SaBRO as """+str(eachRecord.sabro_user.node_user_name)+"""' class='btn btn-primary btn-sm'>
                        </form>
                        </td>
                        </tr></table>"""
                    else:
                        False

    @api.multi
    @api.depends('sabro_user')
    def _compute_sabro_admin_login(self):
        sabroConfigurationObj = self.env['sabro_auth'].sudo().search([])
        if sabroConfigurationObj:
            sabroBaseUrl = sabroConfigurationObj[0].node_web_url
            for eachRecord in self:
                if eachRecord.sabro_user:
                    if sabroConfigurationObj[0].password and sabroConfigurationObj[0].login and sabroBaseUrl:
                        eachRecord.sabro_admin_login = """<table><tr>
                        <td style='padding:5px;'>
                        <form target='_blank' action='"""+str(sabroBaseUrl)+"""/odoo/web/auth' method="post">
                        <input type='hidden' id=login' name='login' value='"""+str(sabroConfigurationObj[0].login)+"""' />
                        <input type='hidden' id=password' name='password' value='"""+str(sabroConfigurationObj[0].password)+"""' />
                        <input type='hidden' id=odoo_login' name='odoo_login' value='admin' />
                        <input type='hidden' id=mode' name='mode' value='user-settings' />
                        <input type='hidden' id=sabro_user_id' name='sabro_user_id' value='"""+str(eachRecord.sabro_user.node_user_id)+"""' />
                        <input type='submit' value='Manage User at SaBRO' class='btn btn-primary btn-sm'>
                        </form>
                        </td>
                        </tr></table>"""
                    else:
                        eachRecord.sabro_admin_login = False


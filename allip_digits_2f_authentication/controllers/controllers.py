# -*- coding: utf-8 -*-
from odoo import http
import logging
_logger = logging.getLogger(__name__)
from odoo.http import request
import werkzeug
import simplejson
import requests
from odoo.addons.web.controllers.main import db_monodb, ensure_db, set_cookie_and_redirect, login_and_redirect
from odoo import registry as registry_get
from odoo import api, http, SUPERUSER_ID, _
import odoo.addons.web.controllers.main as main
import odoo

class Home(main.Home):
    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)
        if not request.uid:
            request.uid = odoo.SUPERUSER_ID
        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None
        if request.httprequest.method == 'POST':
            old_uid = request.uid
            uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
            if uid is not False:
                with registry_get(request.session.db).cursor() as cr:
                    env = api.Environment(cr, SUPERUSER_ID, {})
                    getDigitsConfigSearch=http.request.env['digits.configuration'].search([])
                    if getDigitsConfigSearch:
                        getUserBrowse = env['res.users'].sudo().browse(uid)
                        user_2f_enable_status = getUserBrowse[0].user_2f_enable_status
                        if user_2f_enable_status:
                            logout=request.session.logout(keep_db=True)
                            request.session['loginKey'] = kw['password']
                            request.session['user_identity'] = uid
                            userMobileNumber  = getUserBrowse[0].partner_id.mobile
                            if userMobileNumber:
                                ir_config_id=env['ir.config_parameter'].sudo().search([('key','=','web.base.url')])
                                base_url=env['ir.config_parameter'].sudo().browse(int(ir_config_id))[0].value
                                return http.request.render('allip_digits_2f_authentication.digit_confirmation_template',{'userMobileNumber':userMobileNumber,'callbackUrl' : base_url+'/verify/login'})
                            else:
                                values['error'] = _("You may have enabled two factor authentication using mobile number, but your mobile number is not setup under your profile. Please contact your Administrator!")
                                return request.render('web.login', values)                    
                request.params['login_success'] = True
                if not redirect:
                    redirect = '/web'
                return http.redirect_with_hash(redirect)
            request.uid = old_uid
            values['error'] = _("Wrong login/password")
        return request.render('web.login', values)

    @http.route('/digit_token', auth="public")
    def get_digit_token(self,**kw):
           getDigitsConfigSearch=http.request.env['digits.configuration'].search([])
           if getDigitsConfigSearch:
               dataInArray=[]
               dataInArray.append({'token':getDigitsConfigSearch[0].digits_consumer_key })
               return simplejson.dumps(dataInArray)
           else:
               return False

    @http.route('/verify/login', auth="public")
    def web_digits_verify_login(self,*args,**kw):
        if 'X-Verify-Credentials-Authorization' in kw:
           digitResponse = kw['X-Verify-Credentials-Authorization']
           getDigitsConfigSearch=http.request.env['digits.configuration'].search([])
           if getDigitsConfigSearch:
               response = requests.get(kw['X-Auth-Service-Provider'],headers={"Authorization":digitResponse})
               if response.status_code == 200:
                       user_obj=http.request.env['res.users']
                       credentials = user_obj.digit_authenticate({'phone_number': response.json().get('phone_number'),'access_token': response.json().get('access_token')['token']})
                       if credentials:
                               return login_and_redirect(*credentials, redirect_url='/web')
                       else:
                           logout=request.session.logout(keep_db=True)
                           return werkzeug.utils.redirect('/web/login')
               else:
                   return werkzeug.utils.redirect('/web/login')
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               


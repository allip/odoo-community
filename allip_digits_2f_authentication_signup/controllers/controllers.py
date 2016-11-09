# -*- coding: utf-8 -*-
from odoo import http
import logging
_logger = logging.getLogger(__name__)
from odoo.http import request
import werkzeug
import simplejson
import requests
from odoo import registry as registry_get
from odoo import api, http, SUPERUSER_ID, _
import odoo.addons.web.controllers.main as main
import odoo.addons.auth_signup.controllers.main as main
from odoo.addons.auth_signup.models.res_users import SignupError

class SignupDigits(main.Home):
    @http.route('/web/signup', type='http', auth='public', website=True)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()
        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                if "login" in kw:
                    if qcontext.get('password') != qcontext.get('confirm_password'):
                        qcontext["error"] = _("Passwords do not match; please retype them.")
                        return request.render('auth_signup.signup', qcontext)
                    if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                        qcontext["error"] = _("Another user is already registered using this email address.")
                        return request.render('auth_signup.signup', qcontext)
                    getDigitsConfigSearch=http.request.env['digits.configuration'].search([])
                    if getDigitsConfigSearch:
                        request.session['loginKey'] = kw['password']
                        request.session['country_code'] = kw['country_code']
                        request.session['confirm_password'] = kw['confirm_password']
                        request.session['mobile_number'] = kw['mobile_number']
                        request.session['login'] = kw['login']
                        request.session['name'] = kw['name']
                        mobile_number = '+'+kw['country_code']+kw['mobile_number']
                        ir_config_id=http.request.env['ir.config_parameter'].sudo().search([('key','=','web.base.url')])
                        base_url=http.request.env['ir.config_parameter'].sudo().browse(int(ir_config_id))[0].value
                        return request.render('allip_digits_2f_authentication.digit_confirmation_template',{'userMobileNumber':str(mobile_number),'callbackUrl' : base_url+'/verify/signup'})
                    else:
                        self.do_signup(qcontext)
                        return super(SignupDigits, self).web_login(*args, **kw)
                else:
                    self.do_signup(qcontext)
                    return super(SignupDigits, self).web_login(*args, **kw)
            except (SignupError, AssertionError), e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    qcontext['error'] = _("Could not create a new account.")
        return request.render('auth_signup.signup', qcontext)
    
    @http.route('/verify/signup', auth="public")
    def web_digits_verify_signup(self,*args,**kw):
        if 'X-Verify-Credentials-Authorization' in kw:
           digitResponse = kw['X-Verify-Credentials-Authorization']
           getDigitsConfigSearch=http.request.env['digits.configuration'].search([])
           if getDigitsConfigSearch:
               response = requests.get(kw['X-Auth-Service-Provider'],headers={"Authorization":digitResponse})
               if response.status_code == 200:
                    mobile_signup_form = '+'+str(request.session['country_code'])+str(request.session['mobile_number'])
                    mobile_from_digit = str(response.json().get('phone_number'))
                    qcontext = {
                                'login' : request.session['login'],
                                'name' : request.session['name'],
                                'password' : request.session['loginKey'],
                                'confirm_password' : request.session['confirm_password'],
                                'redirect' : '',
                                'token' : '',
                                'signup_enabled' : 'True',
                                'reset_password_enabled' : 'False',
                                }
                    if mobile_signup_form == mobile_from_digit:
                        try:
                            self.do_signup(qcontext)
                            getUserBrowse = http.request.env['res.users'].sudo().browse(request.session.uid)
                            getUserBrowse[0].partner_id.mobile = str(mobile_signup_form)
                            http.request.env.cr.commit()
                            return werkzeug.utils.redirect('/web')
                        except:
                            return werkzeug.utils.redirect('/web/signup')
                    return werkzeug.utils.redirect('/web')
               else:
                   return werkzeug.utils.redirect('/web/signup')
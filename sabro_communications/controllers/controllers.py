import odoo
import logging
_logger = logging.getLogger(__name__)
from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError, MissingError, UserError, ValidationError
import simplejson

class SabroController(http.Controller):

    @http.route(['/get/pbx/client/auth','/sabro/hub/auth'], auth="user" , csrf= False, methods=['GET','POST'])
    def getSabroHubAuth(self, **kw):
        odooUserObj = request.env['res.users'].sudo().browse(request.session.uid)
        if odooUserObj.sabro_user:
            RPCobject= request.env['sabro_auth'].sudo().getNodeAuthentication()
            webRTCURLInfo = RPCobject.env['allip_pbx_users'].getWazoWebrtcAuth('self', odooUserObj.sabro_user.node_user_id)
            WebrtcLoginAuthInfo = RPCobject.env['allip_pbx_users'].getWazoWebrtcLoginAuth('self', odooUserObj.sabro_user.node_user_id)
            return simplejson.dumps({'uid': request.session.uid, 'partner_id': odooUserObj.partner_id.id, 'wazo_webrtc_url': webRTCURLInfo['wazo_webrtc_url'], 'wazo_webrtc_port':webRTCURLInfo['wazo_webrtc_port'],'wazo_webrtc_username': WebrtcLoginAuthInfo['wazo_webrtc_username'], 'wazo_webrtc_password':WebrtcLoginAuthInfo['wazo_webrtc_password'], 'wazo_user_email':WebrtcLoginAuthInfo['user_email'], 'success': True})
        return False
    
    @http.route(['/sabro/search/contacts','/search/sabro/contacts'], auth="user" , csrf= False, methods=['GET','POST'])
    def searchSabroContacts(self, **kw):
        personalContactsSearchResult = partnerSearchResult = crmSearchResult = userSearchResult = userCallerIdSearchResult = []
        if 'search' in kw.keys():
            try:
                personalContactsSearchResult = request.env['personal_contacts'].search(['|','|',('name', 'ilike', str(kw['search'])),('phone', 'ilike', str(kw['search']).replace(' ','')[-10:]),('mobile', 'ilike', str(kw['search']).replace(' ','')[-10:])])
            except:
                pass
            try:
                partnerSearchResult = request.env['res.partner'].search(['|','|',('name', 'ilike', str(kw['search'])),('phone', 'ilike', str(kw['search']).replace(' ','')[-10:]),('mobile', 'ilike', str(kw['search']).replace(' ','')[-10:])])
            except:
                pass
            try:
                crmSearchResult = request.env['crm.lead'].search(['|','|',('name', 'ilike', str(kw['search'])),('phone', 'ilike', str(kw['search']).replace(' ','')[-10:]),('mobile', 'ilike', str(kw['search']).replace(' ','')[-10:])])
            except:
                pass
            try:
                userSearchResult = request.env['res.users'].sudo().search(['|','|',('name', 'ilike', str(kw['search'])),('login', '=', str(kw['search'])),('sabro_user.node_user_extension', '=', str(kw['search']))])
            except:
                pass
            try:
                if not userSearchResult:
                    userSearchResult = request.env['res.users'].sudo().search(['|',('name', 'ilike', str(kw['search'])),('login', '=', str(kw['search']))])
            except:
                pass
            try:
                userCallerIdSearchResult = request.env['callerid_verification'].sudo().search([('number', 'ilike', str(kw['search']).replace(' ','')[-10:])])
            except:
                pass
        else:
            try:
                personalContactsSearchResult = request.env['personal_contacts'].search([])
            except:
                pass
            try:
                partnerSearchResult = request.env['res.partner'].search([])
            except:
                pass
            try:
                crmSearchResult = request.env['crm.lead'].search([])
            except:
                pass
            try:
                userSearchResult = request.env['res.users'].sudo().search([])
            except:
                pass
        response = []
        try:
            for eachContact in userSearchResult:
                if eachContact.sabro_user:
                    response.append({'label':str(eachContact.name)+' (EXTN:'+str(eachContact.sabro_user.node_user_extension)+')', 'value':eachContact.sabro_user.node_user_extension, 'id':eachContact.id, 'model':'res.users', 'name':str(eachContact.name)})
        except:
            pass
        try:
            for eachContact in userCallerIdSearchResult:
                if eachContact.user_id:
                    response.append({'label':str(eachContact.user_id.name)+' ('+str(eachContact.number).replace(' ','')+')', 'value':eachContact.number.replace(' ',''), 'id':eachContact.user_id.id, 'model':'res.users', 'name':str(eachContact.user_id.name)})
        except:
            pass
        try:
            for eachContact in partnerSearchResult:
                if eachContact.mobile:
                    response.append({'label':str(eachContact.name)+' (MOB:'+str(eachContact.mobile).replace(' ','')+')', 'value':eachContact.mobile.replace(' ',''), 'id':eachContact.id, 'model':'res.partner', 'name':str(eachContact.name)})
                if eachContact.phone:
                    response.append({'label':str(eachContact.name)+' (PH:'+str(eachContact.phone).replace(' ','')+')', 'value':eachContact.phone.replace(' ',''), 'id':eachContact.id, 'model':'res.partner', 'name':str(eachContact.name)})
        except:
            pass
        try:
            for eachContact in crmSearchResult:
                if eachContact.mobile:
                    response.append({'label':str(eachContact.name)+' (MOB:'+str(eachContact.mobile).replace(' ','')+')', 'value':eachContact.mobile.replace(' ',''), 'id':eachContact.id, 'model':'crm.lead', 'name':str(eachContact.name)})
                if eachContact.phone:
                    response.append({'label':str(eachContact.name)+' (PH:'+str(eachContact.phone).replace(' ','')+')', 'value':eachContact.phone.replace(' ',''), 'id':eachContact.id, 'model':'crm.lead', 'name':str(eachContact.name)})
        except:
            pass
        try:
            for eachContact in personalContactsSearchResult:
                if eachContact.mobile:
                    response.append({'label':str(eachContact.name)+' (MOB:'+str(eachContact.mobile).replace(' ','')+')', 'value':eachContact.mobile.replace(' ',''), 'id':eachContact.id, 'model':'personal_contacts', 'name':str(eachContact.name)})
                if eachContact.phone:
                    response.append({'label':str(eachContact.name)+' (PH:'+str(eachContact.phone).replace(' ','')+')', 'value':eachContact.phone.replace(' ',''), 'id':eachContact.id, 'model':'personal_contacts', 'name':str(eachContact.name)})
        except:
            pass
        return simplejson.dumps({'success': True, 'response':response})
    

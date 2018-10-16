odoo.define('sabro_communications.sabro_communications_hub', function (require) {
	var core = require('web.core');
	var Widget = require('web.Widget');
	var _t = core._t;
	var SystrayMenu = require('web.SystrayMenu');
	var Model = require('web.DataModel');
	var session = require('web.session');
	var communications_hub_dailer_button= Widget.extend({
	    template: "communications-hub-dailer-TopButton",
	    start   : function() {
	                   this._super();
	              },
	});
	new Model('res.users')
     .query(['sabro_enabled', 'sabro_user', 'id'])
     .filter([['sabro_enabled','=',true],['sabro_user','!=',false],['id','=',session.uid]])
     .all()
     .then(function(users){
    	 if(users.length > 0){
    		 SystrayMenu.Items.push(communications_hub_dailer_button);   
    		 return communications_hub_dailer_button;
    	 }
     });
	return false;
});
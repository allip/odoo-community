odoo.define('sabro_communications.sabro_communications_hub', function (require) {
	var core = require('web.core');
	var Widget = require('web.Widget');
	var _t = core._t;
	var SystrayMenu = require('web.SystrayMenu');
	var communications_hub_dailer_button= Widget.extend({
	    template: "communications-hub-dailer-TopButton",
	    start   : function() {
	                   this._super();
	              },
	});
	 $.ajax({
		'async': true,
	    'global': false,
	    'type': "POST",
	    'url': '/get/user/sabro/permission',
	    'dataType': "json",
	    'success': function(response) {
	    	if (response.success){
		    	SystrayMenu.Items.push(communications_hub_dailer_button);   
		   	 	return communications_hub_dailer_button;
	    	}
	    },
		'error': function(){} 
	 });
	 return false
});
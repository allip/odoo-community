# -*- coding: utf-8 -*-
{
    'name': "All-IP Two Factor SMS or Call Authentication (2FA)",
    'summary': """Two Factor SMS or Call Authentication (2FA) Powered By Digits""",
    'description': """
      Strengthen a username and password
      Use SMS or automated calling to receive dynamic codes for secure login
      """,
    'author': "ALL IP LTD",
    'website': "https://www.allipcloud.com",
    'category': 'Extra Tools',
    'license': 'LGPL-3',
    'images': ['static/description/Two-Factor-Authenticaton.png'],
    'version': '1.1',
    'depends': ['base','allip_base'],
    'data': [
        'security/ir.model.access.csv',
        'views/configuration.xml',
        'views/template.xml',
        'views/res_users.xml',
    ],
   
}

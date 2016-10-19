# -*- coding: utf-8 -*-
{
    'name': "All-IP Two-Factor SMS & Call Authentication (2FA)",
    'summary': """Two-Factor SMS & Call Authentication (2FA) Powered By Digits""",
    'description': """
      Strengthen a username and password
      Use SMS or automated calling to receive dynamic codes for secure login
      """,
    'author': "All-IP Cloud",
    'website': "https://www.allipcloud.com",
    'category': 'Extra Tools',
    'license': 'LGPL-3',
    'images': ['static/description/Two-Factor-Authenticaton.png'],
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/configuration.xml',
        'views/template.xml',
        'views/res_users.xml',
    ],
   
}

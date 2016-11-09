# -*- coding: utf-8 -*-
{
    'name': "All-IP Signup Two Factor Validation by SMS or Call (2FA)",
    'summary': """Two Factor SMS or Call Validation (2FA) for Signup Powered By Digits""",
    'description': """
      Stop Unwanted Signup and Spammers
      Use SMS or automated calling to validate user's identity during signup
      """,
    'author': "All-IP Cloud",
    'website': "https://www.allipcloud.com",
    'category': 'Extra Tools',
    'license': 'LGPL-3',
    'images': ['static/description/Two-Factor-Authenticaton.png'],
    'version': '1.0',
    'depends': ['base','web','allip_base','allip_digits_2f_authentication','auth_signup'],
    'data': ['views/template.xml',],
   
}

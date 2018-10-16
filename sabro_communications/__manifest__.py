# -*- coding: utf-8 -*-
{
    'name': "SaBRO Communications",

    'summary': """SaBRO Communications""",

    'description': """
        SaBRO Communications
    """,

    'author': "All-IP Cloud",
    'website': "https://www.allip.co.uk",

    'category': 'Communication',
    'version': '1.0',
    'application': True,
    'sequence': 1,

    'external_dependencies': {'python' : ['odoorpc'],},
    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
         'security/ir.model.access.csv',
         'data/ir_cron.xml',
         'views/view.xml',
         'views/res_users_view.xml',
    ],
    'qweb': [
        'static/src/xml/communications_hub_view.xml',
    ],  
}

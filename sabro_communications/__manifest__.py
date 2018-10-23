# -*- coding: utf-8 -*-
{
    'name': "SaBRO Communications",
    'summary': """SaBRO Communications""",
    'description': """
        SaBRO Communications
    """,
    'author': "All-IP Cloud",
    'website': "https://www.allipcloud.com",
    'category': 'Communication',
    'license': 'LGPL-3',
    'version': '1.0',
    'application': True,
    'sequence': 1,
    'images': ['static/src/img/sabroCommunications.png'],
    'external_dependencies': {'python' : ['odoorpc'],},
    'depends': ['base'],
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

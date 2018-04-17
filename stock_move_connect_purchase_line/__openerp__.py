# -*- coding: utf-8 -*-
{
    'name': "Stock Move Connect - Puchase Line",

    'summary': """
        Glue module to allow connection with purchase lines
        """,

    'description': """
    """,

    'author': "Jörn Krenzer",
    'website': "https://github.com/jkrenzer",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'auto_install': True,

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock_move_connect', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'templates.xml',
    ],
}

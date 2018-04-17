# -*- coding: utf-8 -*-
{
    'name': "Stock Move Connect",

    'summary': """
        This module allows to set or edit the connections of a move to purchase lines, invoices lines etc.
        """,

    'description': """
    """,

    'author': "Jörn Krenzer",
    'website': "https://github.com/jkrenzer/odooAddons",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_move.xml',
        'wizard/stock_move_connect.xml',
    ],
}

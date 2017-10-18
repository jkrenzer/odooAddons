# -*- coding: utf-8 -*-
{
    'name': "MRP BoM: Larger Reference-Codes",

    'summary': """
        Allow larger reference-codes in BOMs, so you can fit almost any arbitrary code in there.""",

    'description': """
    """,

    'author': "Jörn Mankiewicz",
    'website': "http://github.com/jmankiewicz",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}

# -*- coding: utf-8 -*-
{
    'name': "Separate Name and Partner Refs for Invoices",

    'summary': """
        Odoo's standard behaviour is to use the invoice-number as main naming context of the invoice documents. This module changes this in the corresponding tree views and adds a partner reference so we can additionally  show from which partner document the invoice originated.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Jörn Krenzer",
    'website': "http://github.com/jkrenzer",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
	'data/invoice_sequence.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}

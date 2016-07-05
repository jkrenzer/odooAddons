# -*- coding: utf-8 -*-
{
    'name': "stock_picking_delivery_note",

    'summary': """
        Add capability to print a delivery note on stock-pickings.""",

    'description': """
        This modules adds a delivery note to stock pickings, which can be printed out and handed to the customer.
    """,

    'author': "Jörn Mankiewicz",
    'website': "https://github.com/jmankiewicz",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '8.0.0.1',

    # any module necessary for this one to work correctly
    'depends': [
	'base',
	'stock',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
	'delivery_note_sequence.xml',
	'stock_picking.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
    'installable': True,
}

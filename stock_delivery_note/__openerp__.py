# -*- coding: utf-8 -*-
{
    'name': "Stock Picking Delivery Notes",

    'summary': """
        Add capability to print a delivery note on stock-pickings.""",

    'description': """
        This modules adds a delivery note to stock pickings, which can be printed out and handed to the customer.
    """,

    'author': "Jörn Krenzer",
    'website': "https://github.com/jkrenzer",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '8.0.0.3',

    # any module necessary for this one to work correctly
    'depends': [
	'base',
	'stock',
	'report_german_letter', #TO BE CHANGED
    ],

    # always loaded
    'data': [
        'security/stock_delivery_note_security.xml',
        'security/ir.model.access.csv',
        'views/stock_delivery_note_report.xml',
	'views/stock_delivery_note_form.xml',
	'views/stock_delivery_note_menu.xml',
	'views/stock_delivery_note_tree.xml',
        'views/stock_delivery_note_search.xml',
        'views/stock_delivery_note_actions.xml',
	'sequences/delivery_note_sequence.xml',
	'views/stock_picking.xml',
	'workflow/stock_delivery_note.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
    'installable': True,
}

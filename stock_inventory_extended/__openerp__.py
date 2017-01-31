# -*- coding: utf-8 -*-
{
    'name': "Stock Inventory Extended",

    'summary': """
        Extends inventories for easier handling.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Jörn Mankiewicz",
    'website': "https://github.com/jmankiewicz",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '8.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'stock_inventory.xml',
	'stock_inventory_line.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}

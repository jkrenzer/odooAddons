# -*- coding: utf-8 -*-
{
    'name': "Product Price and Valuation Correction",

    'summary': """
        Provides tools to correct the product pricing and valuation.
     """,

    'description': """
        Odoo has serverl different strategies to save and calculate costs and prices for the inventory valuation.
        This module provices tools for evaluation the costs and correctin them, if necessary.
    """,

    'author': "Jörn Krenzer",
    'website': "https://github.com/jkrenzer/odooAddons",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'stock_account', 'product_variant_cost_price'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_price_correction_actions.xml',
        'views/product_price_correction_form.xml',
        'views/product_price_correction_menu.xml',
        'views/product_price_correction_search.xml',
        'views/product_price_correction_tree.xml',
	'security/ir.model.access.csv', 
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}

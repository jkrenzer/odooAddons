# -*- coding: utf-8 -*-
{
    'name': "Advanced Product Cost Management",

    'summary': """
        Adds an in-depth managment utility for product costs based on BoMs and production orders.""",

    'description': """
        This module strives to help with the management and awareness of product costs. Therefor it calculates the costs of materials and work
        rendered and makes this information available.""",

    'author': "Jörn Krenzer",
    'website': "https://github.com/jkrenzer/odooAddons",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/mrp_bom.xml',
        'views/product_product.xml',
    ],
    # only loaded in demonstration mode
#    'demo': [
#        'demo.xml',
#    ],
}

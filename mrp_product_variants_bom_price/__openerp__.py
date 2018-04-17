# -*- coding: utf-8 -*-
{
    'name': "MRP - Product variants standard price in BoM",

    'summary': """Glue-module which corrects the price displayed on the BoM.""",

    'description': """
        The module product_extended adds the standard price of the product template as related field in the BoM. This glue-module \
       adds the variant prices instead. It should be automatically installed when all dependencies are fullfilled.
    """,

    'author': "Jörn Krenzer",
    'website': "https://github.com/jkrenzer/odooAddons",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product_extended', 'mrp_product_variants'],
    'auto_install': True,

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

# -*- coding: utf-8 -*-
{
    'name': "Advanced Prodcut Cost Management - Real Production Costs",

    'summary': """
        Glue-module which allows to see real production costs on quants
     """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Jörn Krenzer",
    'website': "https://github.com/jkrenzer/odooAddons",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product_cost_management', 'mrp_production_real_cost'],

    # automatically install
    'auto_install': True,

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_quant.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}

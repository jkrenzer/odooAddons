# -*- coding: utf-8 -*-
{
    'name': "MRP BoM: More informations in tree-view",

    'summary': """
        Show not only the name but also the reference and some more informations in the BoM-tree-view.""",

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
    'depends': ['base','mrp','product_extended'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo.xml',
    ],
}

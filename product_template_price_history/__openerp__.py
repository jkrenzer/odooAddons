# -*- coding: utf-8 -*-
{
    'name': "Product Template Price History",

    'summary': """
        Make the saved, history prices of the product templates accessable.
    """,

    'description': """
        This module allows to see and edit the saved history prices of the product templates and
        makes it feasable to fill in information from before the usage of Odoo or to correct wrong
        entries which confuse the reports generate for bilance and cost accounting.
    """,

    'author': "Jörn Krenzer",
    'website': "https://github.com/jkrenzer/odooAddons",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_price_history_form.xml',
        'views/product_price_history_tree.xml',
        'views/product_price_history_menu.xml',
        'views/product_price_history_search.xml',
    ],
}

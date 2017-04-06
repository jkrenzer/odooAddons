# -*- coding: utf-8 -*-
{
    'name': "Separate Handling of Advance and Discounts",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Jörn Mankiewicz",
    'website': "https://github.com/jmankiewicz",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_invoice_form.xml',
#        'views/report_invoice.xml', Untested!!
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}

# -*- coding: utf-8 -*-
{
    'name': "report_german_letter",

    'summary': """
        German DIN-letter format for your reports""",

    'description': """
        This module changes the format of purchase- and sale-orderes to conform DIN-Brief.
    """,

    'author': "Your Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates/report_german_letter_layout.xml',
        'templates/report_german_letter_layout_header.xml',
        'templates/report_german_letter_layout_footer.xml',
        'templates/report_purchaseorder_document.xml',
        'templates/report_purchasequotation_document.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}

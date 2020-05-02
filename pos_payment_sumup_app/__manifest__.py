# -*- coding: utf-8 -*-
{
    'name': "POS Payment With Sumup App",

    'summary': """
        Add a payment link to the POS checkout to open the installed SUMUP app for \
        payment processing.   
     """,

    'description': """
        This module allows to add a payment link to the POS checkout screen which
        will be open the installed SUMUP-App for processing the payment. \
                                                                         \
        This will only work if the devices used for the POS is using Android or IOS and
        has the SUMUP app installed!
    """,

    'author': "Jörn Krenzer",
    'website': "https://github.com/jkrenzer",
    'license': "AGPL-3",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Point Of Sale',
    'version': '11.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/pos_config.xml',
        'views/account_journal.xml',
        'views/pos_payment_sumup_app_assets.xml',
    ],
    # QWeb templates for POS
    'qweb': [
        'static/src/xml/pos_payment_sumup_app.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
}

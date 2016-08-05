# -*- coding: utf-8 -*-
{
    'name': "Extended Purchase Orders",

    'summary': """
        Module which extends the purchase-order workflow to better differentiate RFQs and POs and also adds the possibility to derive POs without loosing the original RFQ.
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Jörn Mankiewicz",
    'website': "https://github.com/jmankiewicz/odooAddons",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    "version": "8.0.0.1",

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','purchase_rfq_bid_workflow','purchase_order_revision'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'view/purchase_order.xml',
	'data/purchase_sequence.xml',
        #'purchase_order_extended.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
    "installable": True,
}

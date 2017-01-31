# -*- coding: utf-8 -*-
{
    'name': "Quality Control Report",

    'summary': """
        Print quality-reports.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Jörn Mankiewicz",
    'website': "https://github.com/jmankiewicz",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '8.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','quality_control','quality_control_mrp','quality_control_stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'sequences/qc_report_sequence.xml',
        'views/reports.xml',
        'views/workflow.xml',
        'views/form.xml',
        'views/menu.xml',
        'views/print_wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}

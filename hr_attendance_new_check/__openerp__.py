# -*- coding: utf-8 -*-
{
    'name': "Better validation for Attendance",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Jörn Mankiewicz",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '8.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_attendance','hr_timesheet_improvement'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/hr_attendance.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}

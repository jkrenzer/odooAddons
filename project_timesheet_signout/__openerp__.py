# -*- coding: utf-8 -*-
{
    'name': "Bill Timesheet to Task on Signout",

    'summary': """
        Add possibility to assign activity to task on signout screen""",

    'description': """
        project_timesheet adds the capability to assign activities to task. This module adds
        an userfriendly way to do this assignment on signout.
    """,

    'author': "Jörn Mankiewicz",
    'website': "https://github.com/jmankiewicz",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '8.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_timesheet', 'timesheet_task'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/hr_timesheet_sign_in_out_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}

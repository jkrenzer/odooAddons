# -*- coding: utf-8 -*-
{
    'name': "See All User on Task-Timesheet",

    'summary': """
        Make timesheet-activities of all users visible on task to help in coordination of small teams.""",

    'description': """
        This module alles all project members to see what activites where done by all participients. This
	helps in coordinating small teams without having to replicate all information on done activities as
	messages in the tasks.
    """,

    'author': "Jörn Mankiewicz",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '8.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','project_timesheet', 'timesheet_task'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/project_task.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}

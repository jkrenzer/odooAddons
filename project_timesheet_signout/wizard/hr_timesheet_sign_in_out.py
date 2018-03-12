# -*- coding: utf-8 -*-

from openerp import models, api, fields, osv, exceptions
from openerp.tools.translate import _

class SignoutWizard(models.TransientModel):
	_inherit = 'hr.sign.out.project'
	_name = 'hr.sign.out.project'
	_description = 'Sign Out By Project and Task'
	
	task_id = fields.Many2one(comodel_name='project.task', string='Task')
	issue_id = fields.Many2one(comodel_name='project.issue', string='Issue')

	@api.multi
	@api.onchange('account_id')
	def _onchange_account(self):
		for obj in self:
			if self.account_id:
				return {
						'domain': {
							'task_id': [
								('project_id.analytic_account_id.id','=',obj.account_id.id)
							],
							'issue_id': [
                                                                ('project_id.analytic_account_id.id','=',obj.account_id.id)
                                                        ],
						}
					}
			else:
				return {
						'domain': {
							'task_id': [ 
								(1,'=',1)
							],
							'issue_id': [ 
                                                                (1,'=',1)
                                                        ],
						}
					}
	
	@api.multi
	@api.onchange('task_id')
	def _onchange_task(self):
		for obj in self:
			if obj.task_id.project_id and obj.task_id.project_id.analytic_account_id:
				obj.account_id = obj.task_id.project_id.analytic_account_id

	@api.multi
	@api.onchange('issue_id')
	def _onchange_issue(self):
		for obj in self:
			if obj.issue_id.project_id and obj.issue_id.project_id.analytic_account_id:
				obj.account_id = obj.issue_id.project_id.analytic_account_id
	

	@api.model
	def _write(self, data, emp_id, context=None):
		timesheet_act_id = super(SignoutWizard, self)._write(data, emp_id, context=context)
		timesheet_act = self.env['hr.analytic.timesheet'].browse(timesheet_act_id)
		if hasattr(timesheet_act, 'task_id') and data['task_id']:
			timesheet_act.task_id =  data['task_id']
		elif data['task_id']:
			raise Warning(_('Please check module dependencies. Task-Timesheet relation is not implemented!'))
		if hasattr(timesheet_act, 'issue_id') and data['issue_id']:
                        timesheet_act.issue_id =  data['issue_id']
                elif data['issue_id']:
                        raise Warning(_('Please check module dependencies. Issue-Timesheet relation is not implemented!'))
		return timesheet_act_id

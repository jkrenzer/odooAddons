# -*- coding: utf-8 -*-

from openerp import models, api, fields, osv, exceptions
from openerp.tools.translate import _

class SignoutWizard(models.TransientModel):
	_inherit = 'hr.sign.out.project'
	_name = 'hr.sign.out.project'
	_description = 'Sign Out By Project and Task'
	
	task_id = fields.Many2one(comodel_name='project.task', string='Task')

	@api.multi
	@api.onchange('account_id')
	def _onchange_account(self):
		for obj in self:
			if self.account_id:
				return {'domain':{'task_id':[('project_id.analytic_account_id.id','=',obj.account_id.id)]}}
			else:
				return {'domain':{'task_id':[(1,'=',1)]}}
	
	@api.multi
	@api.onchange('task_id')
	def _onchange_task(self):
		for obj in self:
			if obj.task_id.project_id and obj.task_id.project_id.analytic_account_id:
				obj.account_id = obj.task_id.project_id.analytic_account_id
			return {'domain':{'task_id':[('project_id.analytic_account_id','=',obj.account_id)]}}
	

	@api.model
	def _write(self, data, emp_id):
		timesheet_act_id = super(SignoutWizard, self)._write(data, emp_id)
		timesheet_act = self.env['hr.analytic.timesheet'].browse(timesheet_act_id)
		if hasattr(timesheet_act, 'task_id') and data['task_id']:
			timesheet_act.task_id =  data['task_id']
		elif data['task_id']:
			raise Warning(_('Please check module dependencies. Task-Timesheet relation is not implemented!'))
		return timesheet_act_id

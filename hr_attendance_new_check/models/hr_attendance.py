# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import ValidationError

class Attendance(models.Model):
	_inherit="hr.attendance"

	validate = fields.Boolean(string='Validate', help='Check to let Odoo validate if this attendance-event is plausible.', default=True)
	valid = fields.Boolean(string='Valid', help='Indicates, that this item has passed validation successfully.', compute='_compute_valid',default=False, readonly=True)
	worked_hours = fields.Float(string='Worked Hours', store=True, compute='_worked_hours_compute')
	action = fields.Selection([('sign_in', 'Sign In'), ('sign_out', 'Sign Out'), ('action','Action')], 'Action', required=True)

	@api.multi
	@api.onchange('valid','name')
	def _worked_hours_compute(self):
		for obj in self:
			if obj.action == 'sign_in':
				obj.worked_hours = 0
			elif obj.action == 'sign_out' and obj.valid:
				# Get the associated sign-in
				last_signin_id = self.search(cr, uid, [
					('employee_id', '=', obj.employee_id.id), ('valid', '=', True),
					('name', '<', obj.name), ('action', '=', 'sign_in')
				], limit=1, order='name DESC')
				if last_signin_id:
					last_signin = self.browse(cr, uid, last_signin_id, context=context)[0]
					# Compute time elapsed between sign-in and sign-out
					last_signin_datetime = datetime.strptime(last_signin.name, '%Y-%m-%d %H:%M:%S')
					signout_datetime = datetime.strptime(obj.name, '%Y-%m-%d %H:%M:%S')
					workedhours_datetime = (signout_datetime - last_signin_datetime)
					obj.worked_hours = ((workedhours_datetime.seconds) / 60) / 60.0
				else:
					obj.worked_hours = False
	
	@api.multi
	@api.onchange('validate','name','action')
	def _compute_valid(self):
		for obj in self:
			 obj.valid = super(Attendance,obj)._altern_si_so()
	
	@api.multi
	@api.constrains('name','action','validate')
	def _constrain_valid(self):
		for obj in self:
			if obj.validate and not super(Attendance,obj)._altern_si_so():
				raise ValidationError('Error ! Sign in (resp. Sign out) must follow Sign out (resp. Sign in)')
	@api.one
	def _altern_si_so(self): #Dummy to override old constraint
                return True

	_constraints = [(_altern_si_so, 'Error ! Sign in (resp. Sign out) must follow Sign out (resp. Sign in)', ['action'])] #Override old constraint

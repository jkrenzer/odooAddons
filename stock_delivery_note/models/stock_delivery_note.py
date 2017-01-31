# -*- coding: utf-8 -*-

from openerp import models, fields, api

class stock_delivery_note(models.Model):
	_name = 'stock.delivery_note'
	_description = 'Delivery Note'
	_inherit = ['mail.thread', 'ir.needaction_mixin']

	@api.multi
	def _get_current_user(self):
        	return self.env.user

	@api.one
	@api.constrains('name')
	def _check_unique_constraint(self):
         if len(self.search([('name', '=', self.name)])) > 1:
             raise ValidationError("Name already exists and violates unique field constraint")

	STATE_SELECTION = [
                ('draft', 'Draft'),
                ('confirm', 'Confirm'),
                ('done', 'Done'),
                ('cancel', 'Cancelled')
        ]

	name = fields.Char(string="Name", default='/', required=True)
	notes = fields.Html(string="Additional Notes", help="Additional notes which should appear on the Delivery Note")
	pickings = fields.Many2many(string="Pickings", comodel_name="stock.picking", copy=True, readonly=False)
	date = fields.Datetime(string="Created", default=fields.Datetime.now, required=True)
	responsible = fields.Many2one(string="Responsible", comodel_name="res.users", required=True, default=_get_current_user)
	partner_id = fields.Many2one(string="Partner", comodel_name="res.partner", required=True)
	state = fields.Selection(STATE_SELECTION, 'Status', readonly=True, help="State of the delivery note. Draft marks a note being worked on, confirmed notes are filled appropiately. Notes marked as done have been sent or agreed upon by the recipient.", default='draft', select=True) 

	@api.model
	def create(self, vals):
		if vals.get('name', '/') == '/':
        		vals['name'] = self.env['ir.sequence'].get('stock.delivery_note')
        	if vals.get('responsible', '/') == '':
            		vals['responsible'] = self._get_current_user()
        	return super(stock_delivery_note, self).create(vals)

	@api.one
        def print_report(self):
                '''This function prints the delivery note'''
		return self.env['report'].render('report_delivery_note_view')

	#State functions

	@api.one
	def _state_draft(self):
		'''This function marks the delivery note as draft'''
		if self.state != 'draft':
			self.state = 'draft'
			self.message_post(body=_("Delivery Note marked as draft"), subtype="mail.mt_comment")
		return True

        @api.one
        def _state_confirm(self):
                '''This function marks the delivery note as confirmed'''
                if self.state != 'confirm':
                        self.state = 'confirm'
                        self.message_post(body=_("Delivery Note confirmed by %s") % self.env.uid.name, subtype="mail.mt_note")
                return True

        @api.one
        def _state_done(self):
                '''This function marks the delivery note as done'''
                if self.state != 'done':
                        self.state = 'done'
                        self.message_post(body=_("Delivery Note marked done by %s") % self.env.uid.name, subtype="mail.mt_note")
                return True

        @api.one
        def _state_cancel(self):
                '''This function marks the delivery note as cancelled'''
                if self.state != 'cancel':
                        self.state = 'cancel'
                        self.message_post(body=_("Delivery Note cancelled by %s") % self.env.uid.name, subtype="mail.mt_note")
                return True

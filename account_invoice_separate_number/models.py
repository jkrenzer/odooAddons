# -*- coding: utf-8 -*-

from openerp import models, fields, api

class AccountInvoice(models.Model):
	_inherit="account.invoice"
        _order = "name desc, id desc"
        _sql_constraints = [
            ('name_uniq', 'unique(name, company_id)', 'Invoice Reference must be unique per Company!'),
        ]

        partner_ref = fields.Char(string="Partner Reference", copy=True, help="Reference origin of our partner to which this invoice belongs. Can be an order reference for example.")

        @api.one
        def action_number(self):
            if not self.name or self.name == "/":
                recs = self.env['ir.sequence']
		if self.type == "out_invoice" or self.type is None:
	                self.name = recs.next_by_code('account.invoice.customer.invoice')
		elif self.type == "out_refund":
			self.name = recs.next_by_code('account.invoice.customer.refund')
		elif self.type == "in_invoice":
			self.name = recs.next_by_code('account.invoice.supplier.invoice')
		elif self.type == "in_refund":
			self.name = recs.next_by_code('account.invoice.supplier.refund')
            return super(AccountInvoice, self).action_number()

#	@api.model
#        def create(self, values):
#                if 'name' not in values or values['name'] == '/':
#                        recs = self.env['ir.sequence']
#                        values['name'] = recs.next_by_code('account.invoice.number')
#                invoice = super(AccountInvoice, self).create(values)
#                return invoice

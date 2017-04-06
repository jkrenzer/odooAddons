# -*- coding: utf-8 -*-

from openerp import models, fields, api

# class account_invoice_seperate_number(models.Model):
#     _name = 'account_invoice_seperate_number.account_invoice_seperate_number'

#     name = fields.Char()

class AccountInvoice(models.Model):
	_inherit="account.invoice"

	number = fields.Char(readonly=False, copy=False, default="/")

	@api.model
        def create(self, values):
                if 'number' not in values or values['number'] == '/':
                        recs = self.env['ir.sequence']
                        values['number'] = recs.next_by_code('account.invoice.number')
                invoice = super(AccountInvoice, self).create(values)
                return invoice

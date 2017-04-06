# -*- coding: utf-8 -*-

from openerp import models, fields, api

class AccountInvoice(models.Model):
	_inherit = "account.invoice"
	is_installment = fields.Boolean(string="Installment", default=False) 

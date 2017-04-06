# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date

# class account_invoice_provision_date(models.Model):
#     _name = 'account_invoice_provision_date.account_invoice_provision_date'

#     name = fields.Char()

class AccountInvoice(models.Model):
	_inherit="account.invoice"

	date_provision = fields.Date(string="Provision Date", default=date.today())

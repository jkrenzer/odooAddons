# -*- coding: utf-8 -*-

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    amount_pos_untaxed = fields.Float(string='Subtotal', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    amount_pos_tax = fields.Float(string='Tax', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_amount')
    amount_pos_total = fields.Float(string='Total', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_amount')

    amount_neg_untaxed = fields.Float(string='Subtotal', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    amount_neg_tax = fields.Float(string='Tax', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_amount')
    amount_neg_total = fields.Float(string='Total', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_amount')

    invoice_pos_line = fields.One2many('account.invoice.line', 'invoice_id', string='Positive Invoice Lines',
        readonly=True, compute='_compute_lines', store=False)
    invoice_neg_line = fields.One2many('account.invoice.line', 'invoice_id', string='Negative Invoice Lines',
        readonly=True, compute='_compute_lines', store=False)

    @api.one
    @api.depends('invoice_line.price_subtotal')
    def _compute_lines(self):
        self.invoice_pos_line = self.invoice_line.filtered(lambda record: record.price_subtotal >= 0)
        self.invoice_neg_line = self.invoice_line.filtered(lambda record: record.price_subtotal < 0)

    @api.one
#    @api.depends('invoice_pos_line', 'tax_pos_line')
    def _compute_pos_amount(self):
        self.amount_pos_untaxed = sum(line.price_subtotal for line in self.invoice_pos_line)
        self.amount_pos_tax = sum(line.total_tax_amount for line in self.invoice_pos_line)
        self.amount_pos_total = self.amount_pos_untaxed + self.amount_pos_tax

    @api.one
#    @api.depends('invoice_neg_line', 'tax_neg_line')
    def _compute_neg_amount(self):
        self.amount_neg_untaxed = sum(line.price_subtotal for line in self.invoice_neg_line)
        self.amount_neg_tax = sum(line.total_tax_amount for line in self.invoice_neg_line)
        self.amount_neg_total = self.amount_neg_untaxed + self.amount_neg_tax

    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount')
    def _compute_amount(self):
        self._compute_pos_amount()
        self._compute_neg_amount()
        self.amount_untaxed = self.amount_pos_untaxed +  self.amount_neg_untaxed
        #Add alarm if tax-calculations do not match
        self.amount_tax = sum(line.amount for line in self.tax_line)
        self.amount_total = self.amount_untaxed + self.amount_tax

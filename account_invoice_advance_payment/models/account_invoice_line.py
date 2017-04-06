from openerp import api, models, fields
import openerp.addons.decimal_precision as dp

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    price_subtotal_tax = fields.Float(compute='_compute_price_tax', string=' Total including tax', digits= dp.get_precision('Product Price'), store=True)
    total_tax_amount =  fields.Float(compute='_compute_price_tax', string=' Total tax amount', digits= dp.get_precision('Product Price'), store=True)


    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_id', 'quantity', 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id')
    def _compute_price_tax(self):
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        taxes = self.invoice_line_tax_id.compute_all(price, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
        self.price_subtotal_tax = taxes['total_included']
        self.total_tax_amount = sum(tax['amount'] for tax in taxes['taxes'])
        if self.invoice_id:
              self.price_subtotal_tax = self.invoice_id.currency_id.round(self.price_subtotal_tax)
              self.total_tax_amount = self.invoice_id.currency_id.round(self.total_tax_amount)

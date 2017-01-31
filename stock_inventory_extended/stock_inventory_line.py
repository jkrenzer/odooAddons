# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions

class StockInventoryLine(models.Model):
	_inherit = 'stock.inventory.line'

	checked = fields.Boolean(string="Checked", default=False, copy=False, help="Position has been checked")

	@api.onchange("product_qty")
	@api.multi
	def _onchange_product_qty(self):
		for rec in self:
			rec.checked = True

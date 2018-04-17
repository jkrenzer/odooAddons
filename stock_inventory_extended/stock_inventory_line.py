# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions

class StockInventoryLine(models.Model):
	_inherit = 'stock.inventory.line'
        
        @api.one
        def _default_checked(self):
            if self.state == 'done':
               return True
            else:
               return False

	checked = fields.Boolean(string="Checked", default=_default_checked, copy=False, help="Position has been checked")
        real_value = fields.Float(string="Real Value", compute="_compute_value", store=True, help="Value based on counted amount")
        theoretical_value = fields.Float(string="Theoretical Value", compute="_compute_value", store=True, help="Value based on the theoretical amount")
 
        @api.multi
        @api.depends('theoretical_qty','product_qty','product_id')
        def _compute_value(self):
            for line in self:
                line.theoretical_value = line.product_id.estimated_material_cost * line.theoretical_qty
                line.real_value = line.product_id.estimated_material_cost * line.product_qty

	@api.onchange("product_qty")
	@api.multi
	def _onchange_product_qty(self):
		for rec in self:
			rec.checked = True
        
        @api.onchange("state")
        @api.multi
        def _onchange_state(self):
                for rec in self:
                        if rec.state == 'done':
                            rec.checked = True

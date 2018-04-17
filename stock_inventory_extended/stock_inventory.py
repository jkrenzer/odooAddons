# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions

class StockInventory(models.Model):
	_inherit = 'stock.inventory'

	lines_count = fields.Integer(compute='_lines_count', string="Number of inventory lines")
        real_value = fields.Float(string="Real Value", compute="_compute_value", store=False, help="Value based on counted amounts and the corresponding standard-prices.")
        theoretical_value = fields.Float(string="Theoretical Value", compute="_compute_value", store=False, help="Value based on the theoretical amounts and the corresponding standard-prices.")

        @api.multi
        @api.depends('line_ids')
        def _compute_value(self):
            for inventory in self:
                real_value = 0.0
                theoretical_value = 0.0
                for line in inventory.line_ids:
                    real_value += line.real_value
                    theoretical_value += line.theoretical_value
                inventory.real_value = real_value
                inventory.theoretical_value = theoretical_value

	@api.multi
	@api.depends('line_ids')
	def _lines_count(self):
		for rec in self:
			rec.lines_count = rec.line_ids and len(rec.line_ids) or 0

	@api.multi
	def view_lines(self):
		self.ensure_one() #Ensure we have only one object
		action = {
                        "type": "ir.actions.act_window",
                        "res_model": "stock.inventory.line",
                        "views": [(False, "tree"),(False,'form')],
			"context": {'default_inventory_id' : self.id},
                }
		if len(self.line_ids) > 1:
			lines = [line.id for line in self.line_ids]
			action['domain'] = "[('id','in',[" + ','.join(map(str, lines)) + "])]"
#                        raise Warning('Debug','We have an domain of: %s' % action['domain'])
		else:
			action['views'] = [(False, 'tree'),(False,'form')]
			action['res_id'] =  self.line_ids[0].id or False
# 		         raise Warning('Debug','We have an domain of: %s' % action['domain'])
                return action

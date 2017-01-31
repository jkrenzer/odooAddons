# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import except_orm, Warning, RedirectWarning

class stock_picking(models.Model):
	_inherit = "stock.picking"
	
	@api.model
	def _prepare_pack_ops(self, picking, picking_quants, forced_qties):
		prevals = super(stock_picking,self)._prepare_pack_ops(picking, picking_quants, forced_qties, context=self.env.context)
		unique_products = set()
		for move in picking.move_lines:
			if move.unique_serial:
				unique_products.add(move.product_id.id)
		if unique_products:
			vals = []
			for val in prevals:
				if val['product_id'] in unique_products and val['product_qty'].is_integer() and val['product_qty']>1:
					quantity = int(val['product_qty']-1)
					val['product_qty'] = 1
					for qty in range(quantity):
						new_val = val
						vals.append(new_val)
			return (vals + prevals)
		else:
			return prevals
		

class stock_pack_operation(models.Model):
        _inherit = "stock.pack.operation"

        unique_serial = fields.Boolean(compute='_compute_unique')

        @api.depends('product_id')
        @api.multi
        def _compute_unique(self):
                for record in self:
                        record.unique_serial = record.product_id.lot_unique_ok
			record.split_to_single_ids()

	@api.constrains('product_qty')
        @api.one
        def split_to_single_ids(self):
               if self.product_qty.is_integer() and self.product_qty>1 and self.unique_serial:
                       quantity = int(self.product_qty)
                       self.product_qty = 1
                       items = []
                       for n in range(quantity-1):
                               new_id = self.copy(context=self.env.context)
                               self.picking_id.pack_operation_ids += new_id


class stock_move(models.Model):
	_inherit = "stock.move"

	unique_serial = fields.Boolean(compute='_compute_unique')

	@api.depends('product_id')
	@api.multi
	def _compute_unique(self):
		for record in self:
			record.unique_serial = record.product_id.lot_unique_ok

#class stock_transfer_details_items(models.TransientModel):
#	_inherit = 'stock.transfer_details_items'
#	
#	@api.constrains('product_id')
#	@api.constrains('quantity')
#        @api.onchange('quantity')
#	@api.onchange('product_id')
#        @api.multi
#        def check_for_unique_serials(self):
#                for item in self:
#                        if item.product_id.lot_unique_ok:
#				item.lot_id.required=True
#				if item.quantity > 1:
#                                	item.split_to_single_ids()
#			else:
#				item.lot_id.required=False
#
#	@api.one
#	def split_to_single_ids(self):
#		if self.quantity.is_integer() and self.quantity>1:
#			quantity = int(self.quantity)
#			self.quantity = 1
#			items = []
#			for n in range(quantity-1):
#				new_ids = self.copy(context=self.env.context)
#				for new_id in new_ids:
#			                new_id.quantity = 1
#			                new_id.packop_id = False
#				self.transfer_id.item_ids += new_ids
#	@api.multi
#	def split_to_single(self):
#		self.split_to_single_ids()
#		if self and self[0]:
#            		return self[0].transfer_id.wizard_view()

# -*- coding: utf-8 -*-

from openerp import models, api, fields, osv, exceptions
from openerp.tools.translate import _

class StockMove(models.Model):
	_inherit = 'stock.move'

	consumed_ids = fields.One2many(comodel_name='stock.move',inverse_name='consumed_for', string="Consumed Products")

class StockProductionLot(models.Model):
	_inherit = 'stock.production.lot'
	
	hasConsumed = fields.Many2many(comodel_name='stock.production.lot', string='Consumed Lots', readonly=False, copy=False, compute='_get_consum_rel')
	wasConsumedBy = fields.Many2many(comodel_name='stock.production.lot', string='Consumed By', readonly=False, copy=False, compute='_get_consum_rel')

	@api.one
	def _get_consum_rel(self):
		consumed_lots = self.env['stock.production.lot']
		consuming_lots = self.env['stock.production.lot']
		for quant in self.quant_ids:
			for move in quant.history_ids:
				if move.consumed_ids:
					for stockmove in move.consumed_ids:
						if stockmove.lot_ids:
							consumed_lots += stockmove.lot_ids
				if move.consumed_for:
					for stockmove in move.consumed_for:
						if stockmove.lot_ids:
							consuming_lots += stockmove.lot_ids
		self.hasConsumed = consumed_lots
		self.wasConsumedBy = consuming_lots
			
		

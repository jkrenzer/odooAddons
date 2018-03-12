from openerp import models, api, fields, osv, exceptions
#from openerp.osv import fields, osv
from openerp.tools.translate import _

class StockQuant(models.Model):
        _inherit = 'stock.quant'
        _name = 'stock.quant'
	
        delivery_notes_count = fields.Integer(string='Number of References', compute="_delivery_notes_count",  help="Number of Delivery Notes referencing this quant.", readonly=True, copy=False)
	delivery_notes = fields.Many2many(comodel_name='stock.delivery_note', compute="_compute_delivery_notes" , string='Delivery Notes', help="All delivery notes mentioning this quant")

        @api.multi
        @api.depends('delivery_notes')
        def _delivery_notes_count(self):
                for rec in self:
                        rec.delivery_notes_count = rec.delivery_notes and len(rec.delivery_notes) or 0
        @api.multi
        @api.depends('history_ids')
        def _compute_delivery_notes(self):
                for rec in self:
                        delivery_notes = self.env['stock.delivery_note']
                        for move in rec.history_ids:
                                if move.picking_id and move.picking_id.delivery_notes_ids:
                                        delivery_notes += move.picking_id.delivery_notes_ids
                        rec.delivery_notes = delivery_notes

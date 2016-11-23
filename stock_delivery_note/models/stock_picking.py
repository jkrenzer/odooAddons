from openerp import models, api, fields, osv, exceptions
#from openerp.osv import fields, osv
from openerp.tools.translate import _

class StockPicking(models.Model):
        _inherit = 'stock.picking'
        _name = 'stock.picking'
	
	backorders_ids = fields.One2many('stock.picking', 'backorder_id', 'Backorders', readonly=True, copy=False)	
	contact = fields.Many2one('res.users', 'In Charge', readonly=False, copy=True)
	partner_ref = fields.Char('Supplier Reference', copy=True, help="Reference of the sales order or bid sent by your supplier. "
                                        "It's mainly used to do the matching when you receive the "
                                        "products as this reference is usually written on the "
                                        "delivery order sent by your supplier.")
	delivery_note_ref = fields.Char('Delivery Note Reference', copy=True, help="Delivery Note assigned to this picking, if any exists.")
	delivery_notes_ids = fields.Many2many(comodel_name='stock.delivery_note', inverse_name='pickings', string='Delivery Notes', help="All DNs mentioning this picking")

	_sql_constraints = [('delivery_note_company_uniq', 'unique (delivery_note_ref,company_id)', 'The Delivery Note reference number must be unique per company !')]

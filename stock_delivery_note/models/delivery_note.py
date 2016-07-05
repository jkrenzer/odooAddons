from openerp import models, api, fields, osv, exceptions
#from openerp.osv import fields, osv
from openerp.tools.translate import _

class DeliveryNote(models.Model):
        _name = 'stock.delivery_note'
	

	partner = fields.Many2one('res.users', 'Partner', readonly=False, copy=True),
	partner_ref = fields.Char('Partner Reference', 
                                   copy=True,
                                   help="Reference of the sales order or bid sent by your supplier. "
                                        "It's mainly used to do the matching when you receive the "
                                        "products as this reference is usually written on the "
                                        "delivery order sent by your supplier.")
	name = fields.Char('Delivery Note Reference', 
                                   copy=True,
                                   help="Delivery Note name")
        pickings = fields.One2Many('stock.picking','pickings')
        note = fields.Char('Additional Notes', copy=True, help="Any additional notes which have to be appended to the document for the customer.")
        orders = fields.Many2Many('sale.order','orders')
        
	_sql_constraints = [('delivery_note_company_uniq', 'unique (delivery_note_ref,company_id)', 'The Delivery Note reference number must be unique per company !')]

	def do_print(self, cr, uid, ids, context=None):
	        '''This function prints the delivery note'''
	        return self.pool.get("report").get_action(cr, uid, ids, 'stock_delivery_note.report_delivery_note', context=context)

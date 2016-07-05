from openerp import models, api, fields, osv, exceptions
#from openerp.osv import fields, osv
from openerp.tools.translate import _

class StockPicking(models.Model):
        _inherit = 'stock.picking'
        _name = 'stock.picking'
	

	_columns = {
		'contact': osv.fields.many2one('res.users', 'In Charge', readonly=False, copy=True),
		'partner_ref': osv.fields.char('Supplier Reference', 
                                   copy=True,
                                   help="Reference of the sales order or bid sent by your supplier. "
                                        "It's mainly used to do the matching when you receive the "
                                        "products as this reference is usually written on the "
                                        "delivery order sent by your supplier."),
		'delivery_note_ref': osv.fields.char('Delivery Note Reference', 
                                   copy=True,
                                   help="Delivery Note assigned to this picking, if any exists."),
	}
	_sql_constraints = [('delivery_note_company_uniq', 'unique (delivery_note_ref,company_id)', 'The Delivery Note reference number must be unique per company !')]

	def do_print_delivery_note(self, cr, uid, ids, context=None):
	        '''This function prints the delivery note'''
        	context = dict(context or {}, active_ids=ids)
		if not self.contact:
			self.write({'contact': self.env.uid})
		if not self.delivery_note_ref:
			recs = self.env['ir.sequence']
	                self.write({'delivery_note_ref': recs.next_by_code('stock.picking.delivery_note')})
	        return self.pool.get("report").get_action(cr, uid, ids, 'stock_picking_delivery_note.report_delivery_note', context=context)

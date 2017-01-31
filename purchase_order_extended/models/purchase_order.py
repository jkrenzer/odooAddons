# -*- coding: utf-8 -*-

from openerp import models, api, fields, osv, exceptions
#from openerp.osv import fields, osv
from openerp.tools.translate import _
# class purchase_order_extended(models.Model):
#     _name = 'purchase_order_extended.purchase_order_extended'

#     name = fields.Char()

class PurchaseOrder(models.Model):
	_inherit = 'purchase.order'
	_name = 'purchase.order'
	STATE_SELECTION = [
		('draft', 'Draft RFQ'),
		('sent', 'RFQ Sent'),
		('draftbid', 'Draft Bid'),  # added
		('bid', 'Bid Received'),
		('bid_selected', 'Bid selected'),  # added
		('draftpo', 'Draft PO'),  # added
		('confirmed', 'Waiting Approval'),
		('approved', 'Purchase Confirmed'),
                ('ordered', 'Order Sent'),
		('except_picking', 'Shipping Exception'),
		('except_invoice', 'Invoice Exception'),
		('done', 'Done'),
		('cancel', 'Cancelled')
	]
	READONLY_STATES = {
	'confirmed': [('readonly', True)],
	'ordered': [('readonly', True)],
	'done': [('readonly', True)]
    	}

	manual_name = fields.Char('Manual Name', states=READONLY_STATES, related='name', store=False, help='Use this field to manually override the assigned name of the object.')
        state = fields.Selection(STATE_SELECTION, 'Status', readonly=True, help="The status of the purchase order or the quotation request. A quotation is a purchase order in a 'Draft' status. Then the order has to be confirmed by the user, the status switch to 'Confirmed'. Then the supplier must confirm the order to change the status to 'Approved'. When the purchase order is paid and received, the status becomes 'Done'. If a cancel action occurs in the invoice or in the reception of goods, the status becomes in exception.", select=True)
#			'partner_id':osv.fields.many2one('res.partner', 'Supplier', required=True, states=READONLY_STATES,change_default=True, track_visibility='always'),
#			'partner_ref': osv.fields.char('Supplier Reference', states=READONLY_STATES,
#                                   copy=True,
#                                   help="Reference of the sales order or bid sent by your supplier. "
#                                        "It's mainly used to do the matching when you receive the "
#                                        "products as this reference is usually written on the "
#                                        "delivery order sent by your supplier."),
#			'dest_address_id':osv.fields.many2one('res.partner', 'Customer Address (Direct Delivery)',states=READONLY_STATES,help="Put an address if you want to deliver directly from the supplier to the customer. " \
#                "Otherwise, keep empty to deliver to your own company."),
#			'location_id': osv.fields.many2one('stock.location', 'Destination', required=True, domain=[('usage','<>','view')],states=READONLY_STATES),
#			'pricelist_id':osv.fields.many2one('product.pricelist', 'Pricelist', required=True, states=READONLY_STATES, help="The pricelist sets the currency used for this purchase order. It also computes the supplier price for the selected products/quantities."),
#			'currency_id': osv.fields.many2one('res.currency','Currency', required=True, states=READONLY_STATES),
	approver = fields.Many2one('res.users', 'Approved by', readonly=True, copy=False)
	contact = fields.Many2one('res.users', 'In Charge', readonly=False, copy=True, states=READONLY_STATES)
	parent = fields.Many2one('purchase.order', 'Parent Object', readonly=False, copy=False)
        children = fields.One2many('purchase.order', 'parent', 'Derived Objects', readonly=False, copy=False)
	children_count = fields.Integer(compute='_children_count', string="Number of derived children")

	@api.multi
	@api.depends('children')
	def _children_count(self):
		for rec in self:
			rec.children_count = rec.children and len(rec.children) or 0
	@api.multi
	def view_children(self):
		self.ensure_one() #Ensure we have only one object
		action = {
                        "type": "ir.actions.act_window",
                        "res_model": "purchase.order",
                        "views": [[False, "form"]],
                }
		if len(self.children) > 1:
			action['domain'] = "[('id','in',[" + ','.join(map(str, self.children)) + "])]"
		else:
			action['views'] = [(False, 'form')]
			action['res_id'] =  self.children[0].id or False

                return action

	@api.one
	def send_order(self):
		'''
                This function comfirms the order as sent
                '''
		self.write({'state': 'ordered'})
		self.message_post(body=_("Purchase Order marked as sent"),subtype="mail.mt_comment")

	@api.multi
	def print_order(self):
		'''
		This function prints the purchase-order
		'''
#		assert len(ids) == 1, 'This option should only be used for a single id at a time'
#		self.signal_workflow(cr, uid, ids, 'send_order')
		return self.env['report'].render_pdf('purchase.report_purchaseorder')

	@api.multi
	def wkf_approve_order(self):
		self.write({'state': 'approved', 'date_approve': fields.Date.context_today(self),'approver': self.env.uid})
		self.message_post(body=_("Purchase Order approved by %s ") % self.approver.name ,subtype="mail.mt_comment")
		return True
        @api.multi
        def clone_to_draft_po(self):
                self.ensure_one() #Ensure we have only one object
                recs = self.env['ir.sequence']
                new_name = recs.next_by_code('purchase.order')
                # 'orm.Model.copy' is called instead of 'self.copy' in order to avoid
                # 'purchase.order' method to overwrite our values, like name and state
                new_values = {
                        'name': new_name,
                        'manual_name': new_name,
                        'type': 'purchase',
                        'state': self.state,
                        'parent': self.id,
			'date_order': fields.Date.context_today(self),
                }       
                if self.unrevisioned_name:
                        new_values['unrevisioned_name'] =  new_name
                new_revision = super(PurchaseOrder, self).copy(default=new_values)
                new_revision.minimum_planned_date = self.minimum_planned_date
                self.children += new_revision
                msg = _('Cloned RFQ-Bid(s) %s to Purchase Order %s') % (self.name, new_name)
                new_revision.message_post(body=msg)
                self.message_post(body=msg)
                action = {
			"type": "ir.actions.act_window",
			"res_model": "purchase.order",
			"views": [[False, "form"]],
			"res_id": new_revision.id,
		}
                return action


	@api.one
	def copy(self,default=None):
		old_name = self.name
                recs = self.env['ir.sequence']
                new_name = '/'
		old_values = {
                        'name': new_name,
                        'manual_name': new_name,
                        'type': 'rfq',
                        'unrevisioned_name': new_name,
                        }
		defaults = default.copy()
		defaults.update(old_values)
                new_revision = super(PurchaseOrder, self).copy(default=defaults)
                # 'orm.Model.copy' is called instead of 'self.copy' in order to avoid
                # 'purchase.order' method to overwrite our values, like name and state
                return new_revision 

	@api.multi
	def unlink(self):
		for order in self:
			if order.state not in ['draft','draftbid','draftpo','cancel']:
				raise exceptions.except_orm( 
					_('Error!'),
					_('In order to delete a purchase order, you must cancel it first.')
				)
		return models.Model.unlink(self) 


	@api.model
	def create(self, values):
		if 'name' not in values or values['name'] == '/':
			recs = self.env['ir.sequence']
			if 'manual_name' not in values or values['manual_name'] == '/' or values['manual_name'] == '':
				if self._context.get('draft_po'):
        	                        values['name'] = recs.next_by_code('purchase.order')
					values['manual_name'] = values['name']
				elif self._context.get('draft_bid'):
                        	        values['name'] = recs.next_by_code('purchase.order.bid')
                                        values['manual_name'] = values['name']
	                        else:
        	                        values['name'] = recs.next_by_code('purchase.order.rfq')
                                        values['manual_name'] = values['name']
			else:
				values['name'] = values['manual_name']
		values['contact'] = self.env.uid
		order = super(PurchaseOrder, self).create(values)
        	return order
		

#class PurchaseOrderLine(osv.osv):
#	_inherit = 'purchase.order.line'
#	_name = 'puchase.order.line'
#
#	def _amount_line(self, cr, uid, ids, prop, arg, context=None):
#        res = {}
#	if 
#        cur_obj=self.pool.get('res.currency')
#        tax_obj = self.pool.get('account.tax')
#        for line in self.browse(cr, uid, ids, context=context):
#            line_price = self._calc_line_base_price(cr, uid, line,
#                                                    context=context)
#            line_qty = self._calc_line_quantity(cr, uid, line,
#                                                context=context)
#            taxes = tax_obj.compute_all(cr, uid, line.taxes_id, line_price,
#                                        line_qty, line.product_id,
#                                        line.order_id.partner_id)
#            cur = line.order_id.pricelist_id.currency_id
#            res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
#        return res
#
#	_columns = {
#		'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')),
#		'price_subtotal_override': fields.float('Manual Subtotal Price', default=_amount_line),
#		'price_subtotal_override_switch': fields.bool('Override Subtotal?',default=false),
#	}
#purchase_order()

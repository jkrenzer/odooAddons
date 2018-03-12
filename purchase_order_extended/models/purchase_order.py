# -*- coding: utf-8 -*-
from openerp import models, api, fields, osv, exceptions
from openerp.tools.translate import _

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    _name = 'purchase.order'
    _description = 'Purchase Order'

    STATE_SELECTION = [
     ('draft', 'Draft RFQ'),
     ('sent', 'RFQ Sent'),
     ('draftbid', 'Draft Bid'),
     ('bid', 'Bid Received'),
     ('bid_selected', 'Bid selected'),
     ('draftpo', 'Draft PO'),
     ('confirmed', 'Waiting Approval'),
     ('approved', 'Purchase Confirmed'),
     ('sent_order' , 'Order Sent'),
     ('ordered', 'Order Placed'),
     ('except_picking', 'Shipping Exception'),
     ('except_invoice', 'Invoice Exception'),
     ('done', 'Done'),
     ('cancel', 'Cancelled')]

    INVOICE_METHOD_SELECTION = [
      ('manual','Based on Purchase Order lines'),
      ('order','Based on generated draft invoice'),
      ('picking','Based on incoming shipments')
    ]

    READONLY_STATES = {'confirmed': [
                   (
                    'readonly', True)],
       'ordered': [
                 (
                  'readonly', True)],
       'done': [
              (
               'readonly', True)]
    }
    manual_name = fields.Char('Manual Name', states=READONLY_STATES, related='name', store=False, help='Use this field to manually override the assigned name of the object.')
    state = fields.Selection(STATE_SELECTION, 'Status', readonly=True, help="The status of the purchase order or the quotation request. A quotation is a purchase order in a 'Draft' status. Then the order has to be confirmed by the user, the status switch to 'Confirmed'. Then the supplier must confirm the order to change the status to 'Approved'. When the purchase order is paid and received, the status becomes 'Done'. If a cancel action occurs in the invoice or in the reception of goods, the status becomes in exception.", select=True)
    approver = fields.Many2one('res.users', 'Approved by', readonly=True, copy=False)
    contact = fields.Many2one('res.users', 'In Charge', readonly=False, copy=True, states=READONLY_STATES)
    parent = fields.Many2one('purchase.order', 'Parent Object', readonly=False, copy=False)
    children = fields.One2many('purchase.order', 'parent', 'Derived Objects', readonly=False, copy=False)
    children_count = fields.Integer(compute='_children_count', string='Number of derived children')
    invoice_method = fields.Selection(INVOICE_METHOD_SELECTION, 'Invoicing Control', required=True, states=READONLY_STATES, readonly=False,
            help="Based on Purchase Order lines: place individual lines in 'Invoice Control / On Purchase Order lines' from where you can selectively create an invoice.\n" \
                "Based on generated invoice: create a draft invoice you can validate later.\n" \
                "Based on incoming shipments: let you create an invoice when receipts are validated."
    )

    @api.multi
    @api.depends('children')
    def _children_count(self):
        for rec in self:
            rec.children_count = rec.children and len(rec.children) or 0

    @api.multi
    def view_children(self):
        self.ensure_one()
        action = {'type': 'ir.actions.act_window',
           'res_model': 'purchase.order',
           'views': [
                   [
                    False, 'form']]
           }
        if len(self.children) > 1:
            action['domain'] = "[('id','in',[" + (',').join(map(str, self.children)) + '])]'
        else:
            action['views'] = [
             (
              False, 'form')]
            action['res_id'] = self.children[0].id or False
        return action

    @api.one
    def wkf_order_sent(self):
        """
        This function comfirms the order was sent
        """
        self.write({'state': 'sent_order'})
        self.message_post(body=_('Order %s  was marked as sent.' % (self.name or '') ), subtype='mail.mt_comment')


    @api.one
    def wkf_order_ordered(self):
        """
        This function comfirms the order was sucessfully received and placed
        """
        self.write({'state': 'ordered'})
        self.message_post(body=_('Order %s  was marked as successfully placed.' % (self.name or '') ), subtype='mail.mt_comment')

    @api.multi
    def print_order(self):
        """
        This function prints the purchase-order
        """
        return self.env['report'].render_pdf('purchase.report_purchaseorder')

    @api.multi
    def wkf_approve_order(self):
        self.write({'state': 'approved','date_approve': fields.Date.context_today(self),'approver': self.env.uid})
        self.message_post(body=_('Purchase Order approved by %s ') % self.approver.name, subtype='mail.mt_comment')
        return True

    @api.multi
    def clone_to_draft_po(self):
        self.ensure_one()
        recs = self.env['ir.sequence']
        new_name = recs.next_by_code('purchase.order.po')
        new_values = {'name': new_name,
           'manual_name': new_name,
           'type': 'purchase',
           'state': self.state,
           'parent': self.id,
           'partner_ref': self.partner_ref,
           'date_order': fields.Date.context_today(self)
           }
        if self.unrevisioned_name:
            new_values['unrevisioned_name'] = new_name
        new_revision = super(PurchaseOrder, self).copy(default=new_values)
        new_revision.minimum_planned_date = self.minimum_planned_date
        self.children += new_revision
        msg = _('Cloned RFQ-Bid(s) %s to Purchase Order %s') % (self.name, new_name)
        new_revision.message_post(body=msg)
        self.message_post(body=msg)
        action = {'type': 'ir.actions.act_window',
           'res_model': 'purchase.order',
           'views': [
                   [
                    False, 'form']],
           'res_id': new_revision.id
           }
        return action

    @api.one
    def copy(self, default=None):
        old_name = self.name
        recs = self.env['ir.sequence']
        new_name = '/'
        old_values = {'name': new_name,
           'manual_name': new_name,
           'type': 'rfq',
           'unrevisioned_name': new_name
           }
        defaults = default.copy()
        defaults.update(old_values)
        new_revision = super(PurchaseOrder, self).copy(default=defaults)
        return new_revision

    @api.multi
    def unlink(self):
        for order in self:
            if order.state not in ('draft', 'draftbid', 'draftpo', 'cancel'):
                raise exceptions.except_orm(_('Error!'), _('In order to delete a purchase order, you must cancel it first.'))

        return models.Model.unlink(self)

    @api.model
    def create(self, values):
        if 'name' not in values or values['name'] == '/' or values['name'] == '':
            recs = self.env['ir.sequence']
            if 'manual_name' not in values or values['manual_name'] == '/' or values['manual_name'] == '':
                if self._context.get('draft_po'):
                    values['name'] = recs.next_by_code('purchase.order.po')
                    values['manual_name'] = values['name']
                    values['status'] = 'draftpo'
                elif self._context.get('draft_bid'):
                    values['name'] = recs.next_by_code('purchase.order.bid')
                    values['manual_name'] = values['name']
                else:
                    values['name'] = recs.next_by_code('purchase.order')
                    values['manual_name'] = values['name']
            else:
                values['name'] = values['manual_name']
        values['contact'] = self.env.uid
        order = super(PurchaseOrder, self).create(values)
        return order

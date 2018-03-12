# -*- coding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2013 Agile Business Group sagl (<http://www.agilebg.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from openerp import models, fields, api, osv
from openerp.tools.translate import _

class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"
    STATES = [
        ('draft', 'Draft Quotation'),
        ('sent', 'Quotation Sent'),
        ('cancel', 'Cancelled'),
        ('waiting_date', 'Waiting Schedule'),
        ('draft_order', 'Draft Order'), 
        ('progress', 'Sales Order'),
        ('manual', 'Sale to Invoice'),
        ('shipping_except', 'Shipping Exception'),
        ('invoice_except', 'Invoice Exception'),
        ('done', 'Done')
    ]

    READONLY_STATES = {
	'sent': [('readonly', True)],
        'draft_order': [('readonly', False)],
	'progress': [('readonly', True)],
	'done': [('readonly', True)]
    }
    TYPE_SELECTION = [
        ('quotation', 'Quotation'),
        ('order', 'Order')
    ]
    @api.one
    def _default_type(self):
        if self._context.get('draft_order'):
            return 'order'
        else:
            return 'quotation'

    @api.one
    def _default_state(self):
        if self._default_type() == 'order':
            return 'draft_order'
        else:
            return 'draft'

    state = fields.Selection(selection=STATES, string='Status', readonly=True, copy=False, help="Gives the status of the quotation or sales order.\
              \nThe exception status is automatically set when a cancel operation occurs \
              in the invoice validation (Invoice Exception) or in the picking list process (Shipping Exception).\nThe 'Waiting Schedule' status is set when the invoice is confirmed\
               but waiting for the scheduler to run on the order date.", default=_default_state, required=True)
    type = fields.Selection(selection=TYPE_SELECTION, string="Type", help="Type of the object.", required=True, readonly=True, default=_default_type)
    name = fields.Char('Order Reference', required=True, copy=False, readonly=False, states=READONLY_STATES, select=True, help='Unique number of sale order, computed automatically when the order is created.')
    manual_name = fields.Char('Manual Name', states=READONLY_STATES, related='name', store=False, help='Use this field to manually override the assigned name of the object.')
#    manual_name = fields.Char('Manual Name', readonly=False, related='name', store=False, help='Use this field to manually override the assigned name of the object.')
    parents =  fields.Many2many(comodel_name='sale.order', string='Parent Objects', relation="sale_quot_order_rel", column1='parents', column2='children', readonly=False, copy=False)
    children = fields.Many2many(comodel_name='sale.order', string='Children Objects', relation="sale_quot_order_rel", column1='children', column2='parents', readonly=False, copy=False)
    invoiced_total = fields.Float(string="Invoiced Total", compute="_get_invoiced_amount", help="Amount which has been invoiced until now.")
    invoiced_untaxed_total = fields.Float(string="Invoiced Total (untaxed)", compute="_get_invoiced_amount", help="Amount without taxes which has been invoiced.")
    picking_ids = fields.One2many(compute='_get_picking_ids', comodel_name='stock.picking', string='Picking associated to this sale')

    @api.one
    def _get_invoiced_amount(self):
        total = 0.0
        untaxed_total = 0.0
        for invoice in self.invoice_ids:
                untaxed_total += invoice.amount_untaxed
                total += invoice.amount_total
        self.invoiced_total = total
        self.invoiced_untaxed_total = untaxed_total

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/' and vals.get('type','quotation') != 'order':
            vals['name'] = self.env['ir.sequence'].get('sale.order.quotation')
        else:
            vals['name'] = self.env['ir.sequence'].get('sale.order.quotation')
        return super(SaleOrder, self).create(vals)

    @api.one
    def action_button_confirm(self):
	old_name = self.name
        quotation = self.copy()
        self.name = self.env['ir.sequence'].get('sale.order') or '/'
        quotation.write({
	    'name': old_name,
	    'manual_name': old_name,
            'unrevisioned_name': old_name,
            'state': self.state,
            'message_follower_ids': self.message_follower_ids,
            'children': quotation.children + self,
	    'message_ids': self.message_ids,
	    'message_is_follower': self.message_is_follower,
	    'message_last_post': self.message_last_post,
	    'message_summary': self.message_summary,
	    'message_unread': self.message_unread,
	    'create_date': self.create_date,
            'create_uid': self.create_uid,
	})
        if super(SaleOrder, self).action_button_confirm():
#	    sale.write(old_values)
            self.write({
              'parents': self.parents + quotation,
            })
            return True
	else:
	    return False

    @api.one
    def action_order_confirm(self):
        self.write({
            'state': 'progress'
        })

    @api.multi
    def _get_picking_ids(self):
       for rec in self:
            moves = self.env['stock.move'].search([('group_id', '=', rec.procurement_group_id.id)])
            rec.picking_ids = self.env['stock.picking']
            for move in moves:
                if move.picking_id is not None:
                    rec.picking_ids += move.picking_id 

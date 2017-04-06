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
    READONLY_STATES = {
	'sent': [('readonly', True)],
	'progress': [('readonly', True)],
	'done': [('readonly', True)]
    }

    name = fields.Char('Order Reference', required=True, copy=False, readonly=False, states=READONLY_STATES, select=True, help='Unique number of sale order, computed automatically when the order is created.')
    manual_name = fields.Char('Manual Name', states=READONLY_STATES, related='name', store=False, help='Use this field to manually override the assigned name of the object.')
#    manual_name = fields.Char('Manual Name', readonly=False, related='name', store=False, help='Use this field to manually override the assigned name of the object.')
    parents =  fields.Many2many(comodel_name='sale.order', string='Parent Objects', relation="sale_quot_order_rel", column1='parents', column2='children', readonly=False, copy=False)
    children = fields.Many2many(comodel_name='sale.order', string='Children Objects', relation="sale_quot_order_rel", column1='children', column2='parents', readonly=False, copy=False)

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/' and vals.get('type','quotation') != 'order':
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

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

from openerp import models, fields, api

class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"
    
    _columns = {
        'manual_name': fields.char('Manual Name', states=READONLY_STATES, related='name', store=False, help='Use this field to manually override the assigned name of the object.'),
        'parent': fields.many2one('sale.order', 'Parent Object', readonly=False, copy=False),
    }

    @api.multi
    def action_wait(self):
            for sale in self:
                defaults = {
			'name': sale.name,
			'manual_name': sale.name,
                        'unrevisioned_name': new_name,
			}
                if super(SaleOrder, self).action_wait():
                    qou = super(PurchaseOrder, self).copy(default=defaults)
                    sale.write({
                        'parent': qou.id,
                        })
        return True

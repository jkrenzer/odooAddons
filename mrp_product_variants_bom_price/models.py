# -*- coding: utf-8 -*-

from openerp import models, fields, api

class product_bom(models.Model):
    _inherit = 'mrp.bom'

    standard_price = fields.Float(related='product_id.standard_price', string="Standard price of product", store=False)
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

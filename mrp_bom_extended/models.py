# -*- coding: utf-8 -*-

from openerp import models, fields, api

class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line" 
    standard_price = fields.Float(string="Standard Price", related="product_id.standard_price", readonly=True)

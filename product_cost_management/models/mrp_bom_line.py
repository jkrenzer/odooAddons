# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools.translate import _

class MrpBomLine(models.Model):
    _inherit="mrp.bom.line"

    estimated_work_cost = fields.Float(string="Est. Work Costs", related="product_id.estimated_work_cost", store=False, help="Estimated costs for employees for production of one unit of this product.")
    estimated_material_cost = fields.Float(string="Est. Material Costs", related="product_id.estimated_material_cost", store=False, help="Estimated material costs for production of one unit of this product.")
    estimated_total_cost = fields.Float(string="Est. Total Costs", related="product_id.estimated_total_cost", store=False, help="Estimated total costs for production of one unit of this product.")

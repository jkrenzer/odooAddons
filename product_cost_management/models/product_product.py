# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools.translate import _

class ProductProduct(models.Model):
    _inherit="product.product"

    COST_METHODS = [
        ("average", _("Average over all BoMs")),
        ("highest", _("Take highest costs of all BoMs")),
        ("lowest", _("Take lowest costs of all BoMs")),
        ("newest", _("Take costs from most recent BoM")),
    ]

    estimated_work_cost = fields.Float(string="Est. Work Costs", compute="_import_estimated_costs", store=True, help="Estimated costs for employees for production of one unit of this product.")
    estimated_material_cost = fields.Float(string="Est. Material Costs", compute="_import_estimated_costs", store=True, help="Estimated material costs for production of one unit of this product.")
    estimated_total_cost = fields.Float(string="Est. Total Costs", compute="_import_estimated_costs", store=True, help="Estimated total costs for production of one unit of this product.")

    estimated_cost_method = fields.Selection(string="Method for cost-estimation", selection=COST_METHODS, default="average", help="Method for calculation of the estimated costs. By default Odoo averages over all BoMs.")

    @api.multi
    def _get_cost_lists(self):
        for prod in self:
            work = []
            material = []
            boms_ids = self.env['mrp.bom']._bom_find(product_id=prod.id)
            boms = self.env['mrp.bom'].browse(boms_ids).sorted(key=lambda b: b.id)
            for bom in boms:
                work.append(bom.estimated_work_cost)
                material.append(bom.estimated_material_cost)
            if len(work) is 0 and len(material) is 0:
                return None
            else:
                return { "work": work, "material": material}
    @api.multi
    @api.depends('estimated_cost_method')
    def _import_estimated_costs(self):
        for prod in self:
           work_cost = 0.0
           material_cost = prod.standard_price
           costs = prod._get_cost_lists()
           if costs is not None:
               if prod.estimated_cost_method is "highest":
                   work_cost = max(costs["work"])
                   material_cost = max(costs["material"])
               elif prod.estimated_cost_method is "lowest":
                   work_cost = min(costs["work"])
                   material_cost = min(costs["material"])
               elif prod.estimated_cost_method is "newest":
                   work_cost = costs["work"][-1]
                   material_cost = costs["material"][-1]
               else:
                   work_cost = sum(costs["work"])/len(costs["work"])
                   material_cost = sum(costs["material"])/len(costs["material"])
           prod.estimated_work_cost = work_cost
           prod.estimated_material_cost = material_cost
           prod.estimated_total_cost = work_cost + material_cost

    @api.multi
    def get_history_costs(self, date=None, context=None):
        if context is None:
            context = {}
        if date is None:
            date = time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        for prod in self:
            if prod.bom_ids:
                pass #TODO
            else:
                pass

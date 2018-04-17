# -*- coding: utf-8 -*-

from openerp import models, fields, api

class MrpBom(models.Model):
    _inherit="mrp.bom"

    estimated_work_cost = fields.Float(string="Est. Work Costs", compute="_compute_estimated_costs", store=False)
    estimated_inherited_work_cost = fields.Float(string="Est. Inherited Work Costs", compute="_compute_estimated_costs", store=False)
    estimated_own_work_cost = fields.Float(string="Est. Own Work Costs", compute="_compute_estimated_costs", store=False)
    estimated_material_cost = fields.Float(string="Est. Material Costs", compute="_compute_estimated_costs", store=False)
    estimated_total_cost = fields.Float(string="Est. Total Costs", compute="_compute_estimated_costs", store=False)

    @api.multi
    def _compute_estimated_costs(self):
        for bom in self:
            own_work_cost = 0.0
            inherited_work_cost = 0.0
            material_cost = 0.0

            # Calculating work-cost of this BoM
            for wline in bom.routing_id.workcenter_lines:
                wc = wline.workcenter_id
                cycle = wline.cycle_nbr
                hour = (wc.time_start + wc.time_stop + cycle * wc.time_cycle + (wline.hour_nbr or 0) ) *  (wc.time_efficiency or 1.0)
                work_unit_cost = wc.costs_cycle * cycle + wc.costs_hour * hour
                own_work_cost += self.env['product.uom']._compute_price(bom.product_uom.id, work_unit_cost, bom.product_id.uom_id.id)

            # Calculating material-costs and work-cost inherited from children
            for mline in bom.bom_line_ids:
                qty = mline.product_qty / mline.product_efficiency
                prod = mline.product_id
                if not mline.attribute_value_ids or set(mline.attribute_value_ids).intersection(set(bom.product_id.attribute_value_ids)):
                        material_cost += self.env['product.uom']._compute_price(prod.uom_id.id, prod.estimated_material_cost,mline.product_uom.id) * qty
                        inherited_work_cost += self.env['product.uom']._compute_price(prod.uom_id.id, prod.estimated_work_cost,mline.product_uom.id) * qty
            
            # Setting fields
            bom.estimated_material_cost = material_cost
            bom.estimated_work_cost = own_work_cost + inherited_work_cost
            bom.estimated_inherited_work_cost = inherited_work_cost
            bom.estimated_own_work_cost = own_work_cost
            bom.estimated_total_cost = material_cost + own_work_cost + inherited_work_cost

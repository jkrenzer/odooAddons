# -*- coding: utf-8 -*-

from openerp import models, fields, api

class StockQuant(models.Model):
    _inherit='stock.quant'
    
    production_work_cost = fields.Float(string="Production Work Costs", compute="_compute_production_cost", store=False, help="Total work-time and machine costs during manufactoring of this quant")
    production_material_cost = fields.Float(string="Production Material Costs", compute="_compute_production_cost", store=False, help="Total material costs during manufactoring of this quant")
    production_total_cost = fields.Float(string="Total Production Costs", compute="_compute_production_cost", store=False, help="Total costs during manufactoring of this quant")

    @api.multi
    def _compute_production_cost(self):
        for quant in self:
            production_moves = quant.history_ids.filtered(lambda m: m.production_id is not False)
            work_cost = 0.0
            material_cost = 0.0
            for production_move in production_moves:
                production = production_move.production_id
                done_work_orders = production.workcenter_lines.filtered(lambda w: w.state == 'done')
                for dwo in done_work_orders:
                    wc = dwo.workcenter_id
                    work_cost += wc.costs_hour * dwo.hour + wc.costs_cycle * dwo.cycle + dwo.pre_cost + dwo.post_cost
                consumed_lines = production.move_lines2
                for cl in consumed_lines:
                    consumed_quants = cl.quant_ids
                    for cq in consumed_quants:
                        work_cost += cq.production_work_cost
                        material_cost += cq.production_material_cost 
            material_cost = material_cost or quant.inventory_value # If we do not have any production-information we should at least get the history value
            quant.production_work_cost = work_cost
            quant.production_material_cost = material_cost
            quant.production_total_cost = material_cost + work_cost

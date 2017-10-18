# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import except_orm, Warning, RedirectWarning
import pprint

pp = pprint.PrettyPrinter(indent=4)

class Wizard(models.TransientModel):
    _name = 'stock_pickings_from_quants.wizard'

    picking_type_id = fields.Many2one('stock.picking.type', string="Picking Type", required=True)
    destination_location_id = fields.Many2one('stock.location', string="Destination", required=True)
    
    @api.multi
    def collect_sources(self, quants_ids):
        self.ensure_one()
        sources = self.env['stock.location']
        for quant in quants_ids:
            if quant.location_id not in sources:
                sources += quant.location_id
        return sources

    @api.multi
    def action_create_pickings(self):
        self.ensure_one()
        quants_ids = self.get_quants()
        pickings = self.env['stock.picking']
        sources_ids = self.collect_sources(quants_ids)
        for source in sources_ids:
            picking = self.env['stock.picking'].create({
                'picking_type_id' : self.picking_type_id.id,
             })
            pickings += picking
            for quant in quants_ids:
                if quant.location_id == source:
                    picking.move_lines += self.env['stock.move'].create({
                        'location_id': source.id,
                        'location_dest_id': self.destination_location_id.id,
                        'product_id': quant.product_id.id,
                        'product_uom': quant.product_id.uom_id.id,
                        'product_uom_qty': quant.qty,
                        'name': quant.product_id.display_name,
                    })

        action = {
            "type": "ir.actions.act_window",
            "res_model": "stock.picking",
            "views": [[False, "form"]],
        }
        if len(pickings) > 1:
            action['domain'] = "[('id','in',[" + ','.join(map(str, pickings)) + "])]"
        else:
            action['views'] = [(False, 'form')]
            action['res_id'] =  pickings[0].id or False
        return action

    @api.multi
    def get_quants(self):
        self.ensure_one()
        if self._context.get('active_ids'):
            quant_obj = self.env['stock.quant']
            return quant_obj.browse(self._context.get('active_ids'))
        else:
            raise Warning('No quants selected!')


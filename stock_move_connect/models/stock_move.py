# -*- coding: utf-8 -*-

from openerp import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def action_connect_wizard(self):
        new = self.env['stock.move.connect'].create({
            'moves': [(6, False, self.mapped('id'))],
        })
        new.create_lines()
        return {
            "name": "Connection Wizard",
            "res_model": "stock.move.connect",
            "views": [[False,"form"]],
            "target": "new",
            "type": "ir.actions.act_window",
            "res_id": new.id,
            "key2": "client_action_multi",
        }

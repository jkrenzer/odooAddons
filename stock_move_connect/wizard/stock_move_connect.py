# -*- coding: utf-8 -*-

from openerp import models, fields, api

class StockMoveConnectWizardLine(models.TransientModel):
    _name = 'stock.move.connect.line'

    move = fields.Many2one(string="Move", comodel_name="stock.move", required=True, help="Move which this line stands for")
    wizard = fields.Many2one(string="Wizard", comodel_name="stock.move.connect", help="Wizard this line is assigned to.")

    @api.multi
    def apply(self):
        for line in self:
            pass
        return True
    

class StockMoveConnectWizard(models.TransientModel):
    _name = 'stock.move.connect'

    @api.one
    def _default_move_id(self):
       return self.env['stock.move'].browse(self._context.get('active_ids'))

    @api.multi
    def _create_lines(self):
        for rec in self:
            lines = rec.env['stock.move.connect.line']
            for move in rec.moves:
                lines += lines.create({'move': move.id})
            return lines

    moves = fields.Many2many(string="Moves", comodel_name="stock.move", default=_default_move_id, required=True, help="Moves which this wizard should work on")
    lines = fields.One2many(string="Lines", comodel_name="stock.move.connect.line", inverse_name="wizard", default=_create_lines, help="Lines with connections to apply")

    @api.multi
    @api.onchange('moves')
    def create_lines(self):
        for rec in self:
            rec.lines = rec._create_lines()
    

# -*- coding: utf-8 -*-

from openerp import models, fields, api

class StockMoveConnectLine(models.TransientModel):
    _inherit = 'stock.move.connect.line'

    @api.one
    def _get_value(self):
        return self.move.purchase_line_id

    purchase_line = fields.Many2one(string="Purchase Line", comodel_name="purchase.order.line", default=_get_value, help="Purchase line associated with this move")

    @api.multi
    def apply(self):
        for line in self:
           if line.purchase_line:
               line.move.purchase_line_id = line.purchase_line
        super(StockMoveConnectLine, self).apply()

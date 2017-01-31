from openerp import models, fields, api, exceptions, _


class QcInspection(models.Model):
    _name = 'qc.inspection'
    _description = 'Quality control inspection'
    _inherit = ['qc.inspection']

    reports = fields.Many2many(string="reports", comodel_name="qc.report")

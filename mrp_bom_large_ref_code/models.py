# -*- coding: utf-8 -*-

from openerp import models, fields, api

class MrpBOM(models.Model):
    _inherit='mrp.bom'

    code = fields.Char(string="Reference", size=256)

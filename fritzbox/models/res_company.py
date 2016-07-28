 # -*- coding: utf-8 -*-

from openerp import models, api, fields, osv, exceptions
from openerp.tools.translate import _


class Company(models.Model):
    _inherit = 'res.company'
    _name = 'res.company'
    
    fritzbox_ids = fields.One2many(string='FritzBoxes', comodel_name='fritzbox.fritzbox', inverse_name='company_id')
    

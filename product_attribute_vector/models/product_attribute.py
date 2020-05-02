# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError

class ProductAttribute(models.Model):
    _inherit = ["product.attribute"]

    vector = fields.Boolean(default=False, help="Check this if you want to assign multiple instances of this attribute to a product to allow multi-dimensional variants.")


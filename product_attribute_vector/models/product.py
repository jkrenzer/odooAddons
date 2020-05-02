# -*- coding: utf-8 -*-
# 

import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.osv import expression

class ProductProduct(models.Model):
    _inherit = ['product.product']

    @api.constrains('attribute_value_ids')
    def _check_attribute_value_ids(self):
        for product in self:
            attributes = self.env['product.attribute']
            for value in product.attribute_value_ids:
                if value.attribute_id in attributes and not value.attribute_id.vector:
                    raise ValidationError(_('Error! It is not allowed to choose more than one value for a scalar attribute. Remove additonal values or set the attribute to vector-mode.'))
                if value.attribute_id.create_variant:
                    attributes |= value.attribute_id
        return True

# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    payment_mode = fields.Selection( [('manual', 'Manual'), ('sumup_app_url', 'Sumup App')], name='Payment Mode',
help="Select the payment mode for this journal", default="manual")

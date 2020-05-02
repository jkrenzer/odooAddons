# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    iface_sumup_app = fields.Boolean(
        'Proxy Sumup App',
        help="Activate proxy for payment by sumup app."
    )
    module_pos_payment_sumup_app = fields.Boolean(
        'Sumup App-Payment',
        help='Allow payment by sumup app'
    )
    use_local_sumup_app = fields.Boolean(
        'Local Sumup app',
        help='Issue call to a local Android or iOS sumup app for payment. \
        *Be aware*: Without proxy there will be no determination of payment success \
        or failure!'
    )
    sumup_app_affiliate_key = fields.Char(
        'Sumup Affiliate Key',
        help='The affiliate-key you obtained for the app-identifier by usind the developer dashboard of you sumup account.'
    )
    sumup_app_application_identifier = fields.Char(
        'App Identifier',
        help='App identifier set in you sumup account for this POS and the corresponding affiliate-key.',
        default="pos_payment_sumup_app.apps.odoo-community.org"
    )

    @api.one
    def sumup_app_callback_default(self):
        if self.iface_sumup_app:
           self.sumup_app_callback = self.proxy_ip + "/hw_sumup_app/callback" 
        else:
           ir_values = self.env['ir.config_parameter']
           base_url = ir_values.get_param('web.base.url')
           self.sumup_app_callback = base_url + "/pos_payment_sumup_app/callback"

    sumup_app_callback = fields.Char(
    'App Callback URL',
    help='URL which will be called by the sumup appafter end of transaction',
    default=sumup_app_callback_default
    ) 

    @api.onchange('sumup_app_callback')
    def sumup_app_callback_set_default(self):
        if self.sumup_app_callback == "":
           self.sumup_app_callback_default()

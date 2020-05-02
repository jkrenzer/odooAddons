# -*- coding: utf-8 -*-
from odoo import http

# class PosPaymentSumupApp(http.Controller):
#     @http.route('/pos_payment_sumup_app/pos_payment_sumup_app/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_payment_sumup_app/pos_payment_sumup_app/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_payment_sumup_app.listing', {
#             'root': '/pos_payment_sumup_app/pos_payment_sumup_app',
#             'objects': http.request.env['pos_payment_sumup_app.pos_payment_sumup_app'].search([]),
#         })

#     @http.route('/pos_payment_sumup_app/pos_payment_sumup_app/objects/<model("pos_payment_sumup_app.pos_payment_sumup_app"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_payment_sumup_app.object', {
#             'object': obj
#         })
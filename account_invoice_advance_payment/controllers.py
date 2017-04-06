# -*- coding: utf-8 -*-
from openerp import http

# class AccountInvoiceAdvancePayment(http.Controller):
#     @http.route('/account_invoice_advance_payment/account_invoice_advance_payment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_invoice_advance_payment/account_invoice_advance_payment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_invoice_advance_payment.listing', {
#             'root': '/account_invoice_advance_payment/account_invoice_advance_payment',
#             'objects': http.request.env['account_invoice_advance_payment.account_invoice_advance_payment'].search([]),
#         })

#     @http.route('/account_invoice_advance_payment/account_invoice_advance_payment/objects/<model("account_invoice_advance_payment.account_invoice_advance_payment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_invoice_advance_payment.object', {
#             'object': obj
#         })
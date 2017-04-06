# -*- coding: utf-8 -*-
from openerp import http

# class AccountInvoiceAkonto(http.Controller):
#     @http.route('/account_invoice_akonto/account_invoice_akonto/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_invoice_akonto/account_invoice_akonto/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_invoice_akonto.listing', {
#             'root': '/account_invoice_akonto/account_invoice_akonto',
#             'objects': http.request.env['account_invoice_akonto.account_invoice_akonto'].search([]),
#         })

#     @http.route('/account_invoice_akonto/account_invoice_akonto/objects/<model("account_invoice_akonto.account_invoice_akonto"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_invoice_akonto.object', {
#             'object': obj
#         })
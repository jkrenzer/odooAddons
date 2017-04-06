# -*- coding: utf-8 -*-
from openerp import http

# class AccountInvoiceSeperateNumber(http.Controller):
#     @http.route('/account_invoice_seperate_number/account_invoice_seperate_number/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_invoice_seperate_number/account_invoice_seperate_number/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_invoice_seperate_number.listing', {
#             'root': '/account_invoice_seperate_number/account_invoice_seperate_number',
#             'objects': http.request.env['account_invoice_seperate_number.account_invoice_seperate_number'].search([]),
#         })

#     @http.route('/account_invoice_seperate_number/account_invoice_seperate_number/objects/<model("account_invoice_seperate_number.account_invoice_seperate_number"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_invoice_seperate_number.object', {
#             'object': obj
#         })
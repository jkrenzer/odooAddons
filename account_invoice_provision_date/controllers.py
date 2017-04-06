# -*- coding: utf-8 -*-
from openerp import http

# class AccountInvoiceProvisionDate(http.Controller):
#     @http.route('/account_invoice_provision_date/account_invoice_provision_date/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_invoice_provision_date/account_invoice_provision_date/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_invoice_provision_date.listing', {
#             'root': '/account_invoice_provision_date/account_invoice_provision_date',
#             'objects': http.request.env['account_invoice_provision_date.account_invoice_provision_date'].search([]),
#         })

#     @http.route('/account_invoice_provision_date/account_invoice_provision_date/objects/<model("account_invoice_provision_date.account_invoice_provision_date"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_invoice_provision_date.object', {
#             'object': obj
#         })
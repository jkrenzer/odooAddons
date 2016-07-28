# -*- coding: utf-8 -*-
from openerp import http

# class Fritzbox(http.Controller):
#     @http.route('/fritzbox/fritzbox/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fritzbox/fritzbox/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fritzbox.listing', {
#             'root': '/fritzbox/fritzbox',
#             'objects': http.request.env['fritzbox.fritzbox'].search([]),
#         })

#     @http.route('/fritzbox/fritzbox/objects/<model("fritzbox.fritzbox"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fritzbox.object', {
#             'object': obj
#         })
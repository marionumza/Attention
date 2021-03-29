# -*- coding: utf-8 -*-
from odoo import http

# class MegatrustAttend(http.Controller):
#     @http.route('/megatrust_attend/megatrust_attend/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/megatrust_attend/megatrust_attend/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('megatrust_attend.listing', {
#             'root': '/megatrust_attend/megatrust_attend',
#             'objects': http.request.env['megatrust_attend.megatrust_attend'].search([]),
#         })

#     @http.route('/megatrust_attend/megatrust_attend/objects/<model("megatrust_attend.megatrust_attend"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('megatrust_attend.object', {
#             'object': obj
#         })
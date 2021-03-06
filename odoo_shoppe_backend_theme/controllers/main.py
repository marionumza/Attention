# -*- coding: utf-8 -*-

import werkzeug
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import ensure_db, Home


class StarlineThemeAppSwitcher(Home):
    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        ensure_db()
        if not request.session.uid:
            return werkzeug.utils.redirect('/web/login', 303)
        if kw.get('redirect'):
            return werkzeug.utils.redirect(kw.get('redirect'), 303)

        request.uid = request.session.uid
        context = request.env['ir.http'].webclient_rendering_context()
        if request.session.uid:
            ResUserID = request.env['res.users'].sudo().search([
                ('id', '=', request.session.uid)], limit=1)
            if ResUserID.menu_style == 'apps':
                context = dict(
                    context.copy(),
                    app_background_image=ResUserID.company_id.app_background_image or False,
                    user_id=ResUserID.id,
                    company_id=ResUserID.company_id.id
                )
                response = request.render(
                    'odoo_shoppe_backend_theme.webclient_bootstrap_apps', qcontext=context)
                response.headers['X-Frame-Options'] = 'DENY'
                return response
        response = request.render('web.webclient_bootstrap', qcontext=context)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

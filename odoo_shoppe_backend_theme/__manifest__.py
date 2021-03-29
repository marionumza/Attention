# -*- coding: utf-8 -*-
#################################################################################
# Author      : Kanak Infosystems LLP. (<http://kanakinfosystems.com/>)
# Copyright(c): 2012-Present Kanak Infosystems LLP.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <http://kanakinfosystems.com/license>
#################################################################################

{
    'name': "Odoo Shoppe Backend Theme",
    'version': '1.2',
    'summary': 'One of the best backend theme available for Odoo with extensive change in look & feel',
    'description': """
Odoo Shoppe Backend Theme
================================
    """,
    'license': 'OPL-1',
    'author': "Kanak Infosystems LLP.",
    'website': "http://www.kanakinfosystems.com",
    'images': ['static/description/odooshoppe_backend_theme.jpg',
               'static/description/odooshoppe_backend_theme_screenshot.jpg'],
    'category': 'Theme/Backend',
    'depends': ['base', 'mail', 'calendar', 'website'],
    'data': [
        'views/topbar_menu_theme_templates.xml',
        'views/sidebar_theme_templates.xml',
        'views/ir_ui_view_views.xml',
        'views/res_company_views.xml',
        'views/res_partner_views.xml',
        'views/res_users_views.xml',
        'data/data.xml'
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'application': True,
    # 'price': 150,
    # 'currency': 'EUR',
    'live_test_url': 'https://youtu.be/4q-6ve5Oooo',
}

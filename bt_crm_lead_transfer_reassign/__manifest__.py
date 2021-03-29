# -*- coding: utf-8 -*---
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'CRM - Reassign Salesperson',
    'version': '1.0',
    'category': 'Sales',
    'license':'AGPL-3',
    'summary': 'Assign lead to another saleperson',
    'description': """
Assign lead to another saleperson.
========================================

Assign lead to another saleperson.
    """,
    'depends': ['crm'],
    'author' : 'BroadTech IT Solutions Pvt Ltd',
    'website' : 'http://www.broadtech-innovations.com',
    'images': ['static/description/bt_crm_lead_transfer_reassign_banner.jpg'],
    'data': [
       'wizard/transfer_lead_view.xml',
    ],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': True
}

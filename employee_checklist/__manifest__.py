# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Employee Checklist',
    'version': '1.0',
    'category': 'HR',
	'author' : 'me',
    'description': """Employee Checklist""",
    'depends': ['product','hr'],
    'website':'http://www.mycompany.com/',
    'data': ['views/employee_checklist_view.xml','security/ir.model.access.csv'],
    'demo': [],
    'installable': True,
    'auto_install': False,
}

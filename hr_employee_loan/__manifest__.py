# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Employee Loan',
    'version': '12.0',
    'category': 'Human Resources',
    'author' : 'Me',
    'description': """Employee Loan""",
    'depends': ['hr','hr_payroll','account'],
    'website':'http://www.me.com/',
    'data': ['views/employee_loan_views.xml',
			'views/hr_loan_sequence.xml',
			'loan_print_report.xml',
			'views/report_loan_print.xml',
			'security/ir.model.access.csv'],
    'demo': [],
    'installable': True,
    'auto_install': False,
}

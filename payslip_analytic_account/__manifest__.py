# -*- coding: utf-8 -*-
{
    'name': "Payslip Analytic Account",

    'summary': """ This module provides you facility to take analytic account from contract of an employee""",

    'description': """
        By default, In Odoo on confirmation of Payslip Odoo picks analytic account from salary rule but in some use cases we need to pick from its contract. 
        This module will solve your problem.
    """,

    'author': "Odoo Concepts",
    'website': "https://www.odooconcepts.com/",

    'category': 'Human Resources',
    'version': '0.1',
    'license': 'LGPL-3',

    'depends': ['base','hr_payroll', 'hr_payroll_account',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
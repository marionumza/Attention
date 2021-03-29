# -*- coding: utf-8 -*-
{
    'name': 'Account Profit Loss Report',
    'version': '1.0',
    'category': 'Accounts',
    'description': '''
        Prints Account Profit Loss Excel Report.
        ''',
    'author': 'Me',
    'depends': [
        'account',
        'branch',
        'accounting_pdf_reports'
    ],
    'data': [
        'data/data.xml',
        'views/account_move_views.xml',
        'wizard/profit_loss_excel_report_views.xml',
    ],
    'demo': [],  
    'auto_install': False,
    'installable': True,
    'application': True
}
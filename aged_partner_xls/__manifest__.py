# -*- encoding: utf-8 -*-
{
    "name": "Aged Partner Xls Report",
    "version": "12.0",
    "description": """
        Aged Partner Xls Report
    """,
    "author": "Me",
    "category": "Accounting",
    "depends": [
        'account',
        'accounting_pdf_reports',
        'zaki_profit_loss_excel_report'
    ],
    "data":[
        'wizard/aged_partner_xls_views.xml'
    ],
    "installable": True,
    "auto_install": False, 
    "application": True
}


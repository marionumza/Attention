{
    'name': 'SOA Excel Report',
    'author': ' Me', 
    'summary': 'Accounting',
    'depends': ['account', 'account_financial_report', 'zaki_retail', 'zaki_profit_loss_excel_report'],
    'data': [
        'views/account_invoice_view.xml',
        'wizard/soa_report_excel_views.xml',
        'wizard/general_ledger_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto-install': False
}

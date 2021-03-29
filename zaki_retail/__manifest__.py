# -*- coding: utf-8 -*-
{
    'name': 'zaki_retail',
    'description': """ Zaki Retail """,
    'depends': ['sale_management','account','purchase','hr'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/assets.xml',
        'views/product.xml',
        'views/account.xml',
        'views/sale.xml',
        'views/purchase.xml',
        'views/account_move.xml',
        'views/employee.xml',
    ],
    'installable': True,
}
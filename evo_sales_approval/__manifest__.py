# -*- coding: utf-8 -*-
{
    'name': 'Sales Quotation Approval',
    'category': 'Tools',
    'version': '12.0',
    'sequence': 1,
    'author': 'Evozard',
    'category': 'Tools',
    'website': 'http://evozard.com/',
    'description': """Sales Quotation Approval""",
    'depends': ['base', 'sale', 'hr', 'hr_recruitment'],
    'data': [
            'data/so_approval_email_template.xml',
            'security/ir.model.access.csv',
            'security/security.xml',
            'wizard/update_wizard_view.xml',
            'view/sale_order_view.xml',
            'view/approval_workflow_view.xml',
    ],
    'qweb': [
    ],
}

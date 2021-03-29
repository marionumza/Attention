# See LICENSE file for full copyright and licensing details.
{
    'name': 'Pop-up Reminder v12',
    'version': '12.0.1.0.0',
    'category': 'Web',
    'license': 'AGPL-3',
    'summary': """Dynamic reminder of different models.
    popup reminder""",
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'depends': ['base', 'web', 'bus'],
    'data': [
        'security/ir.model.access.csv',
        'views/popup_reminder_view.xml',
        'views/popup_views.xml'
    ],
    'qweb': ['static/src/xml/view.xml'],
    'images': ['static/description/Pop-UpReminder.png'],
    'auto_install': False,
    'application': True,
    'price': 45,
    'currency': 'EUR',
}

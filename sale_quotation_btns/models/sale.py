#   © 2019 Kevin Kamau
#   License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_open_new_tab_pdf(self):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        record_url = base_url + "/report/pdf/sale.report_saleorder/" + \
            str(self.id)
        return {
            'type': 'ir.actions.act_url',
            'name': self.name,
            'target': 'new',
            'url': record_url,
        }

    @api.multi
    def action_open_new_tab_html(self):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        record_url = base_url + "/report/html/sale.report_saleorder/" + \
            str(self.id)

        return {
            'type': 'ir.actions.act_url',
            'name': self.name,
            'target': 'new',
            'url': record_url,
        }

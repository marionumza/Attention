from odoo import models,fields,api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create(self, vals):
        res = super(PurchaseOrder, self).create(vals)
        res.write({'name': 'New'})
        sequence_id = self.env['ir.sequence'].search([('code', '=', 'purchase.order')], limit=1)
        sequence_id.write({
            'number_next_actual': sequence_id.number_next_actual - 1
        })
        return res

    @api.multi
    def button_confirm(self):
        for record in self:
            record.write({
                'name': self.env['ir.sequence'].next_by_code('purchase.order') or '/'
            })
        return super(PurchaseOrder, self).button_confirm()
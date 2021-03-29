# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.multi
    def action_payslip_done(self):
        res = super(HrPayslip, self).action_payslip_done()
        if self.move_id and self.contract_id.use_in_payslip_entry:
            for move_line in self.move_id.line_ids:
                move_line.write({'analytic_account_id':self.contract_id.analytic_account_id.id})
        return res


class HrContract(models.Model):
    _inherit = 'hr.contract'

    use_in_payslip_entry = fields.Boolean(string='Use this analytic account',help="This check box will help to use this analytic account in journal entry of payslip on confimation")

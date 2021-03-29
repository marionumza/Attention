import time
from datetime import datetime, timedelta
from dateutil import relativedelta

import babel

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools import float_is_zero, float_compare
from odoo.addons import decimal_precision as dp

import datetime
from dateutil.relativedelta import relativedelta
import time
from odoo import api, fields, models, _
from odoo.exceptions import UserError
    
class employee_item(models.Model):
    
    _name = "employee.item"
                 
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    department_id = fields.Many2one('hr.department', related="employee_id.department_id", readonly=True, string="Department")
    job_id = fields.Many2one('hr.job', related="employee_id.job_id", readonly=True, string="Job Position")
    date = fields.Date(string="Date", default=fields.Date.today(), readonly=True)
    item_line_ids = fields.One2many('employee.item.line', 'item_id', string='Checklist Lines')
    state = fields.Selection([('draft', 'Draft'), ('checkin', 'Check In'), ('checkout', 'Check Out')], string='Status', default='draft')
    
    @api.one
    def unlink(self):
        for vou in self:
            if vou.state != 'draft':
                raise UserError(_('You Cant Delete Employee Checklist in Check-In Stage'))
        super(employee_item, self).unlink()
    
    @api.one
    def check_in(self):
        for tab in self:
            for cap in tab.item_line_ids:
                if cap.product_id:
                    cap.write({'checklist': True})
        return self.write({'state':'checkin'})
                    
    @api.one
    def check_out(self):
        for tab in self:
            for cap in tab.item_line_ids:
                if cap.checklist:
                    raise UserError(_('Below Item still in Check-In Stage'))
        return self.write({'state':'checkout'})

    
employee_item()

class employee_item_line(models.Model):
    
    _name = "employee.item.line"
    
    item_id = fields.Many2one('employee.item.line', string='Checklist') 
    product_id = fields.Many2one('product.product', string='Items')
    asset_id = fields.Many2one('account.asset.asset', string='Assets')
    quantity = fields.Char(string='Quantity', required=True)
    checklist = fields.Boolean(string='Check In / Out')
    
employee_item_line()                        
                           

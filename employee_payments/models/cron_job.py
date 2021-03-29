import time
from datetime import datetime, timedelta
from dateutil import relativedelta

import babel

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval

from odoo.addons import decimal_precision as dp

import datetime
from dateutil.relativedelta import relativedelta
import time
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class hr_contract(models.Model):

    _inherit='hr.contract'
    
    def process_ticket_exit_scheduler_queue(self):

        scheduler_line_obj = self.env['hr.contract']

        scheduler_line_ids = self.env['hr.contract'].search([])
        
        print "SSSSSSSSSSSSSSSSSSS",scheduler_line_ids
        
        remaining_ticket = 0.0
        remaining_exit_entry = 0.0

        for contract_data in scheduler_line_ids :

            employee_id = contract_data.employee_id.name
            
            print ":::::::::NAME::::::NAME::::::",employee_id
            
            emp_ticket = contract_data.ticket
            print ":::::::::TTTTT::::::TTTTTT::::::",emp_ticket
            
            emp_exit_entry = contract_data.exit_entry
            print ":::::::::EEEEEE::::::EEEEE::::::",emp_exit_entry
            
            
            emp_ticket_bal = contract_data.ticket_balance
            print ":::::::::TBTBTB::::::TBTBTTBT::::::",emp_ticket_bal
            
            emp_exit_entry_bal = contract_data.exit_entry_balance
            print ":::::::::EBEBEBEBE::::::EBEBEBE::::::",emp_exit_entry_bal

            date_format = '%Y-%m-%d'
            start_date = contract_data.end_less_date
            print ":::::::::DTDTDDTDT::::::DTDTDTDTTD::::::",start_date
            if start_date:         
                d1 = fields.Datetime.from_string(start_date)
                print "STSSTSTSTSTSTSTTSTST",d1
                end_date = d1 + relativedelta(years=contract_data.contract_years)
                finish_date = end_date
                print "ENEENENENENENENENNENE",finish_date
                curr_date = fields.datetime.now().strftime(date_format)
                current_date = fields.Datetime.from_string(curr_date)
                print ":::::::::CRCRCRCRCRR::::::CRRCCRCRRCRC::::::",current_date
                                
                if current_date == finish_date:   
                    contract_data.write({'ticket_balance': (emp_ticket_bal+emp_ticket),'exit_entry_balance': (emp_exit_entry_bal+emp_exit_entry),'end_less_date': finish_date})

hr_contract()       

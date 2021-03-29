# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
from odoo import api, fields, models,_
from odoo.exceptions import ValidationError

# create class for Top Saleperson Wizard.
class TopSalepersonWizard(models.TransientModel):
    _name = "top.salepesron.wizard"

    from_date = fields.Date("From date")  
    to_date = fields.Date(string="To date")

    #create function for show Top Saleperson.
    def create_saleperson_form(self): 
        order_user_list = []
        final_sale_person_list = []
        top_sale_person_dict = {}
        order_ids = False
        sale_person_object = self.env['top.sale.person']
        if self.from_date and self.to_date: 
            if self.from_date < self.to_date:
                order_ids = self.env['sale.order'].search([('state', 'in', ['sale','done']),('confirmation_date','>=',self.from_date),('confirmation_date','<=',self.to_date)])
                if order_ids: 
                    for order_id in order_ids:
                        count = 0             
                        for order_user_id in order_id.user_id:
                            if order_user_id not in order_user_list:
                                order_user_list.append(order_user_id)
            else:
                raise ValidationError("Invalid date period") 
        else:
            raise ValidationError("Invalid dates")  
        if order_user_list and order_ids: 
            for user in order_user_list:
                count = 0             
                orders = self.env['sale.order'].search([('user_id','=',user.id),('state', 'in', ['sale','done']),('confirmation_date','>=',self.from_date),('confirmation_date','<=',self.to_date)]) 
                if orders: 
                    for record in orders:
                        count = count + record.amount_total                            
                    sale_person_dict = {'sale_person':user.id,'sale_person_amount':count}
                    create_sale_person = sale_person_object.create(sale_person_dict)
                    top_sale_person_dict[create_sale_person] = count
        if top_sale_person_dict:
            import operator
            top_sale_person_dict = sorted(top_sale_person_dict.items(), key=operator.itemgetter(1), reverse=True)
            for sale_person in top_sale_person_dict:
                final_sale_person_list.append(sale_person[0])
        if len(final_sale_person_list) > 0:
            return {
                    'name': _('Top Sales Persons'),
                    'type': 'ir.actions.act_window',
                    'domain':[('id','in',[x.id for x in final_sale_person_list])],   
                    'view_mode': 'tree',
                    'res_model': 'top.sale.person',
                    'action':'top_sale_person_tree_view',
                    'view_id': False,
                    'target': 'current',
                    }
        else:
            raise ValidationError("No Record Exist") 

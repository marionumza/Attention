# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import ValidationError



class UpdateApprovalLines(models.TransientModel):
    _name = 'update.approval.lines'

    sale_order_id = fields.Many2one('sale.order', 'Order')
    approved_date = fields.Datetime(
        'Approved On', default=lambda self: fields.datetime.now())
    note = fields.Text('Note')
    approve_check = fields.Boolean('Approve Check')
    reject_check = fields.Boolean('Reject Check')

    def update_bom_approval_line(self):
        user_id = self.env.user.id
        emp_id = self.env['hr.employee'].search([('user_id', '=', user_id)])
        print("emp_id",emp_id)
        if emp_id:
            workflow_id = self.env['approval.workflow'].search(
                [('type', '=', 'sale_order'), ('active', '=', True)], limit=1)
            print(workflow_id, "workflow_id ")
            if workflow_id:
                if workflow_id.approval_line_ids:
                    level_line = workflow_id.approval_line_ids.filtered(lambda r: r.job_id.id == emp_id.job_id.id)
                    print(level_line,"level line")
                    if level_line:
                        vals = {
                            'sale_order_id': self.sale_order_id.id,
                            'level': level_line.level,
                            'approved_user_id': self.env.user.id,
                            'approved_date': self.approved_date,
                            'note': self.note,
                            'status': 'approved',
                        }
                        print(vals)
                        approv_line = self.env['record.approval'].sudo().create(vals)
                        print("approve",approv_line)
                        print("approve",approv_line.sale_order_id)
                        print("approve",approv_line.status)
                    print("len(workflow_id.approval_line_ids)",len(workflow_id.approval_line_ids))
                    if len(workflow_id.approval_line_ids) <= 1:
                        print("EEEEEEEEEEe")
                        if self.sale_order_id.approval_user_ids:
                            lst= self.sale_order_id.approval_user_ids.ids

                            print("lst",lst)
                            if self.env.user.id in lst:
                                self.sale_order_id.write({'approva_state': 'approved'})
                                self.sale_order_id.activity_id.action_done()
                            else:
                                raise ValidationError("You Not Allowed To confirm")
                        else:
                            employee_id = self.env['hr.employee'].search([('user_id.id', '=', self.sale_order_id.user_id.id)])
                            print("emp_id", employee_id)
                            emp_id = employee_id.parent_id
                            print("parent emp",emp_id,emp_id.user_id)
                            self.sale_order_id.write({'approval_user_ids': [(4, emp_id.user_id.id)]})
                            lst = self.sale_order_id.approval_user_ids.ids

                            print("lst", lst)
                            if self.env.user.id in lst:
                                self.sale_order_id.write({'approva_state': 'approved'})
                                for rec in  self.sale_order_id.activity_id:
                                    rec.action_done()
                            else:
                                raise ValidationError("You Not Allowed To confirm")


                    elif len(workflow_id.approval_line_ids) > 1:
                        bom_level = []
                        workflow_level = []
                        for data in self.sale_order_id.approval_level_ids:
                            if data.level not in bom_level and data.status not in ('pending', 'rejected'):
                                bom_level.append(data.level)
                        for rec in workflow_id.approval_line_ids:
                            workflow_level.append(rec.level)
                        if bom_level == workflow_level:
                            self.sale_order_id.write({'approva_state': 'approved'})
                        else:
                            level_val2 = self.sale_order_id.level_val + 1
                            level_line2 = workflow_id.approval_line_ids.filtered(lambda r: r.level == level_val2)
                            if not level_line2:
                                self.sale_order_id.write({'approva_state': 'approved'})
                            else:
                                emp_id2 = self.env['hr.employee'].search([('job_id', '=', level_line2.job_id.id)])
                                if emp_id2:
                                    self.sale_order_id.write({'approval_user_ids': [(5, 0, 0)]})
                                    for emp_id in emp_id2:
                                        if emp_id.user_id:
                                            self.sale_order_id.write({'approval_user_ids': [(4, emp_id.user_id.id)]})
                                    if self.sale_order_id and self.sale_order_id.approval_user_ids:
                                        email_to = ''

                                        print(self.sale_order_id.approval_user_ids)
                                        for partner in self.sale_order_id.approval_user_ids:
                                            # if partner.email :
                                            print("222222222",partner)
                                            if partner.email:
                                                print("mmmmmmmmmmmmm",partner.email)
                                                email_to +=  partner.email  + ','
                                        if self.env.user and self.env.user.email:
                                            email_from = self.env.user.email
                                        so_approval_template = workflow_id.mail_template_id
                                        if so_approval_template and email_to and email_from:
                                            mail_res = so_approval_template.with_context(email_from=email_from,email_to=email_to).send_mail(self.sale_order_id.id,force_send=True)
                                            print("Mail Sent===============", mail_res)
                                    print("MMMMM",{
                                        'approva_state': 'approve',
                                        'level_val': level_val2,
                                    })
                                    self.sale_order_id.write({
                                        'approva_state': 'approve',
                                        'level_val': level_val2,
                                    })

    # def update_bom_approval_line(self):
    #     user_id = self.env.user.id
    #     print("user_id",user_id)
    #     employee_id = self.env['hr.employee'].search([('user_id.id', '=', user_id)])
    #     print("emp_id", employee_id)
    #     emp_id = employee_id.parent_id.id
    #     if emp_id and emp_id == 231:
    #         workflow_id = self.env['approval.workflow'].search(
    #             [('type', '=', 'sale_order'), ('active', '=', True)], limit=1)
    #         print(workflow_id, "workflow_id ")
    #         if workflow_id:
    #             if workflow_id.approval_line_ids:
    #                 level_line = workflow_id.approval_line_ids.filtered(lambda r: r.job_id.id == self.env['hr.employee'].browse(emp_id).job_id.id)
    #                 print(level_line,"level line")
    #                 if level_line:
    #                     vals = {
    #                         'sale_order_id': self.sale_order_id.id,
    #                         'level': level_line.level,
    #                         'approved_user_id': self.env.user.id,
    #                         'approved_date': self.approved_date,
    #                         'note': self.note,
    #                         'status': 'approved',
    #                     }
    #                     print(vals)
    #                     approv_line = self.env['record.approval'].sudo().create(vals)
    #                     print("approve",approv_line)
    #                     print("approve",approv_line.sale_order_id)
    #                     print("approve",approv_line.status)
    #                 if len(workflow_id.approval_line_ids) <= 1:
    #                     print("roqyaaa111111111",self.env['hr.employee'].browse(emp_id).user_id.partner_id,self.env['hr.employee'].browse(emp_id).user_id.partner_id.name)
    #
    #                     # mail_content = "  Hello  " + self.env['hr.employee'].browse(emp_id).user_id.partner_id.name + ",<br>Sale Order #  " + \
    #                     #                self.sale_order_id.name + ",<br> amounting = " + str(self.sale_order_id.amount_total) +\
    #                     #                ".is waiting for your approval"
    #                     # main_content = {
    #                     #     'subject': _('Sale Order: Send for Approval') ,
    #                     #     'author_id': self.env.user.partner_id.id,
    #                     #     'body_html': mail_content,
    #                     #     'email_to': self.env['hr.employee'].browse(emp_id).user_id.partner_id.email,
    #                     # }
    #                     # print("################",main_content)
    #                     # self.env['mail.mail'].create(main_content).send()
    #
    #                     # ==========================
    #                     # email_to = ''
    #                     # email_to += self.env['hr.employee'].browse(emp_id).user_id.partner_id.email + ','
    #                     # if self.env.user and self.env.user.email:
    #                     #     email_from = self.env.user.email
    #                     # so_approval_template = workflow_id.mail_template_id
    #                     # body_ht = so_approval_template.body_html
    #                     # print("fsdfsdfsd",body_ht)
    #                     # # print("erwerwe",body_ht.object)
    #                     # print("so_approval_template",so_approval_template)
    #                     # if so_approval_template and email_to and email_from:
    #                     #     mail_res = so_approval_template.with_context(email_from=email_from,
    #                     #                                                  email_to=email_to).send_mail(self.sale_order_id.id,
    #                     #                                                                               force_send=True)
    #                     #     print("Mail Sent===============", mail_res)
    #                     # cccccccccccc
    #                     self.sale_order_id.write({'approva_state': 'approved'})
    #                 elif len(workflow_id.approval_line_ids) > 1:
    #                     print("roqyaaa22222222")
    #                     # vvvvvvvvv
    #                     bom_level = []
    #                     workflow_level = []
    #                     for data in self.sale_order_id.approval_level_ids:
    #                         if data.level not in bom_level and data.status not in ('pending', 'rejected'):
    #                             bom_level.append(data.level)
    #                     for rec in workflow_id.approval_line_ids:
    #                         workflow_level.append(rec.level)
    #                     if bom_level == workflow_level:
    #                         self.sale_order_id.write({'approva_state': 'approved'})
    #                     else:
    #                         level_val2 = self.sale_order_id.level_val + 1
    #                         level_line2 = workflow_id.approval_line_ids.filtered(lambda r: r.level == level_val2)
    #                         if not level_line2:
    #                             self.sale_order_id.write({'approva_state': 'approved'})
    #                         else:
    #                             emp_id2 = self.env['hr.employee'].search([('job_id', '=', level_line2.job_id.id)])
    #                             if emp_id2:
    #                                 self.sale_order_id.write({'approval_user_ids': [(5, 0, 0)]})
    #                                 for emp_id in emp_id2:
    #                                     if emp_id.user_id:
    #                                         self.sale_order_id.write({'approval_user_ids': [(4, emp_id.user_id.id)]})
    #                                 if self.sale_order_id and self.sale_order_id.approval_user_ids:
    #                                     email_to = ''
    #                                     email_to += self.env['hr.employee'].browse(
    #                                         emp_id).user_id.partner_id.email + ','
    #                                     if self.env.user and self.env.user.email:
    #                                         email_from = self.env.user.email
    #                                     so_approval_template = workflow_id.mail_template_id
    #                                     if so_approval_template and email_to and email_from:
    #                                         mail_res = so_approval_template.with_context(email_from=email_from,
    #                                                                                      email_to=email_to).send_mail(
    #                                             self.id,
    #                                             force_send=True)
    #                                         print("Mail Sent===============", mail_res)
    #                                 self.sale_order_id.write({
    #                                     'approva_state': 'pending',
    #                                     'level_val': level_val2,
    #                                 })

    def update_bom_approval_line_reject(self):
        user_id = self.env.user.id
        employee_id = self.env['hr.employee'].search([('user_id', '=', user_id)])
        emp_id = employee_id.parent_id.id
        if emp_id == 231:
            workflow_id = self.env['approval.workflow'].search(
                [('type', '=', 'sale_order'), ('active', '=', True)], limit=1)
            if workflow_id:
                if workflow_id.approval_line_ids:
                    level_line = workflow_id.approval_line_ids.filtered(
                        lambda r: r.job_id.id == emp_id.job_id.id)
                    if level_line:
                        vals = {
                            'sale_order_id': self.sale_order_id.id,
                            'level': level_line.level,
                            'approved_user_id': self.env.user.id,
                            'approved_date': self.approved_date,
                            'note': self.note,
                            'status': 'rejected',
                        }
                        approv_line = self.env['record.approval'].create(vals)
                        self.sale_order_id.write({
                            'approva_state': 'draft',
                            'level_val': 0,
                            'approval_user_ids': [(5, 0, 0)]
                        })

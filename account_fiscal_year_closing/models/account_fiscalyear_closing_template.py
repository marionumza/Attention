# Copyright 2016 Tecnativa - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models , api
from datetime import date


class AccountFiscalyearClosingTemplate(models.Model):
    _inherit = "account.fiscalyear.closing.abstract"
    _name = "account.fiscalyear.closing.template"

    @api.model
    def _getname(self):
        today = date.today()
        print("Today's date year :", today.year)

        return "Closing "+ str((today.year-1))

    @api.model
    def _getname(self):
        today = date.today()
        print("Today's date year :", today.year)

        return "Closing " + str((today.year - 1))

    @api.model
    def _getchart(self):
        mychart = self.env['account.chart.template'].sudo().search([])
        print(mychart)
        return mychart[0]

    name = fields.Char(translate=True ,default=_getname)
    move_config_ids = fields.One2many(
        comodel_name='account.fiscalyear.closing.config.template',
        inverse_name='template_id', string="Moves configuration",
    )
    chart_template_ids = fields.Many2many(
        comodel_name="account.chart.template", string="Available for",
        required=True,default=_getchart
    )


class AccountFiscalyearClosingConfigTemplate(models.Model):
    _inherit = "account.fiscalyear.closing.config.abstract"
    _name = "account.fiscalyear.closing.config.template"
    _order = "sequence asc, id asc"

    @api.model
    def _get_journal(self):
        today = date.today()
        str1 = "Opening " + str((today.year ))
        print(str1)
        myjournal = self.env['account.journal'].sudo().search([('name', '=', str1)])

        vals = {}
        vals['name'] = str1
        vals['type'] = "bank"
        vals['code'] = 'FY-' + str((today.year - 1))
        vals['update_posted'] = True
        vals['default_debit_account_id'] = ""
        vals['default_credit_account_id'] = ""

        print(vals)
        if not myjournal:
            myjournal = self.env['account.journal'].sudo().create(vals)

        mychart=self.env['account.account'].sudo().search([('id','=',myjournal.default_credit_account_id.id)])

        mychart.sudo().unlink()

        print(myjournal)

    @api.model
    def _getname(self):
        today = date.today()
        print("Today's date year :", today.year)
        self._get_journal()

        return "Closing " + str((today.year - 1))

    name = fields.Char(translate=True,default=_getname)

    template_id = fields.Many2one(
        comodel_name='account.fiscalyear.closing.template', index=True,
        readonly=True, string="Fiscal Year Closing Template", required=True,
        ondelete='cascade',
    )




    journal_id = fields.Many2one(company_dependent=True  )

    @api.model
    def _default_so_tc(self):
        terms_obj = self.env['account.account']
        terms = []
        termsids = terms_obj.search([('code', '>=', '4000000'), ('code', '<=', '9999902')])
        for rec in termsids:
            values = {}
            values['name'] = rec.name
            values['src_accounts'] = rec.code
            values['dest_account'] = "3000003"
            terms.append((0, 0, values))
        return terms

    mapping_ids = fields.One2many(
        comodel_name='account.fiscalyear.closing.mapping.template',
        inverse_name='template_config_id', string="Account mappings",copy=True,
    default=_default_so_tc )

    closing_type_ids = fields.One2many(
        comodel_name='account.fiscalyear.closing.type.template',
        inverse_name='template_config_id', string="Closing types",
    )
    move_date = fields.Selection(
        selection=[
            ('last_ending', 'Last date of the ending period'),
            ('first_opening', 'First date of the opening period'),
        ],
        string="Move date",
        default='last_ending',
        required=True,
    )

    _sql_constraints = [
        ('code_uniq', 'unique(code, template_id)',
         'Code must be unique per fiscal year closing!'),
    ]


    # def button_fill(self):
    #
    #     Myaccounts = self.env['account.account'].search(
    #         [('code', '>=', '4000000'), ('code', '<=', '9999902')])
    #     for rec in Myaccounts:
    #         dic_vals ={'name':rec.name , 'src_accounts':rec.code , 'dest_account':"3000003"}
    #
    #         self.mapping_ids.append( (0, 0, dic_vals))

    # By default load the terms and conditions configured in the master T&C configuration




class AccountFiscalyearClosingMappingTemplate(models.Model):
    _inherit = "account.fiscalyear.closing.mapping.abstract"
    _name = "account.fiscalyear.closing.mapping.template"

    name = fields.Char(translate=True)
    template_config_id = fields.Many2one(
        comodel_name='account.fiscalyear.closing.config.template', index=True,
        string="Fiscal year closing config template", readonly=True,
        required=True, ondelete='cascade',
    )
    src_accounts = fields.Char(
        string="Source accounts", required=True,
        help="Account code pattern for the mapping source accounts"
    )
    dest_account = fields.Char(
        string="Destination account",
        help="Account code pattern for the mapping destination account. Only "
             "the first match will be considered. If this field is not "
             "filled, the performed operation will be to remove any existing "
             "balance on the source accounts with an equivalent counterpart "
             "in the same account."
    )



class AccountFiscalyearClosingTypeTemplate(models.Model):
    _inherit = "account.fiscalyear.closing.type.abstract"
    _name = "account.fiscalyear.closing.type.template"

    template_config_id = fields.Many2one(
        comodel_name='account.fiscalyear.closing.config.template', index=True,
        string="Fiscal year closing config template", readonly=True,
        required=True, ondelete='cascade',
    )

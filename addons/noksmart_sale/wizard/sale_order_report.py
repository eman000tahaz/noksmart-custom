# -*- coding: utf-8 -*-

from odoo import fields, models, _, api
from odoo.exceptions import UserError, ValidationError


class SaleOrderReport(models.TransientModel):
    _name = "sale.order.report"

    @api.model
    def _get_team_leader(self):
        sales_team = self.env['crm.team'].search([('user_id', '=', self.env.user.id)])
        if sales_team:
            return True
        else:
            return False

    def _get_current_user(self):
        return self.env.user.id

    @api.model
    def _get_domain(self):
        sales_teams = self.env['crm.team'].search([('user_id', '=', self.env.user.id)])
        if sales_teams:
            ids = []
            for team in sales_teams:
                if team.member_ids:
                    for m_id in team.member_ids:
                        ids.append(m_id.id)
            return [('id', 'in', ids)]

    
    company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.user.company_id)
    # date_from = fields.Date(string='Start Date')
    # date_to = fields.Date(string='End Date')
    is_team_leader = fields.Boolean('Is Team Leader', default=_get_team_leader)
    current_user = fields.Many2one('res.users', 'Current User', default=_get_current_user)
    sales_persons = fields.Many2many('res.users', string='Sales Persons', domain=_get_domain)


    
    @api.multi
    def print_report(self, data):
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['company_id', 'date_from', 'date_to', 'is_team_leader', 'current_user', 'sales_persons'])[0]
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env['report'].get_action(records, 'noksmart_sale.report_sale_order', data=data)
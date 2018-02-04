# -*- coding: utf-8 -*-

import time
from odoo import api, models

class ReportSaleOrder(models.AbstractModel):
	_name = 'report.noksmart_sale.report_sale_order'

	def _get_accounts(self, users):
		result = []
		for user_id in users:
			res = {}
			untaxed_total = 0.0
			total = 0.0
			margin = 0.0
			sales_orders = self.env['sale.order'].search([('user_id', '=', user_id)])
			for order in sales_orders:
				untaxed_total += order.amount_untaxed
				total += order.amount_total
				margin += order.margin
				name = order.user_id.name
			res['name'] = name
			res['untaxed_total'] = untaxed_total
			res['total'] = total
			res['margin'] = margin
			result.append(res)
		return result



	@api.model
	def render_html(self, docids, data=None):
		self.model = self.env.context.get('active_model')
		docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
		is_team_leader = data['form'].get('is_team_leader')
		if is_team_leader:
			users = data['form'].get('sales_persons')
		else:
			users = []
			current_user = data['form'].get('current_user')[0]
			users.append(current_user)	
		records = self._get_accounts(users)

		docargs = {
			'doc_ids': self.ids,
			'doc_model': self.model,
			'data': data['form'],
			'docs': docs,
			'records': records,
		}
		return self.env['report'].render('noksmart_sale.report_sale_order', docargs)


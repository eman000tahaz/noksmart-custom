# -*- coding: utf-8 -*-
{
    'name': 'Noksmart Sale',
    'version': '1.0.1',
    'Author': "Eman Taha",
    'category': 'Sale',
    'sequence': 20,
    'summary': 'Noksmart Sale',
    'depends': ['sale', 'sale_margin', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_team_views.xml',
        'wizard/sale_order_report_view.xml',
        'views/noksmart_sale.xml',
        'views/report_sale_order.xml',
    ],
    'demo': [
    ],
    'qweb': [],
    'installable': True,
    'application': True,
}

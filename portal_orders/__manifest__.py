# -*- coding: utf-8 -*-
{
    'name': 'Portal Orders',
    'version': '15',
    'summary': 'Portal Orders',
    'depends': ['sale','portal'],
    
    'data' : [
         'security/ir.model.access.csv',
        'views/sales_order_design_templates.xml',

       
        ],
    'images': [],
    
    'assets': {
        'web.assets_frontend': [

        'portal_orders/static/src/css/sales_order_design.css',
        'portal_orders/static/src/css/sales_order.css',
         'portal_orders/static/src/js/sales_order_portal.js',
         'portal_orders/static/src/js/sales_order.js',
         ]
        },
     
    'installable': True,
    'auto_install': False,
    'application': True,
   

}

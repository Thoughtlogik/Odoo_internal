# -*- coding: utf-8 -*-
{
    'name': 'Portal Orders',
    'version': '1.5',
    'summary': 'Portal Orders',
    'depends': ['sale','portal'],
    
    'data' : [
         'security/ir.model.access.csv',
        'views/sales_quotation_templates.xml',

       
        ],
    'images': [],
    
    'assets': {
        'web.assets_frontend': [

        'portal_orders/static/src/css/sales_quotation.css',
        'portal_orders/static/src/css/chosen.min.css',
         'portal_orders/static/src/js/chosen.jquery.min.js',
         'portal_orders/static/src/js/portal_quotation.js',
         ]
        },
     
    'installable': True,
    'auto_install': False,
    'application': True,
   

}

# -*- coding: utf-8 -*-

#import of odoo
from odoo import api, fields, models

#inheriting the TAX model
class Tax(models.Model):
    
    _inherit = 'account.tax'
    
    children_tax_ids = fields.Many2many('account.tax',
        'account_tax_filiation_rel', 'parent_tax', 'child_tax',
        check_company=True,
        string='Children Taxes')

#Inherit the sale order
class SaleOrder(models.Model):
    
    _inherit = 'sale.order'
    
    def get_the_price_list(self,partner):
        partner_id = self.env['res.partner'].search([('name', '=', partner)])
        price_name = partner_id.property_product_pricelist.id
        return price_name
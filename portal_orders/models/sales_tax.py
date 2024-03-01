# -*- coding: utf-8 -*-

#import of odoo
from odoo import api, fields, models

#inheriting the account.tax model
class TaxField(models.Model):
    
    _inherit = 'account.tax'
    
    children_tax_ids = fields.Many2many('account.tax',
        'account_tax_filiation_rel', 'parent_tax', 'child_tax',
        check_company=True,
        string='Children Taxes')

#inherit the sale order for get the pricelist
class SaleOrderLane(models.Model):
    
    _inherit = 'sale.order'
    
    def pricce_list_change(self,partner):
        print("lllll")
        partner_id = self.env['res.partner'].search([('name', '=', partner)])
        price_name = partner_id.property_product_pricelist.id
        print("price_name",price_name)
        return price_name
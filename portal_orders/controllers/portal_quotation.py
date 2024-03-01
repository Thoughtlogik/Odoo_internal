# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request, route, Controller
from odoo.exceptions import AccessError
import math

class PortalQuotation(http.Controller):
    #URL Re directed to sale order
    @http.route(['/my/quotation'], type='http', auth="user", website=True)
    def portal_my_quotation(self, **kw):
        values = {}
        user_id = request.session.uid
        customer_id = request.env['res.partner'].sudo().search([])
        payment_id = request.env['account.payment.term'].sudo().search([])
        product_uom_id = request.env['uom.uom'].sudo().search([])
        price_id = request.env['product.pricelist'].sudo().search([])
        product_id = request.env['product.product'].sudo().search([])
        analytic_id = request.env['account.analytic.account'].sudo().search([])
        children_tax_ids = request.env['account.tax'].sudo().search([])
        values['customer_id'] = customer_id
        values['payment_id'] = payment_id
        values['price_id'] = price_id
        values['product_id'] = product_id
        values['product_uom_id'] = product_uom_id
        values['analytic_id'] = analytic_id
        values['children_tax_ids'] = children_tax_ids
        values['page_name'] = 'quotation'
        print("order values-->",values)
        return request.render('portal_orders.sale_my_quotations_agent_portal',values)
    
#get the values from sale order and create the new sale order
    @http.route('/action_add_quotation', type='http', auth="user", website=True)
    def portal_my_quotation_data(self, **post):
        print("post-->",post)
        sale = ''
        product_id = ''
        expiration_date = ''
        quotation_date = ''
        product_ids = ''
        payment_ids = ''
        pricelist_id = ''
        analytic_ids = ''
        product_info = {}
        for key, value in post.items():
            if key.startswith('product_name_'):
                idx = key.split('_')[2]
                product_info[idx] = {'name': value,
                                     'description': post.get(f'description_{idx}'),
                                     'quantity': post.get(f'qty_{idx}'),
                                     'unit': post.get(f'product_uom_{idx}'),
                                     'unit_price': post.get(f'price_unit_{idx}'),
                                     'tax_ids': post.get(f'tax_emp_{idx}'),
                                     'discount': post.get(f'discount_{idx}'),
                                     'subtotal': post.get(f'price_subtotal_{idx}'),
                                      'tax_ids': post.get(f'tax_emp_{idx}')}
        order_lines = []
        if product_info:
            for idx, item in product_info.items():
                split =item['name'].split(' ')
                product_ref = split[0]
                tax = []
                lst = ''
                if item['tax_ids']:
                    tax_rep = item['tax_ids']
                    tax.append(tax_rep)
                    tax_cat = tax[0]
                    li = list(tax_cat.split(",")) 
                    lst = [int(x) if x.isdigit() else float(x) for x in li]
                product_id = request.env['product.product'].sudo().search([('default_code', '=', product_ref)])
                uom_id = request.env['uom.uom'].sudo().search([('name', '=', item['unit'])])
                description = item['name'].split('{')
                order_line = {
                    'product_id': product_id.id,
                    'name': description[0],
                    'product_uom_qty': float(item['quantity']),
                    'product_uom': uom_id.id,
                    'price_unit': float(item['unit_price']),
                    'discount': float(item['discount']) if item['discount'] else 0.0,
                    'tax_id': [(6, 0,lst)],
                    'price_subtotal': float(item['subtotal']),
                }
                # order_lines.append((0, 0, order_line))
                order_lines.append((0,0,order_line))
        partner_name = post.get('partner')
        customer_id = request.env['res.partner'].sudo().search([('name', '=', partner_name)])
        # if post.get('expiration'):
        #     expiration_date = post.get('expiration')
        # else:
        #     expiration_date = ''
        # if post.get('quotation'):
        #     quotation_date = post.get('quotation')
        # else:
        #     quotation_date = '' 
        price_name = post.get('price')
        print("price_name-->",price_name)
        if price_name:
            pricelist = request.env['product.pricelist'].search([('id', '=', price_name)])
            pricelist_id = pricelist.id
        payment = post.get('payment')
        if payment:
            payment_id = request.env['account.payment.term'].search([('name', '=', payment)])
            payment_ids = payment_id.id
        product = post.get('product')
        quantity = post.get('qty')
        analytic = post.get('analytic')
        if analytic:
            analytic_id = request.env['account.analytic.account'].search([('name', '=', analytic)])
            analytic_ids = analytic_id.id
        subtotal = post.get('price_subtotal')
        product_uom = post.get('product_uom')
        uom = request.env['uom.uom'].search([('name', '=', product_uom)])
        if product:
            product_id = request.env['product.product'].search([('default_code', '=', product.split("'")[1])])
            product_ids = product_id.id
        if partner_name:
            sale = request.env['sale.order'].sudo().create({
                'partner_id': customer_id.id,
                # 'validity_date': expiration_date,
                # 'date_order': quotation_date,
                'payment_term_id': payment_ids,
                'pricelist_id': pricelist_id,
                'analytic_account_id': analytic_ids,
                'state':'sale',
                #'order_line': [(0,0, order_lines)]
                })
            print("sale",sale)
            if  post.get('expiration'):
                sale.update({'validity_date': post.get('expiration')})
            if post.get('quotation'):
                sale.update({'date_order': post.get('quotation')})
            if order_lines:   
                sale.update({'order_line': order_lines})
        return request.redirect('/my/quotes#')
    
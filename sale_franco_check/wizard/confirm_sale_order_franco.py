from openerp import models, fields, api, _
from openerp import netsvc
from openerp import tools
from itertools import groupby

class confirm_quotation_franco(models.TransientModel):
    _name = 'confirm.sale.order.franco'
    _description = 'Confirm Sale Order'

    @api.multi
    def confirm_sale_order_franco(self):
        wf_service = netsvc.LocalService('workflow')
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        filtered_sale_orders = filter(lambda order: order.state =='draft', sale_orders) # only consider quotations
        sorted_sale_orders = sorted(filtered_sale_orders, key=lambda order: order.partner_id) # necessary for group_by

        for partner, ordrs in groupby(sorted_sale_orders, lambda order: order.partner_id):
            orders = [order for order in ordrs] # iterator only allows one iteration
            orders_franco_check = filter(lambda order: order.franco_check, orders)
            orders_to_be_confirmed = filter(lambda order: not order.franco_check, orders)

            if not partner.franco_amount or partner.franco_amount <= 0.0:
                amount_total = float("inf")
            else:
                amount_total = sum(map(lambda order: order.amount_untaxed, orders_franco_check))

            if amount_total >= partner.franco_amount:
                orders_to_be_confirmed += orders_franco_check

            for order in orders_to_be_confirmed:
                wf_service.trg_validate(self.env.uid, 'sale.order', order.id, 'order_confirm', self.env.cr)

        return {'type': 'ir.actions.act_window_close'}

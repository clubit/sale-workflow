import logging

from openerp import api, models, fields
from openerp.osv import fields as old_fields
from openerp import netsvc
from datetime import datetime
from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import tools

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    fixed_delivery_day = fields.Selection([
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    ], string='Fixed Delivery Day', required=False)

    # Works when view has no on_change override. Fixed in Odoo 9.
    # @api.onchange('partner_id')
    # def _onchange_partner_id_set_delivery_day(self):
    #     fixed_delivery_day = False
    #     values = {}
    #     if self.partner_id.fixed_delivery_day:
    #         values['fixed_delivery_day'] = self.partner_id.fixed_delivery_day
    #     self.update(values)

    def onchange_partner_id(self, cr, uid, ids, partner_id=None, context=None):
        res = super(SaleOrder, self).onchange_partner_id(cr, uid, ids, partner_id, context=context)
        if 'value' not in res:
            res['value'] = {}
        partner_obj = self.pool.get('res.partner')
        partner = partner_obj.browse(cr, uid, partner_id, context)
        fixed_delivery_day = self._get_partner_fixed_delivery_day(cr, uid, partner, context)
        if fixed_delivery_day:
            res['value'].update({'fixed_delivery_day': fixed_delivery_day})
        return res

    def _get_partner_fixed_delivery_day(self, cr, uid, partner, context=None):
        if not partner: return False # stop recursion when nothing is found
        result = partner.fixed_delivery_day
        if not result:
            result = self._get_partner_fixed_delivery_day(cr, uid, partner.parent_id)
        return result

    # default fixed_delivery_day based on the partner (if provided)
    @api.model
    def create(self, vals):
        partner = self.env['res.partner'].browse(vals.get('partner_id'))
        fixed_delivery_day = partner.fixed_delivery_day
        if fixed_delivery_day: vals.update({'fixed_delivery_day': fixed_delivery_day})
        result = super(SaleOrder, self).create(vals)
        return result

    # override to get correct date based on fixed_delivery_day
    def _get_date_planned(self, cr, uid, order, line, start_date, context=None):
        _logger.debug("get date planned")
        result = super(SaleOrder, self)._get_date_planned(cr, uid, order, line, start_date, context)
        date_format = DEFAULT_SERVER_DATE_FORMAT
        if len(result) > 10: date_format = DEFAULT_SERVER_DATETIME_FORMAT
        result = datetime.strptime(result, date_format)
        if order.fixed_delivery_day:
            result = tools._get_future_next_date_for_day(result, order.fixed_delivery_day)
        return datetime.strftime(result, date_format)

    # override to get correct commitment date_format
    def _get_commitment_date(self, cr, uid, ids, name, arg, context=None):
        _logger.debug("get commitment date")
        res = super(SaleOrder, self)._get_commitment_date(cr, uid, ids, name, arg, context)
        for order in self.browse(cr, uid, ids, context=context):
            if order.state == 'cancel': continue
            if order.fixed_delivery_day:
                date_format = DEFAULT_SERVER_DATETIME_FORMAT
                res_date = datetime.strptime(res[order.id], date_format)
                res_date = tools._get_future_next_date_for_day(res_date, order.fixed_delivery_day)
                res[order.id] = datetime.strftime(res_date, DEFAULT_SERVER_DATETIME_FORMAT)
        return res

    _columns = {
        'commitment_date': old_fields.function(_get_commitment_date, store=True,
            type='datetime', string='Commitment Date',
            help="Date by which the products are sure to be delivered. This is "
                 "a date that you can promise to the customer, based on the "
                 "Product Lead Times.")
    }

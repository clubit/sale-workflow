from openerp.osv import osv, fields
from openerp import netsvc
from datetime import datetime, timedelta
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
import logging
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
import tools

_logger = logging.getLogger(__name__)

class stock_picking(osv.Model):
    _inherit = "stock.picking"

    _columns = {
        'fixed_delivery_day': fields.selection([(1,'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], "Fixed Delivery Day", copy=False),
    }

    # default fixed_delivery_day based on the partner (if provided)
    def create(self, cr, uid, vals, context=None):
        partner_obj = self.pool.get('res.partner')
        partner_id = vals.get('partner_id', None)
        if partner_id:
            fixed_delivery_day = self._get_partner_fixed_delivery_day(cr, uid, partner_id, context)
            if fixed_delivery_day: vals.update({'fixed_delivery_day': fixed_delivery_day})
        return super(stock_picking, self).create(cr, uid, vals, context=context)

    def check_schedule_with_fixed_delivery_day(self, cr, uid, ids, context=None):
        picking_obj = self.pool.get('stock.picking')
        pickings = picking_obj.browse(cr, uid, picking_ids)
        for picking in pickings:
            if not picking.fixed_delivery_day: continue

    def action_fixed_delivery_day(self, cr, uid, ids, context=None):
        for pick in self.browse(cr, uid, ids):
            if not pick.fixed_delivery_day: continue
            old_min_date = datetime.strptime(pick.min_date, DEFAULT_SERVER_DATETIME_FORMAT)
            new_min_date = tools._get_future_next_date_for_day(old_min_date, pick.fixed_delivery_day)
            if old_min_date == new_min_date: continue
            self.write(cr, uid, ids, {'min_date': new_min_date})
        return True

    # method called by scheduler
    def schedule_deliveries_with_fixed_day(self, cr, uid, context=None):
        picking_obj = self.pool.get('stock.picking')
        picking_ids = picking_obj.search(cr, uid, [('type', '=', 'out'), ('fixed_delivery_day', '!=', False), '|', ('state', '!=', 'done'), ('warehouse_sent', '!=', False)])
        self.check_schedule_with_fixed_delivery_day(cr, uid, ids, context)

    def _get_partner_fixed_delivery_day(self, cr, uid, partner_id, context=None):
        partner_obj = self.pool.get('res.partner')
        partner = partner_obj.browse(cr, uid, partner_id, context)
        if not partner: return False # stop recursion when nothing is found
        result = partner.fixed_delivery_day
        if not result:
            result = self._get_partner_fixed_delivery_day(cr, uid, partner.parent_id.id)
        return result

    def _get_next_date_for_day(self, dt, day):
        return tools._get_next_date_for_day(dt, day)

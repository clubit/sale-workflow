from openerp import fields
from openerp.osv import osv

class stock_picking(osv.Model):
    _inherit = "stock.picking"

    order_reference = fields.Char(copy=False)

    def _get_invoice_vals(self, cr, uid, key, inv_type, journal_id, move, context=None):
        inv_vals = super(stock_picking, self)._get_invoice_vals(cr, uid, key, inv_type, journal_id, move, context=context)
        sale = move.picking_id.sale_id
        if sale: inv_vals.update({'reference': sale.client_order_ref})
        return inv_vals

class stock_move(osv.Model):
    _inherit = "stock.move"

    def _prepare_picking_assign(self, cr, uid, move, context=None):
        result = super(stock_move, self)._prepare_picking_assign(cr, uid, move, context=context)
        result.update({'order_reference': move.group_id and move.group_id.order_reference or False})
        return result

    def _create_backorder(self, cr, uid, picking, backorder_moves=[], context=None):
        result = super(stock_picking, self)._create_backorder(cr, uid, picking, backorder_moves=[], context=None)
        result.order_reference = picking.order_reference
        return result

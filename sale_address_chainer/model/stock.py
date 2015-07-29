from openerp import models,fields
from openerp.osv import osv

##############################################################################
#    stock.picking                                                           #
#    This class extends stock.picking with the fields partner_shipping_id    #
#    and partner_buyer_id.
##############################################################################
    
class stock_picking(models.Model):
    _name = "stock.picking"
    _inherit = "stock.picking"
    
    invoice_partner_id = fields.Many2one('res.partner', 'Invoice Address', change_default=True, readonly=False, required=False)
    sale_partner_id = fields.Many2one('res.partner', 'Sale Address', change_default=True, readonly=False, required=False)

    def _get_invoice_vals(self, cr, uid, key, inv_type, journal_id, move, context=None):
        inv_vals = super(stock_picking, self)._get_invoice_vals(cr, uid, key, inv_type, journal_id, move, context=context)
        sale = move.picking_id.sale_id
        if sale: inv_vals.update({'picking_partner_id': sale.partner_shipping_id.id,'sale_partner_id': sale.partner_id.id})
        return inv_vals

class stock_move(osv.Model):
    _inherit = "stock.move"

    def _prepare_picking_assign(self, cr, uid, move, context=None):
        result = super(stock_move, self)._prepare_picking_assign(cr, uid, move, context=context)
        result.update({'invoice_partner_id': move.group_id and move.group_id.invoice_partner_id.id or False,'sale_partner_id': move.group_id and move.group_id.sale_partner_id.id or False})
        return result

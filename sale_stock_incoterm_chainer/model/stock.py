from openerp import models, fields

class stock_picking(models.Model):
    _inherit = "stock.picking"

    incoterm = fields.Many2one('stock.incoterms')

class stock_move(models.Model):
    _inherit = "stock.move"

    def _prepare_picking_assign(self, cr, uid, move, context=None):
        result = super(stock_move, self)._prepare_picking_assign(cr, uid, move, context=context)
        result.update({'incoterm': move.group_id and move.group_id.incoterm.id or False})
        return result
from openerp import models

class sale_order(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    def _prepare_procurement_group(self, cr, uid, order, context=None):
        res = super(sale_order, self)._prepare_procurement_group(cr, uid, order, context=None)
        res.update({'incoterm': order.incoterm.id})
        return res
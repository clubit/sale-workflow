from openerp.osv import osv

class sale_order(osv.Model):
    _inherit = 'sale.order'

    def _prepare_procurement_group(self, cr, uid, order, context=None):
        '''Copy info from sale.order to procurement.group'''
        res = super(sale_order, self)._prepare_procurement_group(cr, uid, order, context=context)
        res.update({'order_reference': order.client_order_ref or False})
        return res
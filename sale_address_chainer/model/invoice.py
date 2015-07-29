from openerp import models,fields
from openerp.osv import osv

##############################################################################
#
#    account.invoice
#
#    This class extends account.invoice with the fields partner_shipping_id
#    and partner_buyer_id.
#
##############################################################################
    
class account_invoice(models.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"
    
    picking_partner_id = fields.Many2one('res.partner', 'Shipping Address', change_default=True, readonly=False, required=False)
    sale_partner_id = fields.Many2one('res.partner', 'Sale Address', change_default=True, readonly=False, required=False)

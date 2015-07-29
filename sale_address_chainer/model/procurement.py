from openerp import models, fields

class procurement_group(models.Model):
    _inherit = 'procurement.group'

    invoice_partner_id = fields.Many2one('res.partner', 'Invoice Address')
    sale_partner_id = fields.Many2one('res.partner', 'Sale Address')

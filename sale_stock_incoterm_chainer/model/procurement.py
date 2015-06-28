from openerp import models, fields

class procurement_group(models.Model):
    _inherit = 'procurement.group'

    incoterm = fields.Many2one('stock.incoterms')
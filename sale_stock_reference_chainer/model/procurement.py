from openerp import models, fields

class procurement_group(models.Model):
    _inherit = 'procurement.group'

    order_reference = fields.Char(copy=False)
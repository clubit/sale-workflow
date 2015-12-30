from openerp import models, fields, api, _

class sale_order(models.Model):
    _inherit = "sale.order"

    franco_check = fields.Boolean(string='Franco Check', help='When active, this order is included in the franco check.')

    _defaults = {
        'franco_check': True,
    }

from openerp import api, models, fields
from openerp.tools.translate import _

class ResPartner(models.Model):
    _inherit = "res.partner"

    fixed_delivery_day = fields.Selection([
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    ], string='Fixed Delivery Day', required=False)

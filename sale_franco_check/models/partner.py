from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

class res_partner(models.Model):
    _inherit = "res.partner"
    franco_amount = fields.Float(
            string='Franco Amount',
            digits=dp.get_precision('Product Price'),
            help="Minimum amount the partner must order. This is used when confirming a group of quotations.")

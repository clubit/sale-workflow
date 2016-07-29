# -*- coding: utf-8 -*-
#
#    Copyright (C) 2016 Clubit BVBA
#    (<http://www.clubit.be>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    order_shadow_line = fields.One2many('sale.order.shadow.line','order_id','Order Lines',readonly=True,copy=True)

    @api.multi
    def copy_to_shadow(self):
        if not self.order_shadow_line:
            for line in self.order_line:
                self.env['sale.order.shadow.line'].create({
                    'order_id': line.order_id.id,
                    'name' : line.name,
                    'sequence' : line.sequence,
                    'product_id' : line.product_id.id,
                    'price_unit' : line.price_unit,
                    'product_uom_qty' : line.product_uom_qty,
                    'product_uom' : line.product_uom.id,
                    'product_uos_qty' : line.product_uos_qty,
                    'product_uos' : line.product_uos.id,
                })
                _logger.debug("order line copied!")
        else:
            _logger.debug("shadow copy exists, aborting")


    @api.multi
    def copy_from_shadow(self):
        if self.order_shadow_line:
            for line in self.order_line:
                line.unlink()
                _logger.debug("order line deleted!")
            for line in self.order_shadow_line:
                self.env['sale.order.line'].create({
                    'order_id': line.order_id.id,
                    'name' : line.name,
                    'sequence' : line.sequence,
                    'product_id' : line.product_id.id,
                    'price_unit' : line.price_unit,
                    'product_uom_qty' : line.product_uom_qty,
                    'product_uom' : line.product_uom.id,
                    'product_uos_qty' : line.product_uos_qty,
                    'product_uos' : line.product_uos.id,
                })
                _logger.debug("order line restored!")
        else:
            _logger.debug("no shadow lines, aborting")

class SaleOrderShadowLine(models.Model):
    _name = 'sale.order.shadow.line'
    _description = 'Sales Order Shadow Line'

    order_id = fields.Many2one('sale.order', 'Order Reference', required=False, ondelete='cascade', select=True, readonly=True)
    name = fields.Text('Description', required=True, readonly=True)
    sequence = fields.Integer('Sequence', help="Gives the sequence order when displaying a list of sales order lines.")
    product_id = fields.Many2one('product.product', 'Product', domain=[('sale_ok', '=', True)], change_default=True, readonly=True, ondelete='restrict')
    price_unit = fields.Float('Unit Price', required=True, readonly=True)
    product_uom_qty = fields.Float('Quantity', required=True, readonly=True)
    product_uom = fields.Many2one('product.uom', 'Unit of Measure ', required=True, readonly=True)
    product_uos_qty = fields.Float('Quantity (UoS)', readonly=True)
    product_uos = fields.Many2one('product.uom', 'Product UoS')

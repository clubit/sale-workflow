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

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    order_bom_line = fields.One2many('sale.order.bom.line','order_id','BOM Lines',readonly=False,copy=True)
    order_bomified = fields.Boolean(string="Bomified",readonly=True)

    @api.multi
    def update_so_lines_from_bomify(self):
        if self.order_bom_line:
            missingproducts = []
            #check if all components for all BOM lines are present in the sales order
            allcomponentquantitiesfound = True
            for line in self.order_bom_line:
                bomfound = False
                for component in line.product_id.bom_ids.bom_line_ids:
                    componentquantityfound = False

                    for orderline in self.order_line:
                        if orderline.product_id.id == component.product_id.id:
                            bomfound = True
                            if orderline.product_uom_qty < component.product_qty*line.product_uom_qty:
                                errormessage = str(line.product_id.name + ' missing ' + str(int(component.product_qty*line.product_uom_qty-orderline.product_uom_qty)) + "x " + component.product_id.name)
                                missingproducts.append(errormessage)
                                missingproducts.append('\n')
                                componentquantityfound = False
                            else:
                                _logger.debug("ok, component found, sufficient qty")
                                componentquantityfound = True

                        
                    if componentquantityfound == False:
                        _logger.debug("insufficient components for one of the BOM's in order!")
                        allcomponentquantitiesfound = False

                if bomfound == False:
                    errormessage = str(line.product_id.name + ' missing all products ' + '\n')
                    missingproducts.append(errormessage)
            
            if allcomponentquantitiesfound == False:
                _logger.debug("not all BOM lines found :(")
                _logger.debug("errormessage: %s", missingproducts)
                raise except_orm(_('Could not complete Reverse BOM!'),_('%s') % ''.join(missingproducts))
                return


            for line in self.order_bom_line:
                for component in line.product_id.bom_ids.bom_line_ids:
                    for orderline in self.order_line:
                        if orderline.product_id.id == component.product_id.id:
                            orderline.write({'product_uom_qty': orderline.product_uom_qty - component.product_qty*line.product_uom_qty, 'product_uos_qty': orderline.product_uos_qty - component.product_qty*line.product_uom_qty})
                            if (orderline.product_uom_qty - component.product_qty*line.product_uom_qty) <= 0:
                                orderline.unlink()

                
                # ADD BOM Products from BOM to SO
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
                _logger.debug("order line from bom created!")
        else:
            _logger.debug("no bom lines, aborting")

class SaleOrderBomLine(models.Model):
    _name = 'sale.order.bom.line'
    _description = 'Sales Order Bom Line'

    @api.onchange('product_id')
    def _onchange_product(self):
        if not self.product_id: return
        prod = self.env['product.product'].browse(self.product_id.id)
        prod_price = 0.0
        for component in prod.bom_ids.bom_line_ids:
            for line in self.order_id.order_line:
                if component.product_id.id == line.product_id.id:
                    prod_price += line.price_unit*component.product_qty
                    _logger.debug("price incremented by order line: %s", line.price_unit*component.product_qty)
                else:
                    prod_price += component.product_id.lst_price*component.product_qty
                    _logger.debug("price incremented by: %s", component.product_id.lst_price*component.product_qty)
        self.name = prod.name
        self.product_uom_qty = 1
        self.product_uos_qty = 1
        self.product_uom = prod.uom_id.id
        self.product_uos = prod.uos_id.id
        self.price_unit = prod_price

    order_id = fields.Many2one('sale.order', 'Order Reference', required=False, ondelete='cascade', select=True, readonly=True)
    name = fields.Text('Description', required=True, readonly=False)
    sequence = fields.Integer('Sequence', help="Gives the sequence order when displaying a list of sales order lines.", default=10)
    product_id = fields.Many2one('product.product', 'Product', domain=[('sale_ok','=',True),('bom_ids','!=',False),('bom_ids.type','!=','phantom')], readonly=False, ondelete='restrict')
    price_unit = fields.Float('Unit Price', required=True, readonly=False)
    product_uom_qty = fields.Float('Quantity', required=True, readonly=False)
    product_uom = fields.Many2one('product.uom', 'Unit of Measure ', required=True, readonly=False)
    product_uos_qty = fields.Float('Quantity (UoS)', readonly=False)
    product_uos = fields.Many2one('product.uom', 'Product UoS')

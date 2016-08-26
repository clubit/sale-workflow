# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    This module copyright (C) 2015 Clubit BVBA
#    ( http://www.clubit.be).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'sale_fixed_delivery_day',
    'version': '8.0',
    'category': 'Sale',
    'description': """
Fixed delivery day configuration for partners
=============================================

This module adds the possibility to indicate what the fixed delivery day is for
a customer. If configured, this causes the requested delivery date to be
recalculated (via a cron job) for a delivery to alway match this day.

The date is recalculated as long as the state of the delivery <> done or/and
the warehouse_sent attribute (edi module) is empty.
    """,
    'author': 'Clubit BVBA',
    'website': 'http://www.clubit.be',
    'summary': 'Add fixed delivery day logic on delivery orders',
    'sequence': 9,
    'depends': [
        'stock',
        'sale',
        'sale_order_dates',
        'sale_address_chainer',
        'sale_stock',
        'edi_tools',
    ],
    'data': [
        'views/partner_view.xml',
        'views/sale_view.xml',
        'views/stock_view.xml',
        'data/scheduler_data.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'css': [
    ],
    'images': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

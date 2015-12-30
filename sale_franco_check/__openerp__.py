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
    'name': 'sale_franco_check',
    'version': '8.0',
    'category': 'Sale',
    'description': """
        Franco Check for Partner
        ========================

        This module provides a possibility to do a franco check when confirming
        quotations. A franco check consists of the following two elements:

        * Franco Amount defined on the partner.
        * Franco Check on a quotation

        When confirming a group of quotations via the wizard, a franco check is
        performed. This checks that the total of the quotations for a certain
        partner is equal or larger than the franco amount defined on that partner.
        Only when this is the case, the quotations are confirmed for that partner.
    """,
    'author': 'Clubit BVBA',
    'website': 'http://www.clubit.be',
    'summary': 'Franco check for quotations',
    'sequence': 9,
    'depends': [
        'base_setup',
        'sale',
        'sale_stock',
    ],
    'data': [
        'views/partner_view.xml',
        'views/sale_view.xml',
        'wizard/confirm_sale_order_franco.xml',
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

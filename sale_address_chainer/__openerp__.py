# -*- coding: utf-8 -*-
#    Author: Dimitri Verhelst
#    Copyright 2015 Clubit BVBA
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

{'name': 'Sale to Picking and Invoice Address Chainer',
 'summary': 'Copy Sale, Picking and Invoice partner to picking and invoice.',
 'version': '0.1',
 'author': "Clubit BVBA",
 'category': 'Warehouse Management',
 'license': 'AGPL-3',
 'images': [],
 'depends': ['sale_stock'],
 'data': [
     'view/invoice_view.xml',
     'view/stock_view.xml',
 ],
 'auto_install': False,
 'installable': True,
 }

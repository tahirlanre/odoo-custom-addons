# -*- encoding: utf-8 -*-
##############################################################################
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
    'name': 'Purchase Order Cost Price Update',
    'version': '1.0',
    'category': 'Purchase',
    'summary': 'Update product cost price from purchase orders',
    'description': """
	After confirming purchase order and validating invoice, automatically updates product cost price with respective purchase order line unit price
    
    
	""",
    'author': 'Tahir Aduragba',
    'website': '',
    'depends': [   
        'purchase',
    ],
    'data': [
        'views/view.xml'
    ],
    'demo': [
    ],
    'test': [

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

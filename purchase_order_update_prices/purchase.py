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

from openerp.osv import osv, orm
from openerp import SUPERUSER_ID, workflow, models, fields


class purchase_order(orm.Model):
    _inherit = 'purchase.order'
    
    def _update_product_cost_price(self, cr, uid, ids, context=None):
        
        purchase_order_line_obj = self.pool.get('purchase.order.line')
        product_template_obj = self.pool.get('product.template')
        
        ## update product cost with unit price of respective po line 
        current_po = self.browse(cr, uid, ids, context=context)
        for po in current_po:
            for po_line in po.order_line:
                product_tmpl = po_line.product_id.product_tmpl_id
                update_price = po_line.price_unit
                ## check if user chose to update cost price & current cost price is same as po line unit cost (update_price)
                if po_line.update_cost_price and (product_tmpl.standard_price != update_price):
                    vals = {
                        'standard_price' : update_price
                    }
                    product_template_obj.write(cr,uid,[product_tmpl.id],vals,context=context)

class purchase_order_line(models.Model):
    _inherit = 'purchase.order.line'
    
    update_cost_price = fields.Boolean(string="Update Cost Price?", default= True, help="Select to update cost price of product after confirming invoice")
     
class account_invoice(osv.Model):
    _inherit = 'account.invoice'

    def invoice_validate(self, cr, uid, ids, context=None):
        res = super(account_invoice, self).invoice_validate(cr, uid, ids, context=context)
        purchase_order_obj = self.pool.get('purchase.order')
        # read access on purchase.order object is not required
        if not purchase_order_obj.check_access_rights(cr, uid, 'read', raise_exception=False):
            user_id = SUPERUSER_ID
        else:
            user_id = uid
        po_ids = purchase_order_obj.search(cr, user_id, [('invoice_ids', 'in', ids)], context=context)
        for po_id in po_ids:
            purchase_order_obj._update_product_cost_price(cr, user_id, [po_id],context=context)
        return res
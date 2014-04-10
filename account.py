# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import date
from openerp import netsvc

class account_move_reversal(osv.osv_memory):
    _name = 'account.move.reversal'
    _description = 'Account move reversal wizard'

    def entry_reversal(self, cr, uid, ids, context=None):

	move_ids = context['active_ids']
	if len(move_ids) == 0:
		raise osv.except_osv(_('Error!'), _("You should select at least one move!!!"))
		return {'type': 'ir.actions.act_window_close'}
	move_obj = self.pool.get('account.move')
	move_line_obj = self.pool.get('account.move.line')
        res = self.read(cr,uid,ids,['post_entry','journal_id','period_id'])
        post_entry = res[0]['post_entry']
        journal_id = res[0]['journal_id']
        period_id = res[0]['period_id']

	for move in move_obj.browse(cr,uid,move_ids):
		if move.state == 'posted':
			vals_move = {
				'partner_id': move.partner_id.id,
				'company_id': move.company_id.id,
				'date': str(date.today()),
				# 'journal_id': move.journal_id.id,
				'journal_id': journal_id[0],
				'period_id': period_id[0],
				'name': 'REVERSAL ' + move.name,
				'narration': move.narration,
				'ref': move.ref,
				'state': 'draft',
				'to_check': True,
				}
			move_id = move_obj.create(cr,uid,vals_move)		
			for line in move.line_id:
				vals_line = {
					'account_id': line.account_id.id,
					'account_tax_id': line.account_tax_id.id,
					'amount_currency': line.amount_currency,
					'amount_residual': line.amount_residual,
					'amount_residual_currency': line.amount_residual_currency,
					'analytic_account_id': line.analytic_account_id.id,
					'balance': line.balance,
					'blocked': line.blocked,
					'centralisation': line.centralisation,
					'company_id': line.company_id.id,
					'credit': line.debit,
					'debit': line.credit,
					'invoice': line.invoice.id,
					'move_id': move_id,
					'name': line.name,
					'narration': line.narration,
					'partner_id': line.partner_id.id,
					'product_id': line.product_id.id,
					'product_uom_id': line.product_uom_id.id,
					'quantity': line.quantity,
					'ref': line.ref,
					'state': 'draft',
					'statement_id': line.statement_id.id,
					'tax_amount': line.tax_amount,
					'tax_code_id': line.tax_code_id.id,
					}
				line_id = move_line_obj.create(cr,uid,vals_line)
		if post_entry:
			return_id = move_obj.button_validate(cr,uid,[move_id])

        return {}

    _columns = {
		'journal_id': fields.many2one('account.journal','Journal'),
		'period_id': fields.many2one('account.period','Period'),
		'post_entry': fields.boolean('Post Entries Automatically')
		}

    _defaults = {
		'post_entry': False,
		}

account_move_reversal()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


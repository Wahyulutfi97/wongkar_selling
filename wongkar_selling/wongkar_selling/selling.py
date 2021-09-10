# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from datetime import date
import datetime


@frappe.whitelist()
def get_disc(item_code,dp,tenor):
	# frappe.msgprint("masuk fungsi")
	data = frappe.db.get_list('Rule',filters={'item_code': item_code},fields=['*'])
	harga = frappe.get_value("Item Price",{"item_code": item_code}, "price_list_rate")
	nominal = float(harga)
	frappe.msgprint(str(data))
	disc=[]
	today = date.today()
	dm = 0.0
	dl = 0.0
	dd = 0.0
	dd = 0.0
	dmd = 0.0
	bs = 0.0
	bb = 0.0
	bg = 0.0
	cbj = ""
	cbb = ""
	cbg = ""

	for i in data:
		# amount
		if i ['discount'] == 'Amount':
			if i['type'] == 'Manufacture':
				if i['valid_from'] <= today and i['valid_to'] >= today:
					frappe.msgprint("benar")
					dm = i['amount']
			if i['type'] == 'Leasing':
				if i['valid_from'] <= today and i['valid_to'] >= today and i['besar_dp'] == dp and i['tenor'] == tenor:
					dl = i['amount']
			if i['type'] == 'Dealer':
				if i['valid_from'] <= today and i['valid_to'] >= today:
					dd = i['amount']
			if i['type'] == 'Main Dealer':
				if i['valid_from'] <= today and i['valid_to'] >= today:
					dmd = i['amount']

		# Percent
		if i ['discount'] == 'Percent':
			if i['type'] == 'Manufacture':
				if i['valid_from'] <= today and i['valid_to'] >= today:
					frappe.msgprint("benar")
					dm = i['percent'] * nominal / 100
			if i['type'] == 'Leasing':
				if i['valid_from'] <= today and i['valid_to'] >= today and i['besar_dp'] == dp and i['tenor'] == tenor:
					frappe.msgprint("percent"+str(i['percent']))
					dl = i['percent'] * nominal / 100
			if i['type'] == 'Dealer':
				if i['valid_from'] <= today and i['valid_to'] >= today:
					dd = i['percent'] * nominal / 100
			if i['type'] == 'Main Dealer':
				if i['valid_from'] <= today and i['valid_to'] >= today:
					dmd = i['percent'] * nominal / 100
		# Biaya
		if i['discount'] == "":
			if i['type'] == 'Biaya Penjualan Kendaraan':
				if i['valid_from'] <= today and i['valid_to'] >= today:
					biaya = frappe.db.get_list('Daftar Biaya',filters={'parent': i['name']},fields=['*'])
					for j in biaya:
						if j['jenis_biaya'] == 'BPKB':
							bs = j['nominal']
							cbj = j['coa']
						if j['jenis_biaya'] == 'STNK':
							bb = j['nominal']
							cbb = j['coa']
						if j['jenis_biaya'] == 'Gift':
							bg = j['nominal']
							cbg = j['coa']


	return dm,dd,dmd,dl,bs,bb,bg,harga,cbj,cbb,cbg
	# dl = frappe.get_value("Rule",{"item_code": item_code,"type": "Leasing"}, "amount")

@frappe.whitelist()
def buat_gl(doc,method):
	if doc.type_penjualan == "Penjualan Motor":
		data = frappe.db.get_list('Rule',filters={'item_code': doc.item_code},fields=['*'])
		cost_center = frappe.get_value("Sales Invoice Item",{"parent": doc.name}, "cost_center")
		for i in data:
			if i ['discount'] == 'Amount':
				if i['type'] == 'Manufacture':
					buat_gl2(i['coa_receivable'],i['amount'],0,i['amount'],0,doc.customer,doc.name,cost_center,doc.due_date) # debit
					buat_gl2(i['coa_expense'],0,i['amount'],0,i['amount'],doc.customer,doc.name,cost_center,doc.due_date) # kredit
				if i['type'] == 'Main Dealer':
					buat_gl2(i['coa_receivable'],i['amount'],0,i['amount'],0,doc.customer,doc.name,cost_center,doc.due_date) # debit
					buat_gl2(i['coa_expense'],0,i['amount'],0,i['amount'],doc.customer,doc.name,cost_center,doc.due_date) # kredit
				if i['type'] == 'Leasing' and i['besar_dp'] == doc.dp and i['tenor'] == doc.tenor:
					buat_gl2(i['coa_receivable'],i['amount'],0,i['amount'],0,doc.customer,doc.name,cost_center,doc.due_date) # debit
					buat_gl2(i['coa_expense'],0,i['amount'],0,i['amount'],doc.customer,doc.name,cost_center,doc.due_date) # kredit
				if i['type'] == 'Dealer':
					buat_gl2(i['coa_cash'],i['amount'],0,i['amount'],0,doc.customer,doc.name,cost_center,doc.due_date) # debit
					buat_gl2(i['coa_discount'],0,i['amount'],0,i['amount'],doc.customer,doc.name,cost_center,doc.due_date) # kredit
			
			if i ['discount'] == 'Percent':
				if i['type'] == 'Manufacture':
					buat_gl2(i['coa_receivable'],doc.discount_manufacture,0,doc.discount_manufacture,0,doc.customer,doc.name,cost_center,doc.due_date) # debit
					buat_gl2(i['coa_expense'],0,doc.discount_manufacture,0,doc.discount_manufacture,doc.customer,doc.name,cost_center,doc.due_date) # kredit
				if i['type'] == 'Main Dealer':
					buat_gl2(i['coa_receivable'],doc.discount_main_dealer,0,doc.discount_main_dealer,0,doc.customer,doc.name,cost_center,doc.due_date) # debit
					buat_gl2(i['coa_expense'],0,doc.discount_main_dealer,0,doc.discount_main_dealer,doc.customer,doc.name,cost_center,doc.due_date) # kredit
				if i['type'] == 'Leasing' and i['besar_dp'] == doc.dp and i['tenor'] == doc.tenor:
					buat_gl2(i['coa_receivable'],doc.leasing,0,doc.leasing,0,doc.customer,doc.name,cost_center,doc.due_date) # debit
					buat_gl2(i['coa_expense'],0,doc.leasing,0,doc.leasing,doc.customer,doc.name,cost_center,doc.due_date) # kredit
				if i['type'] == 'Dealer':
					buat_gl2(i['coa_cash'],doc.discount_dealer,0,doc.discount_dealer,0,doc.customer,doc.name,cost_center,doc.due_date) # debit
					buat_gl2(i['coa_discount'],0,doc.discount_dealer,0,doc.discount_dealer,doc.customer,doc.name,cost_center,doc.due_date) # kredit
		
@frappe.whitelist()
def buat_gl2(akun,debit,kredit,debitcr,kreditcr,customer,name,cost_center,due_date):	
	mydate= datetime.date.today()
	docgl = frappe.new_doc('GL Entry')
	docgl.posting_date = date.today()
	docgl.party_type = "Customer"
	docgl.party = customer
	docgl.account = akun
	docgl.cost_center = cost_center
	docgl.debit = debit
	docgl.credit = kredit
	docgl.debit_in_account_currency = debitcr
	docgl.credit_in_account_currency = kreditcr
	docgl.against = "4110.000 - Penjualan - DAS"
	docgl.against_voucher_type = "Sales Invoice"
	docgl.against_voucher = name
	docgl.voucher_type = "Sales Invoice"
	docgl.voucher_no = name
	docgl.remarks = "No Remarks"
	docgl.is_opening = "No"
	docgl.is_advance = "No"
	# docgl.company = "DAS"
	docgl.fiscal_year = mydate.year
	docgl.due_date = due_date
	docgl.docstatus = 1
	docgl.flags.ignore_permission = True
	docgl.save()
	frappe.msgprint("buat GL akun berhasil !")


# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from datetime import date


@frappe.whitelist()
def get_disc(item_code,price):
	# frappe.msgprint("masuk fungsi")
	nominal = float(price)
	data = frappe.db.get_list('Rule',filters={'item_code': item_code},fields=['*'])
	harga = frappe.get_value("Item Price",{"item_code": item_code}, "price_list_rate")
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
				if i['valid_from'] <= today and i['valid_to'] >= today:
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
				if i['valid_from'] <= today and i['valid_to'] >= today:
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

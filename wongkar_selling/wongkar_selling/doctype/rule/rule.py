# -*- coding: utf-8 -*-
# Copyright (c) 2021, Wongkar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Rule(Document):
	def validate(self):
		frappe.msgprint("after_insert")
		# manufacture = frappe.get_value("Rule",{"item_code": self.item_code,"type": "Manufacture"}, "item_code")
		# if manufacture:
		# 	frappe.throw("Disconut Manufature Item "+manufacture+" sudah ada !")
		
		# dealer = frappe.get_value("Rule",{"item_code": self.item_code,"type": "Dealer"}, "item_code")
		# if dealer:
		# 	frappe.throw("Disconut Dealer Item "+dealer+" sudah ada !")

		# main_dealer = frappe.get_value("Rule",{"item_code": self.item_code,"type": "Main Dealer"}, "item_code")
		# if main_dealer:
		# 	frappe.throw("Disconut Main Dealer Item "+main_dealer+" sudah ada !")

		leasing = frappe.db.get_value("Rule",{"item_code": self.item_code, "besar_dp" : self.besar_dp, "tenor": self.tenor}, "item_code")
		if leasing:
			frappe.throw("Disconut Item "+leasing+" sudah ada !")
		
		if self.type == "Leasing" and self.besar_dp == "":
			frappe.throw("Masukkan besad DP !")
		if self.type == "Leasing" and self.tenor == "":
			frappe.throw("Masukkan besad Tenor !")

		# biaya_penjualan_kendaraan = frappe.get_value("Rule",{"item_code": self.item_code,"type": "Biaya Penjualan Kendaraan"}, "item_code")
		# if biaya_penjualan_kendaraan:
		# 	frappe.throw("Disconut Biaya Penjualan Kendaraan Item "+biaya_penjualan_kendaraan+" sudah ada !")

		


from rent_gen import RentalReceipt
import datetime

#Single copy mode
pars = {"medium":"Interac e-transfer",
	"amount":"XXX ZZZ",
	"tenantname":"Mr. Spam Egg",
	"address":"Spam egg ave., spammer street, Egg - 123123",
	"landlordname":" Mr. Egg Spam"}
receipts = RentalReceipt(pars,"rental_receipt_single_copy_example.tex",mode='single_copy')
receipts.gen_receipt(datetime.date(2019,1,1),3)
receipts.params["amount"] = "YYY ZZZ"
receipts.gen_receipt(datetime.date(2019,12,1),3)
receipts.write_file()


#Dual copy mode
pars = {"medium":"Interac e-transfer",
	"amount":"XXX ZZZ",
	"tenantname":"Mr. Spam Egg",
	"address":"Spam egg ave., spammer street, Egg - 123123",
	"landlordname":" Mr. Egg Spam"}
receipts = RentalReceipt(pars,"rental_receipt_dual_copy_example.tex",mode='dual_copy')
receipts.gen_receipt(datetime.date(2019,1,1),3)
receipts.params["amount"] = "YYY ZZZ"
receipts.gen_receipt(datetime.date(2019,12,1),3)
receipts.write_file()

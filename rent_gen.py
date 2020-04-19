#Generate rental receipts from the latex template files
#Requires pdflatex and pdfnup in path
#
#author: m.sainathgupta@gmail.com

import pprint
import os
import time
import datetime
from dateutil.relativedelta import relativedelta

mode_map = {'single_copy'	: os.path.dirname(__file__)+'/latex_templates/rental_receipt_single_copy_template.tex',
			'dual_copy'		: os.path.dirname(__file__)+'/latex_templates/rental_receipt_2_copies_template.tex'}

page_stack_map = {'single_copy'	: '1x4',
				  'dual_copy'	: '1x2'}


class RentalReceipt(object):
    def __init__(self,params,output_file,mode='single_copy'):
        self.params = params
        self.mode = mode
        template_file = mode_map[mode]
        #initialize the template
        template = open(template_file,"r").read()
        self.template = {}
        for i in ["top","repeat","join_alternate","join","bottom"]:
            self.template[i] = template.split("%%template_"+i+"_start%%")[1].split("%%template_"+i+"_end%%")[0]
        os.makedirs("tempfiles",exist_ok=True)
        self.output_filename = "tempfiles/"+output_file
        self.output_file = open(self.output_filename,"w")
        self.output_file.write(self.template["top"])
        self.page_count = 0
        
    def gen_receipt(self,from_month,numofmonths):
        for mon in range(numofmonths):
            curmon = from_month+relativedelta(months=mon)
            self.params["receiptdate"] = curmon.strftime("%B %d %Y")
            self.params["paymentfor"] = curmon.strftime("Rent %B %Y")
            self.output_file.write(self.template["repeat"] % self.params)
            if self.page_count%2 == 0:
                self.output_file.write(self.template["join_alternate"])
            else:
                self.output_file.write(self.template["join"])
            self.page_count+=1
            
    def write_file(self):
        self.output_file.write(self.template["bottom"])
        self.output_file.close()
        os.system("pdflatex -output-directory tempfiles "+self.output_filename)
        os.system("pdflatex -output-directory tempfiles "+self.output_filename)
        filename = self.output_filename.split(".tex")[0]
        pdfnup_cmd = "pdfnup --nup {0} --no-landscape {1}.pdf -o {2}.pdf" 
        os.system(pdfnup_cmd.format(page_stack_map[self.mode],filename,filename.split("/")[1]))
        

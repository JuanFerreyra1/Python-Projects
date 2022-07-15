import codecs
import re

class Converter_to_csv:
	def __init__(self,inp_file_route,out_file_route,delimiter):
		self.input_file_route = inp_file_route
		self.output_file_route = out_file_route
		self.delimiter = delimiter

	def columns_size(self,cursor):
		self.number_of_columns = len(cursor.readline().split('\t'))
		cursor.seek(0)

	def line_cleaning(self,line):
		line = line.split("\t")
		new_content = str()
		for x in range(0,self.number_of_columns):
			add_content = line[x].rstrip().lstrip()
			if x != self.number_of_columns-1:
				new_content = new_content + add_content +self.delimiter
			else: 
				new_content = new_content + add_content
	
		return new_content

	def transformation(self):
		with codecs.open(self.input_file_route,"r",encoding='utf-16-le') as tsv_file:
			with codecs.open(self.output_file_route,"w",encoding="utf-8") as target_file:
				self.columns_size(tsv_file)
				self.row = str()
				for line in tsv_file:
					if len(line.rstrip().split('\t')) == self.number_of_columns:
						new_line = self.line_cleaning(line)
						target_file.write(new_line+'\n')

					else:
						self.row = self.row + line
						self.row = self.row.rstrip()

					if len(self.row.split("\t")) == self.number_of_columns:
						new_line_fixed = self.line_cleaning(self.row)
						target_file.write(new_line_fixed+'\n')
						self.row = str()

Operation = Converter_to_csv("C:\Pruebas2/datos_data_engineer.tsv","C:\Pruebas2/nuevo.csv",'|').transformation()


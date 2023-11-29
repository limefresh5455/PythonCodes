import os
import webbrowser
import fitz  # PyMuPDF
import pandas as pd

def extract_text_from_pdf(pdf_path):
	# setting up all column names as empty
	column_names = [
	"stage_cd", "route_cd", "dsp_cd", "van_type", "station_cd",	"route_dt", "cycle_cd", "loadout_tm", "bags_tot", "bag_line_no",
	"bag_sort_zn", "bag_id",'bag_pkgs', "overflow_tot", "overflow_line_no",	"overflow_sort_zn", "overflow_pkgs", "packages_tot", "commercial_packages_tot"]
	empty_list = [[] for _ in range(len(column_names))]
	stage_cd, route_cd, dsp_cd, van_type, station_cd, route_dt, cycle_cd, loadout_tm, bags_tot, bag_line_no, bag_sort_zn, bag_id,bag_pkgs, overflow_tot, overflow_line_no,overflow_sort_zn, overflow_pkgs, packages_tot, commercial_packages_tot = empty_list

	try:
		pdf_document = fitz.open(pdf_path)
	except FileNotFoundError:
		print('File not found')

	# for page_number in range(pdf_document.page_count-1):
	for page_number in range(pdf_document.page_count):
		page = pdf_document[page_number]
		#page = pdf_document[pdf_document.page_count-2]

		table = page.get_text("blocks")
		# Adding exception
		try:
			# page_data = [x[-3] for x in table]
			page_data = [x[-3] for x in table]
			# print(page_data)
			#return page_data
		except Exception:
			print('some Exception')
			continue

		if len(page_data) == 0:
			print('blank'*33)
			continue
		# setting up empty tables per page
		bag_table = []
		overflow_table = []

		overflow_index = next((i for i, line in enumerate(page_data) if 'over' in line), None)
		# print('overflow_index is ',overflow_index)

		# Confirming stage_cd value as a first read
		if page_data[0].count('.') != 2:
			page_data.insert(0,'')

		# getting table data
		try:
			bag_unordered_table = page_data[page_data.index('Sort Zone\nBag\nPkgs\n')+1:overflow_index]
			overflow_unordered_table = page_data[overflow_index+2:-1]
		except Exception as e:
			print('line 68 Exception')
			# Adding condition to not include last empty page of the file
			if int(pdf_document.page_count) == int(page_number+1):
				continue
			else:
				print('File format is not matching on page')
				return

		# Handling missing values
		for i in bag_unordered_table:
			data_liss = i.strip().split('\n')
			if len(data_liss)<4:
				data_liss.insert(1,'')
			bag_table.append(data_liss)

		for i in overflow_unordered_table:
			data_liss = i.strip().split('\n')
			# handling missing value if any
			if len(data_liss)<3:
				data_liss.insert(1,'')
			overflow_table.append(data_liss)

		#defining all columns values of the page here
		stage_cd_value = page_data[0].strip()
		route_cd_value = page_data[1].strip()
		route_dt_value = page_data[3].split('·')[1].strip()
		cycle_cd_value = page_data[3].split('·')[2].strip()
		station_cd_value = page_data[3].split('·')[0].strip()
		van_type_value = page_data[2].split('·')[1].strip()
		dsp_cd_value = page_data[2].split('·')[0].strip()
		if len(page_data[3].split('·')) == 3:
			loadout_tm_value = ''
		else:
			loadout_tm_value =  page_data[3].split('·')[3].strip()
		total_v = page_data[-1].split('\n')
		if 'Total Packages' in total_v:
			t_value = total_v[total_v.index('Total Packages')+1]
		else:
			t_value = ''

		if 'Commercial Packages' in total_v:
			c_value = total_v[total_v.index('Commercial Packages')+1]
		else:
			c_value = ''
			

		# try:
		for bag in bag_table:
			bag_line_no.append(bag[0])
			bag_sort_zn.append(bag[1])
			bag_id.append(bag[2])
			bag_pkgs.append(bag[3])
			bags_tot.append(page_data[4].split(' ')[0].strip())

			# setting up empty values for overflow table data
			overflow_tot.append('')
			overflow_line_no.append('')
			overflow_sort_zn.append('')
			overflow_pkgs.append('')

			# route_cd.append(page_data[1].strip())
			# appending common values
			stage_cd.append(stage_cd_value)
			route_cd.append(route_cd_value)
			dsp_cd.append(dsp_cd_value)
			van_type.append(van_type_value)
			station_cd.append(station_cd_value)
			route_dt.append(route_dt_value)
			cycle_cd.append(cycle_cd_value)
			loadout_tm.append(loadout_tm_value)
			packages_tot.append(t_value)
			commercial_packages_tot.append(c_value)


		for o_bag in overflow_table:
			# adding empty values for bag table
			bag_line_no.append('')
			bag_sort_zn .append('')
			bag_id .append('')
			bag_pkgs.append('')
			bags_tot.append('')
			# overflow_tot.append(o_bag)

			if overflow_index is not None:
				overflow_value = page_data[overflow_index].split(' ')[0]
				overflow_tot.append(overflow_value)
			else:
				overflow_tot.append('0')

			overflow_line_no.append(o_bag[0])
			overflow_sort_zn.append(o_bag[1])
			overflow_pkgs.append(o_bag[2])

			# appending common values
			stage_cd.append(stage_cd_value)
			route_cd.append(route_cd_value)
			dsp_cd.append(dsp_cd_value)
			van_type.append(van_type_value)
			station_cd.append(station_cd_value)
			route_dt.append(route_dt_value)
			cycle_cd.append(cycle_cd_value)
			loadout_tm.append(loadout_tm_value)
			packages_tot.append(t_value)
			commercial_packages_tot.append(c_value)

	pdf_document.close()
	data = {'stage_cd': stage_cd,'route_cd':route_cd,'dsp_cd':dsp_cd,'van_type':van_type,'station_cd':station_cd,'route_dt':route_dt,'cycle_cd':cycle_cd,'loadout_tm':loadout_tm,'bags_tot':bags_tot,'bag_line_no':bag_line_no,'bag_sort_zn':bag_sort_zn,'bag_id':bag_id,'bag_pkgs':bag_pkgs,'overflow_tot':overflow_tot,'overflow_line_no':overflow_line_no,'overflow_sort_zn':overflow_sort_zn,'overflow_pkgs':overflow_pkgs,'packages_tot':packages_tot,'commercial_packages_tot':commercial_packages_tot}
	#creating dataframe with this data

	df = pd.DataFrame(data)
	# csv_filename = f"{pdf_path}.csv"
	xlsx_filename = f"rahul_check.xlsx"
	# xlsx_filename = f"{pdf_path}.xlsx"
	
	# df.to_csv(csv_filename, index=False)  # Save as CSV without index
	df.to_excel(xlsx_filename, index=False)  # Save as XLSX without index
	
	# print(f"CSV and XLSX files saved: {csv_filename}, {xlsx_filename}")
	print(f"XLSX files saved: {xlsx_filename}")
	
	return df



if __name__ == "__main__":
	folder_path = input(r'Enter file or folder name : ')
	if os.path.exists(folder_path):
		if os.path.isfile(folder_path):
			# files =  [os.path.join(folder_path)]
			files = [folder_path]  # Use a list with the single file
		elif os.path.isdir(folder_path):
			# files =  [filename for filename in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, filename))]
			files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, filename))]

	else:
		print('incorrect path, please enter correct path without quotes')

	print("List of files:", files)

	if 'files' in locals():
	# check only for pdf files
		pdfs = [x for x in files if x.endswith('.pdf')]
	for pdf_path in pdfs:
		try:
			print('file name', pdf_path)
			t = extract_text_from_pdf(pdf_path)
		except Exception as e:
			print('line 323')
			print(e)







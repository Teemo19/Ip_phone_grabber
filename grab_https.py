import urllib2
from bs4 import BeautifulSoup
import pandas as pd
arr_ip=[]
arr_model=[]
arr_serial=[]
def grab_phones(cont):
	contents=""
	ip="10.11.1."+cont
	try:
		try:
			contents = urllib2.urlopen("http://10.11.1."+cont,timeout=1).read()
		except:
			contents = urllib2.urlopen("http://10.11.1."+cont,timeout=1).read()
	except:
		try:
			try:
				contents = urllib2.urlopen("https://10.11.1."+cont,timeout=1).read()
			except:
				contents = urllib2.urlopen("https://10.11.1."+cont,timeout=1).read()
		except:
			contents =""
	if(contents!=""):
		soup=BeautifulSoup(contents,'html.parser')
		parse_data(ip,soup)
	else:
		print(ip+" no encontrada")


def parse_data(ip,soup):
	file=open("resultados.txt","r+")
	try:
		raw_arr=[]
		arr=[]
		arr2=[]
		arr_sernum=[]
		raw_arr.append(soup.find_all("td"))
		for i in range(len(raw_arr[0])):
			if("Serial Number" in str(raw_arr[0][i]) or "Serial number" in str(raw_arr[0][i])):
				arr.append(i)
			if("Model Number" in str(raw_arr[0][i]) or "Model number" in str(raw_arr[0][i])):
				arr2.append(i)
		serial_number=arr[len(arr)-1]
		model_number=arr2[len(arr2)-1]
		n_model=model_number+2
		n_serial=serial_number+2
		print(ip)
		print(remove_trash(raw_arr[0][serial_number]))
		print(remove_trash(raw_arr[0][n_serial]))
		print(remove_trash(raw_arr[0][model_number]))
		print(remove_trash(raw_arr[0][n_model]))
		arr_ip.append(ip)
		arr_serial.append(remove_trash(raw_arr[0][n_serial]))
		arr_model.append(remove_trash(raw_arr[0][n_model]))
	except:
		pass

def remove_trash(data):
	r=""
	result=str(data)
	result=result.replace("<td><b>","")
	result=result.replace("</b></td>","")
	if("<strong>"in result):
		result=result.replace("<strong>","")
		result=result.replace("</strong>","")
	if(result[0]==" "):
		for i in range(1,len(result)):
			r+=result[i]
	else:
		r=result
	return r

def main():
	for i in range(1,255):
		grab_phones(str(i))
	df = pd.DataFrame({'IP': arr_ip,'Serial Number':arr_serial,'Model Number':arr_model})
	# Create a Pandas Excel writer using XlsxWriter as the engine.
	writer = pd.ExcelWriter('ip_phone.xlsx', engine='xlsxwriter')
	# Convert the dataframe to an XlsxWriter Excel object.
	df.to_excel(writer, sheet_name='Sheet1')
	worksheet = writer.sheets['Sheet1']
	worksheet.set_column('B:D', 20)
	# Close the Pandas Excel writer and output the Excel file.
	writer.save()
main()

import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2.extensions import AsIs

DB_URL = '<url>'

base = psycopg2.connect(DB_URL, sslmode='require')
if base:
	print('database succesfully connected')
	print('start writing data in database')
cur = base.cursor()

def add_data():
	global base,cur
	cur.execute('INSERT INTO nissan VALUES')

url = 'https://www.auto-data.net/en/nissan-brand-4'
response = requests.get(url)
soup = BeautifulSoup(response.text,'lxml')
data = soup.find('ul', class_='modelite')
model = data.find_all('a',class_='modeli')
# print(model)

count = 0
age = [19,20]


for i in model:
	link_ = 'https://www.auto-data.net' + i.get('href')
	link_response = requests.get(link_)
	link_soup = BeautifulSoup(link_response.text,'lxml')
	data_link = link_soup.find('table',class_='generr')
	model_link = data_link.find_all('a')
	for i in model_link:
		if i is None:
			continue
		else:	 
			link_2 = 'https://www.auto-data.net' + i.get('href')
			link_2response = requests.get(link_2)
			link_2soup = BeautifulSoup(link_2response.text,'lxml')
			data_link2 = link_2soup.find('table', class_='carlist')
			try:
				model_link2 = data_link2.find_all('a')
			except:
				continue			
			for i in model_link2:
				link_3 = 'https://www.auto-data.net' + i.get('href')
				link_3response = requests.get(link_3)
				link_3soup = BeautifulSoup(link_3response.text,'lxml')
				img_link = link_3soup.find('div',class_='float336 left top')
				try:
					images_src = img_link.find('img')
					imge = 'https://www.auto-data.net' + images_src.get('src')
				except AttributeError:
					pass				
				data_link3 = link_3soup.find('table',class_='cardetailsout car2')
				tags = data_link3.find_all('tr')
				for i in tags:
					th_tag = i.find('th')
					td_tag = i.find('td')
					try:
						i.select_one('span',class_='val2').decompose()
					except AttributeError:
						pass	
					if "Generation" in th_tag.text:
						generation_1 = str(i.find('a').text.strip())
						generation_ = generation_1.replace('(','')
						generation = AsIs(generation_.replace(')',''))
					elif 'Modification' in th_tag.text:
						engine_ = td_tag.text.strip()
					elif 'Start of production' in th_tag.text:
					 	start_age = td_tag.text.strip()
					elif 'End of production' in th_tag.text:
					 	end_age = td_tag.text.strip()
					elif 'Body' in th_tag.text:
					 	vehicle_type = td_tag.text.strip()
					elif 'Fuel Type' in th_tag.text:
					 	fuel_type = td_tag.text.strip()
					elif 'Acceleration 0 - 100 km/h' in th_tag.text:
						speedto100 = td_tag.text.strip()		
					elif "Maximum speed" in th_tag.text:
					 	maxspeed = td_tag.text.strip()
					elif "Power" == th_tag.text.strip():
						power = td_tag.text.strip()
					elif "Drive wheel" in th_tag.text:
						drive_wheel = td_tag.text.strip()
						name = AsIs('name_car')
						a = f"INSERT INTO nissan({name},age_start,class,engine,time_speed,max_speed,power_engine,type_engine,drive_unit,age_end,img_url) VALUES('{generation}','{start_age}','{vehicle_type}','{engine_}','{speedto100}','{maxspeed}','{power}','{fuel_type}','{drive_wheel}','{end_age}','{imge}');"	
						try:
							cur.execute(a)							
						except psycopg2.errors.UniqueViolation:
							pass	
						base.commit()
					else:
						continue		



		


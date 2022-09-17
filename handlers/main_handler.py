from aiogram import types,Dispatcher
from create import dp,bot
from aiogram.utils.markdown import text,code
from aiogram.types import ParseMode
from fuzzywuzzy import process
import psycopg2
from psycopg2.extensions import AsIs
from googletrans import Translator

DB_URL = '<url>'
base = psycopg2.connect(DB_URL, sslmode='require')
if base:
	print('database succesfully connected')
	print('start writing data in database')
cur = base.cursor()

ts = Translator()

async def start_command(message : types.Message):
	name_user = text(code(message.from_user.first_name))
	nissan_silvias15 = text(code('Nissan silvia s15'))
	await message.answer(f'Привет {name_user}!\nЯ могу предоставить вам информацию о любом авто!\nПросто введите: <марка> <модель>\nНапример: {nissan_silvias15}',parse_mode=ParseMode.MARKDOWN)

async def nissan(message : types.Message):
	global cur
	await message.reply('Одну секундочку...')
	car = str(message.text.lower())
	model = car.replace('nissan ', '')
	cur.execute('SELECT name_car FROM nissan')
	gen_list = cur.fetchall()
	gen_fuzz = process.extractOne(model, gen_list)
	gen_ = gen_fuzz[0]
	gen_replace_1 = str(gen_).replace("('","")
	gen_replace_2 = gen_replace_1.replace("',)","")
	generation = str(gen_replace_2)
	mark = 'Nissan'
	###
	cur.execute('SELECT age_start FROM nissan WHERE %s=%s',(AsIs('name_car'),generation))
	start_production = cur.fetchone()
	cur.execute('SELECT class FROM nissan WHERE %s=%s',(AsIs('name_car'),generation))
	type_translate = cur.fetchone()
	type_ = type_translate[0]
	car_type = ts.translate(type_,src='en',dest='ru')
	cur.execute('SELECT engine FROM nissan WHERE %s=%s',(AsIs('name_car'),generation))
	engine_tuple = cur.fetchone()
	engine_car = engine_tuple[0].replace('Hp','Л.с')
	cur.execute('SELECT time_speed FROM nissan WHere %s=%s',(AsIs('name_car'),generation))
	timeto100 = cur.fetchone()
	cur.execute('SELECT max_speed FROM nissan WHERE %s=%s',(AsIs('name_car'),generation))
	maxspeed = cur.fetchone()
	cur.execute('SELECT power_engine FROM nissan WHERE %s=%s',(AsIs('name_car'),generation))
	power_tuple = cur.fetchone()
	power = power_tuple[0].replace('Hp','Л.с')
	cur.execute('SELECT type_engine FROM nissan WHERE %s=%s',(AsIs('name_car'),generation))
	type_tuple = cur.fetchone()
	type_ = type_tuple[0]
	type_replace_1 = str(type_).replace("('","")
	type_replace_2 = type_replace_1.replace("',)","")
	type_2 = str(type_replace_2)
	cur.execute('SELECT drive_unit FROM nissan WHERE %s=%s',(AsIs('name_car'),generation))
	unit_tuple = cur.fetchone()
	unit_ = unit_tuple[0]	
	unit_ts = ts.translate(unit_,src='en',dest='ru')
	cur.execute('SELECT age_end FROM nissan WHERE %s=%s',(AsIs('name_car'),generation))
	end_production = cur.fetchone()
	cur.execute('SELECT img_url FROM nissan WHERE %s=%s',(AsIs('name_car'),generation))
	img = cur.fetchone()
	await bot.send_photo(message.from_user.id,photo=img[0])
	await bot.send_message(message.from_user.id,f'Марка - Nissan\nМодель - {generation}\nТип - {car_type.text}\nНачало производства - {start_production[0]}\nЗакончилось производство - {end_production[0]}\nДвигатель - {engine_car}\nТип топлива - {type_2}\nМощность двигателя - {power}\nВремя разгона до 100 Км/ч - {timeto100[0]}\nМаксимальная скорость - {maxspeed[0]}\nПривод - {unit_ts.text}')




def register_message_main():
	dp.register_message_handler(start_command,commands=['start'])
	dp.register_message_handler(nissan, lambda message : message.text.lower().startswith('nissan'))
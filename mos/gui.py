from tkinter import *
from tkinter.font import *
from PIL import Image, ImageTk
import BTgui_17
import bfs
import time
import csv
import threading
import sys

"""
communication = BTgui_17.interface()
bt_process = None
def receive():
	while True:
		print("start to receive")
		word = communication.get_response()

		if word == 'b':
			print("need to send")
			send()
			print("send complete")
		else:
			continue
def process():
	global bt_process
	bt_process = threading.Thread(target=receive)
	bt_process.daemon = True
	bt_process.start()

process()
"""

window = Tk()
window.title("老司機送餐系統")
window.resizable(False, False)


def center_window(window, width, height):
    window.update() 
    screenwidth, screenheight = window.maxsize()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2-10, (screenheight - height)/2-30)
    window.geometry(size)

center_window(window, 1500, 750)
window.config(bg="sienna1")


seats = bfs.Map("map/map.csv")
counter_num = 6


label_font = Font(family="UD Digi Kyokasho N-B", size=30)
choose_font = Font(family="UD Digi Kyokasho N-B", size=20)
dish_font = Font(family="Yu Gothic UI Semibold", size=15)
button_font = Font(family="Yu Gothic UI Semibold", size=10)
info_font = Font(family="UD Digi Kyokasho N-B", size=20)
ask_font = Font(family="Yu Gothic UI Semibold", size=15)
table_font = Font(family="Yu Gothic UI Semibold", size=18)

logo_temp = Image.open("pic/logo.jpg")
logo_temp = logo_temp.resize((250, 150), Image.ANTIALIAS)
logo_pic = ImageTk.PhotoImage(logo_temp)

dish_name = ["套餐A", "套餐B", "套餐C", "哞哞堡", "小豬多P堡", "香吉堡"]
dish = dict()
drink_name = ["老司機特調", "可樂", "雪碧", "檸檬紅茶", "神秘液體", "初戀的滋味", "愛如潮水"]
drink = dict()

up_temp = Image.open("pic/up.jpg")
up_temp = up_temp.resize((24, 24), Image.ANTIALIAS)
up_pic = ImageTk.PhotoImage(up_temp)

down_temp = Image.open("pic/down.jpg")
down_temp = down_temp.resize((24, 24), Image.ANTIALIAS)
down_pic = ImageTk.PhotoImage(down_temp)

table_temp = Image.open("pic/桌號.png")
table_temp = table_temp.resize((151, 170), Image.ANTIALIAS)
table_pic = ImageTk.PhotoImage(table_temp)

hamburger_temp = Image.open("pic/hbg.jpg")
hamburger_temp = hamburger_temp.resize((100, 100), Image.ANTIALIAS)
hamburger_pic = ImageTk.PhotoImage(hamburger_temp)

car_temp = Image.open("pic/快上車.jpg")
car_temp = car_temp.resize((430, 170), Image.ANTIALIAS)
car_pic = ImageTk.PhotoImage(car_temp)

carcar_temp = Image.open("pic/carcar.jpg")
carcar_temp = carcar_temp.resize((430, 170), Image.ANTIALIAS)
carcar_pic = ImageTk.PhotoImage(carcar_temp)

ji_temp = Image.open("pic/雞.jpg")
ji_temp = ji_temp.resize((230, 160), Image.ANTIALIAS)
ji_pic = ImageTk.PhotoImage(ji_temp)

water_temp = Image.open("pic/water.jpg")
water_temp = water_temp.resize((230, 160), Image.ANTIALIAS)
water_pic = ImageTk.PhotoImage(water_temp)

class Dish():
	pos = 20
	total = 0
	order = 0
	def __init__(self, name):
		self.name = name
		self.num = 0
		self.label = Label(choose, text=self.name, font=dish_font, bg="goldenrod1", fg="brown1")
		self.count = Button(choose, width=2, height=1, text=self.num, font=button_font, bg="mint cream", fg="Blue", pady=1, state='disabled')
		self.down = Button(choose, image=down_pic, bg="mint cream", command=self.minus, state='disabled')
		self.up = Button(choose, image=up_pic, bg="mint cream", command=self.plus)
		self.zero = Button(choose, text="R", width=2, font=button_font, bg="mint cream", command=self.reset)
		self.label.place(x=30, y=Dish.pos-4)
		self.count.place(x=135, y=Dish.pos)
		self.up.place(x=175, y=Dish.pos)
		self.down.place(x=215, y=Dish.pos)
		self.zero.place(x=255, y=Dish.pos)
		Dish.pos += 35
		Dish.total += 1

	def plus(self):
		self.num += 1
		Dish.order += 1
		self.count.config(text=self.num)
		self.down.config(state='normal')
		nothing.up.config(state="disabled")
		nothing.down.config(state="disabled")
		nothing.zero.config(state="disabled")
	def minus(self):
		self.num -= 1
		Dish.order -= 1
		self.count.config(text=self.num)
		if self.num == 0:
			self.down.config(state="disabled")
		if (Drink.order+Dish.order) == 0:
			nothing.up.config(state="normal")
			nothing.down.config(state="disabled")
			nothing.zero.config(state="normal")
	def reset(self):
		Dish.order -= self.num
		self.num = 0
		self.count.config(text=self.num)
		self.down.config(state="disabled")
		if (Drink.order+Dish.order) == 0:
			nothing.up.config(state="normal")
			nothing.down.config(state="disabled")
			nothing.zero.config(state="normal")

class Drink():
	pos = 20
	total = 0
	order = 0
	def __init__(self, name):
		self.name = name
		self.num = 0
		self.label = Label(choose, text=self.name, font=dish_font, bg="goldenrod1", fg="brown1")
		self.count = Button(choose, width=2, height=1, text=self.num, font=button_font, bg="mint cream", fg="Blue", pady=1, state='disabled')
		self.down = Button(choose, image=down_pic, bg="mint cream", command=self.minus, state='disabled')
		self.up = Button(choose, image=up_pic, bg="mint cream", command=self.plus)
		self.zero = Button(choose, text="R", width=2, font=button_font, bg="mint cream", command=self.reset)
		self.label.place(x=350, y=Drink.pos-4)
		self.count.place(x=470, y=Drink.pos)
		self.up.place(x=510, y=Drink.pos)
		self.down.place(x=550, y=Drink.pos)
		self.zero.place(x=590, y=Drink.pos)
		Drink.pos += 35
		Drink.total += 1

	def plus(self):
		self.num += 1
		Drink.order += 1
		self.count.config(text=self.num)
		self.down.config(state='normal')
		nothing.up.config(state="disabled")
		nothing.down.config(state="disabled")
		nothing.zero.config(state="disabled")

	def minus(self):
		self.num -= 1
		Drink.order -= 1
		self.count.config(text=self.num)
		if self.num == 0:
			self.down.config(state="disabled")
		if (Drink.order+Dish.order) == 0:
			nothing.up.config(state="normal")
			nothing.down.config(state="disabled")
			nothing.zero.config(state="normal")
	
	def reset(self):
		Drink.order -= self.num
		self.num = 0
		self.count.config(text=self.num)
		self.down.config(state="disabled")
		if (Drink.order+Dish.order) == 0:
			nothing.up.config(state="normal")
			nothing.down.config(state="disabled")
			nothing.zero.config(state="normal")

class Africa():
	pos = 230
	order = 0
	def __init__(self, name):
		self.name = name
		self.num = 0
		self.label = Label(choose, text=self.name, font=dish_font, bg="goldenrod1", fg="brown1")
		self.count = Button(choose, width=2, height=1, text=self.num, font=button_font, bg="mint cream", fg="Blue", pady=1, state='disabled')
		self.down = Button(choose, image=down_pic, bg="mint cream", command=self.minus, state='disabled')
		self.up = Button(choose, image=up_pic, bg="mint cream", command=self.plus)
		self.zero = Button(choose, text="R", width=2, font=button_font, bg="mint cream", command=self.reset)
		self.label.place(x=30, y=Africa.pos-4)
		self.count.place(x=135, y=Africa.pos)
		self.up.place(x=175, y=Africa.pos)
		self.down.place(x=215, y=Africa.pos)
		self.zero.place(x=255, y=Africa.pos)

	def plus(self):
		self.num += 1
		Africa.order = 100
		self.count.config(text=self.num)
		self.up.config(state="disabled")
		self.down.config(state='normal')
		for ele in dish_name:
			dish[ele].down.config(state="disabled")
			dish[ele].up.config(state="disabled") 
			dish[ele].zero.config(state="disabled") 

		for ele in drink_name:
			drink[ele].down.config(state="disabled")
			drink[ele].up.config(state="disabled")
			drink[ele].zero.config(state="disabled")


	def minus(self):
		self.num -= 1
		Africa.order = 0
		self.count.config(text=self.num)
		self.down.config(state="disabled")
		self.up.config(state="normal")
		for ele in dish_name:
			dish[ele].down.config(state="disabled")
			dish[ele].up.config(state="normal") 
			dish[ele].zero.config(state="normal") 

		for ele in drink_name:
			drink[ele].down.config(state="disabled")
			drink[ele].up.config(state="normal")
			drink[ele].zero.config(state="normal")
		
	def reset(self):
		self.num = 0
		Africa.order = 0
		self.count.config(text=self.num)
		self.down.config(state="disabled")
		self.up.config(state="normal")
		for ele in dish_name:
			dish[ele].down.config(state="disabled")
			dish[ele].up.config(state="normal") 
			dish[ele].zero.config(state="normal") 

		for ele in drink_name:
			drink[ele].down.config(state="disabled")
			drink[ele].up.config(state="normal")
			drink[ele].zero.config(state="normal")

class Table_number():	
	
	number = None
	def __init__(self, num, x, y):
		self.num = num
		self.button = Button(info, text=str(num), font=table_font, width=3, height=1, bd=1, bg="firebrick1", activebackground="DodgerBlue3", padx=1, pady=1, command=self.change)
		self.button.place(x=x, y=y)
	def change(self):
		Table_number.number = self.num
		for i in range(1,6):
			if table_button[i].num == Table_number.number:
				table_button[i].button.config(bg="Yellow", state="disabled")
			else:
				table_button[i].button.config(bg="firebrick1", state="normal")

logo_img = Label(window, image=logo_pic)
logo_img.pack()
welcome = Label(window, text="歡迎光臨老司機！", font=label_font, bg="sienna1", fg="gold")
welcome.pack()

car_img = Label(window, image=car_pic, bd=5, relief="ridge")
car_img.place(x=70, y=20)

carcar_img = Label(window, image=carcar_pic, bd=5, relief="sunken")
carcar_img.place(x=980, y=20)


#Choose your orders
choose = LabelFrame(window, text="請選擇您的餐點", labelanchor=N, width=600, height=500, bg="goldenrod1", bd=10, relief="ridge", fg="brown1", font=choose_font)
choose.pack(padx=30, ipadx=50, side=LEFT)

for ele in dish_name:
	dish[ele] = Dish(ele)
for ele in drink_name:
	drink[ele] = Drink(ele)
nothing = Africa("非洲佳餚")

ji_img = Label(choose, image=ji_pic, bd=3, relief="sunken")
ji_img.place(x=40, y=285)

"""
def sing():

song_img = Button(choose, image=song_pic, bd=3, relief="sunken", command=sing)
song_img.place(x=330, y=295)
"""
water_img = Label(choose, image=water_pic, bd=3, relief="sunken")
water_img.place(x=370, y=285)

#Info
info = LabelFrame(window, text="請確認您的用餐資訊", labelanchor=N, width=500, height=500, bg="tomato1", bd=10, relief="ridge", fg="goldenrod1", font=info_font)
info.pack(padx=30, ipadx=50, side=RIGHT)

ask = Label(info, text="您的用餐桌號", font=ask_font, bg="tomato1", fg="Black")
ask.place(x=40, y=10)

table = Label(info, image=table_pic, bd=2, relief="ridge")
table.place(x=380, y=30)

table_button = dict()

for i in range(1,4):
	table_button[i] = Table_number(i, 70+(i-1)*90, 60)
for i in range(4,6):
	table_button[i] = Table_number(i, 115+(i-4)*90, 140)

#PS.
PS = Label(info, text="備註(有其他需要可在此註明)", font=ask_font, bg="tomato1", fg="Black")
PS.place(x=40, y=220)

var = StringVar()
content = Entry(info, width=70, textvariable=var, bg="white", bd=4, font=button_font)
content.place(x=40, y=260)

valid = True
dish_order = ""
now = ""
date = ""
clock = "" 
PS_word = ""


weight_list, go_path_list, number_list, back_path_list = [], [], [], []

def store():
	global weight_list, go_path_list, number_list, back_path_list, PS_word

	weight_list.append(Dish.order+Drink.order+Africa.order)
	
	path = seats.strategy(counter_num, Table_number.number)
	go_path_list.append(path)

	number_list.append(Table_number.number)

	path = seats.strategy(Table_number.number, counter_num)
	back_path_list.append(path)

	with open("database/mos_data.csv", 'a', newline='') as csvfile:
		writer = csv.writer(csvfile)
		dish_order = ""
		for key, value in dish.items():
			if value.num == 0:
				continue
			else:
				quantity = value.num
				mes = str(quantity)+"×"+ key
				dish_order += (mes+',')
		for key, value in drink.items():
			if value.num == 0:
				continue
			else:
				quantity = value.num
				mes = str(quantity)+"×"+ key
				dish_order += (mes+',')
		if Africa.order != 0:
			dish_order += "非洲佳餚x1,"

		now = time.localtime()
		date = str(now.tm_year)+'/'+str(now.tm_mon)+'/'+str(now.tm_mday)
		clock = str(now.tm_hour) +':'+str(now.tm_min)+':'+str(now.tm_sec).zfill(2)
		PS_word = var.get()
		if Africa.order == 0:
			writer.writerow([date, clock, dish_order[:-1], str(Dish.order+Drink.order), str(Table_number.number), PS_word])
		else:
			writer.writerow([date, clock, dish_order[:-1], "1", str(Table_number.number), PS_word])
def delete():
	global PS_word, var

	if Table_number.number == None or (Dish.order+Drink.order+Africa.order) == 0:
		valid = False
	else:
		valid = True

	if valid:
		store()
		PS_word = var.get()
		logo_img.pack_forget()
		welcome.pack_forget()
		choose.pack_forget()
		info.pack_forget()
		car_img.place_forget()
		carcar_img.place_forget()
		content.destroy()
		finish()

		table_button[Table_number.number].button.config(bg="firebrick1", state="normal")
		Table_number.number = None
		for key in dish:
			dish[key].reset()
		for key in drink:
			drink[key].reset()
		nothing.reset()

	else:
		send_label.config(text="餐點或桌號尚未選擇！")
		send_label.place(x=75, y=350)
		window.update()
		window.after(1500)
		send_label.config(text="點擊送出訂單！")
		send_label.place(x=160, y=350)
		window.update()

def finish():
	thank = Label(window, text="已收到您的訂單，訂單如下：", font=label_font, bg="sienna1", fg="Black")
	thank.place(x=500, y=100)
	allinfo = LabelFrame(window, text="您的訂單", labelanchor=N, width=700, height=480, bg="tomato1", bd=10, relief="ridge", fg="goldenrod1", font=info_font)
	allinfo.place(x=400, y=200)

	left_info = Frame(allinfo, width=350, height=480, bg="tomato2", bd=5, relief="ridge")
	right_info = Frame(allinfo, width=350, height=480, bg="tomato2", bd=5, relief="ridge")
	left_info.pack(side=LEFT, fill=Y, expand=1)
	right_info.pack(side=RIGHT, fill=Y, expand=1)

	order_info = Label(left_info, text="餐點明細", bg='tomato2', fg='black', font=ask_font)
	order_info.place(x=20, y=15)
	order_dict = dict()
	num_dict = dict()
	c = 0
	for key, value in dish.items():
		if value.num == 0:
			continue
		else:
			quantity = str(value.num)
			order_dict[key] = Label(left_info, text=key, bg='tomato2', fg='black', font=ask_font)
			order_dict[key].place(x=20, y=70+30*c)
			num_dict[key] = Label(left_info, text=quantity+"份", bg='tomato2', fg='black', font=ask_font)
			num_dict[key].place(x=180, y=70+30*c)
			c += 1
	for key, value in drink.items():
		if value.num == 0:
			continue
		else:
			quantity = str(value.num)
			order_dict[key] = Label(left_info, text=key, bg='tomato2', fg='black', font=ask_font)
			order_dict[key].place(x=20, y=70+30*c)
			num_dict[key] = Label(left_info, text=quantity+"份", bg='tomato2', fg='black', font=ask_font)
			num_dict[key].place(x=180, y=70+30*c)
			c += 1
	if Africa.order != 0:
		key = "非洲佳餚"
		quantity = "1"
		order_dict[key] = Label(left_info, text=key, bg='tomato2', fg='black', font=ask_font)
		order_dict[key].place(x=20, y=70+30*c)
		num_dict[key] = Label(left_info, text=quantity+"份", bg='tomato2', fg='black', font=ask_font)
		num_dict[key].place(x=180, y=70+30*c)

	table_info = Label(right_info, text="您的用餐桌號", bg='tomato2', fg='black', font=ask_font)
	table_info.place(x=20, y=15)
	table_num_info = Label(right_info, text=str(Table_number.number)+"號桌", bg='tomato2', fg='black', font=ask_font)
	table_num_info.place(x=70, y=80)
	PS_info = Label(right_info, text="您的備註", bg='tomato2', fg='black', font=ask_font)
	PS_info.place(x=20, y=170)
	PS_infoC = Label(right_info, text=PS_word, bg='tomato2', fg='black', font=ask_font, wraplength=240, justify='left')
	PS_infoC.place(x=20, y=220)
	window.update()
	window.after(5000)
	thank.destroy()
	allinfo.destroy()
	set()

def set():
	global var
	logo_img.pack()
	welcome.pack()
	choose.pack(padx=30, ipadx=50, side=LEFT)
	info.pack(padx=30, ipadx=50, side=RIGHT)
	ask.place(x=40, y=10)
	table.place(x=380, y=30)
	car_img.place(x=70, y=20)
	carcar_img.place(x=980, y=20)
	for i in range(1,4):
		table_button[i] = Table_number(i, 70+(i-1)*90, 60)
	for i in range(4,6):
		table_button[i] = Table_number(i, 115+(i-4)*90, 140)
	var = StringVar()
	content = Entry(info, width=70, textvariable=var, bg="white", bd=4, font=button_font)
	content.place(x=40, y=260)

def send():
	global weight_list, go_path_list, number_list, back_path_list
	cc = 0
	
	while len(weight_list) == 0:
		pass
	
	#start to send the message
	communication.start_signal()

	#weight
	communication.send_weight(weight_list.pop(0))
	communication.get_response()

	#path:go
	communication.send_action_go(go_path_list.pop(0))
	communication.get_response()

	#table_number
	communication.send_number(number_list.pop(0))
	communication.get_response()

	#path:back
	communication.send_action_back(back_path_list.pop(0))
	communication.get_response()

#send
send_label = Label(info, text="點擊送出訂單！", font=info_font, bg="tomato1", fg="black")
send_label.place(x=160, y=350)
send_button = Button(info, image=hamburger_pic, bg="honeydew", command=delete)
send_button.place(x=400, y=320)

window.mainloop()

print("ending")
sys.exit()

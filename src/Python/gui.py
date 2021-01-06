from tkinter import *
from tkinter.font import *
from PIL import Image, ImageTk
import BT

window = Tk()

window.title("mos送餐系統")

def center_window(window, width, height):
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2-20)
    window.geometry(size)


center_window(window, 1200, 750)
window.config(bg="gold")

label_font = Font(family="微軟正黑體", size=30)
choose_font = Font(family="微軟正黑體", size=20)
dish_font = Font(family="微軟正黑體", size=15)
button_font = Font(family="微軟正黑體", size=10)
info_font = Font(family="微軟正黑體", size=20)
ask_font = Font(family="微軟正黑體", size=15)
table_font = Font(family="微軟正黑體", size=18)

logo_temp = Image.open("pic/mos_logo.jpg")
logo_temp = logo_temp.resize((100, 100), Image.ANTIALIAS)
logo_pic = ImageTk.PhotoImage(logo_temp)
logo_img = Label(window, image=logo_pic)
logo_img.pack()

welcome = Label(window, text="歡迎光臨摩斯漢堡！", font=label_font, bg="gold", fg="Red")
welcome.pack()

#Choose your orders
choose = LabelFrame(window, text="請選擇您的餐點", labelanchor=N, width=500, height=500, bg="Red", bd=10, relief="ridge", fg="Yellow", font=choose_font)
choose.pack(padx=30, ipadx=50, side=LEFT)

dish_name = ["套餐A", "套餐B", "套餐C", "漢堡A", "漢堡B", "漢堡C"]
dish = dict()


up_temp = Image.open("pic/up.jpg")
up_temp = up_temp.resize((24, 24), Image.ANTIALIAS)
up_pic = ImageTk.PhotoImage(up_temp)

down_temp = Image.open("pic/down.jpg")
down_temp = down_temp.resize((24, 24), Image.ANTIALIAS)
down_pic = ImageTk.PhotoImage(down_temp)

#up_pic = PhotoImage(file="pic/up.gif").subsample(15)
#down_pic = PhotoImage(file="pic/down.gif").subsample(30)

class Dish():
	pos = 40
	total = 0
	def __init__(self, name):
		self.name = name
		self.num = 0
		self.label = Label(choose, text=self.name, font=dish_font, bg="Red", fg="Yellow")
		self.count = Button(choose, width=2, height=1, text=self.num, font=button_font, bg="Yellow", fg="Blue", pady=1)
		self.down = Button(choose, image=down_pic, bg="Yellow", command=self.minus, state='disabled')
		self.up = Button(choose, image=up_pic, bg="Yellow", command=self.plus)
		self.zero = Button(choose, text="R", width=2, font=button_font, bg="Yellow", command=self.reset)
		self.label.place(x=30, y=Dish.pos)
		self.count.place(x=100, y=Dish.pos)
		self.up.place(x=140, y=Dish.pos)
		self.down.place(x=180, y=Dish.pos)
		self.zero.place(x=220, y=Dish.pos)
		Dish.pos += 35
		Dish.total += 1

	def plus(self):
		self.num += 1
		self.count.config(text=self.num)
		self.down.config(state='normal')
	def minus(self):
		self.num -= 1
		self.count.config(text=self.num)
		if self.num == 0:
			self.down.config(state="disabled")
	def reset(self):
		self.num = 0
		self.count.config(text=self.num)
		self.down.config(state="disabled")

for ele in dish_name:
	dish[ele] = Dish(ele)


#Info
info = LabelFrame(window, text="請確認您的用餐資訊", labelanchor=N, width=500, height=500, bg="lightblue", bd=10, relief="ridge", fg="Blue", font=info_font)
info.pack(padx=30, ipadx=50, side=RIGHT)

ask = Label(info, text="您的用餐桌號", font=ask_font, bg="lightblue", fg="Black")
ask.place(x=10, y=10)

table_temp = Image.open("pic/桌號.png")
table_temp = table_temp.resize((151, 170), Image.ANTIALIAS)
table_pic = ImageTk.PhotoImage(table_temp)
table = Label(info, image=table_pic, bd=2, relief="ridge")
table.place(x=290, y=30)

class Table_number():	
	
	number = None
	def __init__(self, num, x, y):
		self.num = num
		self.button = Button(info, text=str(num), font=table_font, width=3, height=1, bd=1, bg="DodgerBlue2", activebackground="DodgerBlue3", padx=1, pady=1, command=self.change)
		self.button.place(x=x, y=y)
	def change(self):
		Table_number.number = self.num
		for i in range(1,6):
			if table_button[i].num == Table_number.number:
				table_button[i].button.config(bg="Yellow", state="disabled")
			else:
				table_button[i].button.config(bg="DodgerBlue2", state="normal")

table_button = dict()

for i in range(1,4):
	table_button[i] = Table_number(i, 20+(i-1)*90, 50)
for i in range(4,6):
	table_button[i] = Table_number(i, 65+(i-4)*90, 130)



#PS.
PS = Label(info, text="備註(有其他需要可在此註明)", font=ask_font, bg="lightblue", fg="Black")
PS.place(x=10, y=200)
var = StringVar()
content = Entry(info, width=50, textvariable=var, bg="white", bd=4, font=button_font)
content.place(x=10, y=240)

#send
hamburger_temp = Image.open("pic/hbg.jpg")
hamburger_temp = hamburger_temp.resize((100, 100), Image.ANTIALIAS)
hamburger_pic = ImageTk.PhotoImage(hamburger_temp)

send_label = Label(info, text="點擊送出訂單！", font=info_font, bg="lightblue", fg="DarkGreen")
send_label.place(x=100, y=330)
send_button = Button(info, image=hamburger_pic, bg="Yellow")
send_button.place(x=300, y=300)

window.mainloop()
import csv 

with open("mos_data.csv", 'w', newline='') as file:
	writer = csv.writer(file)

	writer.writerow(["用餐日期", "用餐時間", "用餐內容", "餐點數量", "桌號", "備註"])



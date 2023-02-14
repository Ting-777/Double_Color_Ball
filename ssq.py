import tkinter as tk
import tkinter.filedialog as filedialog
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageTk
import os
import re

def draw_text(image,x,y,text,font_size=40):
    font_path = os.path.join(os.path.dirname(__file__), "fonts/simhei.ttf")
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(image)
    draw.text((x, y), text, fill="black", font=font)
    return image
    
def image_joint(img1, img2):
    # 创建一个新的Image对象，大小为第一张图片的宽度和所有图片的高度之和
    new_img = Image.new('RGB', (img1.width, img1.height + img2.height))
    
    new_img.paste(img1, (0, 0))
    new_img.paste(img2, (0, img1.height))

    new_img.save('ssq.png')

    return new_img

def generate_image_part(text, font_size=40):
    # 分离文本中的红色部分、蓝色部分和黑色部分
    red_text, blue_text, black_text = text.split('|')
    red_text = red_text.strip()
    blue_text = blue_text.strip()

    # 加载字体文件和字体大小
    font_path = os.path.join(os.path.dirname(__file__), "fonts/simhei.ttf")
    font = ImageFont.truetype(font_path, font_size)

    # 计算文本的大小
    red_size = font.getsize(red_text)
    blue_size = font.getsize(blue_text)
    black_size = font.getsize(black_text)

    # 计算图片的大小
    image_width = red_size[0] + blue_size[0] + black_size[0] + 80
    image_height = max(red_size[1], blue_size[1], black_size[1]) + 20

    # 创建空白图片
    image = Image.new("RGB", (image_width, image_height), "white")

    # 绘制红色部分的文本
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), red_text, fill="red", font=font)

    # 绘制蓝色部分的文本
    draw.text((red_size[0] + 40, 10), blue_text, fill="blue", font=font)

    # 绘制黑色部分的文本
    draw.text((red_size[0] + blue_size[0] + 40, 10), black_text, fill="black", font=font)

    # 将绘制好的图像保存到文件中，文件名为输入文本的第一部分。
    #image.save('ssq.png')
    return image

def generate_image(file_path):
    with open(file_path,'r',encoding = 'utf-8') as f:
        lines = f.readlines()
        i = 0
    for line in lines:
        if i == 0:
            generate_image_part(line).save('ssq.png')
        else:
            img1 = Image.open('ssq.png')
            img2 = image_joint(img1, generate_image_part(line))
        i += 1
    return img2

# 双色球号码
red_balls = list(range(1, 34))
blue_balls = list(range(1, 17))

class DoubleColorBall:
    def __init__(self, master):
        self.master = master
        master.title("双色球开奖")

        self.tickets = []
        self.red_checkboxes = []
        self.blue_checkboxes = []
        self.red_counts = []
        self.blue_counts = []
        self.image_frame = tk.Frame(self.master)
        self.image_frame.pack(side=tk.TOP, pady=10)
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(side=tk.LEFT, padx=10, pady=10)
        # 创建控件
        self.create_widgets()

    def create_widgets(self):
        # 创建选择文件按钮
        self.import_button = tk.Button(self.master, text="导入号码文件", command=self.import_numbers)
        self.import_button.pack()


        # 创建输入号码框和开奖按钮
        self.number_entry = tk.Entry(self.master, width=5)
        self.number_entry.pack()
        self.check_button1 = tk.Button(self.master, text="红球输入", command=self.check_red_number, state="disabled")
        self.check_button1.pack()
        self.check_button2 = tk.Button(self.master, text="蓝球输入", command=self.check_blue_number, state="disabled")
        self.check_button2.pack()
        self.check_button = tk.Button(self.master, text="判定是否中奖", command=self.check_numbers, state="disabled")
        self.check_button.pack()

    def import_numbers(self):
        # 打开文件对话框选择号码文件
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            image = generate_image(file_path)
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
            with open(file_path, "r",encoding='utf-8') as f:
                for line in f:
                    items = line.strip().split('|')
                    redballs = [int(x) for x in items[0].strip().split()]
                    blueball = int(items[1].strip())
                    registrant = items[2].strip()
                    result_dict = {'redballs': redballs, 'blueball': blueball, 'registrant': registrant}
                    self.tickets.append(result_dict)
                    self.red_counts.append(0)
                    self.blue_counts.append(0)

            # 启用开奖按钮
            self.check_button1.configure(state="normal")
            self.check_button2.configure(state="normal")
            self.check_button.configure(state="normal")
        
        
    def check_red_number(self):
        # 获取用户输入的号码
        input_number = int(self.number_entry.get())
        self.number_entry.delete(0,"end")
        # 判定用户输入的号码是否中奖
        i = 0
        for ticket in self.tickets:
            j = 0
            for redball in ticket['redballs']:
                if redball == input_number:
                    self.red_counts[i] += 1
                    img = Image.open('ssq.png')
                    img1 = draw_text(img,10+60*j,10+59*i,'√')
                    img1.save('ssq.png')
                    photo = ImageTk.PhotoImage(img1)
                    self.image_label.config(image=photo)
                    self.image_label.image = photo
                j += 1
            i += 1

    def check_blue_number(self):
        # 获取用户输入的号码
        input_number = int(self.number_entry.get())
        self.number_entry.delete(0,"end")
        # 判定用户输入的号码是否中奖
        i = 0
        for ticket in self.tickets:
            if ticket['blueball'] == input_number:
                self.blue_counts[i] += 1
                img = Image.open('ssq.png')
                img1 = draw_text(img,380,10+59*i,'√')
                img1.save('ssq.png')
                photo = ImageTk.PhotoImage(img1)
                self.image_label.config(image=photo)
                self.image_label.image = photo
            i += 1

    def check_numbers(self):
        for i in range(len(self.red_counts)):
            red_count = self.red_counts[i]
            blue_count = self.blue_counts[i]
            if red_count == 6 and blue_count == 1:
                prize = "壹"
            elif red_count == 6 and blue_count == 0:
                prize = "贰"
            elif red_count == 5 and blue_count == 1:
                prize = "叁"
            elif (red_count == 5 and blue_count == 0) or (red_count == 4 and blue_count == 1):
                prize = "肆"
            elif (red_count == 4 and blue_count == 0) or (red_count == 3 and blue_count == 1):
                prize = "伍"
            elif blue_count == 1:
                prize = "陆"
            else:
                prize = "無"
            img = Image.open('ssq.png')
            img1 = draw_text(img,500,11+59*i,prize)
            img1.save('ssq.png')
            photo = ImageTk.PhotoImage(img1)
            self.image_label.config(image=photo)
            self.image_label.image = photo

root = tk.Tk()
app = DoubleColorBall(root)
root.mainloop()

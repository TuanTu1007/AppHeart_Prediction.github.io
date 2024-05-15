"""
Import thư viện
"""
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter.ttk import Combobox
from datetime import date
import datetime
import matplotlib
import matplotlib.pyplot as plt 
from matplotlib.figure import Figure
from PIL import ImageTk, Image
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from info import InfoData
from heart_prediction import *
from database import DatabaseManager
from login import LoginForm
from fpdf import FPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from heart_prediction import HeartDiseasePredictor

class HeartDiseasePredictionApp:
    """
    Ứng dụng Dự đoán Bệnh tim.

    Attributes:
        root (tk.Tk): Cửa sổ chính của ứng dụng.
        image_icon (tk.PhotoImage): Hình ảnh frame của ứng dụng.
        header (tk.PhotoImage): Hình ảnh tiêu đề của ứng dụng.
        prediction (int): Kết quả dự đoán bệnh tim.
        is_logged_in (bool): Trạng thái đăng nhập của người dùng.
    
    Phương thức:
    __init__(self, root): Phương thức khởi tạo đối tượng HeartDiseasePredictionApp với các thuộc tính cần thiết và cấu hình giao diện người dùng.
    create_heading_entry_frame(self): Tạo frame tiêu đề và nhập thông tin chung của bệnh nhân.
    create_detail_entry_frame(self): Tạo frame để nhập thông tin chi tiết về các thông số của bệnh nhân.
    create_report_frame(self): Tạo frame để hiển thị báo cáo dự đoán kết quả với các thông số đã nhập.
    create_graphs(self): Tạo các đồ thị dự đoán mặc định và hiển thị chúng trên giao diện.
    create_buttons(self): Tạo và thiết lập các nút điều khiển trên giao diện người dùng.
    LoginForm(self): Hiển thị giao diện đăng nhập và xử lý sự kiện đăng nhập.
    Logout(self): Đăng xuất và hiển thị giao diện đăng nhập.
    change_mode(self): Chuyển đổi giữa chế độ hút thuốc và không hút thuốc.
    Clear(self): Xóa trắng các trường thông tin trong ứng dụng sau khi đăng xuất.
    selecGender(self): Lấy thông tin giới tính từ RadioButton.
    selecfbs(self): Lấy thông tin fbs từ RadioButton.
    selecexang(self): Lấy thông tin exang từ RadioButton.
    seleccp(self): Lấy thông tin cp từ Combobox.
    selecslope(self): Lấy thông tin slope từ Combobox.
    check_login(self): Kiểm tra trạng thái đăng nhập của người dùng.
    create_bar_chart(self, figure_size, position, patient_data, standard_values, labels, x, y): Tạo biểu đồ cột.
    Analysis(self): Phương thức này thực hiện phân tích dữ liệu bệnh tim của người dùng và hiển thị kết quả dự đoán, cùng với các biểu đồ thống kê.
    Save(self): Phương thức này lưu dữ liệu phân tích bệnh tim của người dùng vào cơ sở dữ liệu.
    User(self): Phương thức này hiển thị thông tin của người dùng trong cửa sổ Profile.
    display_recommendations(self): Phương thức này hiển thị khuyến cáo cho người mắc bệnh tim.
    export_to_pdf(self): Phương thức này xuất thông tin của người dùng ra file PDF.
    """
    def __init__(self, root):
        """
        Khởi tạo đối tượng HeartDiseasePredictionApp.

        Args:
            root (Tk): Cửa sổ gốc của ứng dụng.

        Hàm này khởi tạo một đối tượng ứng dụng dự đoán bệnh tim mạch. Nó cài đặt các thuộc tính cần thiết và cấu hình giao diện người dùng.

        Các bước thực hiện bao gồm:
        - Thiết lập cửa sổ gốc với tiêu đề "Heart Disease Prediction" và kích thước 1550x800 pixels.
        - Cấu hình màu nền của ứng dụng.
        - Đặt biểu tượng cho ứng dụng.
        - Hiển thị header của ứng dụng.
        - Tạo các khung chứa các thành phần giao diện khác nhau như thông tin đầu vào, báo cáo, biểu đồ và nút điều khiển.
        - Khởi tạo một số biến quan trọng như prediction (dự đoán) và is_logged_in (đã đăng nhập hay chưa).
        """
        self.root = root
        self.root.title("Heart Disease Prediction")
        self.root.geometry("1550x800")
        self.root.config(bg="#f0ddd5")

        # Icon
        self.image_icon = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\icon.png")
        self.root.iconphoto(False, self.image_icon)

        # Header
        self.header = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\header.png")
        self.myImage = Label(image=self.header, bg="#f0ddd5")
        self.myImage.place(x=0, y=0)

        # Frames
        self.create_heading_entry_frame()
        self.create_detail_entry_frame()
        self.create_report_frame()
        self.create_graphs()
        self.create_buttons()
        self.info_labels = []
        self.prediction = None
        self.is_logged_in = False
        
    def create_heading_entry_frame(self):
        """
        Tạo khung tiêu đề và nhập các thông tin chung của bệnh nhân.

        Hàm này tạo một khung tiêu đề bao gồm các trường nhập liệu cho các thông tin chung của bệnh nhân như số thứ tự, ngày tháng hiện tại, tên và tuổi. 
        
        Các trường thông tin bao gồm:
        - Số thứ tự(No.)
        - Ngày (Date)
        - Tên (Name)
        - Tuổi (Age)
        
        """
        self.heading_entry = Frame(self.root, width=995, height=216, bg="#df2d4b")
        self.heading_entry.place(x=600, y=2)

        # Labels
        Label(self.heading_entry, text="No.", font="TimesNewRoman 13", bg="#df2d4b", fg="#fefbfb").place(x=30, y=0)
        Label(self.heading_entry, text="Date", font="TimesNewRoman 13", bg="#df2d4b", fg="#fefbfb").place(x=430, y=0)
        Label(self.heading_entry, text="Name", font="TimesNewRoman 13", bg="#df2d4b", fg="#fefbfb").place(x=30, y=90)
        Label(self.heading_entry, text="Age", font="TimesNewRoman 13", bg="#df2d4b", fg="#fefbfb").place(x=430, y=90)

        # Entry Images
        self.entry_image = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\Rounded Rectangle 1.png")
        Label(self.heading_entry, image=self.entry_image, bg="#df2d4b").place(x=20, y=30)
        Label(self.heading_entry, image=self.entry_image, bg="#df2d4b").place(x=430, y=30)
        self.entry_image2 = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\Rounded Rectangle 2.png")
        Label(self.heading_entry, image=self.entry_image2, bg="#df2d4b").place(x=20, y=120)
        Label(self.heading_entry, image=self.entry_image2, bg="#df2d4b").place(x=430, y=120)

        # Entry Widgets
        self.Registration = IntVar()
        self.reg_entry = Entry(self.heading_entry, textvariable=self.Registration, width=30, font="TimesNewRoman 15", bg="#0e5363", fg="white", bd=0)
        self.reg_entry.place(x=30, y=45)

        self.Date = StringVar()
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        self.date_entry = Entry(self.heading_entry, textvariable=self.Date, width=15, font="TimesNewRoman 15", bg="#0e5363", fg="white", bd=0)
        self.date_entry.place(x=450, y=45)
        self.Date.set(d1)

        self.Name = StringVar()
        self.name_entry = Entry(self.heading_entry, textvariable=self.Name, width=20, font="TimesNewRoman 15", bg="#ededed", fg="#222222", bd=0)
        self.name_entry.place(x=30, y=130)

        self.BD = StringVar()
        self.BD_entry = Entry(self.heading_entry, textvariable=self.BD, width=20, font="TimesNewRoman 15", bg="#ededed", fg="#222222", bd=0)
        self.BD_entry.place(x=450, y=130)

    def create_detail_entry_frame(self):
        """
        Tạo frame nhập thông tin các thông số của bệnh nhân.

        Hàm này tạo một frame để nhập thông tin chi tiết về các thông số của bệnh nhân, bao gồm giới tính, đường huyết, tình trạng tập thể dục, 
        cảm giác đau ngực, kết quả điện tâm đồ nghỉ, độ dốc của đoạn ST, số mạch và hình dạng của mạch và các chỉ số huyết áp, cholesterol,
        nhịp tim tối đa, cũng như đỉnh giảm ST.

        Các bước thực hiện bao gồm:
        - Tạo một frame với kích thước và màu nền nhất định để chứa các thành phần.
        - Tạo các nút radio cho giới tính, đường huyết nhanh và tình trạng tập thể dục.
        - Tạo các hộp combobox để chọn các thông số khác như cảm giác đau ngực, kết quả điện tâm đồ nghỉ, độ dốc của đoạn ST, số mạch, và hình dạng mạch.
        - Tạo các ô nhập dữ liệu cho các chỉ số huyết áp, cholesterol, nhịp tim tối đa và đỉnh giảm ST.
        """
        self.Detail_entry = Frame(self.root, width=490, height=325, bg="#dae9f2")
        self.Detail_entry.place(x=30, y=450)

        # Radio Buttons
        Label(self.Detail_entry, text="sex: ", font="TimesNewRoman 13", bg="#dae9f2", fg="#1b2631").place(x=10, y=20)
        Label(self.Detail_entry, text="fbs: ", font="TimesNewRoman 13", bg="#dae9f2", fg="#1b2631").place(x=180, y=20)
        Label(self.Detail_entry, text="exang: ", font="TimesNewRoman 13", bg="#dae9f2", fg="#1b2631").place(x=335, y=20)

        self.gen = IntVar()
        self.R1 = Radiobutton(self.Detail_entry, text='Male', variable=self.gen, value=1)
        self.R2 = Radiobutton(self.Detail_entry, text='Female', variable=self.gen, value=2)
        self.R1.place(x=43, y=20)
        self.R2.place(x=93, y=20)

        self.fbs = IntVar()
        self.R3 = Radiobutton(self.Detail_entry, text='True', variable=self.fbs, value=1)
        self.R4 = Radiobutton(self.Detail_entry, text='False', variable=self.fbs, value=2)
        self.R3.place(x=213, y=20)
        self.R4.place(x=263, y=20)

        self.exang = IntVar()
        self.R5 = Radiobutton(self.Detail_entry, text='Yes', variable=self.exang, value=1)
        self.R6 = Radiobutton(self.Detail_entry, text='No', variable=self.exang, value=2)
        self.R5.place(x=387, y=20)
        self.R6.place(x=430, y=20)

        # Comboboxes
        Label(self.Detail_entry, text="cp: ", font="TimesNewRoman 13", bg="#dae9f2", fg="#1b2631").place(x=10, y=65)
        Label(self.Detail_entry, text="restecg:", font="TimesNewRoman 13", bg="#dae9f2", fg="#1b2631").place(x=10, y=120)
        Label(self.Detail_entry, text="slope:", font="TimesNewRoman 13", bg="#dae9f2", fg="#1b2631").place(x=10, y=175)
        Label(self.Detail_entry, text="ca:", font="TimesNewRoman 13", bg="#dae9f2", fg="#1b2631").place(x=10, y=230)
        Label(self.Detail_entry, text="thal:", font="TimesNewRoman 13", bg="#dae9f2", fg="#1b2631").place(x=10, y=285)

        self.cp_combobox = Combobox(self.Detail_entry, values=['0', '1', '2', '3'], font="TimesNewRoman 12", state="readonly", width=14)
        self.cp_combobox.place(x=50, y=65)

        self.restecg_combobox = Combobox(self.Detail_entry, values=['0', '1', '2'], font="TimesNewRoman 12", state="readonly", width=11)
        self.restecg_combobox.place(x=80, y=120)

        self.slope_combobox = Combobox(self.Detail_entry, values=['0', '1', '2'], font="TimesNewRoman 12", state="readonly", width=12)
        self.slope_combobox.place(x=70, y=175)

        self.ca_combobox = Combobox(self.Detail_entry, values=['0', '1', '2', '3'], font="TimesNewRoman 12", state="readonly", width=14)
        self.ca_combobox.place(x=50, y=230)

        self.thal_combobox = Combobox(self.Detail_entry, values=['0', '1', '2'], font="TimesNewRoman 12", state="readonly", width=14)
        self.thal_combobox.place(x=50, y=285)

        # Data Entry Box
        Label(self.Detail_entry, text="Smoking:", font="TimesNewRoman 13", width=7, bg="#dae9f2", fg="black").place(x=240, y=65)
        Label(self.Detail_entry, text="trestbps:", font="TimesNewRoman 13", width=7, bg="#dae9f2", fg="#1b2631").place(x=240, y=120)
        Label(self.Detail_entry, text="chol:", font="TimesNewRoman 13", width=7, bg="#dae9f2", fg="#1b2631").place(x=240, y=175)
        Label(self.Detail_entry, text="thalach:", font="TimesNewRoman 13", width=7, bg="#dae9f2", fg="#1b2631").place(x=240, y=230)
        Label(self.Detail_entry, text="oldpeak:", font="TimesNewRoman 13", width=7, bg="#dae9f2", fg="#1b2631").place(x=240, y=285)

        self.trestbps = StringVar()
        self.chol = StringVar()
        self.thalach = StringVar()
        self.oldpeak = StringVar()

        self.trestbps_entry = Entry(self.Detail_entry, textvariable=self.trestbps, width=10, font="TimesNewRoman 15", bg="white", fg="#222222", bd=0)
        self.trestbps_entry.place(x=320, y=120)

        self.chol_entry = Entry(self.Detail_entry, textvariable=self.chol, width=10, font="TimesNewRoman 15", bg="white", fg="#222222", bd=0)
        self.chol_entry.place(x=320, y=175)

        self.thalach_entry = Entry(self.Detail_entry, textvariable=self.thalach, width=10, font="TimesNewRoman 15", bg="white", fg="#222222", bd=0)
        self.thalach_entry.place(x=320, y=230)

        self.oldpeak_entry = Entry(self.Detail_entry, textvariable=self.oldpeak, width=10, font="TimesNewRoman 15", bg="white", fg="#222222", bd=0)
        self.oldpeak_entry.place(x=320, y=285)

    def create_report_frame(self):
        """
        Tạo frame hiển thị báo cáo dự đoán kết quả.

        Hàm này tạo một frame để hiển thị báo cáo dự đoán kết quả với các thông số đã nhập. 

        Các bước thực hiện bao gồm:
        - Tạo một hình ảnh nền cho frame hiển thị báo cáo.
        - Tạo một frame với kích thước và màu nền để chứa các phần tử hiển thị báo cáo.
        - Hiển thị tiêu đề "Result Prediction".
        - Hiển thị nội dung báo cáo dự đoán kết quả.
        """
        self.report_background = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\report1.png")
        Label(image=self.report_background, bg="#f0ddd5").place(x=520, y=220)

        self.Report_entry = Frame(self.root, width=550, height=155, bg="#dbe0e3")
        self.Report_entry.place(x=700, y=260)

        Label(self.root, text="Result Prediction", font="TimesNewRoman 20 bold", bg="#dbe0e3", fg="black").place(x=850, y=280)
        self.report1 = Label(self.root, font="Charmonman 15 bold", bg="#dbe0e3")
        self.report1.place(x=800, y=330)

    def create_graphs(self):
        """
        Tạo các đồ thị dự đoán mặc định, hiển thị khi người dùng chưa dự đoán.

        Hàm này tạo các đồ thị dự đoán và hiển thị chúng trên giao diện.

        Các bước thực hiện bao gồm:
        - Tạo một hình ảnh đồ thị từ tệp hình ảnh đã cho.
        - Tạo các nhãn hình ảnh cho các đồ thị và thiết lập hình ảnh của chúng.
        - Đặt vị trí của các nhãn hình ảnh trên giao diện để hiển thị đồ thị.
        """
        self.graph_image = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\graph.png")
        self.graph_label1 = Label(image=self.graph_image)
        self.graph_label2 = Label(image=self.graph_image)
        self.graph_label3 = Label(image=self.graph_image)
        self.graph_label4 = Label(image=self.graph_image)
        self.graph_label1.place(x=550, y=510)
        self.graph_label2.place(x=800, y=510)
        self.graph_label3.place(x=1050, y=510)
        self.graph_label4.place(x=1300, y=510)


    def create_buttons(self):
        """
        Tạo các nút điều khiển trên giao diện.

        Hàm này tạo và thiết lập các nút điều khiển trên giao diện người dùng.

        Các bước thực hiện bao gồm:
        - Tạo nút ĐĂNG NHẬP với các thuộc tính như chữ, font, màu sắc, và vị trí.
        - Tạo nút Đăng Xuất với hình ảnh và thiết lập các thuộc tính như màu sắc và vị trí.
        - Tạo nút Prediction với hình ảnh và thiết lập các thuộc tính như màu sắc và vị trí.
        - Tạo nút Info với hình ảnh và thiết lập các thuộc tính như màu sắc và vị trí.
        - Tạo nút Save với hình ảnh và thiết lập các thuộc tính như màu sắc và vị trí.
        - Tạo nút Kiểm Tra Hút Thuốc với hình ảnh và thiết lập các thuộc tính như màu sắc và vị trí.
        - Tạo nút User với hình ảnh và thiết lập các thuộc tính như màu sắc và vị trí.
        - Tạo nút Xuất PDF với hình ảnh và thiết lập các thuộc tính như màu sắc và vị trí.
        """
        # Login button
        self.login_button = Button(text="ĐĂNG NHẬP",bd=1, font="TimesNewRoman 12 bold", bg="#df2d4b", cursor="hand2", command=self.LoginForm)
        self.login_button.place(width=100, height=50, x=1410, y=80)
        
        # Logout button
        self.logout_button_image = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\logout.png")
        self.logout_button = Button(image=self.logout_button_image,bd=0,bg="#df2d4b",cursor="hand2",command=self.Logout)
        
        # Analysis Button
        self.analysis_button = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\Analysis.png")
        Button(image=self.analysis_button, bd=0, bg="#f0ddd5", cursor="hand2", command=self.Analysis).place(x=920, y=425)

        # Info button
        self.info_button = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\info.png")
        Button(image=self.info_button, bd=0, bg="#f0ddd5", cursor="hand2", command=InfoData).place(x=490, y=410)

        # Save button
        self.save_button = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\save.png")
        Button(image=self.save_button, bd=0, bg="#f0ddd5", cursor="hand2", command=self.Save).place(x=1300, y=260)

        # Smoking Button
        self.button_mode = True
        self.choice = "smoking"
        self.smoking_image = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\smoker.png")
        self.non_smoking_image = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\non-smoker.png")
        self.mode = Button(image=self.smoking_image, bg="#dae9f2", bd=0, cursor="hand2", command=self.change_mode)
        self.mode.place(x=350, y=510)
        
        # user button
        self.user_image = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\login.png")
        self.user_button = Button(image=self.user_image, bg="#df2d4b", bd=0, cursor="hand2", command=self.User)
        
        # pdf button
        self.pdf_img = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\pdf.png")
        Button(image=self.pdf_img, bg="#f0ddd5", bd=0, cursor="hand2", command=self.export_to_pdf).place(x=1400,y=260)
        

    def LoginForm(self):
        """
        Hiển thị giao diện đăng nhập và xử lý sự kiện đăng nhập.

        Hàm này mở cửa sổ đăng nhập và xử lý sự kiện đăng nhập bằng cách gọi hàm `login_callback`.

        Args:
            success (bool): Kết quả đăng nhập thành công hoặc không.
            username (str): Tên người dùng đăng nhập thành công.
        """
        def login_callback(success, username):
            if success:
                messagebox.showinfo("Login", "Đăng nhập thành công")  # Xử lý đăng nhập thành công
                self.login_button.place_forget()
                self.user_button.place(x=1405, y=70)
                self.logout_button.place(x=1480,y=80)
                self.username = username  # Lưu trữ username
                self.username_label = Label(text=f"Xin chào {username}", bg="#df2d4b", bd=0)
                self.username_label.place(x=1390, y=130)
                self.is_logged_in = True
        LoginForm(login_callback)
        
    def Logout(self):
        """
        Đăng xuất và hiển thị giao diện đăng nhập.

        Hàm này yêu cầu xác nhận từ người dùng trước khi đăng xuất và xóa thông tin người dùng đã đăng nhập.

        Returns:
            None
        """
        result = messagebox.askquestion("Đăng xuất", "Bạn muốn đăng xuất!")  # Xử lý đăng nhập thành công
        if result == 'yes':
            # Xử lý khi người dùng đồng ý đăng xuất
            self.user_button.place_forget()
            self.logout_button.place_forget()
            self.username_label.place_forget()
            self.login_button.place(width=100, height=50, x=1410, y=80)
        
        self.Clear()
        
        
    def change_mode(self):
        """
        Chuyển đổi giữa chế độ hút thuốc và không hút thuốc.

        Hàm này thay đổi hình ảnh của nút và cập nhật lựa chọn tương ứng.

        Returns:
            None
        """
        if self.button_mode:
            self.choice = "non_smoking"
            self.mode.config(image=self.non_smoking_image, activebackground="white")
            self.button_mode = False
        else:
            self.choice = "smoking"
            self.mode.config(image=self.smoking_image, activebackground="white")
            self.button_mode = True
    
    def Clear(self):
        """
        Xóa trắng các trường thông tin trong ứng dụng sau khi đăng xuất.

        Returns:
            None
        """
        self.Name.set('')
        self.trestbps.set('')
        self.chol.set('')
        self.thalach.set('')
        self.oldpeak.set('')
        self.BD.set('')
        self.cp_combobox.set('')
        self.slope_combobox.set('')
        self.restecg_combobox.set('')
        self.ca_combobox.set('')
        self.thal_combobox.set('')
        
        
        
        
    
    def selecGender(self):
        """
        Lấy thông tin giới tính từ RadioButton.

        Returns:
            int or None: Trả về 1 nếu là Nam, 0 nếu là Nữ, None nếu không có lựa chọn.
        """
        if self.gen.get() == 1:
            Gender = 1
            return Gender
        elif self.gen.get() == 2:
            Gender = 0
            return Gender
        else:
            return None
    
    def selecfbs(self):
        """
        Lấy thông tin fbs từ RadioButton.

        Returns:
            int: Trả về 1 nếu có, 0 nếu không.
        """
        if self.fbs.get() == 1:
            Fbs = 1
            return(Fbs)
        elif self.fbs.get() == 2:
            Fbs = 0
            return(Fbs)

    def selecexang(self):
        """
        Lấy thông tin exang từ RadioButton.

        Returns:
            int: Trả về 1 nếu có, 0 nếu không.
        """
        if self.exang.get() == 1:
            Exang = 1
            return(Exang)
        elif self.exang.get() == 2:
            Exang = 0
            return(Exang)
    
    def seleccp(self):
        """
        Lấy thông tin cp từ Combobox.

        Returns:
            int: Giá trị cp được chọn.
        """
        input = self.cp_combobox.get()
        if input == "0":
            return (0)
        elif input == "1":
            return (1)
        elif input == "2":
            return(2)
        elif input == "3":
            return(3)
            
    def selecslope(self):
        """
        Lấy thông tin slope từ Combobox.

        Returns:
            int: Giá trị slope được chọn.
        """
        input = self.slope_combobox.get()
        if input == "0":
            return (0)
        elif input == "1":
            return (1)
        elif input == "2":
            return(2)
    
    
    def check_login(self):
        """
        Kiểm tra trạng thái đăng nhập của người dùng.

        Returns:
            bool: True nếu đã đăng nhập, False nếu chưa đăng nhập.
        """
        if not self.is_logged_in:
            messagebox.showerror("Error", "Bạn chưa đăng nhập!!!")
            return False
        return True
    
    def create_bar_chart(self, figure_size, position, patient_data, standard_values, labels, x, y):
        """
        Tạo biểu đồ cột.

        Args:
            figure_size (tuple): Kích thước của hình vẽ.
            position (tuple): Vị trí của biểu đồ trên cửa sổ.
            patient_data (dict): Dữ liệu của bệnh nhân.
            standard_values (dict): Giá trị chuẩn.
            labels (list): Danh sách nhãn.
            x (int): Tọa độ x của biểu đồ trên cửa sổ.
            y (int): Tọa độ y của biểu đồ trên cửa sổ.
        """
        f = Figure(figsize=figure_size)
        a = f.add_subplot(111)
        
        indices = list(patient_data.keys())
        patient_values = [patient_data[key] for key in indices]
        standard_values_list = [standard_values[key] for key in indices]
        x_pos = range(len(indices))
        bar_width = 0.35

        a.bar([i - bar_width / 2 for i in x_pos], patient_values, bar_width, label='Bệnh nhân', color='b')
        a.bar([i + bar_width / 2 for i in x_pos], standard_values_list, bar_width, label='Giá trị chuẩn', color='r', alpha=0.5)
        
        a.set_xticks(x_pos)
        a.set_xticklabels(indices)
        a.legend()

        canvas = FigureCanvasTkAgg(f, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().place(x=x, y=y)

    def Analysis(self):
        """
        Phân tích dữ liệu bệnh tim của người dùng và hiển thị kết quả dự đoán, cùng với các biểu đồ thống kê.

        Hàm này thực hiện các bước sau:
        1. Kiểm tra xem người dùng đã đăng nhập chưa, nếu chưa thì kết thúc hàm.
        2. Nhận dữ liệu nhập từ giao diện người dùng và kiểm tra tính hợp lệ của dữ liệu.
        3. Tiến hành dự đoán bệnh tim dựa trên dữ liệu nhập và hiển thị kết quả.
        4. Tạo và hiển thị các biểu đồ thống kê về các thuộc tính liên quan đến bệnh tim.
        5. Loại bỏ các nhãn của biểu đồ thống kê nếu chúng đã tồn tại.

        Returns:
            None

        Raises:
            ValueError: Nếu không nhập tên.
        """
        if not self.check_login():
            return
        
        global prediction
        
        try:
            c_name = self.Name.get()
            if not c_name:  
                raise ValueError("Chưa nhập tên!!!")
        except ValueError as e:
            messagebox.showerror("Error", str(e)) 
            return
        
        try:
            age = int(self.BD.get())
            B = int(self.selecGender())
            F = int(self.selecfbs())
            I = int(self.selecexang())
            C = int(self.seleccp())
            K = int(self.selecslope())
            G = int(self.restecg_combobox.get())
            L = int(self.ca_combobox.get())
            M = int(self.thal_combobox.get())
            D = int(self.trestbps.get())
            E = int(self.chol.get())
            H = int(self.thalach.get())
            J = int(self.oldpeak.get())

        except:
            messagebox.showerror("Message", "Thiếu dữ liệu!!!")
            return
        
        input_new = (age,B,C,D,E,F,G,H,I,J,K,L,M)

        # Dự đoán
        predictor = HeartDiseasePredictor('D:\Subject\IE221_Python\DoAn\heart.csv')
        predictor.preprocess_data()
        predictor.train_model()
        processed_new_data = predictor.preprocess_new_data(input_new)
        prediction = predictor.model.predict(processed_new_data)
        self.prediction = prediction[0]
        
        
        if prediction[0] == 0:
            self.report1.config(text=f"{self.Name.get()} bạn không mắc bệnh tim!!!")
        else:
            self.report1.config(text=f"{self.Name.get()} bạn có mắc bệnh tim!!!")

        # recommend button
        self.recommend_img = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\recommend.png")
        recommend_button = Button(image=self.recommend_img, bg="#f0ddd5", bd=0, cursor="hand2", command=self.display_recommendations)
        recommend_button.place(x=1300,y=340)
            
        # figure 1
        f = Figure(figsize=(2.5, 2.5))
        a = f.add_subplot(111)
        a.plot(["Sex","fbs","exang"],[B,F,I])
        canvas = FigureCanvasTkAgg(f)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.place(x=550,y=510)
        
        self.create_bar_chart(
            figure_size=(3, 2.5),
            position=(800, 510),
            patient_data={
                "trestbps": int(self.trestbps.get()),
                "chol": int(self.chol.get()),
                "thalach": int(self.thalach.get()),
            },
            standard_values={
                "trestbps": 120,
                "chol": 200,
                "thalach": 70
            },
            labels=["trestbps", "chol", "thalach"],
            x=800,
            y=510
        )
        
        self.create_bar_chart(
            figure_size=(2, 2.5),
            position=(1100, 510),
            patient_data={
                "slope": int(self.slope_combobox.get()),
                "cp": int(self.cp_combobox.get()),
                "oldpeak": float(self.oldpeak.get())
            },
            standard_values={
                "slope": 1,
                "cp": 3,
                "oldpeak": 1.0
            },
            labels=["slope", "cp", "oldpeak"],
            x=1100,
            y=510
        )
        
        self.create_bar_chart(
            figure_size=(2.1, 2.5),
            position=(1300, 510),
            patient_data={
                "restecg": int(self.restecg_combobox.get()),
                "ca": int(self.ca_combobox.get()),
                "thal": int(self.thal_combobox.get())
            },
            standard_values={
                "restecg": 0,
                "ca": 0,
                "thal": 0
            },
            labels=["restecg", "ca", "thal"],
            x=1300,
            y=510
        )

        self.graph_label1.place_forget()
        self.graph_label2.place_forget()
        self.graph_label3.place_forget()
        self.graph_label4.place_forget()
            
        
    
    def Save(self):
        """
        Lưu dữ liệu phân tích bệnh tim của người dùng vào cơ sở dữ liệu.

        Hàm này thực hiện các bước sau:
        1. Kiểm tra xem người dùng đã đăng nhập chưa, nếu chưa thì kết thúc hàm.
        2. Nhận dữ liệu nhập từ giao diện người dùng và kiểm tra tính hợp lệ của dữ liệu.
        3. Kết nối đến cơ sở dữ liệu và tạo bảng nếu chưa tồn tại.
        4. Lưu dữ liệu vào cơ sở dữ liệu.

        Returns:
            None

        Raises:
            None
        """
        if not self.check_login():
            return
        
        try:
            name = self.Name.get()
            today = self.Date.get()
            age = int(self.BD.get())
            B = int(self.selecGender())
            F = int(self.selecfbs())
            I = int(self.selecexang())
            C = int(self.seleccp())
            K = int(self.selecslope())
            G = int(self.restecg_combobox.get())
            L = int(self.ca_combobox.get())
            M = int(self.thal_combobox.get())
            D = int(self.trestbps.get())
            E = int(self.chol.get())
            H = int(self.thalach.get())
            J = int(self.oldpeak.get())
            prediction = int(self.prediction)

        except:
            messagebox.showerror("Message", "Missing data!!!")
            return
        db_manager = DatabaseManager(host='localhost', user='root', password='trinhtuantu1723@', database_name='Heart_Data')
        db_manager.connect()
        db_manager.create_tables()
        
        db_manager.save_data(name,today,int(age),int(B),int(C),int(D),int(E),int(F),int(G),int(H),int(I),int(J),int(K),int(L),int(M),prediction)
        db_manager.insert_recommendations(self.info_labels)
        
    def User(self):
        """
        Hiển thị thông tin của người dùng trong cửa sổ Profile.

        Hàm này thực hiện các bước sau:
        1. Tạo một cửa sổ con (Toplevel) để hiển thị thông tin người dùng.
        2. Tạo và định dạng các nhãn để hiển thị thông tin chi tiết của người dùng, bao gồm:
        - Tên, Ngày sinh, Tuổi, Giới tính,
        - Loại đau ngực, Huyết áp tĩnh, Lượng cholesterol, Đường huyết, 
        - Điện tâm đồ nghỉ, Tần suất nhịp tim, Viêm mạch do tập thể dục,
        - Sự giảm ST, Độ dốc của đoạn ST, Số mạch lớn, Kiểm tra căng thallium,
        - Kết quả dự đoán về mắc bệnh tim.
        3. Hiển thị các giá trị tương ứng với thông tin của người dùng.

        Returns:
            None

        Raises:
            None
        """
        user_window = tk.Toplevel(self.root)
        user_window.title("Profile")
        user_window.geometry("500x600")

        labels = [
            "Thông tin của bệnh nhân",
            "Name:", "Date:", "Age:", "Gender:",
            "cp - Loại đau ngực:", "trestbps - Huyết áp tĩnh:",
            "chol - Lượng cholesterol:", "fbs - Đường huyết:",
            "restecg - Điện tâm đồ nghỉ:", "thalach - Tần suất nhịp tim:",
            "exang - Viêm mạch do tập thể dục:", "oldpeak - Sự giảm ST:",
            "slope - Độ dốc của đoạn ST:", "ca - Số mạch lớn:",
            "thal - Kiểm tra căng thallium:", "Kết quả dự đoán:"
        ]
        
        for i, text in enumerate(labels):
            Label(user_window, text=text).grid(row=i, column=0, padx=10, pady=5, sticky="e")

        # Chuyển các thông tin thành mô tả
        name = self.Name.get()
        date = self.Date.get()
        age = self.BD.get()

        B = "Nam" if self.selecGender() == 1 else "Nữ"
        F = "Đường huyết nhanh hơn 120 mg/dl" if self.selecfbs() == 1 else "Đường huyết bình thường"
        I = "Viêm mạch do tập thể dục" if self.selecexang() == 1 else "Không có triệu chứng"
        
        cp_dict = {0: "0 = typical angina", 1: "1 = atypical angina", 2: "2 = non-anginal pain", 3: "3 = asymptomatic"}
        slope_dict = {0: "0 = upsloping", 1: "1 = flat", 2: "2 = downsloping"}
        restecg_dict = {0: "0 = normal", 1: "1 = having ST-T", 2: "2 = hypertrophy"}
        ca_dict = {0: "0: Không có barium sulfate.", 1: "1: Có một ít barium sulfate", 2: "2: Có một lượng lớn barium sulfate.", 3: "3: Có một lượng rất lớn barium sulfate."}
        thal_dict = {0: "0 = normal", 1: "1 = fixed defect", 2: "2 = reversable defect"}
        
        C = cp_dict[self.seleccp()]
        K = slope_dict[self.selecslope()]
        G = restecg_dict[int(self.restecg_combobox.get())]
        L = ca_dict[int(self.ca_combobox.get())]
        M = thal_dict[int(self.thal_combobox.get())]

        D = "Huyết áp thấp" if int(self.trestbps.get()) < 110 else "Bình thường" if int(self.trestbps.get()) < 130 else "Cao nhẹ" if int(self.trestbps.get()) < 140 else "Cao tương đối" if int(self.trestbps.get()) < 180 else "Cao nghiêm trọng"
        E = "Bình thường" if int(self.chol.get()) < 340 else "Có nguy cơ mắc bệnh tim mạch" if int(self.chol.get()) > 410 else "Bình thường"
        H = "Mạch đập nhanh" if int(self.thalach.get()) > 100 else "Mạch đập chậm" if int(self.thalach.get()) < 60 else "Bình thường"
        J = "Có nguy cơ mắc bệnh tim mạch" if int(self.oldpeak.get()) < 0 else "Bình thường"
        
        result = "Mắc bệnh tim" if self.prediction == 1 else "Không mắc bệnh tim"

        values = ["", name, date, age, B, C, D, E, F, G, H, I, J, K, L, M, result]
        
        for i, value in enumerate(values):
            Label(user_window, text=value).grid(row=i, column=1, padx=10, pady=5, sticky="w")
            
    def display_recommendations(self):
        """
        Hiển thị các khuyến cáo dựa trên kết quả dự đoán về bệnh tim.

        Parameters:
            self (object): Đối tượng của lớp chứa phương thức.

        Returns:
            None

        Ghi chú:
            Hàm này tạo một cửa sổ mới hoặc cửa sổ con để hiển thị các khuyến cáo liên quan đến sức khỏe tim mạch.
            Nếu dự đoán là mắc bệnh tim, hàm sẽ hiển thị các khuyến cáo cụ thể về kiểm tra sức khỏe, chế độ ăn uống, 
            tập thể dục, kiểm soát cân nặng, quản lý căng thẳng và các hành vi khác có lợi cho sức khỏe tim mạch.
            Nếu không mắc bệnh tim, hàm sẽ hiển thị thông báo cho biết sức khỏe đang ổn định và khuyến khích duy trì một lối sống lành mạnh.
        """
        # Tạo cửa sổ mới hoặc cửa sổ con
        recommendations_window = tk.Toplevel(self.root)
        recommendations_window.title("Recommendations")
        recommendations_window.geometry("1050x500")

        # Tạo và hiển thị các khuyến cáo
        recommendation_label = Label(recommendations_window, text="Dựa trên kết quả dự đoán, dưới đây là một số khuyến cáo", font="robot 19 bold")
        recommendation_label.pack()
        
        self.info_labels = [
            "1. Hãy thực hiện thường xuyên kiểm tra sức khỏe với bác sĩ chuyên khoa tim mạch.",
            
            "2. Tuân thủ chế độ ăn uống lành mạnh và tăng cường hoạt động thể chất.",
            
            "3. Tuân thủ liệu pháp và điều trị: Điều quan trọng nhất là tuân thủ đúng liệu pháp được chỉ định bởi bác sĩ.",
            
            "   Điều này có thể bao gồm việc sử dụng thuốc theo đúng hướng dẫn, tuân thủ chế độ ăn uống và tập thể dục phù hợp.",
            
            "4. Chế độ ăn uống lành mạnh: Hãy ăn ít chất béo bão hòa và cholesterol, hạn chế natri, đường và thức ăn chế biến.",
            
            "   Thêm vào đó, hãy tăng cường tiêu thụ rau củ, hoa quả, hạt và các nguồn protein lành mạnh như cá và gà.",
            
            "5. Tập thể dục: Thực hiện các hoạt động thể chất như đi bộ, đạp xe, bơi lội, yoga hoặc các bài tập aerobic nhẹ nhàng.",
            "   Tuy nhiên, trước khi bắt đầu bất kỳ chương trình tập luyện mới nào, hãy thảo luận với bác sĩ để đảm bảo rằng nó là phù hợp với tình trạng sức khỏe của bạn.",
            "6. Kiểm soát cân nặng: Đối với những người mắc bệnh tim, việc giữ cân nặng ở mức ổn định là rất quan trọng. ",
            "   Hãy tìm hiểu về chế độ ăn uống cân đối và duy trì một lối sống lành mạnh để giúp kiểm soát cân nặng.",
            "7. Quản lý căng thẳng: Căng thẳng có thể gây ra tăng huyết áp và tăng nguy cơ bệnh tim. ",
            "   Hãy tìm hiểu các kỹ thuật giảm căng thẳng như thiền, yoga, hoặc các phương pháp thư giãn khác để giúp giảm căng thẳng và cải thiện tâm trạng.",
            "8. Kiểm tra định kỳ: Điều này rất quan trọng để theo dõi tiến triển của bệnh tim và điều chỉnh liệu pháp khi cần thiết. ",
            "   Hãy đảm bảo bạn đến kiểm tra sức khỏe định kỳ theo hướng dẫn của bác sĩ.",
            "9. Hãy dừng hút thuốc: Hút thuốc lá là một trong những yếu tố rủi ro lớn đối với sức khỏe tim mạch. ",
            "   Nếu bạn hút thuốc, hãy tìm kiếm sự hỗ trợ để dừng lại.",
            "10. Hạn chế cồn: Uống rượu cồn có thể tăng nguy cơ bệnh tim. Hãy hạn chế tiêu thụ cồn hoặc tốt nhất là tránh hoàn toàn.",
            "11. Hãy giữ một tâm trạng tích cực: Tâm trạng tích cực có thể có lợi cho sức khỏe tim mạch. ",
            "    Hãy tìm kiếm sự hỗ trợ từ bạn bè, gia đình hoặc các nhóm hỗ trợ nếu cần.",
            
        ]

        if self.prediction == 1:  # Nếu dự đoán mắc bệnh tim
            for info_label_text in self.info_labels:
                Label(recommendations_window, text=info_label_text, font="TimesNewRoman 11", anchor="w").pack(fill="x")

        else:  # Nếu không mắc bệnh tim
            recommendation = tk.Label(recommendations_window, text="Sức khỏe đang ổn định. Hãy duy trì một lối sống lành mạnh.", font="TimesNewRoman 11")
            recommendation.pack()

        
    def export_to_pdf(self):
        """
        Xuất thông tin của người dùng ra file PDF.

        Hàm này thực hiện các bước sau:
        1. Kiểm tra xem người dùng đã đăng nhập chưa, nếu chưa thì kết thúc hàm.
        2. Tạo dữ liệu từ các thông tin của người dùng.
        3. Đăng ký font chữ và tạo file PDF.
        4. Lưu thông tin của người dùng vào file PDF và thông báo thành công.

        Returns:
            None

        Raises:
            None
        """
        if not self.check_login():
            return
        
        cp_dict = {0: "0 = typical angina", 1: "1 = atypical angina", 2: "2 = non-anginal pain", 3: "3 = asymptomatic"}
        slope_dict = {0: "0 = upsloping", 1: "1 = flat", 2: "2 = downsloping"}
        restecg_dict = {0: "0 = normal", 1: "1 = having ST-T", 2: "2 = hypertrophy"}
        ca_dict = {0: "0: Không có barium sulfate.", 1: "1: Có một ít barium sulfate", 2: "2: Có một lượng lớn barium sulfate.", 3: "3: Có một lượng rất lớn barium sulfate."}
        thal_dict = {0: "0 = normal", 1: "1 = fixed defect", 2: "2 = reversable defect"}
        
        data = {
            "name": self.Name.get(),
            "date": self.Date.get(),
            "age": self.BD.get(),
            "gender": "Nam" if self.selecGender() == 1 else "Nữ",
            "fbs": "Đường huyết nhanh hơn 120 mg/dl" if self.selecfbs() == 1 else "Đường huyết bình thường",
            "exang": "Viêm mạch do tập thể dục" if self.selecexang() == 1 else "Không có triệu chứng",
            "cp": cp_dict[self.seleccp()],
            "slope": slope_dict[self.selecslope()],
            "restecg": restecg_dict[int(self.restecg_combobox.get())],
            "ca": ca_dict[int(self.ca_combobox.get())],
            "thal": thal_dict[int(self.thal_combobox.get())],
            "trestbps": "Huyết áp thấp" if int(self.trestbps.get()) < 110 else "Bình thường" if int(self.trestbps.get()) < 130 else "Cao nhẹ" if int(self.trestbps.get()) < 140 else "Cao tương đối" if int(self.trestbps.get()) < 180 else "Cao nghiêm trọng",
            "chol": "Bình thường" if int(self.chol.get()) < 340 else "Có nguy cơ mắc bệnh tim mạch" if int(self.chol.get()) > 410 else "Bình thường",
            "thalach": "Mạch đập nhanh" if int(self.thalach.get()) > 100 else "Mạch đập chậm" if int(self.thalach.get()) < 60 else "Bình thường",
            "oldpeak": "Có nguy cơ mắc bệnh tim mạch" if int(self.oldpeak.get()) < 0 else "Bình thường",
            "result": "Mắc bệnh tim" if int(self.prediction) == 1 else "Không mắc bệnh tim",
        }
        
        arial_path = "C:\\Windows\\Fonts\\arial.ttf"

        # Đăng ký các font chữ
        pdfmetrics.registerFont(TTFont('Arial', arial_path))

        # Tạo tên file PDF
        base_pdf_file_path = "user_info.pdf"
        pdf_file_path = base_pdf_file_path

        # Nếu file tồn tại, tạo tên file mới
        if os.path.exists(pdf_file_path):
            i = 0
            while os.path.exists(pdf_file_path):
                pdf_file_path = f"user_info_{data['name']}_{i}.pdf"
                i += 1
                
        c = canvas.Canvas(pdf_file_path, pagesize=letter)
        c.setFont('Arial', 12)

        y = 750
        for key, value in data.items():
            c.drawString(100, y, f"{key}: {value}")
            y -= 20

        c.save()

        # Hiển thị thông báo
        messagebox.showinfo("Xuất PDF", f"Thông tin người dùng đã được xuất ra file: {pdf_file_path}")
        
    


if __name__ == "__main__":
    # Tạo một cửa sổ gốc Tkinter
    root = tk.Tk()
    
    # Khởi tạo ứng dụng dự đoán bệnh tim và gắn với cửa sổ gốc
    HeartDiseasePredictionApp(root)
    
    # Mở cửa sổ và chờ các sự kiện từ người dùng
    root.mainloop()


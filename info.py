from tkinter import *

class InfoData:
    """
    Class để hiển thị thông tin dataset.

    Attributes:
        icon_info (Toplevel): Cửa sổ để hiển thị thông tin.
    
    Phương thức:
    __init__(self): Khởi tạo đối tượng InfoData và thiết lập giao diện người dùng.
    setup_ui(self): Thiết lập giao diện người dùng cho cửa sổ thông tin.
    """
    def __init__(self):
        """
        Khởi tạo đối tượng InfoData và thiết lập giao diện người dùng.
        """
        self.icon_info = Toplevel()
        self.icon_info.title("info")
        self.icon_info.geometry("700x700+400+100")
        self.setup_ui()

    def setup_ui(self):
        """
        Thiết lập giao diện người dùng cho cửa sổ thông tin.

        Gồm các bước sau:
        1. Thiết lập biểu tượng cho cửa sổ.
        2. Tạo khung chứa thông tin.
        3. Hiển thị tiêu đề.
        4. Hiển thị các nhãn thông tin về dataset.

        Returns:
            None
        """
        icon_image = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\info.png")
        self.icon_info.iconphoto(False, icon_image)

        info_frame = Frame(self.icon_info)
        info_frame.pack(padx=20, pady=20, anchor="n")

        heading_label = Label(info_frame, text="Infomation Related to Dataset", font="robot 19 bold")
        heading_label.pack()

        info_labels = [
            "age -  Độ tuổi của bệnh nhân.",
            "sex - Giới tính của bệnh nhân, với 1 là nam và 0 là nữ.",
            "cp (chest pain type): Loại đau ngực mà bệnh nhân trải qua, với các giá trị sau:",
            "        0 = typical angina (0: Đau thắt ngực điển hình);",
            "        1 = atypical angina (1: Đau thắt ngực không điển hình); ",
            "        2 = non-anginal pain (2: Đau không phải thắt ngực); ",
            "        3 = asymptomatic (3: Không có triệu chứng)",
            "trestbps - Huyết áp tĩnh của bệnh nhân khi được nhập viện, được đo bằng mmHg.",
            "chol - Lượng cholesterol trong huyết thanh của bệnh nhân, được đo bằng mg/dl.",
            "fbs - Đường huyết nhanh trong máu sau khi nhận dạng nhanh hơn 120 mg/dl, với 1 là đúng và 0 là sai.",
            "restecg - Kết quả điện tâm đồ nghỉ của bệnh nhân, với các giá trị sau:",
            "         0 = normal (0: Bình thường);",
            "         1 = having ST-T (1: Có biểu hiện ST-T); ",
            "         2 = hypertrophy (2: Tăng thể)",
            "thalach - Tần suất nhịp tim tối đa đạt được.",
            "exang - Viêm mạch do tập thể dục gây ra, với 1 là có và 0 là không.",
            "oldpeak - Sự giảm ST do tập luyện so với nghỉ.",
            "slope - Độ dốc của đoạn ST cao nhất sau khi tập thể dục, với các giá trị sau:",
            "         0 = upsloping (0: Lên dốc); ",
            "         1 = flat (1: Bằng phẳng); ",
            "         2 = downsloping (2: Xuống dốc)",
            "ca - Số mạch lớn được nhuộm bằng flourosopy, trong khoảng từ 0 đến 3.",
            "thal - Kết quả của kiểm tra căng thể Thallium, với các giá trị sau:",
            "         0 = normal (0: Bình thường); ",
            "         1 = fixed defect (1: Hỏng cố định); ",
            "         2 = reversable defect (2: Hỏng có thể đảo ngược)"
        ]

        for info_label_text in info_labels:
            Label(info_frame, text=info_label_text, font="TimesNewRoman 11", anchor="w").pack(fill="x")

        self.icon_info.mainloop()

def Info():
    """
    Hiển thị cửa sổ thông tin về dataset.

    Returns:
        None
    """
    info_window = InfoData()
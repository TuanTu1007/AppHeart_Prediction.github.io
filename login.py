from tkinter import *
from tkinter import messagebox
import mysql.connector as mySQL

class LoginForm:
    """
    Lớp LoginForm chịu trách nhiệm tạo và hiển thị form đăng nhập.

    Thuộc tính:
        callback (function): Hàm callback được gọi khi người dùng đăng nhập thành công.
        limit (int): Giới hạn số lần thử đăng nhập không thành công.
        root (Toplevel): Cửa sổ Toplevel cho form đăng nhập.

    Phương thức:
        __init__(self, callback): Khởi tạo form đăng nhập với các thuộc tính và thiết lập giao diện người dùng.
        setup_ui(self): Thiết lập giao diện người dùng cho form đăng nhập.
        setup_entries(self): Thiết lập các ô nhập liệu cho tên người dùng và mật khẩu.
        setup_buttons(self): Thiết lập các nút bấm cho form đăng nhập.
        enter_user(self, e): Xóa văn bản mặc định trong ô nhập liệu tên người dùng khi có sự kiện focus.
        leave_user(self, e): Đặt lại văn bản mặc định trong ô nhập liệu tên người dùng khi mất sự kiện focus nếu trống.
        enter_passwd(self, e): Xóa văn bản mặc định và thiết lập chế độ hiển thị mật khẩu khi có sự kiện focus.
        leave_passwd(self, e): Đặt lại văn bản mặc định trong ô nhập liệu mật khẩu khi mất sự kiện focus nếu trống.
        signup(self): Chuyển sang form đăng ký.
        login_user(self): Xử lý đăng nhập người dùng.
        limit_login(self): Giới hạn số lần thử đăng nhập không thành công.
    """
    def __init__(self, callback):
        """
        Khởi tạo một instance của LoginForm.

        Hàm này thiết lập hàm callback, giới hạn số lần thử đăng nhập, tạo cửa sổ Toplevel cho form
        đăng nhập và gọi hàm thiết lập giao diện người dùng.

        Args:
            callback (function): Hàm callback được gọi khi người dùng đăng nhập thành công.
        """
        self.callback = callback
        self.limit = 0
        self.root = Toplevel()
        self.root.title("Login")
        self.root.geometry("925x500+300+200")
        self.root.configure(bg="#fff")
        self.setup_ui()

    def setup_ui(self):
        """
        Thiết lập giao diện người dùng cho form đăng nhập.

        Hàm này thiết lập các thành phần giao diện người dùng bao gồm hình ảnh nền, biểu tượng,
        khung chứa form đăng nhập, nhãn tiêu đề, nhãn thông báo lỗi, và gọi các hàm để thiết lập
        các ô nhập liệu và nút bấm.
        """
        self.image = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\login0.png")
        Label(self.root, image=self.image, bg="white").place(x=50, y=50)

        self.image_icon = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\login.png")
        self.root.iconphoto(False, self.image_icon)

        self.frame = Frame(self.root, width=350, height=350, bg="white")
        self.frame.place(x=480, y=70)

        heading = Label(self.frame, text="Log in", fg="#57a1f8", bg="white", font=("Microsoft YaHei UI Light", 23, "bold"))
        heading.place(x=100, y=5)

        self.error_label = Label(self.frame, text="", fg="red", bg="white")
        self.error_label.place(x=120, y=250)

        self.setup_entries()
        self.setup_buttons()

    def setup_entries(self):
        """
        Thiết lập các ô nhập liệu cho tên người dùng và mật khẩu.

        Hàm này tạo ra các ô nhập liệu cho tên người dùng và mật khẩu, đặt chúng ở các vị trí xác định
        trong khung chứa và thiết lập các sự kiện focus vào và ra cho các ô nhập liệu.
        """
        self.user = Entry(self.frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        self.user.place(x=30, y=80)
        self.user.insert(0, "Username")
        self.user.bind("<FocusIn>", self.enter_user)
        self.user.bind("<FocusOut>", self.leave_user)
        Frame(self.frame, width=295, height=2, bg="black").place(x=25, y=107)

        self.passwd = Entry(self.frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11), show="*")
        self.passwd.place(x=30, y=150)
        self.passwd.insert(0, "Password")
        self.passwd.bind("<FocusIn>", self.enter_passwd)
        self.passwd.bind("<FocusOut>", self.leave_passwd)
        Frame(self.frame, width=295, height=2, bg="black").place(x=25, y=177)

    def setup_buttons(self):
        """
        Thiết lập các nút bấm cho form đăng nhập.

        Hàm này tạo ra nút "Log in" để đăng nhập và nút "Sign Up" để chuyển sang form đăng ký,
        và đặt chúng ở các vị trí xác định trong khung chứa.
        """
        Button(self.frame, width=39, pady=7, text="Log in", cursor="hand2", bg="#57a1f8", fg="white", border=0, command=self.login_user).place(x=35, y=204)
        Label(self.frame, text="Don't have account?", fg="black", bg="white", font=("Microsoft YaHei UI Light", 9)).place(x=75, y=270)
        Button(self.frame, width=6, text="Sign Up", border=0, bg="white", cursor="hand2", fg="#57a1f8", command=self.signup).place(x=215, y=270)

    def enter_user(self, e):
        """
        Xóa văn bản mặc định trong ô nhập liệu tên người dùng khi có sự kiện focus.

        Args:
            e (Event): Sự kiện focus.
        """
        self.user.delete(0, 'end')

    def leave_user(self, e):
        """
        Đặt lại văn bản mặc định trong ô nhập liệu tên người dùng khi mất sự kiện focus nếu trống.

        Args:
            e (Event): Sự kiện mất focus.
        """
        if not self.user.get():
            self.user.insert(0, "Username")

    def enter_passwd(self, e):
        """
        Xóa văn bản mặc định và thiết lập chế độ hiển thị mật khẩu khi có sự kiện focus.

        Args:
            e (Event): Sự kiện focus.
        """
        self.passwd.delete(0, 'end')
        self.passwd.config(show="*")

    def leave_passwd(self, e):
        """
        Đặt lại văn bản mặc định trong ô nhập liệu mật khẩu khi mất sự kiện focus nếu trống.

        Args:
            e (Event): Sự kiện mất focus.
        """
        if not self.passwd.get():
            self.passwd.insert(0, "Password")

    def signup(self):
        """
        Chuyển sang form đăng ký.

        Hàm này đóng cửa sổ hiện tại và mở form đăng ký mới.
        """
        self.root.destroy()
        # Delay the import of SignUp
        import SignUp
        SignUp.Sign_Up(self.callback)

    def login_user(self):
        """
        Xử lý đăng nhập người dùng.

        Hàm này lấy thông tin từ các ô nhập liệu, kiểm tra tính hợp lệ của thông tin và thực hiện
        kiểm tra thông tin đăng nhập trong cơ sở dữ liệu. Nếu thông tin không hợp lệ hoặc sai, hiển thị
        thông báo lỗi và giới hạn số lần thử đăng nhập.
        """
        self.error_label.config(text="")
        username = self.user.get()
        password = self.passwd.get()

        if (username == "" or username == "Username") or (password == "" or password == "Password"):
            self.error_label.config(text="Hãy nhập đủ thông tin!!!")
        else:
            try:
                mydb = mySQL.connect(host='localhost', user='root', password='trinhtuantu1723@', database="heart_data")
                mycursor = mydb.cursor()
                print("Connect Successed!!!")
            except:
                self.error_label.config(text="Database Failed!!!")
                return

            command = "USE Heart_Data"
            mycursor.execute(command)

            command = "select * from login where Username = %s and Password = %s"
            mycursor.execute(command, (username, password))
            myresult = mycursor.fetchone()
            if myresult is None:
                self.error_label.config(text="Sai tài khoản hoặc mật khẩu!!!")
                self.limit_login()
            else:
                self.root.destroy()
                self.callback(True, username)

    def limit_login(self):
        """
        Giới hạn số lần thử đăng nhập không thành công.

        Hàm này tăng biến đếm số lần thử đăng nhập không thành công. Nếu số lần thử vượt quá 3, hiển thị
        thông báo và đóng cửa sổ đăng nhập.
        """
        self.limit += 1
        if self.limit == 3:
            messagebox.showinfo("Thông báo", "Nhập sai thông tin tài khoản quá 3 lần!!!")
            self.root.destroy()

def Login_Form(callback):
    """
    Khởi tạo và hiển thị form đăng nhập.

    Hàm này tạo ra một instance của lớp LoginForm và gọi hàm khởi tạo của nó.

    Args:
        callback (function): Hàm callback được gọi khi người dùng đăng nhập thành công.
    """
    LoginForm(callback)

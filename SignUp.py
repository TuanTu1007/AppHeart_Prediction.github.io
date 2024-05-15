from tkinter import *
import ast 
from login import *
from login import LoginForm

class SignUpForm(LoginForm):
    """
    Lớp SignUpForm chịu trách nhiệm tạo và hiển thị form đăng ký người dùng.

    Attributes:
        callback (function): Hàm gọi lại khi đăng ký thành công.
        root (Toplevel): Cửa sổ Toplevel cho form đăng ký.
        
    Phương thức:
    __init__(self, callback): Phương thức khởi tạo, tạo một đối tượng SignUpForm với callback như một tham số.
    setup_ui(self): Thiết lập giao diện người dùng cho form đăng ký.
    setup_entries(self): Thiết lập các ô nhập liệu cho tên người dùng, mật khẩu và xác nhận mật khẩu.
    setup_buttons(self): Thiết lập các nút bấm cho form đăng ký.
    create_entry(self, placeholder, y, show=None): Tạo một ô nhập liệu với placeholder và vị trí xác định.
    login_form(self): Chuyển sang form đăng nhập.
    signup_user(self): Xử lý đăng ký người dùng.
    """
    def __init__(self, callback):
        """
        Khởi tạo một đối tượng SignUpForm.

        Args:
            callback: Hàm gọi lại khi đăng ký thành công.
        """
        self.callback = callback
        self.root = Toplevel()
        self.root.title("Sign Up")
        self.root.geometry("925x500+300+200")
        self.root.configure(bg="#fff")
        self.setup_ui()

    def setup_ui(self):
        """
        Thiết lập giao diện người dùng cho form đăng ký.

        Hàm này thiết lập các thành phần giao diện người dùng bao gồm hình ảnh nền, biểu tượng,
        khung chứa form đăng ký, nhãn tiêu đề, nhãn thông báo lỗi, và gọi các hàm để thiết lập
        các ô nhập liệu và nút bấm.
        """
        self.image = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\signup.png")
        Label(self.root, image=self.image, bg="white").place(x=50, y=100)

        self.image_icon = PhotoImage(file=r"D:\Subject\IE221_Python\DoAn\Images\login.png")
        self.root.iconphoto(False, self.image_icon)

        self.frame = Frame(self.root, width=350, height=350, bg="white")
        self.frame.place(x=480, y=70)

        heading = Label(self.frame, text="Sign up", fg="#57a1f8", bg="white", font=("Microsoft YaHei UI Light", 23, "bold"))
        heading.place(x=100, y=5)

        self.error_label = Label(self.frame, text="", fg="red", bg="white")
        self.error_label.place(x=40, y=250)

        self.setup_entries()
        self.setup_buttons()

    def setup_entries(self):
        """
        Thiết lập các ô nhập liệu cho tên người dùng, mật khẩu và xác nhận mật khẩu.

        Hàm này tạo ra các ô nhập liệu cho tên người dùng, mật khẩu và xác nhận mật khẩu,
        và đặt chúng ở các vị trí xác định trong khung chứa.
        """
        self.user = self.create_entry("Username", 80)
        self.passwd = self.create_entry("Password", 150, show="*")
        self.c_passwd = self.create_entry("Password", 220, show="*")

    def setup_buttons(self):
        """
        Thiết lập các nút bấm cho form đăng ký.

        Hàm này tạo ra nút "Sign up" để đăng ký và nút "Sign In" để chuyển sang form đăng nhập,
        và đặt chúng ở các vị trí xác định trong khung chứa.
        """
        Button(self.frame, width=39, pady=7, text="Sign up", cursor="hand2", bg="#57a1f8", fg="white", border=0, command=self.signup_user).place(x=35, y=274)
        Label(self.frame, text="I have an account?", fg="black", bg="white", font=("Microsoft YaHei UI Light", 9)).place(x=75, y=320)
        Button(self.frame, width=6, text="Sign In", border=0, bg="white", cursor="hand2", fg="#57a1f8", command=self.login_form).place(x=215, y=320)

    def create_entry(self, placeholder, y, show=None):
        """
        Tạo một ô nhập liệu với placeholder và vị trí xác định.

        Hàm này tạo ra một ô nhập liệu với placeholder, đặt vị trí của ô trên khung chứa và thiết lập
        các sự kiện focus vào và ra cho ô nhập liệu.

        Args:
            placeholder (str): Văn bản hiển thị mặc định trong ô nhập liệu.
            y (int): Vị trí theo trục y để đặt ô nhập liệu.
            show (str, optional): Ký tự để hiển thị thay cho ký tự nhập vào.

        Returns:
            Entry: Ô nhập liệu đã được tạo.
        """
        def enter(e):
            entry.delete(0, 'end')
            if show:
                entry.config(show=show)

        def leave(e):
            if entry.get() == '':
                entry.insert(0, placeholder)
                if show:
                    entry.config(show="")

        entry = Entry(self.frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        entry.place(x=30, y=y)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", enter)
        entry.bind("<FocusOut>", leave)
        Frame(self.frame, width=295, height=2, bg="black").place(x=25, y=y + 27)
        return entry

    def login_form(self):
        """
        Chuyển sang form đăng nhập.

        Hàm này đóng cửa sổ hiện tại và mở form đăng nhập mới.
        """
        self.root.destroy()
        LoginForm(self.callback)

    def signup_user(self):
        """
        Xử lý đăng ký người dùng.

        Hàm này lấy thông tin từ các ô nhập liệu, kiểm tra tính hợp lệ của thông tin và thực hiện
        đăng ký người dùng vào cơ sở dữ liệu. Nếu có lỗi xảy ra, hiển thị thông báo lỗi tương ứng.
        """
        username = self.user.get()
        password = self.passwd.get()
        c_password = self.c_passwd.get()
        self.error_label.config(text="")
        try:
            mydb = mySQL.connect(host='localhost', user='root', password='trinhtuantu1723@', database="heart_data")
            mycursor = mydb.cursor()
            print("Connect Successed!!!")
            mycursor.execute("use heart_data")
            if (username == "" or username == "Username") or (password == "" or password == "Password"):
                self.error_label.config(text="Hãy nhập đủ thông tin!!!")
            elif c_password != password:
                self.error_label.config(text="Xác nhận mật khẩu không đúng!!!")
            else:
                command = "insert into login(Username,Password) values(%s,%s)"
                mycursor.execute(command, (username, password))

                mydb.commit()
                mydb.close()
                messagebox.showinfo("ĐĂNG KÝ", "Đăng ký thành công!!!")
                self.root.destroy()
                LoginForm(self.callback)

        except Exception as e:
            if e.errno == mySQL.errorcode.ER_DUP_ENTRY:
                self.error_label.config(text="Tên người dùng đã tồn tại, vui lòng chọn tên khác!!!")
            else:
                messagebox.showerror("Error", f"MySQL Error: {e.msg}")
            mydb.rollback()
        finally:
            mydb.close()

def Sign_Up(callback):
    """
    Khởi tạo và hiển thị form đăng ký.

    Hàm này tạo ra một instance của lớp SignUpForm và hiển thị nó.

    Args:
        callback (function): Hàm callback được gọi khi người dùng đăng ký thành công.
    """
    SignUpForm(callback)
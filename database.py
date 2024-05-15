import mysql.connector as mySQL
from tkinter import messagebox

class DatabaseManager:
    """
    class này quản lý cơ sở dữ liệu
    
    Attributes:
            host (str): Địa chỉ host của cơ sở dữ liệu.
            user (str): Tên người dùng để truy cập cơ sở dữ liệu.
            password (str): Mật khẩu để truy cập cơ sở dữ liệu.
            database_name (str): Tên cơ sở dữ liệu.
            connection: Kết nối đến cơ sở dữ liệu.
            cursor: Con trỏ để thực hiện các truy vấn SQL.
            
    Phương thức:
    __init__(self, host, user, password, database_name): Phương thức khởi tạo một đối tượng DatabaseManager 
    và thiết lập các thuộc tính cơ bản như host, user, password, database_name, connection, và cursor.
    connect(self): Phương thức này kết nối đến cơ sở dữ liệu MySQL sử dụng thông tin được cung cấp.
    create_tables(self): Phương thức này tạo các bảng trong cơ sở dữ liệu nếu chúng chưa tồn tại.
    save_data(self, name, today, age, B2, C2, D2, E2, F2, G2, H2, I2, J2, K2, L2, M2, result): Phương thức này lưu thông tin của một bệnh nhân vào cơ sở dữ liệu.
    login(self, username, password): Phương thức này thêm một tài khoản người dùng mới vào cơ sở dữ liệu.
    close_connection(self): Phương thức này đóng kết nối với cơ sở dữ liệu.
    """
    def __init__(self, host, user, password, database_name):
        """
        Khởi tạo một đối tượng DatabaseManager.

        Args:
            host (str): Địa chỉ host của cơ sở dữ liệu.
            user (str): Tên người dùng để truy cập cơ sở dữ liệu.
            password (str): Mật khẩu để truy cập cơ sở dữ liệu.
            database_name (str): Tên cơ sở dữ liệu.

        Returns:
            None
        """
        self.host = host
        self.user = user
        self.password = password
        self.database_name = database_name
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Kết nối đến cơ sở dữ liệu.

        Raises:
            messagebox.showerror: Hiển thị thông báo lỗi nếu kết nối không thành công.

        Returns:
            None
        """
        try:
            self.connection = mySQL.connect(host=self.host, user=self.user, password=self.password)
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_name}")
            self.cursor.execute(f"USE {self.database_name}")
            print("Connection Successed")
        except mySQL.Error as e:
            messagebox.showerror("Error", f"Connection Failed: {e.msg}")

    def create_tables(self):
        """
        Tạo các bảng trong cơ sở dữ liệu nếu chúng chưa tồn tại.

        Returns:
            None
        """
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS data (
                    user INT AUTO_INCREMENT PRIMARY KEY not null,
                    Name VARCHAR(50) NOT NULL,
                    Date VARCHAR(100),
                    BD INT,
                    sex VARCHAR(10),
                    cp VARCHAR(50),
                    trestbps VARCHAR(50),
                    chol VARCHAR(50),
                    fbs VARCHAR(50),
                    restecg VARCHAR(50),
                    thalach VARCHAR(50),
                    exang VARCHAR(50),
                    oldpeak VARCHAR(50),
                    slope VARCHAR(50),
                    ca VARCHAR(50),
                    thal VARCHAR(50),
                    result VARCHAR(50)
                )
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS login (
                    user INT AUTO_INCREMENT PRIMARY KEY not null,
                    Username varchar(50) UNIQUE,
                    Password varchar(50)
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS recommendations
                    (id INT AUTO_INCREMENT PRIMARY KEY,
                    recommendation TEXT)
            """)
            self.connection.commit()
        except mySQL.Error as e:
            messagebox.showerror("Error", f"MySQL Error: {e.msg}")
            self.connection.rollback()

    def save_data(self, name, today, age, B2, C2, D2, E2, F2, G2, H2, I2, J2, K2, L2, M2, result):
        """
        Lưu thông tin của một bệnh nhân vào cơ sở dữ liệu.

        Args:
            name: Tên của bệnh nhân.
            today: Ngày.
            age: Tuổi của bệnh nhân.
            B2: Giới tính của bệnh nhân.
            C2: Loại đau ngực.
            D2: Huyết áp tĩnh.
            E2: Lượng cholesterol.
            F2: Đường huyết.
            G2: Điện tâm đồ nghỉ.
            H2: Tần suất nhịp tim.
            I2: Viêm mạch do tập thể dục.
            J2: Sự giảm ST.
            K2: Độ dốc của đoạn ST.
            L2: Số mạch lớn.
            M2: Kiểm tra căng thallium.
            result: Kết quả dự đoán.

        Returns:
            None
        """
        try:
            insert_query = """
                INSERT INTO data (Name, Date, BD, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            insert_data = (name, today, age, B2, C2, D2, E2, F2, G2, H2, I2, J2, K2, L2, M2, result)
            self.cursor.execute(insert_query, insert_data)
            self.connection.commit()
            messagebox.showinfo("Thêm bệnh nhân", "Thêm một bệnh nhân mới thành công")
        except mySQL.Error as e:
            messagebox.showerror("Error", f"MySQL Error: {e.msg}")
            self.connection.rollback()
            
    def insert_recommendations(self, recommendations):
        """
        Chèn các khuyến cáo vào bảng cơ sở dữ liệu.

        Parameters:
            cursor: Đối tượng con trỏ của MySQL.
            recommendations (list): Danh sách các khuyến cáo cần chèn vào cơ sở dữ liệu.
        """
        try:
            for recommendation in recommendations:
                self.cursor.execute("INSERT INTO recommendations (recommendation) VALUES (%s)", (recommendation,))
            self.connection.commit()
            messagebox.showinfo("Lưu khuyến cáo", "Lưu khuyến cáo thành công")
        except mySQL.Error as e:
            messagebox.showerror("Error", f"MySQL Error: {e.msg}")
            self.connection.rollback()
        

    def login(self, username, password):
        """
        Thêm một tài khoản người dùng mới vào cơ sở dữ liệu.

        Args:
            username: Tên người dùng.
            password: Mật khẩu.

        Returns:
            None
        """
        self.create_tables
        try:
            insert_query = """
                INSERT INTO login (Username, Password)
                VALUES (%s, %s)
            """
            insert_data = (username, password)
            self.cursor.execute(insert_query, insert_data)
            self.connection.commit()
            messagebox.showinfo("Đăng ký người dùng", "Người dùng mới đã được thêm thành công")
        except mySQL.Error as e:
            messagebox.showerror("Error", f"MySQL Error: {e.msg}")
            self.connection.rollback()

    def close_connection(self):
        """
        Đóng kết nối với cơ sở dữ liệu.

        Returns:
            None
        """
        if self.connection:
            self.connection.close()
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

class HeartDiseasePredictor:
    """
    Lớp này dùng để dự đoán bệnh tim dựa trên dữ liệu từ tệp CSV.

    Thuộc tính:
    - data: Dữ liệu gốc từ tệp CSV.
    - data_no_outlier: Dữ liệu đã loại bỏ các giá trị ngoại lai.
    - numeric_columns: Các cột số trong dữ liệu.
    - nominal_columns: Các cột nominal trong dữ liệu.
    - age_group_mapping: nhóm tuổi thành các giá trị số.
    - bloodp_mapping: nhóm huyết áp thành các giá trị số.
    - chol_mapping: nhóm cholesterol thành các giá trị số.
    - scaler: Bộ chuẩn hóa dữ liệu MinMaxScaler.
    - ohc: Bộ mã hóa OneHotEncoder cho các cột nominal.
    - model: Mô hình phân loại RandomForestClassifier.
    
    Phương thức:
    - __init__(self, data_path): Khởi tạo đối tượng HeartDiseasePredictor.
    - remove_outliers_iqr(self, column_name, lower_bound_factor=1.5, upper_bound_factor=1.5): Loại bỏ các giá trị ngoại lai trong cột dữ liệu dựa trên phương pháp IQR.
    - assign_age_group(self, age): Phân nhóm tuổi dựa trên giá trị tuổi.
    - categorize_blood_pressure(self, resting_blood_pressure): Phân loại nhóm huyết áp dựa trên giá trị huyết áp nghỉ ngơi.
    - categorize_cholesterol(self, cholesterol): Phân loại nhóm cholesterol dựa trên giá trị cholesterol.
    - preprocess_data(self): Tiền xử lý dữ liệu bao gồm loại bỏ giá trị ngoại lai, chuẩn hóa dữ liệu số, mã hóa các biến nominal và biến hạng.
    - train_model(self): Huấn luyện mô hình RandomForestClassifier trên dữ liệu đã tiền xử lý.
    - preprocess_new_data(self, new_data): Tiền xử lý dữ liệu mới để dự đoán.
    """
    def __init__(self, data_path):
        """
        Khởi tạo đối tượng HeartDiseasePredictor.

        Tham số:
        - data_path: Đường dẫn đến tệp CSV chứa dữ liệu.
        """
        self.data = pd.read_csv(data_path)
        self.data_no_outlier = self.data.copy()
        self.numeric_columns = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'slope', 'ca']
        self.nominal_columns = ['cp', 'restecg', 'thal']
        self.age_group_mapping = {'Young': 0, 'Middle-aged': 1, 'Elderly': 2, 'Very Elderly': 3}
        self.bloodp_mapping = {'Low': 0, 'Normal': 1, 'High': 2}
        self.chol_mapping = {'Desirable': 0, 'Borderline High': 1, 'High': 2}
        self.scaler = MinMaxScaler()
        self.ohc = OneHotEncoder(sparse_output=False, drop='first')
        self.model = RandomForestClassifier()

    def remove_outliers_iqr(self, column_name, lower_bound_factor=1.5, upper_bound_factor=1.5):
        """
        Loại bỏ các giá trị ngoại lai trong cột dữ liệu dựa trên phương pháp IQR.

        Tham số:
        - column_name: Tên cột cần loại bỏ giá trị ngoại lai.
        - lower_bound_factor: Hệ số cho cận dưới của IQR.
        - upper_bound_factor: Hệ số cho cận trên của IQR.
        """
        Q1 = self.data_no_outlier[column_name].quantile(0.25)
        Q3 = self.data_no_outlier[column_name].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - lower_bound_factor * IQR
        upper_bound = Q3 + upper_bound_factor * IQR
        self.data_no_outlier = self.data_no_outlier[(self.data_no_outlier[column_name] >= lower_bound) & (self.data_no_outlier[column_name] <= upper_bound)]


    def assign_age_group(self, age):
        """
        Phân nhóm tuổi dựa trên giá trị tuổi.

        Tham số:
        - age: Tuổi của bệnh nhân.

        Trả về:
        - Nhóm tuổi tương ứng.
        """
        age_groups = {
            (0, 40): 'Young',
            (41, 60): 'Middle-aged',
            (61, 80): 'Elderly',
            (81, float('inf')): 'Very Elderly'
        }
        for age_range, group in age_groups.items():
            if age_range[0] <= age <= age_range[1]:
                return group

    def categorize_blood_pressure(self, resting_blood_pressure):
        """
        Phân loại nhóm huyết áp dựa trên giá trị huyết áp nghỉ ngơi.

        Tham số:
        - resting_blood_pressure: Giá trị huyết áp nghỉ ngơi.

        Trả về:
        - Nhóm huyết áp tương ứng.
        """
        if resting_blood_pressure < 90:
            return "Low"
        elif 90 <= resting_blood_pressure <= 120:
            return "Normal"
        else:
            return "High"

    def categorize_cholesterol(self, cholesterol):
        """
        Phân loại nhóm cholesterol dựa trên giá trị cholesterol.

        Tham số:
        - cholesterol: Giá trị cholesterol.

        Trả về:
        - Nhóm cholesterol tương ứng.
        """
        if cholesterol < 200:
            return "Desirable"
        elif 200 <= cholesterol <= 239:
            return "Borderline High"
        else:
            return "High"
    
    def preprocess_data(self):
        """
        Tiền xử lý dữ liệu bao gồm: loại bỏ giá trị ngoại lai, chuẩn hóa dữ liệu số,
        mã hóa các biến nominal và biến hạng.

        Hàm này thực hiện các bước sau:
        1. Loại bỏ giá trị ngoại lai cho các biến số.
        2. Chuẩn hóa dữ liệu số sử dụng phép chia tỷ lệ.
        3. Mã hóa biến nominal và biến hạng thành dạng số.
        4. Ghép các DataFrame sau xử lý thành một DataFrame duy nhất.

        Returns:
            None

        Raises:
            None
        """
        for column in self.numeric_columns:
            self.remove_outliers_iqr(column)
        
        self.data_no_outlier.reset_index(inplace=True, drop=True)
        numeric_df = self.data_no_outlier[self.numeric_columns]
        numeric_scaled_df = pd.DataFrame(self.scaler.fit_transform(numeric_df), columns=self.scaler.get_feature_names_out())
        self.data_no_outlier[self.numeric_columns] = numeric_scaled_df

        self.data_no_outlier['age_group'] = self.data_no_outlier['age'].apply(self.assign_age_group)
        self.data_no_outlier['blood_pressure_group'] = self.data_no_outlier['trestbps'].apply(self.categorize_blood_pressure)
        self.data_no_outlier['cholestoral_group'] = self.data_no_outlier['chol'].apply(self.categorize_cholesterol)

        dummies_df = pd.DataFrame(self.ohc.fit_transform(self.data_no_outlier[self.nominal_columns]), columns=self.ohc.get_feature_names_out())
        ordinal_df = pd.DataFrame({
            'age_group': self.data_no_outlier['age_group'].map(self.age_group_mapping),
            'blood_pressure': self.data_no_outlier['blood_pressure_group'].map(self.bloodp_mapping),
            'cholesterol_group': self.data_no_outlier['cholestoral_group'].map(self.chol_mapping)
        })

        self.last_data = pd.concat([numeric_scaled_df, dummies_df, ordinal_df, self.data_no_outlier[['sex', 'fbs', 'exang', 'target']]], axis=1)

    def train_model(self):
        """
        Huấn luyện mô hình RandomForestClassifier trên dữ liệu đã tiền xử lý.

        Hàm này thực hiện các bước sau:
        1. Tách dữ liệu thành các tập huấn luyện và kiểm tra.
        2. Tiến hành huấn luyện mô hình RandomForestClassifier trên tập huấn luyện.

        Returns:
            None

        Raises:
            None
        """
        X = self.last_data.drop('target', axis=1)
        y = self.last_data['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.3, random_state=42)
        self.model.fit(X_train, y_train)

    def preprocess_new_data(self, new_data):
        """
        Tiền xử lý dữ liệu mới để dự đoán.

        Tham số:
        - new_data: Dữ liệu mới dưới dạng danh sách.

        Trả về:
        - Dữ liệu mới đã tiền xử lý.
        """
        new_data_dict = {
            'age': [new_data[0]],
            'sex': [new_data[1]],
            'cp': [new_data[2]],
            'trestbps': [new_data[3]],
            'chol': [new_data[4]],
            'fbs': [new_data[5]],
            'restecg': [new_data[6]],
            'thalach': [new_data[7]],
            'exang': [new_data[8]],
            'oldpeak': [new_data[9]],
            'slope': [new_data[10]],
            'ca': [new_data[11]],
            'thal': [new_data[12]]
        }
        df = pd.DataFrame(new_data_dict)
        numeric_columns = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'slope', 'ca']
        numeric_scaled_df_new_data = pd.DataFrame(self.scaler.transform(df[numeric_columns]), columns=numeric_columns)

        df['age_group'] = df['age'].apply(self.assign_age_group)
        df['blood_pressure_group'] = df['trestbps'].apply(self.categorize_blood_pressure)
        df['cholestoral_group'] = df['chol'].apply(self.categorize_cholesterol)

        ordinal_df_new_data = pd.DataFrame({
            'age_group': df['age_group'].map(self.age_group_mapping),
            'blood_pressure': df['blood_pressure_group'].map(self.bloodp_mapping),
            'cholesterol_group': df['cholestoral_group'].map(self.chol_mapping)
        })
        
        dummies_df_new_data = pd.DataFrame(self.ohc.transform(df[self.nominal_columns]), columns=self.ohc.get_feature_names_out())

        last_new_data = pd.concat([numeric_scaled_df_new_data, dummies_df_new_data, ordinal_df_new_data, df[['sex', 'fbs', 'exang']]], axis=1)
        return last_new_data
    
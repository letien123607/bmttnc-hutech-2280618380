import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import requests
import os

# Đảm bảo đường dẫn này đúng để PyQt tìm thấy các plugin
# Nếu bạn đang chạy từ thư mục 'lab_03' và 'platforms' nằm ngang hàng với 'lab_03',
# thì đường dẫn này là đúng.
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = "../platforms"

# Nhập lớp Ui_MainWindow từ file playfair.py đã được tạo từ playfair.ui
# Giả sử file playfair.py nằm trong thư mục 'ui'
from ui.playfair import Ui_MainWindow # Đảm bảo đường dẫn và tên file này chính xác

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Kết nối các nút với các hàm xử lý
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
    
    def call_api_encrypt(self):
        # URL của API Flask cho mã hóa Playfair
        # Đảm bảo rằng API Flask của bạn có endpoint này và lắng nghe trên port 5000
        url = "http://127.0.0.1:5000/api/playfair/encrypt" 
        
        # Lấy văn bản gốc và khóa từ các QPlainTextEdit
        plaintext = self.ui.txt_plaintext.toPlainText()
        key = self.ui.txt_key.toPlainText() # Key cho Playfair là một chuỗi

        # Kiểm tra key trống
        if not key:
            QMessageBox.warning(self, "Invalid Key", "Key cannot be empty for Playfair Cipher.")
            return

        # Chuẩn bị payload để gửi đến API
        # Dựa trên lịch sử lỗi của bạn, tôi sử dụng tên key với chữ cái đầu viết hoa
        payload = {
            "plain_text": plaintext, # Tên key này phải khớp với tên key mà API Flask mong đợi
            "key": key              # Key là chuỗi
        }

        # Debug: In ra payload trước khi gửi để kiểm tra
        print(f"Sending encryption request to URL: {url}")
        print(f"Payload for encryption: {payload}")

        try:
            # Gửi yêu cầu POST đến API
            response = requests.post(url, json=payload)
            
            # Debug: In ra trạng thái và phản hồi từ API
            print(f"Encrypt API Status Code: {response.status_code}")
            print(f"Encrypt API Response Text: {response.text}")

            if response.status_code == 200:
                data = response.json()
                # Kiểm tra xem key 'encrypted_message' có tồn tại trong phản hồi không
                if "encrypted_text" in data:
                    # Hiển thị văn bản đã mã hóa vào ô txt_ciphertext
                    self.ui.txt_ciphertext.setPlainText(data["encrypted_text"])

                    # Hiển thị thông báo thành công
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Encrypted Successfully")
                    msg.setWindowTitle("Success")
                    msg.exec_()
                else:
                    QMessageBox.warning(self, "API Response Error", 
                                        "API did not return 'encrypted_text' in response.")
            else:
                # Xử lý lỗi từ phía API (ví dụ: lỗi 4xx, 5xx)
                error_info = response.text # Lấy thông tin lỗi từ phản hồi
                QMessageBox.critical(self, "Encryption API Error", 
                                     f"Error from API: {response.status_code} - {error_info}")
                print(f"Error calling Encrypt API: {response.status_code} - {error_info}")
        except requests.exceptions.RequestException as e:
            # Xử lý lỗi kết nối mạng hoặc API không hoạt động
            QMessageBox.critical(self, "Network Error", 
                                 f"Could not connect to API. Is the server running? Details: {e}")
            print(f"Network error during encryption: {e}")
        except Exception as e:
            # Xử lý các lỗi không mong muốn khác
            QMessageBox.critical(self, "Unexpected Error", 
                                 f"An unexpected error occurred during encryption: {e}")
            print(f"An unexpected error occurred during encryption: {e}")
    
    def call_api_decrypt(self):
        # URL của API Flask cho giải mã Playfair
        url = "http://127.0.0.1:5000/api/playfair/decrypt"
        
        # Lấy văn bản mã hóa và khóa từ các QPlainTextEdit
        ciphertext = self.ui.txt_ciphertext.toPlainText()
        key = self.ui.txt_key.toPlainText() # Key cho Playfair là một chuỗi

        # Kiểm tra key trống
        if not key:
            QMessageBox.warning(self, "Invalid Key", "Key cannot be empty for Playfair Cipher.")
            return

        # Chuẩn bị payload để gửi đến API
        # Dựa trên lịch sử lỗi của bạn, tôi sử dụng tên key với chữ cái đầu viết hoa
        payload = {
            "cipher_text": ciphertext, # Tên key này phải khớp với tên key mà API Flask mong đợi
            "key": key               # Key là chuỗi
        }

        # Debug: In ra payload trước khi gửi để kiểm tra
        print(f"Sending decryption request to URL: {url}")
        print(f"Payload for decryption: {payload}")

        try:
            # Gửi yêu cầu POST đến API
            response = requests.post(url, json=payload)
            
            # Debug: In ra trạng thái và phản hồi từ API
            print(f"Decrypt API Status Code: {response.status_code}")
            print(f"Decrypt API Response Text: {response.text}")

            if response.status_code == 200:
                data = response.json()
                # Kiểm tra xem key 'decrypted_message' có tồn tại trong phản hồi không
                if "decrypted_text" in data:
                    # Hiển thị văn bản đã giải mã vào ô txt_plaintext
                    self.ui.txt_plaintext.setPlainText(data["decrypted_text"])

                    # Hiển thị thông báo thành công
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Decrypted Successfully")
                    msg.setWindowTitle("Success")
                    msg.exec_()
                else:
                    QMessageBox.warning(self, "API Response Error", 
                                        "API did not return 'decrypted_text' in response.")
            else:
                # Xử lý lỗi từ phía API (ví dụ: lỗi 4xx, 5xx)
                error_info = response.text # Lấy thông tin lỗi từ phản hồi
                QMessageBox.critical(self, "Decryption API Error", 
                                     f"Error from API: {response.status_code} - {error_info}")
                print(f"Error calling Decrypt API: {response.status_code} - {error_info}")
        except requests.exceptions.RequestException as e:
            # Xử lý lỗi kết nối mạng hoặc API không hoạt động
            QMessageBox.critical(self, "Network Error", 
                                 f"Could not connect to API. Is the server running? Details: {e}")
            print(f"Network error during decryption: {e}")
        except Exception as e:
            # Xử lý các lỗi không mong muốn khác
            QMessageBox.critical(self, "Unexpected Error", 
                                 f"An unexpected error occurred during decryption: {e}")
            print(f"An unexpected error occurred during decryption: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
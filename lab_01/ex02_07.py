# Nhập các dòng từ người dùng
print("Nhập các dòng văn bản (Nhập 'done' để kết thúc):")
lines = []

while True:
    line = input()  # Sửa lỗi ở đây bằng cách thêm dấu "=" để gán giá trị cho biến line
    
    if line.lower() == 'done':
        break
    
    lines.append(line)

# Chuyển các dòng thành chữ in hoa và in ra màn hình
print("\nCác dòng đã nhập sau khi chuyển thành chữ in hoa:")
for line in lines:
    print(line.upper())

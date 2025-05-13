# Nhập X và Y từ người dùng
input_str = input("Nhập X, Y: ")

# Tách chuỗi và chuyển thành danh sách số nguyên
dimensions = [int(x) for x in input_str.split(',')]

# Lấy số dòng và số cột từ dimensions
rowNum = dimensions[0]
colNum = dimensions[1]

# Tạo một danh sách hai chiều với số dòng và số cột
multilist = [[0 for col in range(colNum)] for row in range(rowNum)]

# Duyệt qua từng dòng và cột để gán giá trị
for row in range(rowNum):
    for col in range(colNum):
        multilist[row][col] = row * col

# In ra danh sách hai chiều
print(multilist)

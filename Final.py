# Input
Plain_text = "133457799BBCDFF0"
Key = "A0B1C2D3E4F56789"
# Hoán vị ban đầu
# ASCII -> Hex
def ASCII_to_Hex(plain_text):
    return ''.join([hex(ord(c))[2:].zfill(2) for c in plain_text])

# Hex -> Binary
def Hex_to_Binary(hex_text):
    return ''.join([bin(int(i, 16))[2:].zfill(4) for i in hex_text])

# Vì bài của thầy là chuỗi ký tự hex nên chỉ cần chuyển sang binary là được
def Initial_Permutation(plain_text):
    binary_text = Hex_to_Binary(plain_text)
    Left_1 = binary_text[:32]
    Right_1 = binary_text[32:]
    return Left_1, Right_1

# Sinh khóa con
def Generate_Subkey(key):
    key_result = Hex_to_Binary(key)
    
    # Hoán vị PC1
    PC1 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

    key_binary = ""
    for i in PC1:
        key_binary += key_result[i-1] # Vì index bắt đầu từ 0 nên phải trừ 1

    # Chia thành 2 khóa con
    left_key = key_binary[:28]
    right_key = key_binary[28:]

    # Bảng số bit dịch trái cho mỗi vòng
    shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    
    # Hoán vị PC2
    PC2 = [14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32]

    subkeys = []
    for i in range(16):
        # Dịch trái theo bảng shift_table
        left_key = left_key[shift_table[i]:] + left_key[:shift_table[i]]
        right_key = right_key[shift_table[i]:] + right_key[:shift_table[i]]
        
        # Kết hợp left_key và right_key
        combined_key = left_key + right_key
        
        # Áp dụng PC2 để tạo khóa con
        subkey = ""
        for j in PC2:
            subkey += combined_key[j-1]
        
        subkeys.append(subkey)
    
    # Trả về 16 khóa con
    return subkeys

# E function
# Biến thứ nhất Ri-1 được mở rộng thành một xâu có độ dài 48 bit theo một hàm mở rộng hoán vị E (Expansion permutation).
# Thực chất hàm mở rộng E(Ri-1) là một hoán vị có lặp trong đó lặp lại 16 bit của Ri-1.
def E_function(right):
    E = [32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1]

    right_result = ""
    for i in E:
        right_result += right[i-1]
    return right_result

# XOR
def XOR(right, key):
    result = ""
    for i in range(len(right)):
        result += str(int(right[i]) ^ int(key[i]))
    return result
def S_box(right):
    S = [
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
        ],
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
        ],
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
        ],
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
        ],
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
        ],
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
        ],
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
        ]
    ]
    
    # Chia chuỗi 48 bit thành 8 khối, mỗi khối 6 bit
    blocks = [right[i:i+6] for i in range(0, 48, 6)]
    result = ""
    
    # Xử lý mỗi khối qua S-box tương ứng
    for i in range(8):
        # Lấy bit đầu và bit cuối để xác định hàng
        row = int(blocks[i][0] + blocks[i][5], 2)
        # Lấy 4 bit ở giữa để xác định cột
        col = int(blocks[i][1:5], 2)
        
        # Lấy giá trị từ S-box thứ i, tại hàng row, cột col
        val = S[i][row][col]
        
        # Chuyển số thành chuỗi nhị phân 4 bit
        result += bin(val)[2:].zfill(4)
    
    return result
# P-box
def P_box(input_bits):
    # Bảng hoán vị P của DES
    P = [
        16, 7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9,
        19, 13, 30, 6, 22, 11, 4, 25
    ]
    
    # Thực hiện hoán vị theo bảng P
    result = ""
    for i in P:
        result += input_bits[i-1] # -1 vì bảng hoán vị bắt đầu từ 1 còn index của chuỗi bắt đầu từ 0
    
    return result

# Final Li = R(i-1) và Ri = L(i-1) XOR f(R(i-1), K(i))
def DES_Encryption(plain_text):
    # Hoán vị ban đầu
    Left, Right = Initial_Permutation(plain_text)
    subkeys = Generate_Subkey(Key)
    # 16 vòng lặp
    for i in range(16):
        # Lưu lại giá trị của Right
        temp = Right
        
        # Right = Left XOR f(Right, subkey)
        Right = E_function(Right)          # Mở rộng Right từ 32 bit lên 48 bit
        Right = XOR(Right, subkeys[i])     # XOR với khóa con
        Right = S_box(Right)               # Thay thế bằng S-box
        Right = P_box(Right)               # Hoán vị P-box
        Right = XOR(Right, Left)           # XOR với Left
        
        # Left = Right
        Left = temp
        print(f"Round {i+1}: Cipher_text = {Left + Right}")
    
    # Kết quả cuối cùng
    result = Left + Right
    return result
# Chuyển kết quả từ binary sang hex
def Binary_to_Hex(binary_text):
    return ''.join([hex(int(binary_text[i:i+4], 2))[2:] for i in range(0, len(binary_text), 4)])

# Hex -> ASCII
def Hex_to_ASCII(hex_text):
    return ''.join([chr(int(hex_text[i:i+2], 16)) for i in range(0, len(hex_text), 2)])

# Hoán vị IP-1
def Final_Permutation(input_bits):
    FP = [
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25
    ]
    
    result = ""
    for i in FP:
        result += input_bits[i-1] # -1 vì bảng hoán vị bắt đầu từ 1 còn index của chuỗi bắt đầu từ 0
    
    return result

cipher = Final_Permutation(DES_Encryption(Plain_text))
cipher_hex = Binary_to_Hex(cipher)

print(cipher_hex)
print(Binary_to_Hex("1001101110111100110111111111000010101101111001101001100100111111"))
print(Generate_Subkey(Key))
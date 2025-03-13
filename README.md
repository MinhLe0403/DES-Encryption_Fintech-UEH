# DES-Encryption_Fintech-UEH
Diễn giải mã hóa DES bằng code và giải thích giải thuật cho ae
# **Mã hóa Des**
## **Dữ liệu đầu vào**

- Nếu dữ liệu là 1 chuỗi thuộc bảng ASCII thì chỉ được 8 ký tự
- Nếu dữ liệu là 1 chuỗi thuộc bảng Hex thì chỉ được 16 ký tự

Vì bài của thầy có `M=133457799BBCDFF0` nên ta mặc định nó là chuỗi hex.

## 1.1. Bước 1: Hoán vị ban đầu (Initial Permutation - IP)
Dữ liệu đầu vào (64-bit) được sắp xếp lại theo một hoán vị cố định IP, tạo ra hai nửa dữ liệu:

- L0 (Left 32-bit)
- R0 (Right 32-bit)

# Input
    Plain_text = "133457799BBCDFF0"
    Key = "A0B1C2D3E4F56789"

***1. Hoán vị lần đầu Initial Permute***

**Nhận vào khối dữ liệu 64 bit:** Khối dữ liệu đầu vào có độ dài 64 bit.

**Sử dụng bảng hoán vị IP:** Bảng hoán vị IP xác định thứ tự mới của các bit. Thứ tự mới của dãy đầu vào là thứ tự bị xáo trộn như trong bảng IP nếu nhìn từ trái sang phải.

**Sắp xếp lại các bit:** Mỗi bit trong khối dữ liệu đầu vào được di chuyển đến vị trí mới theo bảng hoán vị IP.
# ASCII -> Hex
    def ASCII_to_Hex(plain_text):
        return ''.join([hex(ord(c))[2:].zfill(2) for c in plain_text])

# Hex -> Binary
    def Hex_to_Binary(hex_text):
        return ''.join([bin(int(i, 16))[2:].zfill(4) for i in hex_text])

# Hoán vị ban đầu
# Vì bài của thầy là chuỗi ký tự hex nên chỉ cần chuyển sang binary là được
    def Initial_Permutation(plain_text):
        binary_text = Hex_to_Binary(plain_text)
        IP = [
            58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7
        ]
    
    permuted = ""
    for i in IP:
        permuted += binary_text[i-1]
    
    Left = permuted[:32]
    Right = permuted[32:]
    return Left, Right

## 1.2. Bước 2: 16 vòng Feistel (Feistel Rounds)
Mỗi vòng Feistel bao gồm các bước sau:

1. Sinh khóa con (Key Schedule) - Là bước sinh khóa

- Khóa chính (64-bit) được chia thành hai phần theo phép hoán vị chọn lọc Permutation Choice 1 - PC1 : C (28-bit) và D (28-bit).
- Mỗi vòng, C và D được dịch vòng (left shift) theo số bước xác định rồi kết hợp lại.
- Sau đó, khóa con Ki (48-bit) được trích xuất bằng phép hoán vị chọn lọc (Permutation Choice 2 - PC2).

2. Mã hóa từng vòng - Là bước expand:

- F-function: Lấy R(i-1) mở rộng từ 32-bit thành 48-bit bằng Expansion (E) function.
- XOR với khóa con Ki: R′=E(R(i−1))⊕Ki.
- S-Box Substitution: 48-bit đầu ra được chia thành 8 nhóm 6-bit, mỗi nhóm đi qua một bảng thay thế (S-Box), giảm từ 6-bit xuống 4-bit.
- Permutation (P-box): 32-bit kết quả từ S-Box được hoán vị để khuếch đại sự nhiễu loạn.

3. Hoán đổi vị trí - Tạo ra Li và Ri cuối cùng

- Li=Ri−1
- Ri=Li−1⊕F(Ri−1,Ki)

### 1.2.1. Sinh khóa
# Sinh khóa con
    def Generate_Subkey(key):
        # Chuyển khóa sang binary
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

    # Áp dụng PC1 để tạo khóa 56 bit
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

    # Sinh 16 khóa con
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
### 1.2.2. Mã hóa từng vòng
***1. Expand function***

Nhìn vào bảng **Expand**, ta có thể lấy thứ tự của các bit theo hàng ngang xuống để tạo thành 1 bit mới có độ dài 48 bit.

Khi quan sát kỹ, ở 2 dữ liệu cuối mỗi hàng sẽ được lặp lại ở hàng tiếp theo.

**Ví dụ:** 4,5 ở hàng 1 được lặp lại ở hàng đầu tiếp theo.
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
***2. XOR giữa right_text và key***

XOR (Exclusive OR) là một phép toán logic nhị phân được sử dụng rộng rãi trong mật mã học và các ứng dụng kỹ thuật số khác:

- **XOR của hai bit giống nhau là 0.**
- **XOR của hai bit khác nhau là 1.**

Cơ chế của đoạn code sau được diễn giải trong code, đặc biệt:

`result += str(int(right[i]) ^ int(key[i]))`: Hàm sẽ trả về kết quả của phép XOR.

***Lưu ý, `^` không phải phép mũ***

**Ví dụ:** `1^0 = 1`; `1^1 = 0`
# XOR
    def XOR(right, key):
        result = ""
        for i in range(len(right)):
            result += str(int(right[i]) ^ int(key[i]))
        return result
***3. Hàm S_box***

Sau khi mã hóa, right_text đang có 48 bit. Ta sẽ chia thành 8 khối, mỗi khối 6 bit. Ta có định dạng 1 khối 6 bit như sau:

**Khối 1 = abcdef**

Ta cần quan tâm tới 2 thứ, 1 là sự kết hợp giữa **af**, 2 là 4 bit ở trong là **bcde**

**S_box** là 8 boxes, trong đó mỗi boxes là 1 ma trận 4x16 (4 hàng, 16 cột).

Ta sẽ xác định được giá trị của 1 khối bằng **S_box**, với giá trị đó sẽ là ô nằm ở hàng thứ **af** cột thứ **bcde**

**Ví dụ:** Ta có khối `101011`, có **af** = `11`, **bcde** = `0101`. Chuyển sang hệ số 10 thì sẽ là hàng **af** = `3`, cột **bcde** = `5`. Lưu ý thứ tự hàng và cột bắt đầu từ 0.

Nếu đối chiếu hàng `3` cột `5` ở box `1` thì sẽ trả về giá trị `9` hệ số 10 và giá trị `1001` hệ số 2.
    
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
***4. Hàm P_box***

Sau khi Right_text còn 32 bit, ta sẽ hoán vị nó theo bảng P_box theo thứ tự từ trái sang
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


### 1.2.3. Hoán vị Li và Ri cuối cùng
***1. XOR giữa Right_text và Left_text***

Sau khi ta đã mã hóa được Right_text qua các bước trên, bước cuối cùng để kết thúc 1 vòng Fistel chính là phải XOR giữa Right_text và Left_text để trả về Right_text cuối cùng
***2. Cho Left_text là Right_text ban đầu***
# Final Li = R(i-1) và Ri = L(i-1) XOR f(R(i-1), K(i))
    def DES_Encryption(plain_text):
        # Hoán vị ban đầu
        Left, Right = Initial_Permutation(plain_text)
        subkeys = Generate_Subkey(Key)
    
    # 16 vòng lặp
    for i in range(16):
        # Lưu lại giá trị của Right
        temp = Right
        
        # Tính f(Right, subkey)
        f_result = E_function(Right)       # Mở rộng Right từ 32 bit lên 48 bit
        f_result = XOR(f_result, subkeys[i])  # XOR với khóa con
        f_result = S_box(f_result)         # Thay thế bằng S-box
        f_result = P_box(f_result)         # Hoán vị P-box
        
        # Right = Left XOR f(Right, subkey)
        Right = XOR(Left, f_result)
        
        # Left = Right cũ
        Left = temp
    
    # Đổi vị trí Left và Right cuối cùng (swap)
    Left, Right = Right, Left
    
    # Kết quả cuối cùng
    result = Left + Right
    return result
## 1.3. Bước 3: Hoán vị IP -1 cuối cùng (Final Permutation - FP)

***1. Hoán vị IP-1***

Sau 16 vòng, hai nửa L16​ và R16​ được kết hợp lại và hoán vị ngược bằng FP để tạo ra văn bản mã hóa 64-bit.
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
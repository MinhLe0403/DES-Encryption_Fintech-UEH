# Mã DES cải tiến
class DES:
    def __init__(self):
        # Bảng hoán vị ban đầu (IP)
        self.initial_perm = [
            58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7
        ]
        
        # Bảng hoán vị cuối (IP^-1)
        self.final_perm = [
            40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25
        ]
        
        # Bảng mở rộng E
        self.expansion_table = [
            32, 1, 2, 3, 4, 5,
            4, 5, 6, 7, 8, 9,
            8, 9, 10, 11, 12, 13,
            12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21,
            20, 21, 22, 23, 24, 25,
            24, 25, 26, 27, 28, 29,
            28, 29, 30, 31, 32, 1
        ]
        
        # Bảng hoán vị PC1 cho khóa
        self.pc1 = [
            57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4
        ]
        
        # Bảng hoán vị PC2 cho khóa
        self.pc2 = [
            14, 17, 11, 24, 1, 5, 3, 28,
            15, 6, 21, 10, 23, 19, 12, 4,
            26, 8, 16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55, 30, 40,
            51, 45, 33, 48, 44, 49, 39, 56,
            34, 53, 46, 42, 50, 36, 29, 32
        ]
        
        # Số lượng bit dịch trái cho mỗi vòng
        self.shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
        
        # Bảng hoán vị P
        self.p_box = [
            16, 7, 20, 21, 29, 12, 28, 17,
            1, 15, 23, 26, 5, 18, 31, 10,
            2, 8, 24, 14, 32, 27, 3, 9,
            19, 13, 30, 6, 22, 11, 4, 25
        ]
        
        # S-boxes
        self.s_boxes = [
            # S1
            [
                [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
            ],
            # S2
            [
                [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
            ],
            # S3
            [
                [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
            ],
            # S4
            [
                [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
            ],
            # S5
            [
                [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
            ],
            # S6
            [
                [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
            ],
            # S7
            [
                [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
            ],
            # S8
            [
                [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
            ]
        ]
    
    # Các hàm chuyển đổi
    def ascii_to_hex(self, text):
        """Chuyển đổi ASCII sang HEX"""
        return ''.join([hex(ord(c))[2:].zfill(2) for c in text])
    
    def hex_to_binary(self, hex_text):
        """Chuyển đổi HEX sang nhị phân"""
        return ''.join([bin(int(i, 16))[2:].zfill(4) for i in hex_text])
    
    def binary_to_hex(self, binary_text):
        """Chuyển đổi nhị phân sang HEX"""
        return ''.join([hex(int(binary_text[i:i+4], 2))[2:] for i in range(0, len(binary_text), 4)])
    
    def hex_to_ascii(self, hex_text):
        """Chuyển đổi HEX sang ASCII"""
        return ''.join([chr(int(hex_text[i:i+2], 16)) for i in range(0, len(hex_text), 2)])
    
    def permute(self, k, table):
        """Hoán vị một chuỗi bit theo bảng cho trước"""
        return ''.join([k[i-1] for i in table])
    
    def shift_left(self, k, shifts):
        """Dịch trái một chuỗi bit"""
        return k[shifts:] + k[:shifts]
    
    def xor(self, a, b):
        """Phép XOR giữa hai chuỗi bit"""
        return ''.join([str(int(x) ^ int(y)) for x, y in zip(a, b)])
    
    def apply_sbox(self, expanded_block):
        """Áp dụng S-box cho một khối 48 bit"""
        blocks = [expanded_block[i:i+6] for i in range(0, 48, 6)]
        result = ""
        
        for i in range(8):
            block = blocks[i]
            row = int(block[0] + block[5], 2)
            col = int(block[1:5], 2)
            val = self.s_boxes[i][row][col]
            result += bin(val)[2:].zfill(4)
            
        return result
    
    def generate_subkeys(self, key):
        """Sinh 16 khóa con từ khóa chính"""
        # Chuyển khóa sang nhị phân
        key_bin = self.hex_to_binary(key)
        
        # Hoán vị PC1
        key_pc1 = self.permute(key_bin, self.pc1)
        
        # Chia thành nửa trái và phải
        left = key_pc1[:28]
        right = key_pc1[28:]
        
        # Tạo 16 khóa con
        subkeys = []
        for i in range(16):
            # Dịch trái theo bảng dịch
            left = self.shift_left(left, self.shift_table[i])
            right = self.shift_left(right, self.shift_table[i])
            
            # Kết hợp hai nửa và áp dụng PC2
            combined = left + right
            subkey = self.permute(combined, self.pc2)
            subkeys.append(subkey)
            
        return subkeys
    
    def f_function(self, right, subkey):
        """Hàm f trong thuật toán DES"""
        # Mở rộng nửa phải từ 32 bit thành 48 bit
        expanded = self.permute(right, self.expansion_table)
        
        # XOR với khóa con
        xored = self.xor(expanded, subkey)
        
        # Áp dụng S-box
        sboxed = self.apply_sbox(xored)
        
        # Hoán vị P
        return self.permute(sboxed, self.p_box)
    
    def encrypt(self, plaintext, key):
        """Mã hóa thông điệp bằng thuật toán DES"""
        # Sinh các khóa con
        subkeys = self.generate_subkeys(key)
        
        # Chuyển plaintext sang nhị phân
        binary = self.hex_to_binary(plaintext)
        
        # Hoán vị ban đầu
        binary = self.permute(binary, self.initial_perm)
        
        # Chia thành nửa trái và phải
        left = binary[:32]
        right = binary[32:]
        
        # 16 vòng lặp
        for i in range(16):
            # Lưu lại nửa phải
            old_right = right
            
            # Tính hàm f
            f_result = self.f_function(right, subkeys[i])
            
            # Cập nhật nửa trái và phải
            right = self.xor(left, f_result)
            left = old_right
        
        # Đổi chỗ L16 và R16 (nối R16L16)
        combined = right + left
        
        # Hoán vị cuối cùng
        ciphertext_bin = self.permute(combined, self.final_perm)
        
        # Chuyển về định dạng hex
        ciphertext = self.binary_to_hex(ciphertext_bin)
        
        return ciphertext
    
    def decrypt(self, ciphertext, key):
        """Giải mã thông điệp bằng thuật toán DES"""
        # Sinh các khóa con (trong thứ tự ngược lại cho quá trình giải mã)
        subkeys = self.generate_subkeys(key)
        subkeys.reverse()  # Đảo ngược thứ tự các khóa con
        
        # Chuyển ciphertext sang nhị phân
        binary = self.hex_to_binary(ciphertext)
        
        # Hoán vị ban đầu
        binary = self.permute(binary, self.initial_perm)
        
        # Chia thành nửa trái và phải
        left = binary[:32]
        right = binary[32:]
        
        # 16 vòng lặp
        for i in range(16):
            # Lưu lại nửa phải
            old_right = right
            
            # Tính hàm f
            f_result = self.f_function(right, subkeys[i])
            
            # Cập nhật nửa trái và phải
            right = self.xor(left, f_result)
            left = old_right
        
        # Đổi chỗ L16 và R16 (nối R16L16)
        combined = right + left
        
        # Hoán vị cuối cùng
        plaintext_bin = self.permute(combined, self.final_perm)
        
        # Chuyển về định dạng hex
        plaintext = self.binary_to_hex(plaintext_bin)
        
        return plaintext

# Sử dụng mã DES
if __name__ == "__main__":
    des = DES()
    
    # Giá trị ban đầu
    plaintext = "133457799BBCDFF0"
    key = "A0B1C2D3E4F56789"
    
    # Mã hóa
    ciphertext = des.encrypt(plaintext, key)
    print(f"Plaintext:  {plaintext}")
    print(f"Key:        {key}")
    print(f"Ciphertext: {ciphertext}")
    
    # Giải mã
    decrypted = des.decrypt(ciphertext, key)
    print(f"Decrypted:  {decrypted}")
    
    # Khóa con
    subkeys = des.generate_subkeys(key)
    for i, subkey in enumerate(subkeys):
        print(f"Subkey {i + 1}: {des.binary_to_hex(subkey)}")

    # Kiểm tra kết quả
    if decrypted == plaintext:
        print("Mã hóa và giải mã thành công!")
    else:
        print("Có lỗi xảy ra trong quá trình mã hóa/giải mã.")
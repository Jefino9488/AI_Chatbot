# caesar cipher

def encryptCC(text):
    result = ""
    t = 3
    for i in range(len(text)):
        char = text[i]
        if char.isupper():
            result += chr((ord(char) + t - 65) % 26 + 65)
        else:
            result += chr((ord(char) + t - 97) % 26 + 97)

    return result


# playfair

def generateKeySquare(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key = key.upper()
    key = "".join(sorted(set(key), key=key.index))  # Remove duplicates while maintaining order
    key_square = [c for c in key if c in alphabet]
    for c in alphabet:
        if c not in key_square:
            key_square.append(c)
    key_matrix = [key_square[i:i + 5] for i in range(0, 25, 5)]
    return key_matrix


def preprocessText(text):
    text = text.upper().replace("J", "I").replace(" ", "")
    processed_text = ""
    i = 0
    while i < len(text):
        processed_text += text[i]
        if i + 1 < len(text) and text[i] == text[i + 1]:
            processed_text += "X"
        elif i + 1 < len(text):
            processed_text += text[i + 1]
            i += 1
        i += 1
    if len(processed_text) % 2 != 0:
        processed_text += "X"
    return processed_text


def findPosition(key_matrix, letter):
    for row in range(5):
        for col in range(5):
            if key_matrix[row][col] == letter:
                return row, col
    return None


def encryptPlayfair(text, key="monarchy"):
    key_matrix = generateKeySquare(key)
    text = preprocessText(text)
    result = ""

    i = 0
    while i < len(text):
        a = text[i]
        b = text[i + 1]
        row1, col1 = findPosition(key_matrix, a)
        row2, col2 = findPosition(key_matrix, b)

        if row1 == row2:
            result += key_matrix[row1][(col1 + 1) % 5]
            result += key_matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            result += key_matrix[(row1 + 1) % 5][col1]
            result += key_matrix[(row2 + 1) % 5][col2]
        else:
            result += key_matrix[row1][col2]
            result += key_matrix[row2][col1]

        i += 2

    return result


# Example usage:
s = input("Enter Text to encrypt : ")
print("Caesar Cipher Encrypted Text : ", encryptCC(s))
#print("Playfair Encrypted Text : ", encryptPlayfair(s))

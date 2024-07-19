# playfair

def keySquare(key):
    alpha = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key = key.upper()
    key = "".join(sorted(set(key), key=key.index))
    keySquare = []
    for i in key:
        if i in alpha:
            keySquare.append(i)
    for i in alpha:
        if i not in keySquare:
            keySquare.append(i)
    keyMatrix = []
    for i in range(0, 25, 5):
        keyMatrix.append(keySquare[i:i + 5])
    return keyMatrix


print(keySquare("monarchy"))


def processText(text):
    text = text.upper()
    text = text.replace("J", "I")
    text = text.replace(" ", "")
    processedText = ""
    i = 0
    while i < len(text):
        processedText += text[i]
        print(processedText)
        if i + 1 < len(text) and text[i] == text[i + 1]:
            processedText += "X"
        elif i + 1 < len(text):
            processedText += text[i + 1]
            i += 1
        i += 1
    if len(processedText) % 2 != 0:
        processedText += "X"
    return processedText


def findPosition(keyMatrix, letter):
    for row in range(5):
        for col in range(5):
            if keyMatrix[row][col] == letter:
                return row, col
    return None

print(findPosition(keySquare("monarchy"), "A"))


def encryptPlayfair(text, key="monarchy"):
    keyMatrix = keySquare(key)
    text = processText(text)
    result = ""
    i = 0
    while i < len(text):
        print(result)
        a = text[i]
        b = text[i + 1]
        row1, col1 = findPosition(keyMatrix, a)
        print(row1, col1)
        row2, col2 = findPosition(keyMatrix, b)
        print(row2, col2)
        if row1 == row2:
            result += keyMatrix[row1][(col1 + 1) % 5]
            result += keyMatrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            result += keyMatrix[(row1 + 1) % 5][col1]
            result += keyMatrix[(row2 + 1) % 5][col2]
        else:
            result += keyMatrix[row1][col2]
            result += keyMatrix[row2][col1]
        i += 2

    return result

print(encryptPlayfair("Hello World", "monarchy"))

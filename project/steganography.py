import cv2
import numpy as np

def messageToBinary(message):
    messageInBin = ''

    # if message is in string form
    if type(message) == str:
        # convert each char in message into binary
        # concatenate all to form the message in binary
        for i in message:
            messageInBin += format(ord(i), '08b')
    # else if message is in integer form
    elif type(message) == int or type(message) == np.uint8:
        messageInBin = format(message, "08b")

    #print(messageInBin)
    return messageInBin

def hideData(image, message):
    # copy of image, the cover
    cover = image.copy()

    # append a delimiter at the end of message
    message += '#####'
    # convert message to binary, the payload
    payload = messageToBinary(message)
    # length of the payload to keep track the number of bytes going to be used
    payloadLen = len(payload)
    # index to keep track of the bit of payload to replace on the cover
    payloadIndex = 0

    for rows in cover:              # traverse rows of image (height)
        for pixel in rows:          # traverse each column of each row (pixel)
            # extract binary B, G and R value from each pixel
            b, g, r = messageToBinary(pixel[0]),    \
                      messageToBinary(pixel[1]),    \
                      messageToBinary(pixel[2])
            # index of R is 2 (pixel[2] = r, pixel[1] = g, pixel[0] = b)
            bgrIndex = 2
            for colour in (r, g, b):
                # if there are still bits left to be replaced
                if payloadIndex < payloadLen:
                    # retain value from bit 7 to 1, replace only bit 0 (LSB), convert value to binary using base 2
                    pixel[bgrIndex] = int(colour[:-1] + payload[payloadIndex], 2)
                    bgrIndex -= 1
                    payloadIndex += 1
                # else all bits of payload are replaced on the cover
                else:
                    cv2.imwrite('cover.png', cover)
                    return

def decoder(image):
    sImage = cv2.imread(image)
    hiddenBinary = ''
    for rows in sImage:
        for pixel in rows:
            b, g, r = messageToBinary(pixel[0]), \
                      messageToBinary(pixel[1]), \
                      messageToBinary(pixel[2])
            hiddenBinary += r[-1]
            hiddenBinary += g[-1]
            hiddenBinary += b[-1]

    # group 8 bits into a byte
    hiddenByte = [hiddenBinary[i: i + 8] for i in range(0, len(hiddenBinary), 8)]
    # convert from byte to char
    message = ''
    for byte in hiddenByte:
        # convert to int using base 2 then to char
        message += chr(int(byte, 2))
        # if the last 5 decoded char is '#####' (delimiter) stop converting
        if message[-5:] == '#####':
            # return message without the delimiter
            return message[:-5]
    return


if __name__ == '__main__':
    message = 'hello darkness my old friend'
    image = cv2.imread('Lenna.png')
    hideData(image, message)
    messageDecoded = decoder('cover.png')
    print(messageDecoded)


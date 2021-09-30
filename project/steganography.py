import cv2
import numpy as np
import speech_recognition as sr


class Steganography:
    image = None
    imageExtension = None
    message = None
    # messageExtension = None
    mode = 0
    bitSelect = 0
    stegoImageFileName = None
    stegoImagePath = None
    audioFileName = None

    def __init__(self, imagePath, messagePath, mode, bitSelect, stegoImageFileName):

        self.image = cv2.imread(imagePath)
        self.imageExtension = imagePath.split('.')[-1]
        try:
            with open(messagePath) as f:
                self.message = f.read()
        except:
            pass
        self.mode = mode
        self.bitSelect = bitSelect
        self.stegoImageFileName = stegoImageFileName

    def changeImage(self, imagePath):
        self.image = cv2.imread(imagePath)

    def changeMessage(self, messagePath):
        try:
            with open(messagePath) as f:
                self.message = f.read()
        except:
            pass

    def changeMode(self, mode):
        self.mode = mode

    def changeBitSelect(self, bitSelect):
        self.bitSelect = bitSelect

    def changeStegoImageFileName(self, stegoImageFileName):
        self.stegoImageFileName = stegoImageFileName

    def changeStegoImagePath(self, stegoImagePath):
        self.stegoImagePath = stegoImagePath

    def messageToBinary(self, message):
        messageInBin = ''
        # if message is in integer form
        if type(message) == int or type(message) == np.uint8:
            messageInBin = format(message, "08b")
        # else if message is in string form
        elif type(self.message) == str:
            # convert each char in message into binary
            # concatenate all to form the message in binary
            for i in message:
                messageInBin += format(ord(i), '08b')
        # print(messageInBin)
        return messageInBin

    def AudiotoText(self, text):
        # showing file name
        filename = "16-122828-0002"

        # initialize the recognizer
        r = sr.Recognizer()

        # open the file
        with sr.AudioFile(filename) as source:
            # listen to data (load audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            text = r.recognize_google(audio_data)
            print(text)




    def hideData(self):
        # copy of image, the cover
        cover = self.image.copy()
        # append a delimiter at the end of message
        self.message += '#####'
        # convert message to binary, the payload
        payload = self.messageToBinary(self.message)
        # length of the payload to keep track the number of bytes going to be used
        payloadLen = len(payload)
        # index to keep track of the bit of payload to replace on the cover
        payloadIndex = 0

        # validate if there are enough bit on cover for replacement (different value for each mode)
        # number of possible single bit replacement on cover
        if self.mode == 1:
            # pixel count * 3 (RGB)
            limit = cover.shape[0] * cover.shape[1] * 3
            # initialise bit range as 1
            bitRange = 1
        # number of possible multiple bit replacement on cover
        elif self.mode == 2:
            # pixel count * 3 (RGB) * number of bits
            limit = cover.shape[0] * cover.shape[1] * 3 * (self.bitSelect + 1)
            # initialise bit range as bitSelect + 1 (start from bit 0)
            bitRange = self.bitSelect + 1
        if payloadLen > limit:
            raise Exception("Error: Insufficient bit on cover!")

        for i in range(bitRange):
            # if mode selected is single bit replacement, change bit to be replaced to the bit selected
            if self.mode == 1: i = self.bitSelect
            # traverse image's pixel
            for rows in cover:  # traverse rows of image (height)
                for pixel in rows:  # traverse each column of each row (pixel)
                    # extract binary B, G and R value from each pixel
                    b, g, r = self.messageToBinary(pixel[0]), \
                              self.messageToBinary(pixel[1]), \
                              self.messageToBinary(pixel[2])
                    # index of R is 2 (pixel[2] = r, pixel[1] = g, pixel[0] = b)
                    bgrIndex = 2
                    for colour in (r, g, b):
                        # if there are still bits left to be replaced
                        if payloadIndex < payloadLen:
                            # replace the current selected bit on bitRange
                            # special case when current selected bit is bit 0
                            if i == 0:
                                pixel[bgrIndex] = int(colour[:-(i + 1)] + payload[payloadIndex], 2)
                            else:
                                # print(pixel[bgrIndex])
                                pixel[bgrIndex] = int(colour[:-(i + 1)] + payload[payloadIndex] + colour[-i:], 2)
                                # print(pixel[bgrIndex])
                            # shift indexes accordingly
                            bgrIndex -= 1
                            payloadIndex += 1
                        # else all bits of payload are placed on the cover
                        else:
                            self.stegoImagePath = 'result/' + self.stegoImageFileName + '.' + self.imageExtension
                            cv2.imwrite(self.stegoImagePath, cover)
                            return

    # require stegoImagePath, mode and bitSelect to be configured
    def decode(self):
        stegoImage = cv2.imread(self.stegoImagePath)
        hiddenBinary = ''
        # check for range of bit to decode depending on mode selected
        if self.mode == 1:
            bitRange = 1
        elif self.mode == 2:
            bitRange = self.bitSelect + 1

        for i in range(bitRange):
            # if mode selected is single bit replacement, change bit to be decode to the bit selected
            if self.mode == 1: i = self.bitSelect
            # append LSB (with range) from cover together to form the message in binary
            for rows in stegoImage:
                for pixel in rows:
                    b, g, r = self.messageToBinary(pixel[0]), \
                              self.messageToBinary(pixel[1]), \
                              self.messageToBinary(pixel[2])
                    hiddenBinary += r[-(i + 1)]
                    hiddenBinary += g[-(i + 1)]
                    hiddenBinary += b[-(i + 1)]

        # group 8 bits into a byte
        hiddenByte = [hiddenBinary[i: i + 8] for i in range(0, len(hiddenBinary), 8)]
        # convert from byte to char
        hiddenMessage = ''
        for byte in hiddenByte:
            # convert to int using base 2 then to char
            hiddenMessage += chr(int(byte, 2))
            # if the last 5 decoded char is '#####' (delimiter) stop converting
            if hiddenMessage[-5:] == '#####':
                # return message without the delimiter
                with open('extracted/messageDecoded.txt', "w") as f:
                    f.write(hiddenMessage[:-5])
                return
        # if run out of the loop and decoding is still not done, something must have went wrong
        raise Exception("Error encountered while decoding!")


if __name__ == '__main__':
    # mode: 1. change single bit, 2. multiple bit replacement
    # bitSelect: 0 to 7
    stegasaurus = Steganography('cover/Lenna.png', 'payload/message.txt', 2, 7, 'stegoImage')
    stegasaurus.hideData()
    stegasaurus.decode()

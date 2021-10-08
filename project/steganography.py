import cv2
import numpy as np
import os
import base64
import magic
import pymsgbox
import wave
from scipy.io.wavfile import read, write
import io


class Steganography:
    image = None
    message = None
    mode = 0
    bitSelect = 0
    stegoImageFileName = None
    stegoImagePath = None
    audioFileName = None
    audioFilePath = None
    stegoExtractPath = None
    ExtractType = None
    paddingBitCount = 0

    def __init__(self, imagePath, messagePath, mode, bitSelect, stegoImageFileName):
        if imagePath != "":
            self.image = cv2.imread(imagePath)
            self.stegoImageFileName = stegoImageFileName
            try:
                with open(messagePath) as f:
                    self.message = f.read()
            except:
                print("running path 2")

                # if message (payload) is audio file
                if messagePath.split('.')[-1] == 'wav':
                    # Read file as byte
                    with open(messagePath, "rb") as wavfile:
                        input_wav = wavfile.read()
                    # save message as a BytesIO object, which is a buffer for bytes object
                    rate, data = read(io.BytesIO(input_wav))
                    wav_byte = bytes()
                    byte_io = io.BytesIO(wav_byte)
                    write(byte_io, rate, data)
                    self.message = byte_io.read()

                # else message (payload) is image file
                else:
                    # Read file as byte
                    with open(messagePath, "rb") as image2string:
                        self.message = base64.b64encode(image2string.read())
                    # Convert byte to string
                    self.message = str(self.message.decode('utf-8'))

                # decodeit = open('hello_level.png', 'wb')
                # decodeit.write(base64.b64decode((converted_string)))
                # decodeit.close()

                # print(self.message.decode('utf-8'))
                # self.message = str(self.message)

        self.mode = mode
        self.bitSelect = bitSelect

    def setImage(self, imagePath):
        self.image = cv2.imread(imagePath)

    def setMessage(self, messagePath):
        try:
            with open(messagePath) as f:
                self.message = f.read()
        except:
            pass

    def setMode(self, mode):
        self.mode = mode

    def setBitSelect(self, bitSelect):
        self.bitSelect = bitSelect

    def setStegoImageFileName(self, stegoImageFileName):
        self.stegoImageFileName = stegoImageFileName

    def setStegoImagePath(self, stegoImagePath):
        self.stegoImagePath = stegoImagePath

    def setStegoExtractPath(self, stegoExtractPath):
        self.stegoExtractPath = stegoExtractPath

    def setExtractFileType(self, ExtractType):
        self.ExtractType = ExtractType

    def setAudioFileName(self, audioFileName):
        self.audioFileName = audioFileName

    def setAudioFilePath(self, audioFilePath):
        self.audioFilePath = audioFilePath

    def messageToBinary(self, message):
        messageInBin = ''
        # if message is in integer form
        if type(message) == int or type(message) == np.uint8:
            messageInBin = format(message, "08b")
        # else if message is in string form
        elif type(message) == str:
            # convert each char in message into binary
            # concatenate all to form the message in binary
            for i in message:
                messageInBin += format(ord(i), '08b')
        # else, message is in byte
        else:
            # convert to binary, remove the leading '0b' notation which can corrupt the data
            messageInBin = bin(int.from_bytes(message, byteorder='big'))[2:]
            # check if padding bit is required make sure payload is in full byte
            # if payload bit count is not divisible by 8, need to add padding bit
            messageInBinLen = len(messageInBin)
            if (messageInBinLen % 8) != 0:
                self.paddingBitCount = 8 - (messageInBinLen % 8)
            messageInBin += '0' * self.paddingBitCount

            encodingPaddingBitCount = self.messageToBinary(self.paddingBitCount)
            #print(encodingPaddingBitCount)

            # append delimiter at the end
            messageInBin += encodingPaddingBitCount + ''.join(format(ord(i), '08b') for i in '#####')
        return messageInBin

    def bitStringToBytes(self, bitString):
        return int(bitString, 2).to_bytes((len(bitString) + 7) // 8, byteorder='big')

    def hideData(self):
        # copy of image, the cover
        cover = self.image.copy()
        # append a delimiter at the end of message, note that byte message (wav) will not perform this here
        try:
            self.message += '#####'
        except:
            pass
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
            raise Exception("Not enough bits")

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
                            self.stegoImagePath = 'result/' + self.stegoImageFileName + '.png'
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
                if self.ExtractType == "txt":
                    # return message without the delimiter
                    with open('extracted/messageDecoded.txt', "w") as f:
                        f.write(hiddenMessage[:-5])
                elif self.ExtractType == "img":
                    with open('extracted/' + self.stegoExtractPath, "wb") as f:
                        f.write(base64.b64decode(hiddenMessage[:-5]))
                    # Rename file to based on detected extension
                    extension = magic.from_file('extracted/' + self.stegoExtractPath, mime=True).split('/')[1]
                    rename_file = 'extracted/' + self.stegoExtractPath
                    base = os.path.splitext(rename_file)[0]
                    os.rename(rename_file, base + "." + extension)
                elif self.ExtractType == "wav":
                    #Decode padding value
                    decodedPadding = int(self.messageToBinary(hiddenMessage[-6:-5]),2)
                    # remove delimiter and the padding bit
                    bin_data = self.messageToBinary(hiddenMessage[:-6])[:-decodedPadding]
                    #print(bin_data)
                    wav_byte = self.bitStringToBytes(bin_data)


                    with open('extracted/audioDecoded.wav', 'wb') as wavfile:
                        wavfile.write(wav_byte)

                return
        # if run out of the loop and decoding is still not done, something must have went wrong
        raise Exception("Error encountered while decoding!")


if __name__ == '__main__':
    # mode: 1. change single bit, 2. multiple bit replacement
    # bitSelect: 0 to 7
    # a = Steganography('cover/testocr.png', 'payload/thunder3.wav', 2, 7, '123test')
    # a.hideData()
    # 
    # a.setStegoImagePath('result/123test.png')
    # a.setStegoExtractPath('decoded')
    # a.setExtractFileType("wav")
    # a.decode()

    pass

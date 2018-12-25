#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""
import hashlib

import fingerprint


class EnrollUser(object):

    def __init__(self):
        try:
            self.f = fingerprint.pyfingerprint.PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
            if (self.f.verifyPassword() == False):
                raise ValueError('The given fingerprint sensor password is wrong!')
        except Exception as e:
            exit(1)
        print('Currently used templates: ' + str(self.f.getTemplateCount()) + '/' + str(self.f.getStorageCapacity()))

    def getCurrentPosition(self):
        return self.f.getTemplateCount()

    def inputFingerprint(self):

        while (self.f.readImage() == False):
            pass
        self.f.convertImage(0x01)
        result = self.f.searchTemplate()
        positionNumber = result[0]
        print(positionNumber)
        if positionNumber == -1:
            return dict({'res': False, 'message': 'Something Went Wrong, Please try again!'})
        else:
            return dict({'res': True, 'message': 'The user is registered!', 'pos': positionNumber})

    def getDecryptedText(self):
        characterics = str(self.f.downloadCharacteristics(0x01)).encode('utf-8')
        hx = hashlib.sha256(characterics).hexdigest()
        print('SHA-2 hash of template: ' + hx)
        return hx

    def save_fingerpring(self):
        self.f.createTemplate()
        positionNumber = self.f.storeTemplate()
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))
        return positionNumber

    if __name__ == '__main__':
        pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""
import hashlib
import time

import fingerprint


class EnrollUser(object):

    def __init__(self):
        try:
            self.f = fingerprint.pyfingerprint.PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
            if (self.f.verifyPassword() == False):
                raise ValueError('The given fingerprint sensor password is wrong!')
        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            exit(1)
        print('Currently used templates: ' + str(self.f.getTemplateCount()) + '/' + str(self.f.getStorageCapacity()))

    def inputFingerprint(self):
        while (self.f.readImage() == False):
            pass
        self.f.convertImage(0x01)
        result = self.f.searchTemplate()
        positionNumber = result[0]
        if (positionNumber >= 0):
            print('Template already exists at position #' + str(positionNumber))
            return dict({'res': False, 'message': 'Template already exists at position #' + str(positionNumber)})
        else:
            return dict({'res': True, 'message': 'Please enter the same finger again'})

    def getDecryptedText(self):
        ## Downloads the characteristics of template loaded in charbuffer 1
        characterics = str(self.f.downloadCharacteristics(0x01)).encode('utf-8')
        hx = hashlib.sha256(characterics).hexdigest()
        ## Hashes characteristics of template
        print('SHA-2 hash of template: ' + hx)
        return hx

        pass

    def input_finger_first_time(self):
        print('Waiting for finger...')
        while (self.f.readImage() == False):
            pass
        self.f.convertImage(0x01)
        result = self.f.searchTemplate()
        positionNumber = result[0]
        if (positionNumber >= 0):
            print('Template already exists at position #' + str(positionNumber))
            return dict({'res': False, 'message': 'Template already exists at position #' + str(positionNumber)})
        else:
            return dict({'res': True, 'message': 'Please enter the same finger again'})

    def input_finger_second_time(self):
        print('Remove finger...')
        time.sleep(2)
        print('Waiting for same finger again...')
        ## Wait that finger is read again
        while (self.f.readImage() == False):
            pass
        ## Converts read image to characteristics and stores it in charbuffer 2
        self.f.convertImage(0x02)
        ## Compares the charbuffers
        if (self.f.compareCharacteristics() == 0):
            return False

    def save_fingerpring(self):
        ## Creates a template
        self.f.createTemplate()
        ## Saves template at new position number
        positionNumber = self.f.storeTemplate()
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))

    # def enrollMe(self):
    #     try:
    #         print('Waiting for finger...')
    #         while (self.f.readImage() == False):
    #             pass
    #         self.f.convertImage(0x01)
    #         result = self.f.searchTemplate()
    #         positionNumber = result[0]
    #         if (positionNumber >= 0):
    #             print('Template already exists at position #' + str(positionNumber))
    #             exit(0)
    #
    #         print('Remove finger...')
    #         time.sleep(2)
    #
    #         print('Waiting for same finger again...')
    #
    #         ## Wait that finger is read again
    #         while (self.f.readImage() == False):
    #             pass
    #
    #         ## Converts read image to characteristics and stores it in charbuffer 2
    #         self.f.convertImage(0x02)
    #
    #         ## Compares the charbuffers
    #         if (self.f.compareCharacteristics() == 0):
    #             raise Exception('Fingers do not match')
    #
    #         ## Creates a template
    #         self.f.createTemplate()
    #
    #         ## Saves template at new position number
    #         positionNumber = self.f.storeTemplate()
    #         print('Finger enrolled successfully!')
    #         print('New template position #' + str(positionNumber))
    #
    #     except Exception as e:
    #         print('Operation failed!')
    #         print('Exception message: ' + str(e))
    #         exit(1)

    if __name__ == '__main__':
        pass
        # enrollMe()

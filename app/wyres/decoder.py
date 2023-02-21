
import base64
import math

from .tlv import TLV

class Decoder:

    def __init__(self, payload:str, encoding_format:str):
        self.__payload = payload
        self.__encoding_format = encoding_format



    def decode(self):
        payload_b = None
        if self.__encoding_format=="b64":
            payload_b = base64.b64decode(self.__payload).hex()
        else:
            raise Exception("Bad encoding format only b64 is supported")

        tlv_list = self.get_tlv(payload_b)

        to_rtn = {}
        for tlv in tlv_list:
            decodedKey, decodedValue = self.map_app_generic(tlv)
            print(decodedKey,decodedValue)
            to_rtn[decodedKey] = decodedValue

        return to_rtn


    @staticmethod
    def get_tlv(payload):
        print(payload)
        if payload is None or len(payload)<2:
            return []
        returnedList = []
        # payloadLength = int(payload[2:4], 16)
        # log.info('payloadLength :'+str(payloadLength))

        i = 4
        while (i < len(payload)):
            tval=0
            lval = 0
            valval = ""
            tval = int(payload[i:i+2],16)
            lval = int(payload[i+2:i+4],16)

            j = i+4
            while(j<i+4+(lval*2)):
                valval += payload[j:j+2]
                j=j+2
            i = i + 4 + (lval * 2)

            returnedList.append(TLV(tval,lval,valval))
        return returnedList

    @staticmethod
    def map_app_generic(tlv)->tuple:
        if(tlv.key == 3):
            return ('temperature', TLV.s16(int(TLV.invertValue(tlv.value),16))/100)
        elif(tlv.key == 4):
            return ('pressure', int(TLV.invertValue(tlv.value),16)/100)
        elif(tlv.key == 5):
            return ('humidity', int(TLV.invertValue(tlv.value),16)/100)
        elif(tlv.key == 6):
            return ('light', int(TLV.invertValue(tlv.value),16))
        elif(tlv.key == 7):
            return ('battery', int(TLV.invertValue(tlv.value), 16) / 1000)
        elif(tlv.key == 12):
            return ('hasMoved', 1)
        elif(tlv.key == 13):
            return ('hasFall', 1)
        elif(tlv.key == 14):
            return ('hasShock', 1)
        elif(tlv.key == 15):
            x=TLV.s8(tlv.value[2:4])
            y=TLV.s8(tlv.value[4:6])
            z=TLV.s8(tlv.value[6:8])
            # calculation of pitch and yaw in 3D  (note assumes 0deg is box vertical)
            try:
                pitch=math.degrees(math.acos(y/math.hypot(x,y)))
            except Exception as err:
                log.info("math err %s for pitch (%d, %d)", err, x, y)
                pitch=0
            # calculate cos of pitch to integrate in yaw calculation
            # TODO not sure how, stackoverflow says do acos(y/cos(pitch)*hypot(z,y)) but this ends up with acos(value>1) which is math error....
            try:
                cosp = math.cos(math.radians(pitch))
                # ignore pitch for now
                yaw=math.degrees(math.acos(y/math.hypot(z,y)))
            except Exception as err:
                log.info("math err %s for yaw (%d, %d, %d)", err, pitch, z, y)
                yaw=0
            # river depth calculations - angle of box, water depth for a unit length bar hinged on xy axis(scale as required)
            # for diagram of the triangles involved see a whiteboard near you
            try:
                rd=(2*math.sin(math.radians(pitch/2)))*math.sin(math.radians(90-((180-pitch)/2)))
            except Exception as err:
                log.info("math err %s for depth (%d)", err, pitch)
                rd=0
            return ('orient,x,y,z,pitch,yaw,rdepth', (TLV.s8(tlv.value[0:2]), x,y,z,pitch,yaw,rd))
        return (None, None)

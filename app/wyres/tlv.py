class TLV:
    key: int
    length: int
    value: str
    def __init__(self, key,length, value):
        self.key = key
        self.length = length
        self.value = value

    def print(self):
        print(str(self.key)+' not decoded')

    @staticmethod
    def invertValue(value):
        i=len(value)
        rtn = []
        while(i>0):
            rtn.append(value[i-2:i])
            i=i-2
        return "".join(rtn)

    @staticmethod
    def s16(value):
        return -(value & 0x8000) | (value & 0x7fff)

    @staticmethod
    def s8(hexb_str):
        value = int(hexb_str, 16)
        return -(value & 0x80) | (value & 0x7f)

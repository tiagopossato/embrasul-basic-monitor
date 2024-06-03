from enum import Enum

class point_type(Enum):
    int16 = 1
    int32 = 2
    int64 = 3
    raw16 = 4
    uint16 = 5
    uint32 = 6
    uint64 = 7
    acc16 = 8
    acc32 = 9
    acc64 = 10
    bitfield16 = 11
    bitfield32 = 12
    bitfield64 = 13
    enum16 = 14
    enum32 = 15
    float32 = 16
    float64 = 17
    string = 18
    sf = 19
    pad = 20
    ipaddr = 21
    ipv6addr = 22
    eui48 = 23
    sunssf = 24
    count = 25

class mandatory_type(Enum):
    M = 1
    O = 2

class access_type(Enum):
    R = 1
    RW = 2

class static_type(Enum):
    D = 1
    S = 2

class group_type(Enum):
    group = 1
    sync = 2

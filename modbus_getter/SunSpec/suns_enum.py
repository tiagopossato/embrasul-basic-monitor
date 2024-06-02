from enum import Enum

class point_type(Enum):
    pt_int16 = 1
    pt_int32 = 2
    pt_int64 = 3
    pt_raw16 = 4
    pt_uint16 = 5
    pt_uint32 = 6
    pt_uint64 = 7
    pt_acc16 = 8
    pt_acc32 = 9
    pt_acc64 = 10
    pt_bitfield16 = 11
    pt_bitfield32 = 12
    pt_bitfield64 = 13
    pt_enum16 = 14
    pt_enum32 = 15
    pt_float32 = 16
    pt_float64 = 17
    pt_string = 18
    pt_sf = 19
    pt_pad = 20
    pt_ipaddr = 21
    pt_ipv6addr = 22
    pt_eui48 = 23
    pt_sunssf = 24
    pt_count = 25

class mandatory_type(Enum):
    mt_M = 1
    mt_O = 2

class access_type(Enum):
    at_R = 1
    at_RW = 2

class static_type(Enum):
    st_D = 1
    st_S = 2

class group_type(Enum):
    gt_group = 1
    gt_sync = 2

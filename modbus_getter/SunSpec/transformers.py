import struct

from . import point_type

def transformer_value(pt_type: point_type, registers):
    # Validate pt_type
    if not isinstance(pt_type, point_type):
        raise TypeError("pt_type must be of type point_type.")
        
    match pt_type:
        case point_type.float32:
            return tr_float32(registers)
        case _:
            print("transformer not implemented...")
            return None


def tr_float32(value):
    # Combine the two registers into a single 32-bit value
    # Use 'H' for unsigned short (16 bits) and '<' for little-endian byte order
    # on systems that use little-endian for modbus
    combined_value = struct.pack('<HH', *value)
    # Unpack the combined value as a 32-bit float
    # Use 'f' for float (32 bits)
    float_number = struct.unpack('<f', combined_value)[0]
    return float_number
                
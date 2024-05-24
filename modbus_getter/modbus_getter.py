from time import sleep
from time import time
from pymodbus.client import ModbusSerialClient as ModbusClient
import logging
import struct
from read_config import read_config
from Point import Point, PointList
from save_data import start_db_session, save_data

logging.basicConfig(level=logging.INFO, format='(%(threadName)-9s) %(message)s',)

def transform_float(values):
    # Combine the two registers into a single 32-bit value
    # Use 'H' for unsigned short (16 bits) and '<' for little-endian byte order
    # on systems that use little-endian for modbus
    combined_value = struct.pack('<HH', *values)
    # Unpack the combined value as a 32-bit float
    # Use 'f' for float (32 bits)
    float_number = struct.unpack('<f', combined_value)[0]
    return float_number

def transform_float_PotAtivT(value):
    """
    Estiva a potencia ativa total multiplicando a potencia da Fase Ativa atual por 3.
    Atualmente a potencia ativa total é a mesma da Fase A, por que está sendo medido somente uma fase
    """
    return transform_float(value) * 3

<<<<<<< HEAD
UrmsA = Point('UrmsA', base_address=68, count=2)
UrmsA.set_transformer(transform_float)

IrmsA = Point('IrmsA', base_address=74, count=2)
IrmsA.set_transformer(transform_float)

PotAtivA = Point('PotAtivA', base_address=80, count=2)
PotAtivA.set_transformer(transform_float)

PotAtivT = Point('PotAtivT', base_address=86, count=2)

def transform_float_PotAtivT(value):
    """
    Estiva a potencia ativa total multiplicando a potencia da Fase Ativa atual por 3.
    Atualmente a potencia ativa total é a mesma da Fase A, por que está sendo medido somente uma fase
    """
    return transform_float(value) * 3
PotAtivT.set_transformer(transform_float_PotAtivT)

PotReatA = Point('PotReatA', base_address=88, count=2)
PotReatA.set_transformer(transform_float)

PotAparA = Point('PotAparA', base_address=96, count=2)
PotAparA.set_transformer(transform_float)

FatPotA = Point('FatPotA', base_address=104, count=2)
FatPotA.set_transformer(transform_float)
=======
FreqA = Point('FreqA', base_address=66, count=2, update_interval=5, transformer=transform_float)
UrmsA = Point('UrmsA', base_address=68, count=2, update_interval=5, transformer=transform_float)
UrmsB = Point('UrmsB', base_address=70, count=2, update_interval=5, transformer=transform_float)
UrmsC = Point('UrmsC', base_address=72, count=2, update_interval=5, transformer=transform_float)
IrmsA = Point('IrmsA', base_address=74, count=2, update_interval=5, transformer=transform_float)
PotAtivA = Point('PotAtivA', base_address=80, count=2, update_interval=5, transformer=transform_float)
PotReatA = Point('PotReatA', base_address=88, count=2, update_interval=5, transformer=transform_float)
PotAparA = Point('PotAparA', base_address=96, count=2, update_interval=5, transformer=transform_float)
FatPotA = Point('FatPotA', base_address=104, count=2, update_interval=5, transformer=transform_float)
PotAtivT = Point('PotAtivT', base_address=86, count=2, update_interval=5, transformer=transform_float_PotAtivT)
>>>>>>> dev


MMDemP = Point('MMDemP', base_address=602, count=2)
MMDemP.set_transformer(transform_float)


if __name__ == '__main__':
    config = read_config()
    logging.info("Inicializando leitor dos sensores via Modbus")

    # start the database session
    session = start_db_session()

    modbus_client = ModbusClient(method='rtu', port=config['serial_port']['port'], 
                          baudrate=int(config['serial_port']['baudrate']), 
                          timeout=float(config['serial_port']['timeout']),
                          parity='N', stopbits=2, retry_on_empty=2, reconnect_delay=0.5)

    while(True):
        try:
            for data in PointList:
                if(data.update_value(int(config['serial_port']['slave_id']), modbus_client)):
                    save_data(point=data.get_name(), value=data.get_value(), datetime=time(), session=session)
                sleep(.1)
            sleep(1)
        except Exception as e:
            logging.exception(e)
            sleep(10)
            #tenta novamente
        except KeyboardInterrupt as e:
            logging.exception("Saindo...")
            exit(0)
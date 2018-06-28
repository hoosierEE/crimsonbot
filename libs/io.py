# SparkFun SX1509 GPIO expander library
from machine import Pin, I2C #pylint:disable=import-error
from ustruct import pack, unpack #pylint:disable=import-error

R_PU_B = 0x06 # pull-up 0:disable 1:enable
R_PU_A = 0x07
R_PD_B = 0x08 # pull-down 0:disable 1:enable
R_PD_A = 0x09
R_OD_B = 0x0a # open drain; 0:push-pull, 1:open-drain
R_OD_A = 0x0b
R_DIR_B = 0x0e # pin direction; 0:output, 1:input
R_DIR_A = 0x0f
R_DATA_B = 0x10 # read pin (or write if direction set to output)
R_DATA_A = 0x11

# FIXME interrupts are wonky (writing to (any?) output clears interrupt pin)
R_INTMASK_B = 0x12 # 0:pin interrupts, 1:pin ignored
R_INTMASK_A = 0x13
R_SENS_B = 0x14 # trigger type (2 bits per pin)
R_SENS_A = 0x16 # trigger type (2 bits per pin)
R_INT_SOURCE = 0x18 # 2 bytes, stores status of last interrupt (1: was interrupted) for each pin
RISING = 0b01 # trigger types
FALLING = 0b10
BOTH = 0b11
INPUT = 0 # pin modes
INPUT_PULLUP = 1
INPUT_PULLDOWN = 2
OUTPUT = 3
OUTPUT_PWM = 4  # TODO
OUTPUT_OPENDRAIN = 5

class IO(object):
    # Interface to the SX1509 GPIO expander.
    # Solder-bridge or cut address pads to use non-default address.
    # Constructor:
    # adr (default=0x3e) can be any of: (0x3e|0x3f|0x70|0x71)
    # scl (default=Pin(14)) can be any digital pin.
    # sda (default=Pin(12)) can be any digital pin.
    def __init__(self, adr=0x3e, scl=Pin(14), sda=Pin(12)):
        if adr not in [0x3e, 0x3f, 0x70, 0x71]:
            raise KeyError
        self.scl = scl
        self.sda = sda
        self.adr = adr
        self.I = I2C(sda=sda, scl=scl, freq=100000)
        assert unpack('>H', self.I.readfrom_mem(self.adr, 0x13, 2))[0] == 0xff00 # ensure big endian


    # read/write
    def pin_mode(self, x, y): # x: pin, y: mode (INPUT_PULLUP|INPUT_PULLDOWN|INPUT|OUTPUT|OUTPUT_PWM)
        if y == OUTPUT:
            self.pin_dir(x, 0) # output
            self.write_16(R_OD_B, self.read_16(R_OD_B)&~(1<<x))
        # elif y == OUTPUT_PWM:  # TODO clock setup
        #     self.pin_dir(x, 0)
        #     self.pwm_init(x)
        elif y == OUTPUT_OPENDRAIN:
            self.pin_dir(x, 0)
            self.write_16(R_OD_B, self.read_16(R_OD_B)|(1<<x))
        else:
            self.pin_dir(x, 1) # input
            if y == INPUT_PULLUP:
                self.pin_pull(x, 1)
            elif y == INPUT_PULLDOWN:
                self.pin_pull(x, -1)
            else:
                self.pin_pull(x, 0)
    def pin_read(self, x): # x: pin
        return (self.read_16(R_DATA_B)&(1<<x))>>x
    def pin_write(self, x, y): # x: pin, y: value (0|1)
        if y == 1:
            self.write_16(R_DATA_B, self.read_16(R_DATA_B)|(1<<x))
        else:
            self.write_16(R_DATA_B, self.read_16(R_DATA_B)&~(1<<x))
    def pin_info(self):
        return {'direction': self.read_16(R_DIR_B),
                'value': self.read_16(R_DATA_B),
                'open-drain': self.read_16(R_OD_B),
                'input-pullup': self.read_16(R_PU_B),
                'input-pulldown': self.read_16(R_PD_B)}

    # interrupts
    # FIXME interrupts are wonky (writing to (any?) output clears interrupt pin)
    def interrupt_info(self):
        return {'source': self.interrupt_get_all(),
                'sense': (self.read_16(R_SENS_B)<<8)+self.read_16(R_SENS_A),
                'mask': self.read_16(R_INTMASK_B)}
    def interrupt_enable(self, x, y): # x: pin, y: interrupt type (NONE|RISING|FALLING|BOTH)
        imask = self.read_16(R_INTMASK_B) # 0 sets that pin to be an interrupt
        self.write_16(R_INTMASK_B, imask&~(1<<x))
        mask = (x&7)<<1
        sens = R_SENS_A if x < 8 else R_SENS_B
        isen = self.read_16(sens)&(~(0b11<<mask))|(y<<mask)
        self.write_16(sens, isen)
    def interrupt_get(self, x): # x:pin
        return self.interrupt_get_all()&1<<x
    def interrupt_get_all(self):
        return self.read_16(R_INT_SOURCE)
    def interrupt_clear(self):
        self.write_16(R_INT_SOURCE, 0xffff)

    # helpers
    def read_8(self, x):
        return self.I.readfrom_mem(self.adr, x, 1)[0]
    def read_16(self, x):
        return unpack('>H', self.I.readfrom_mem(self.adr, x, 2))[0]
    def write_8(self, x, y): # x:address, y:data
        self.I.writeto_mem(self.adr, x, y)
    def write_16(self, x, y):
        self.I.writeto_mem(self.adr, x, pack('>H', y))
    def pin_dir(self, x, y): # x:pin, y:direction (0:output 1:input), default:1
        tmp = self.read_16(R_DIR_B)
        if y == 1:
            self.write_16(R_DIR_B, tmp|1<<x)
        else:
            self.write_16(R_DIR_B, tmp&~(1<<x))
    def pin_pull(self, x, y): # x:pin, y:down|none|up (-1|0|1)
        if y == -1:
            tmp = self.read_16(R_PD_B)
            self.write_16(R_PD_B, tmp|(1<<x))
        elif y == 1:
            tmp = self.read_16(R_PU_B)
            self.write_16(R_PU_B, tmp|(1<<x))
        else: # clear BOTH pullup AND pulldown bits for this pin
            tmp = self.I.readfrom_mem(self.adr, R_PU_B, 4)
            self.I.writeto_mem(self.adr, R_PU_B, pack('>I', tmp|1<<x|1<<x+16))

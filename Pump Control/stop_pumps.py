import serial
import milligat

stop = 1

FR_a = 0
FR_e = 0
ser_obj = serial.Serial('COM5',9600)

pump_aLF = milligat.Milligat('A', ser_obj)
pump_eLF = milligat.Milligat('E', ser_obj)
pump_a2LF = milligat.Milligat('A', serial.Serial('COM22',9600))

if stop==1:
    # pump_cLF.stop_pump()
    pump_aLF.stop_pump()
    pump_eLF.stop_pump()
    pump_a2LF.stop_pump()

else:
    # pump_cLF.set_flow_rate(FR_c, pump_type= 'LF')
    pump_aLF.set_flow_rate(FR_a, pump_type= 'LF')
    pump_eLF.set_flow_rate(FR_e, pump_type= 'LF')
    # pump_a2LF.set_flow_rate(FR_a2, pump_type= 'LF')
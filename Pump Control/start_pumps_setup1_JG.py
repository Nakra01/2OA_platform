import serial
import milligat
import time

FR_a = 2
FR_e = 2
#FR_a2 = 0
# Define pumps
ser_obj = serial.Serial('COM5',9600)
pump_aLF = milligat.Milligat('A', ser_obj)
pump_eLF = milligat.Milligat('E', ser_obj)
#pump_a2LF = milligat.Milligat('A', serial.Serial('COM22',9600))
# Set flow rates
pump_aLF.set_flow_rate(FR_a, pump_type= 'LF')
pump_eLF.set_flow_rate(FR_e, pump_type= 'LF')
#pump_a2LF.set_flow_rate(FR_a2, pump_type= 'LF')
time.sleep(0.1)
pump_aLF.set_flow_rate(FR_a, pump_type= 'LF')
pump_eLF.set_flow_rate(FR_e, pump_type= 'LF')
import serial
import milligat

FR_a = 1
FR_e = 1

# Define pumps
ser_obj = serial.Serial('COM5',9600)
pump_aLF = milligat.Milligat('A', ser_obj)
pump_eLF = milligat.Milligat('E', ser_obj)
# Set flow rates
pump_aLF.set_flow_rate(FR_a, pump_type= 'LF')
pump_eLF.set_flow_rate(FR_e, pump_type= 'LF')

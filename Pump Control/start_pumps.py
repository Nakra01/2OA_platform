import serial
import milligat

stop = 0
FR_c = 0.1
FR_a =0.1
FR_e = 0.1

# pump_a = milligat.Milligat('F', serial.Serial('COM14', 9600)) 
# pump_a.set_flow_rate(0.5) 
#pump_c = milligat.Milligat('C', serial.Serial('COM6', 9600)) 
#pump_b = milligat.Milligat('B', serial.Serial('COM5', 9600)) 
ser_obj = serial.Serial('COM5',9600)

pump_cLF = milligat.Milligat('C', serial.Serial('COM22',9600))
# pump_bLF = milligat.Milligat('B', ser_obj5)

pump_aLF = milligat.Milligat('A', ser_obj)

pump_eLF = milligat.Milligat('E', ser_obj)

#pump_b.set_flow_rate(0.5) 
#pump_c.set_flow_rate(0.5) 
if stop==1:
    pump_cLF.stop_pump()
    pump_aLF.stop_pump()
    pump_eLF.stop_pump()
    # pump_bLF.stop_pump()

else:
    pump_cLF.set_flow_rate(FR_c, pump_type= 'LF')
    pump_aLF.set_flow_rate(FR_a, pump_type= 'LF')
    pump_eLF.set_flow_rate(FR_e, pump_type= 'LF')
    # pump_bLF.set_flow_rate(FR_e, pump_type= 'LF')
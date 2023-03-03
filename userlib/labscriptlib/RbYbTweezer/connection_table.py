from labscript import *

from labscript_devices.PulseBlasterUSB import PulseBlasterUSB
from naqslab_devices.NovaTechDDS.labscript_device import NovaTech409B_AC
from labscript_devices.NI_DAQmx.models.NI_USB_6229 import NI_USB_6229
from labscript_devices.NI_DAQmx.models.NI_PCI_6733 import NI_PCI_6733
from labscript_devices.NI_DAQmx.models.NI_USB_6363 import NI_USB_6363
from labscript_devices.IMAQdxCamera.labscript_devices import IMAQdxCamera
from labscript_devices.AndorSolis.labscript_devices import AndorSolis
from labscript_devices.PrincetonInstrumentsCamera.labscript_devices import PrincetonInstrumentsCamera

from labscript_devices.TCPDH_Synth.labscript_devices import *
from labscript_devices.FPGA_Synth.labscript_devices import *

s, ms, us, ns = 1.0, 1e-3, 1e-6, 1e-9

#from labscript_devices.Pyncmaster import Pyncmaster as PulseBlasterUSB
#from labscript_devices.NI_DAQmx.labscript_devices import NI_PCI_6733, NI_PXIe_6361
# from labscript_devices.Arduino_DDS import Arduino_DDS
# from labscript_devices.Arduino_Single_DDS import Arduino_Single_DDS
# from labscript_devices.Arduino_Repump_DDS import Arduino_Repump_DDS
# from labscript_devices.RepumpDDS import RepumpDDS
# from labscript_devices.DDSAD9954 import DDSAD9954
# from labscript_devices.IMAQdxCamera.labscript_devices import IMAQdxCamera
# from labscript_devices.LightCrafterDMD import LightCrafterDMD, ImageSet

# from labscript_utils.unitconversions.AOM_VCO import AOMVCO
# from labscript_utils.unitconversions import UnidirectionalCoilDriver

###############################################################################
#    CONNECTION TABLE
###############################################################################

###############################################################################
#    PULSEBLASTER
###############################################################################

PulseBlasterUSB(name='pulseblaster_0', board_number=1, time_based_stop_workaround=True, time_based_stop_workaround_extra_time=0.5)

Trigger(name='flea2_trigger',        parent_device=pulseblaster_0.direct_outputs, connection = 'flag 3', trigger_edge_type = 'rising')
Trigger(name='andor_camera_trigger', parent_device=pulseblaster_0.direct_outputs, connection = 'flag 1', trigger_edge_type = 'rising')
Trigger(name='flea3_trigger',        parent_device=pulseblaster_0.direct_outputs, connection = 'flag 2', trigger_edge_type = 'rising')



#ClockLine(name='pulseblaster_0_ni_2_clock',             pseudoclock=pulseblaster_0.pseudoclock, connection='flag 23')




# DigitalOut(name='pb_3',  parent_device=pulseblaster_0.direct_outputs, connection = 'flag 3')
DigitalOut(name='pb_4',  parent_device=pulseblaster_0.direct_outputs, connection = 'flag 4', inverted=True)
DigitalOut(name='pb_5',  parent_device=pulseblaster_0.direct_outputs, connection = 'flag 5')
DigitalOut(name='pb_6',  parent_device=pulseblaster_0.direct_outputs, connection = 'flag 6')
DigitalOut(name='pb_7',  parent_device=pulseblaster_0.direct_outputs, connection = 'flag 7')
DigitalOut(name='pb_8',  parent_device=pulseblaster_0.direct_outputs,    connection='flag 8')
# DigitalOut(name='pb_9',  parent_device=pulseblaster_0.direct_outputs, connection = 'flag 9')
DigitalOut(name='pb_10', parent_device=pulseblaster_0.direct_outputs, connection = 'flag 10')
DigitalOut(name='pb_11', parent_device=pulseblaster_0.direct_outputs, connection = 'flag 11')
DigitalOut(name='pb_12', parent_device=pulseblaster_0.direct_outputs, connection = 'flag 12')
# DigitalOut(name='pb_13', parent_device=pulseblaster_0.direct_outputs, connection = 'flag 13')
# DigitalOut(name='pb_14', parent_device=pulseblaster_0.direct_outputs, connection = 'flag 14')
DigitalOut(name='pb_15', parent_device=pulseblaster_0.direct_outputs, connection = 'flag 15')
DigitalOut(name='pb_16', parent_device=pulseblaster_0.direct_outputs, connection = 'flag 16')
DigitalOut(name='pb_17', parent_device=pulseblaster_0.direct_outputs, connection = 'flag 17')

DigitalOut(name='RbImgProbe', parent_device=pulseblaster_0.direct_outputs, connection='flag 9') 
# ClockLine(name='TCPDH_clockline',      pseudoclock=pulseblaster_0.pseudoclock, connection='flag 18')
ClockLine(name='novatech_dds_1_clock', pseudoclock=pulseblaster_0.pseudoclock, connection='flag 13') # Unconneted
ClockLine(name='novatech_dds_2_clock', pseudoclock=pulseblaster_0.pseudoclock, connection='flag 14') 
ClockLine(name='ni_3_clock',            pseudoclock=pulseblaster_0.pseudoclock, connection='flag 20')
ClockLine(name='ni_2_clock',	       pseudoclock=pulseblaster_0.pseudoclock, connection='flag 21')
ClockLine(name='ni_1_clock',           pseudoclock=pulseblaster_0.pseudoclock, connection='flag 22')


# TCPDH_Synth(name='TCPDH_controller',TCPIP_address='192.168.1.100',TCPIP_port=6750,parent_device=TCPDH_clockline,update_mode='synchronous')
# TCPDH_DDS(name='Carrier', parent_device=TCPDH_controller, connection='PDH_carrier')
# TCPDH_StaticDDS(name='Modulation', parent_device=TCPDH_controller, connection='PDH_mod')

# FPGA_Synth(name='FPGA_controller3',TCPIP_address='192.168.1.103',TCPIP_port=5000,parent_device=FPGA_clockline3)
# FPGA_DDS(name='FPGA_DDS3', parent_device=FPGA_controller3, connection='DDS_channel')


'''
Novatech 1
'''
NovaTech409B_AC(name='novatech_dds_1', parent_device=novatech_dds_1_clock, com_port='com3',
              baud_rate=19200,  update_mode='asynchronous')
DDS(name='NT1_1', parent_device=novatech_dds_1, connection='channel 1')
DDS(name='NT1_0', parent_device=novatech_dds_1, connection='channel 0')

# '''
# Novatech 2
# '''
NovaTech409B_AC(name='novatech_dds_2', parent_device=novatech_dds_2_clock, com_port='com5',
              baud_rate=19200,  update_mode='asynchronous')
DDS(name='Rb_repump_F', parent_device=novatech_dds_2, connection='channel 1')
DDS(name='Rb_cooling_F', parent_device=novatech_dds_2, connection='channel 0')


# ClockLine(name='NT_rf_clock', pseudoclock=pb0.pseudoclock, connection='flag 3')
# NovaTechDDS9M(name='novatechdds9m_rf', parent_device=NT_rf_clock, com_port='com4',
              # baud_rate=19200, default_baud_rate=19200, update_mode='asynchronous')
# DDS(name='evap_rf', parent_device=novatechdds9m_rf, connection='channel 0')

# NovaTech409B(name='novatech_static', com_port="com4", baud_rate = 115200,
                # phase_mode='aligned',ext_clk=True, clk_freq=100, clk_mult=5)
# NovaTech409B_AC(name='novatech', parent_device=pulseblaster_0_clockline_slow,
                # com_port="com3", update_mode='asynchronous', phase_mode='aligned',
                # baud_rate = 115200, ext_clk=True, clk_freq=100, clk_mult=5)


###############################################################################
#    NI device 0
###############################################################################

# NI_USB_6233(name='ni_0', parent_device=pulseblaster_0_ni_0_clock, clock_terminal='/Dev0/PFI1', MAX_name = 'Dev0')

# AnalogOut(name='red_MOT_VCO',           parent_device=ni_0, connection='ao0',
#           unit_conversion_class=AOMVCO,                     unit_conversion_parameters={'m':-22.422*10**6, 'b':60.831*10**6, 'magnitudes':['k','M']})
# AnalogOut(name='red_SRS_amp',           parent_device=ni_0, connection='ao1',
#           unit_conversion_class=AOMVCO,                     unit_conversion_parameters={'m':5.4466*10**6, 'b':0.14*10**6, 'magnitudes':['k','M']})
# AnalogOut(name='MOT_field',             parent_device=ni_0, connection='ao2',
#           unit_conversion_class=UnidirectionalCoilDriver,   unit_conversion_parameters={'slope':25, 'shift':0})
# AnalogOut(name='shim_X',                parent_device=ni_0, connection='ao3',
#           unit_conversion_class=UnidirectionalCoilDriver,   unit_conversion_parameters={'slope':0.6, 'shift':-0.022})
# AnalogOut(name='shim_Y',                parent_device=ni_0, connection='ao4',
#           unit_conversion_class=UnidirectionalCoilDriver,   unit_conversion_parameters={'slope':0.6, 'shift':-0.022})
# AnalogOut(name='shim_Z',                parent_device=ni_0, connection='ao5',
#           unit_conversion_class=UnidirectionalCoilDriver,   unit_conversion_parameters={'slope':0.6, 'shift':-0.022})
# AnalogOut(name='blue_MOT_power',        parent_device=ni_0, connection='ao6')
# AnalogOut(name='red_MOT_power',         parent_device=ni_0, connection='ao7')

# DigitalOut(name='blue_MOT_shutter',     parent_device=ni_0, connection='port0/line0')
# DigitalOut(name='blue_MOT_RF_TTL',      parent_device=ni_0, connection='port0/line1')
# DigitalOut(name='MOT_2D_RF_TTL',        parent_device=ni_0, connection='port0/line2')
# DigitalOut(name='red_MOT_shutter',      parent_device=ni_0, connection='port0/line3')
# DigitalOut(name='red_MOT_RF_TTL',       parent_device=ni_0, connection='port0/line4')
# DigitalOut(name='red_SRS_TTL',          parent_device=ni_0, connection='port0/line5')
# DigitalOut(name='repump_707_shutter',   parent_device=ni_0, connection='port0/line6')
# DigitalOut(name='repump_679_shutter',   parent_device=ni_0, connection='port0/line7')

###############################################################################
#    NI device 1
###############################################################################

NI_USB_6229(name='ni_1', parent_device=ni_1_clock, clock_terminal='/Dev1/PFI4', MAX_name = 'Dev1')

AnalogOut(name='Dev1_AO0', parent_device=ni_1, connection='ao0') #,
#           unit_conversion_class=AOMVCO,                     unit_conversion_parameters={'m':-21.57549*10**6, 'b':61.48349*10**6, 'magnitudes':['k','M']})
AnalogOut(name='Dev1_AO1', parent_device=ni_1, connection='ao1')

AnalogOut(name='Dev1_AO2', parent_device=ni_1, connection='ao2') #,
#           unit_conversion_class=AOMVCO,                     unit_conversion_parameters={'m':-21.57549*10**6, 'b':61.48349*10**6, 'magnitudes':['k','M']})
AnalogOut(name='Dev1_AO3', parent_device=ni_1, connection='ao3')

#AnalogIn(name='Dev1_AI0', parent_device=ni_1,connection='ai1')

DigitalOut(name='Dev1_DO0', parent_device=ni_1, connection='port0/line0') # 
DigitalOut(name='Dev1_DO1', parent_device=ni_1, connection='port0/line1')
DigitalOut(name='Dev1_DO2', parent_device=ni_1, connection='port0/line2')
DigitalOut(name='Dev1_DO3', parent_device=ni_1, connection='port0/line3')
DigitalOut(name='Dev1_DO4', parent_device=ni_1, connection='port0/line4')
DigitalOut(name='Dev1_DO5', parent_device=ni_1, connection='port0/line5')
DigitalOut(name='Dev1_DO6', parent_device=ni_1, connection='port0/line6')
DigitalOut(name='Dev1_DO7', parent_device=ni_1, connection='port0/line7')
DigitalOut(name='Dev1_DO8', parent_device=ni_1, connection='port0/line8')
DigitalOut(name='Dev1_DO9', parent_device=ni_1, connection='port0/line9')
DigitalOut(name='Dev1_DO10', parent_device=ni_1, connection='port0/line10')
DigitalOut(name='Dev1_DO11', parent_device=ni_1, connection='port0/line11')
DigitalOut(name='Dev1_DO12', parent_device=ni_1, connection='port0/line12')
DigitalOut(name='Dev1_DO13', parent_device=ni_1, connection='port0/line13')
DigitalOut(name='Dev1_DO14', parent_device=ni_1, connection='port0/line14')
DigitalOut(name='Dev1_DO15', parent_device=ni_1, connection='port0/line15')

###############################################################################
#    NI device 2
###############################################################################

NI_PCI_6733(name='ni_2', parent_device=ni_2_clock, clock_terminal='/Dev2/PFI0', MAX_name = 'Dev2')

AnalogOut(name='Dev2_AO0', parent_device=ni_2, connection='ao0') #,
#           unit_conversion_class=AOMVCO,                     unit_conversion_parameters={'m':-21.57549*10**6, 'b':61.48349*10**6, 'magnitudes':['k','M']})
AnalogOut(name='Coil_Current_Control_1', parent_device=ni_2, connection='ao1')

AnalogOut(name='Coil_Current_Control_2', parent_device=ni_2, connection='ao2') #,
#           unit_conversion_class=AOMVCO,                     unit_conversion_parameters={'m':-21.57549*10**6, 'b':61.48349*10**6, 'magnitudes':['k','M']})
AnalogOut(name='Coil_Current_Control_3', parent_device=ni_2, connection='ao3')


DigitalOut(name='Dev2_DO0', parent_device=ni_2, connection='port0/line0')
DigitalOut(name='Dev2_DO1', parent_device=ni_2, connection='port0/line1')
DigitalOut(name='Dev2_DO2', parent_device=ni_2, connection='port0/line2')
DigitalOut(name='Dev2_DO3', parent_device=ni_2, connection='port0/line3')
DigitalOut(name='Dev2_DO4', parent_device=ni_2, connection='port0/line4')
DigitalOut(name='Dev2_DO5', parent_device=ni_2, connection='port0/line5')
DigitalOut(name='Dev2_DO6', parent_device=ni_2, connection='port0/line6')
DigitalOut(name='Dev2_DO7', parent_device=ni_2, connection='port0/line7')

# # Trigger(   name='GH_camera_trigger',        parent_device=ni_1, connection='port0/line2',  trigger_edge_type = 'falling')


###############################################################################
#    NI device 3
###############################################################################

NI_PCI_6733(name='ni_3', parent_device=ni_3_clock, clock_terminal='/Dev3/PFI0', MAX_name = 'Dev3')

AnalogOut(name='Dev3_AO0', parent_device=ni_2, connection='ao0') #,
#           unit_conversion_class=AOMVCO,                     unit_conversion_parameters={'m':-21.57549*10**6, 'b':61.48349*10**6, 'magnitudes':['k','M']})


DigitalOut(name='Dev3_DO0', parent_device=ni_2, connection='port0/line0')


# # Trigger(   name='GH_camera_trigger',        parent_device=ni_1, connection='port0/line2',  trigger_edge_type = 'falling')

################################################################################
#   NI device 4
################################################################################

# NI_USB_6363(name='ni_3', parent_device=ni_3_clock, clock_terminal='', MAX_name = '')

################################################################################
#   NI device 5
################################################################################

# NI_USB_6363(name='ni_4', parent_device=ni_4_clock, clock_terminal='', MAX_name = '')

################################################################################
#   NI device 6
################################################################################

# NI_PXIe_6361(name='ni_3', parent_device=pulseblaster_0_ni_2_clock, clock_terminal='/Dev2/PFI0', MAX_name = 'Dev2')

# AnalogOut(name='grating_shim_x', parent_device=ni_2, connection='ao0')
# AnalogOut(name='extra', parent_device=ni_2, connection='ao1')

# # DigitalOut(name='newNITest',parent_device=ni_2,connection = 'port0/line0')
# DigitalOut(name='fake3',  parent_device=ni_2, connection = 'port0/line1')

################################################################################
#   Wait Monitor
################################################################################

# WaitMonitor(name='blue_fluor_wait',
#             parent_device=ni_2, connection='port0/line0',
#             acquisition_device=ni_2, acquisition_connection='ctr0',
#             timeout_device=ni_2, timeout_connection='pfi13')


################################################################################
#	FLEA CAMERA
################################################################################

RemoteBLACS('acquisition_computer', 'RbYbCameraPC')

flea2_fw_aquisition_attributes = {
    'AcquisitionAttributes::Height': 964,
    'AcquisitionAttributes::OffsetX': 0,
    'AcquisitionAttributes::OffsetY': 0,
    'AcquisitionAttributes::OutputImageType': 'Grayscale (U8)',
    'AcquisitionAttributes::PacketSize': 4872,
    'AcquisitionAttributes::PixelFormat': 'Mono 8',
    'AcquisitionAttributes::Speed': '800 Mbps',
    'AcquisitionAttributes::Timeout': 10000,
    'AcquisitionAttributes::VideoMode': 'Format 7, Mode 0, 1288 x 964',
    'AcquisitionAttributes::Width': 1288,
}

flea2_fw_sequence_camera_attributes = {
    'CameraAttributes::AutoExposure::Mode': 'Off',
    'CameraAttributes::Brightness::Mode': 'Ignored',
    'CameraAttributes::FrameRate::Mode': 'Off',
    'CameraAttributes::Gain::Mode': 'Absolute',
    'CameraAttributes::Gain::Value': '0.0',
    'CameraAttributes::Gamma::Mode': 'Off',
    'CameraAttributes::Pan::Mode': 'Ignored',
    'CameraAttributes::Sharpness::Mode': 'Off',
    'CameraAttributes::Shutter::Mode': 'Absolute',
    'CameraAttributes::Shutter::Value': 500*us,
    'CameraAttributes::Tilt::Mode': 'Ignored',
    'CameraAttributes::Trigger::TriggerActivation': 'Level High',
    'CameraAttributes::Trigger::TriggerMode': 'Mode 0',
    'CameraAttributes::Trigger::TriggerParameter': 0,
    'CameraAttributes::Trigger::TriggerSource': 'Source 0',
    'CameraAttributes::TriggerDelay::Mode': 'Off'
}

flea2_fw_sequence_camera_attributes = {**flea2_fw_aquisition_attributes, **flea2_fw_sequence_camera_attributes}

flea2_fw_manual_camera_attributes = {
    'CameraAttributes::AutoExposure::Mode': 'Off',
    'CameraAttributes::Brightness::Mode': 'Ignored',
    'CameraAttributes::FrameRate::Mode': 'Off',
    'CameraAttributes::Gain::Mode': 'Absolute',
    'CameraAttributes::Gain::Value': '0.0',
    'CameraAttributes::Gamma::Mode': 'Off',
    'CameraAttributes::Pan::Mode': 'Ignored',
    'CameraAttributes::Sharpness::Mode': 'Off',
    'CameraAttributes::Shutter::Mode': 'Absolute',
    'CameraAttributes::Shutter::Value': 40*us,
    'CameraAttributes::Tilt::Mode': 'Ignored',
    'CameraAttributes::Trigger::TriggerActivation': 'Level High',
    'CameraAttributes::Trigger::TriggerMode': 'Mode 3',
    'CameraAttributes::Trigger::TriggerParameter': 1,
    'CameraAttributes::Trigger::TriggerSource': 'Source 0',
    'CameraAttributes::TriggerDelay::Mode': 'Off'
}

flea2_fw_manual_camera_attributes = {**flea2_fw_aquisition_attributes, **flea2_fw_manual_camera_attributes}

Flea3_USB_1_acquisition_attributes = {
    'ImageFormatControl::Height': 1024,
    'OffsetX': 0,
    'OffsetY': 0,
    'OutputImageType': 'Auto',
    # 'PacketSize': 5184,
    'PixelFormat': 'Mono 8',
    # 'Speed': '800 Mbps',
    'Timeout': 10000,
    # 'VideoMode': 'Format 7, Mode 0, 648 x 488',
    'Width': 1280
}

Flea3_USB_1_sequence_camera_attributes = {
    # 'AutoExposure::Mode': 'Off',
    # 'Brightness::Mode': 'Ignored',
    # 'FrameRate::Mode': 'Off',
    # 'Gain::Mode': 'Absolute',
    # 'Gain::Value': '0.0',
    # 'Gamma::Mode': 'Off',
    # # 'Pan::Mode': 'Ignored',
    # 'Sharpness::Mode': 'Off',
    # 'Shutter::Mode': 'Absolute',
    # 'Shutter::Value': 40*us,
    # # 'Tilt::Mode': 'Ignored',
    # 'Trigger::TriggerActivation': 'Level High',
    # 'Trigger::TriggerMode': 'Mode 1',
    # 'Trigger::TriggerParameter': 0,
    # 'Trigger::TriggerSource': 'Source 0',
    # 'TriggerDelay::Mode': 'Off'
}

Flea3_USB_1_sequence_camera_attributes = {**Flea3_USB_1_acquisition_attributes, **Flea3_USB_1_sequence_camera_attributes}


Flea3_USB_1_manual_camera_attributes = {
    # 'AutoExposure::Mode': 'Off',
    # 'Brightness::Mode': 'Ignored',
    # 'FrameRate::Mode': 'Off',
    # 'Gain::Mode': 'Absolute',
    # 'Gain::Value': '0.0',
    # 'Gamma::Mode': 'Off',
    # # 'Pan::Mode': 'Ignored',
    # 'Sharpness::Mode': 'Off',
    # 'Shutter::Mode': 'Absolute',
    # 'Shutter::Value': 1*ms,
    # # 'Tilt::Mode': 'Ignored',
    # 'Trigger::TriggerActivation': 'Level High',
    # 'Trigger::TriggerMode': 'Mode 3',
    # 'Trigger::TriggerParameter': 1,
    # 'Trigger::TriggerSource': 'Source 0',
    # 'TriggerDelay::Mode': 'Off'
}

Flea3_USB_1_manual_camera_attributes = {**Flea3_USB_1_acquisition_attributes, **Flea3_USB_1_manual_camera_attributes}


Flea3_USB_2_acquisition_attributes = {
    'ImageFormatControl::Height': 1024,
    'OffsetX': 0,
    'OffsetY': 0,
    'OutputImageType': 'Auto',
    # 'PacketSize': 5184,
    'PixelFormat': 'Mono 8',
    # 'Speed': '800 Mbps',
    'Timeout': 10000,
    # 'VideoMode': 'Format 7, Mode 0, 648 x 488',
    'Width': 1280
}

Flea3_USB_2_sequence_camera_attributes = {
    # 'AutoExposure::Mode': 'Off',
    # 'Brightness::Mode': 'Ignored',
    # 'FrameRate::Mode': 'Off',
    # 'Gain::Mode': 'Absolute',
    # 'Gain::Value': '0.0',
    # 'Gamma::Mode': 'Off',
    # # 'Pan::Mode': 'Ignored',
    # 'Sharpness::Mode': 'Off',
    # 'Shutter::Mode': 'Absolute',
    # 'Shutter::Value': 40*us,
    # # 'Tilt::Mode': 'Ignored',
    # 'Trigger::TriggerActivation': 'Level High',
    # 'Trigger::TriggerMode': 'Mode 1',
    # 'Trigger::TriggerParameter': 0,
    # 'Trigger::TriggerSource': 'Source 0',
    # 'TriggerDelay::Mode': 'Off'
}

Flea3_USB_2_sequence_camera_attributes = {**Flea3_USB_2_acquisition_attributes, **Flea3_USB_2_sequence_camera_attributes}


Flea3_USB_2_manual_camera_attributes = {
    # 'AutoExposure::Mode': 'Off',
    # 'Brightness::Mode': 'Ignored',
    # 'FrameRate::Mode': 'Off',
    # 'Gain::Mode': 'Absolute',
    # 'Gain::Value': '0.0',
    # 'Gamma::Mode': 'Off',
    # # 'Pan::Mode': 'Ignored',
    # 'Sharpness::Mode': 'Off',
    # 'Shutter::Mode': 'Absolute',
    # 'Shutter::Value': 1*ms,
    # # 'Tilt::Mode': 'Ignored',
    # 'Trigger::TriggerActivation': 'Level High',
    # 'Trigger::TriggerMode': 'Mode 3',
    # 'Trigger::TriggerParameter': 1,
    # 'Trigger::TriggerSource': 'Source 0',
    # 'TriggerDelay::Mode': 'Off'
}

Flea3_USB_2_manual_camera_attributes = {**Flea3_USB_2_acquisition_attributes, **Flea3_USB_2_manual_camera_attributes}


# IMAQdxCamera(
#    name ='Flea2_FW',
#    parent_device=flea2_trigger,
#    connection='trigger',
#    trigger_duration=10*us,
#    serial_number='B09D01008CFFD7',
#    trigger_edge_type='rising',
# #    worker= localhost,
# #    orientation = 'grating',
#    camera_attributes=flea2_fw_sequence_camera_attributes,
#    manual_mode_camera_attributes=flea2_fw_manual_camera_attributes
# )

IMAQdxCamera(
   name ='Flea3_USB_1',
   parent_device=flea3_trigger,
   connection='trigger',
   trigger_duration=10*us,
#    serial_number='B09D01009014F1',
    serial_number='1E1001539FC5',
   trigger_edge_type='rising',
#    worker= localhost,
#    orientation = 'grating',
   camera_attributes=Flea3_USB_1_sequence_camera_attributes,
   manual_mode_camera_attributes=Flea3_USB_1_manual_camera_attributes
)


IMAQdxCamera(
   name ='Flea3_USB_2',
   parent_device=flea3_trigger,
   connection='trigger',
   trigger_duration=10*us,
#    serial_number='B09D01009014F1',
    serial_number='1E10015491E3',
   trigger_edge_type='rising',
#    worker= localhost,
#    orientation = 'grating',
   camera_attributes=Flea3_USB_2_sequence_camera_attributes,
   manual_mode_camera_attributes=Flea3_USB_2_manual_camera_attributes
)


andor_attributes = {
    'trigger': 'external', 
    'exposure_time':  200 * us,     
    'acquisition': 'kinetic_series',
    'number_kinetics': 3,  
    'kinetics_period': 30 * ms,
    'readout': 'full_image',
    'int_shutter_mode': 'perm_open',
    'acquisition_timeout': 130000,
    'temperature': -70,
    'water_cooling': False,
    'cooldown':True,
}

manual_mode_andor_attributes = {
    'acquisition': 'single',
    'trigger': 'internal',
    'exposure_time': 20 * us,
    'number_kinetics': 1,
    'int_shutter_mode': 'perm_open',
}

# AndorSolis(name='Andor_iXon_ultra',
#     parent_device=andor_camera_trigger,
#     connection='trigger',
#     orientation = 'z_insitu_ccd',
#     trigger_duration=102*us,
#     serial_number=5555,
#     camera_attributes=andor_attributes,
#     manual_mode_camera_attributes=manual_mode_andor_attributes,
#     exception_on_failed_shot=False,
#     worker=acquisition_computer)

################################################################################
#   PIXIS Camera
################################################################################

# PIXIS_sequence_camera_attributes = {'ExposureTime': 10, 'SensorTemperatureSetPoint': -75}

# PrincetonInstrumentsCamera(name='PIXIS', parent_device=PIXIS_trigger, connection = 'trigger', camera_ID = 0, orientation = "vertical"
# , camera_attributes=PIXIS_sequence_camera_attributes, worker=acquisition_computer)

# FlyCapture2Camera(
#     name = 'flea_camera',
#     parent_device=flea_camera_trigger,
#     connection='trigger',
#     serial_number='1E1000F7DC41',
#     trigger_edge_type='rising',
#     worker=acquisition_computer,
#     orientation = 'grating',
#     camera_attributes=FleaCameraUSB_sequence_camera_attributes,
#     manual_mode_camera_attributes=FleaCameraUSB_manual_camera_attributes
# )

# Grasshopper_manual_camera_attributes = {
#     'CameraAttributes::AcquisitionControl::ExposureMode': 'Timed',
#     'CameraAttributes::AcquisitionControl::TriggerActivation': 'Falling Edge',
#     'CameraAttributes::AcquisitionControl::TriggerMode': 'Off',
#     'CameraAttributes::AcquisitionControl::TriggerSelector': 'Frame Start',
#     'CameraAttributes::AcquisitionControl::TriggerSource': 'Line 0',
# }

# Grasshopper_sequence_camera_attributes = {
#     'CameraAttributes::AcquisitionControl::ExposureMode': 'Trigger Width',
#     'CameraAttributes::AcquisitionControl::TriggerActivation': 'Falling Edge',
#     'CameraAttributes::AcquisitionControl::TriggerMode': 'On',
#     'CameraAttributes::AcquisitionControl::TriggerSelector': 'Exposure Active',
#     'CameraAttributes::AcquisitionControl::TriggerSource': 'Line 0',
# }

# FleaCameraUSB_camera_attributes = {
#     'AcquisitionAttributes::Timeout': 10000,
#     'CameraAttributes::AcquisitionControl::AcquisitionMode': 'Continuous',
#     'CameraAttributes::AcquisitionControl::ExposureMode': 'Trigger Width',
#     'CameraAttributes::AcquisitionControl::TriggerActivation': 'Falling Edge',
#     'CameraAttributes::AcquisitionControl::TriggerDelay': 0.0,
#     'CameraAttributes::AcquisitionControl::TriggerDelayEnabled': 0,
#     'CameraAttributes::AcquisitionControl::TriggerMode': 'On',
#     'CameraAttributes::AcquisitionControl::TriggerSelector': 'Exposure Active',
#     'CameraAttributes::AcquisitionControl::TriggerSource': 'Line 0',
# }

# IMAQdxCamera(
#     name ='GrassHp_XZ',
#     parent_device=GH_camera_trigger,
#     connection='trigger',
#     serial_number='1E1000E6C21E',
#     trigger_edge_type='falling',
# 	worker=acquisition_computer,
# 	orientation = 'horizontal',
#     camera_attributes=Grasshopper_sequence_camera_attributes,
#     manual_mode_camera_attributes=Grasshopper_manual_camera_attributes,
# )
################################################################################
if __name__ == '__main__':
    start()
    # Carrier.set_freq(0,1e9) # This line is required for succesful compilation of the connection table.
    stop(1)

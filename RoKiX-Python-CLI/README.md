# RoKiX Python CLI


## Rohm sensors and applications

| Part / Name | Part type | Directory | Driver|  Application | File|
|:-|:-|:-|:-|:-|:-|
| BD7411G | HALL sensor | bd7411g | bd7411g_driver.py 
||||| DataLogger | bd7411g_data_logger.py |
| BH1726NUC | Light sensor | bh1726nuc | bh1726nuc_driver.py 
|||||| DataLogger | bh1726nuc_data_logger.py |
| BH1730FVC | Light sensor | bh1730fvc | bh1730fvc_driver.py 
||||| DataLogger | bh1730fvc_data_logger.py |
| BH1749NUC | RGB color sensor | bh1749nuc | bh1749nuc_driver.py 
||||| DataLogger | bh1749nuc_data_logger.py |
| BH1792GLC | Optical heart rate | bh1792glc |bh1792glc_driver.py |||
|||||Datalogger in synchronized mode|bh1792glc_data_logger.py|
|||||Datalogger with non synchronized measurement mode using IR leds|bh1792glc_data_logger_nosync.py|
|||||Datalogger in non synchronized mode|bh1792glc_data_logger_single_meas.py.py|
| BM1383AGLV | Barometer | bm1383aglv |bm1383aglv_driver.py |||
|||||Datalogger|bm1383aglv_data_logger.py|
| BM1422AGMV | Magnetometer | bm1422agmv |bm1422agmv_driver.py 
|||||Datalogger|bm1422agmv_data_logger.py|
| RPR0521RS | 3 in 1 proximity sensor | rpr0521rs | rpr0521rs_driver.py |
|||||Datalogger|rpr0521rs_data_logger.py |

## Kionix sensors and applications

| Part / Name | Part type | Directory | Driver|  Application | File|
|:-|:-|:-|:-|:-|:-|
| KMX62 | Accelerometer/Magnetometer 6-axis combo | kmx62 |kmx62_driver.py		|  | |
|||||Datalogger|kmx62_data_logger.py|
| KMX64 | Accelerometer/Magnetometer 6-axis combo | kmx64 |kmx64_driver.py		|  | |
|||||Datalogger|kmx64_data_logger.py|
| KX012 / KX022 / KX023 / KX112 / KX122 / KX123 / KX124  | Accelerometer | kx022_kx122 |kx022_driver.py		|||
||||| Data- & double tap event logger| kx022_data_dt_logger.py |
||||| Datalogger | kx022_data_logger.py|
||||| Data- & tilt event logger | kx022_data_tilt_logger.py |
||||| Data- & Wake up event logger | kx022_data_wu_logger.py |
||||| Accelerometer + Magnetometer(kmx62) Datalogger|kx022_kmx62_data_logger.py|
||||| Double tap gesture test applcation | kx022_test_dt.py |
||||| tilt test application |kx022_test_tilt_position.py|
||||| Wakeup test application |kx022_test_wu.py|
||||| Data- & free fall event logger | kx122_data_ff_logger.py |
||||| Data- & free fall event test application | kx122_test_freefall.py
| KX126 / KX127 | Pedometer / Accelerometer | kx126 |kx126_driver.py		|||
|||||Data- & Doubletap event logger|kx126_data_dt_logger.py|
|||||Data- & Freefall event logger|kx126_data_ff_logger.py|
|||||Datalogger|kx126_data_logger.py|
|||||Data- & Pedometer event logger|kx126_data_pedometer_logger.py|
|||||Data- & Pedometer event logger|kx126_data_step_logger.py|
|||||Data- & Tiltposition event logger|kx126_data_tilt_logger.py|
|||||Data- & Wake up + Back to sleep event logger|kx126_data_wu_bts_logger.py|
|||||Pedometer test applications |kx126_pedometer.py|
|||||Start pedometer/ Read accumulated steps|kx126_read_step_count.py|
|||||Doubletap test application | kx126_test_double_tap.py|
|||||Freefall test application |  kx126_test_freefall.py|
|||||Tilt position test application |kx126_test_tilt_position.py|
|||||Wake up + Back to Sleep test application | kx126_test_wu_bts.py |
|||||Pedometer event logger|kx126_pedometer.py|
| KX132 | Accelerometer | kx132 |kx132_driver.py|||
|||||Datalogger|kx132_data_logger.py|
|||||Data- & Wake Up + Back to Sleep event logger|kx132_data_wu_bts_logger.py|
|||||Dual Accelerometer Datalogger|kx132_kx122_data_logger.py|
|||||ADP- & Raw-Datalogger|kx132_raw_adp_logger.py|
||||| Raw data, ADP data and wake up from ADP data datalogger| kx132_raw_adpwufbts_logger.py
||||| FIFO watermark test application | kx132_test_fifo_stream_w_watermark.py |
|||||Wake Up + Back to Sleep|kx132_test_wu_bts.py|
| KX220  | Accelerometer | kx220 |kx220_driver.py		|||
|||||Datalogger|kx220_data_logger.py|
| KX222 / KX224 | Accelerometer | kx224 |kx224_driver.py		|||
|||||Datalogger|kx224_data_logger.py|
| KXD94 | Analog Accelerometer | kxd94 |kxr9d_driver.py		|||
|||||Datalogger|kxr9d_data_logger.py|
| KXR94 | Analog Accelerometer | kxr94 |kxr94_driver.py		|||
|||||Datalogger|kxr94_data_logger.py|
| KXTJ3 / KXCJC | Accelerometer | kxtj3 |kxtj3_driver.py		|||
|||||Datalogger|kxtj3_data_logger.py.py|

## Dependencies

To install dependencies run:

* Windows
    
        pip install -r requirements_windows.txt -r requirements_cloud.txt
    
* Linux

        pip install -r requirements_linux.txt -r requirements_cloud.txt

* <p>(Optional) Install  dependencies for plot.py</p>

        pip install -r requirements_plot.py
    
* To get/update board configuration files run:

        python get_configs.py

    Board configurations will be placed to cfg/. Stream configuration files will be included in this download.

## Quick guide

By default RoKiX Python CLI uses board rokix_board_rokix_sensor_node_i2c. To use different board, change board value in rokix_settings.cfg. More info can be found in "RoKiX IoT Platform Users Guide.pdf" chapter 6.4.

* Datalogging
    
    RoKiX Python CLI supports many prebuilt dataloggers listed above. You can start datalogging with following command:
        
        cd kx022
        python kx022_data_logging.py

    To save log data to file run

        python kx022_data_logging.py --filename <filename>
    
    if file with the same name exists, it will be renamed with trailing numbers, e.g. filename0000 or filename0001

* stream_logger.py

    stream_logger.py can be used to log data using stream_configuration files as are used by RoKiX Windows GUI. 

        python stream_logger.py <stream_configuration_file_name>
    
    stream configuration files can be fetched with get_configs.py [Refer to dependencies section](##Dependencies) on using get_configs.py.

* <p>plot.py</p>

    <p>plot.py can be used to plot data that have been logged with RoKiX platform.</p>

        python plot.py <filename>


For more information about RoKiX Python CLI refer to chapter 6. in "RoKiX IoT Platform Users Guide.pdf".

## Examples

Examples directory contains examples on using RoKiX Python CLI library.

|file           |   Purpose |
|:-------------|:-------------|
|i2c_test.py | Minimal application to access sensor through i2c bus
|kx022_register_dump.py|Displays register contents of kx022|
|rokix_board_version_info.py|Displays information about RoKiX Sensor Node|
|rokix_sensor_node_gpio.py|Utility functions to control RoKiX Sensor Node|
|tilt_algorithm.py|Tilt algorithm for acceleration data|

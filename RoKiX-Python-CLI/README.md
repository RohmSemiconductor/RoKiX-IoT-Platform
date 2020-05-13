# RoKiX Python CLI

## Kionix sensors and applications

| Part / Name | Part type | Directory | Driver|  Application | File|
|:-|:-|:-|:-|:-|:-|
| KX132 | Accelerometer | kx132 |kx132_driver.py|||
|||||Datalogger|kx132_data_logger.py|
||||| Data logger using FIFO | kx132_fifo_logger.py |
|||||Data- & Wake Up + Back to Sleep event logger|kx132_data_wu_bts_logger.py|
|||||Dual Accelerometer Datalogger|kx132_kx122_data_logger.py|
|||||ADP- & Raw-Datalogger|kx132_raw_adp_logger.py|
||||| Raw data, ADP data and wake up from ADP data datalogger| kx132_raw_adpwufbts_logger.py |
||||| FIFO watermark test application | kx132_test_fifo_stream_w_watermark.py |
|||||Wake Up + Back to Sleep|kx132_test_wu_bts.py|
| KX134 | Accelerometer | kx134 |kx134_driver.py|||
||||| ADP data and wake up from ADP data datalogger| kx134_adpwufbts_logger.py |
|||||Datalogger|kx134_data_logger.py|
||||| Data logger using FIFO | kx134_fifo_logger.py |
|||||ADP- & Raw-Datalogger|kx134_raw_adp_logger.py|
||||| Raw data, ADP data and wake up from ADP data datalogger| kx134_raw_adpwufbts_logger.py |
|||||Wake Up + Back to Sleep|kx134_test_wu_bts.py|
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

By default RoKiX Python CLI uses board cfg\rokix_board_cy8ckit059_i2c_a3.json. To use different board, change board value in rokix_settings.cfg. More info can be found in "RoKiX IoT Platform Users Guide.pdf" chapter 6.4.

* Datalogging
    
    RoKiX Python CLI supports many prebuilt dataloggers listed above. You can start datalogging with following command:
        
        cd kx132
        python kx132_data_logging.py

    To save log data to file run

        python kx132_data_logging.py --filename <filename>
    
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
|rokix_board_version_info.py|Displays information about RoKiX Sensor Node|

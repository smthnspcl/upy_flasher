## upy_flasher
[![Build Status](http://build.eberlein.io:8080/job/upy_flasher/badge/icon)](http://build.eberlein.io:8080/job/upy_flasher/)

### how to ...

#### ... use it
```
./flash.py --help

./flash.py {arguments}
{arguments}			{default}
	-p	--port		/dev/ttyUSB0
	-b	--binary	firmware/esp32-20180627-v1.9.4-225-gd8dc918d.bin
	-e	--erase		not set / false
	-c	--chip		esp32
	-u	--upload	[]
				-u can be used multiple times for multiple files
	-h	--help
```
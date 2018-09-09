import pyb

uart = pyb.UART(6, 115200)
pyb.repl_uart(uart)
print("REPL is also on UART 6 (Y1=Tx Y2=Rx)")

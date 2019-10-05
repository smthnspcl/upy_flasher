#!/usr/bin/python3

from os import listdir
from subprocess import Popen, PIPE
from sys import argv
from time import sleep


class Runnable(object):
    @staticmethod
    def run(cmd, success=None, fail=None, _print=False):
        print(cmd)
        p = Popen(cmd.split(' '), stdout=PIPE)
        p.wait()
        d = p.stdout.read()
        if _print:
            print(d)
        if success is not None:
            for s in success:
                if s not in d:
                    return False
        if fail is not None:
            for f in fail:
                if f in d:
                    return False
        return True


class Configuration(object):
    port = "/dev/ttyUSB0"
    chip = "esp32"
    binary = "firmware/esp32-20180627-v1.9.4-225-gd8dc918d.bin"
    erase = False
    upload = []

    def __init__(self, **kwargs):
        if "port" in kwargs:
            self.port = kwargs.get("port")
        if "chip" in kwargs:
            self.chip = kwargs.get("chip")
        if "binary" in kwargs:
            self.binary = kwargs.get("binary")
        if "erase" in kwargs:
            self.erase = kwargs.get("erase")
        if "upload" in kwargs:
            self.upload += kwargs.get("upload")

    @staticmethod
    def help():
        print("./flash.py {arguments}")
        print("{arguments}\t\t\t{default}")
        print("\t-p\t--port\t\t/dev/ttyUSB0")
        print("\t-b\t--binary\tfirmware/esp32-20180627-v1.9.4-225-gd8dc918d.bin")
        print("\t-e\t--erase\t\tnot set / false")
        print("\t-c\t--chip\t\tesp32")
        print("\t-u\t--upload\t[]")
        print("\t\t\t\t-u can be used multiple times for multiple files")
        print("\t-h\t--help")
        exit()

    @staticmethod
    def parse(_argv):
        cfg = Configuration()
        i = 0
        while i < len(_argv):
            if _argv[i] in ["-p", "--port"]:
                cfg.port = _argv[i + 1]
            elif _argv[i] in ["-b", "--binary"]:
                cfg.binary = _argv[i + 1]
            elif _argv[i] in ["-e", "--erase"]:
                cfg.erase = True
            elif argv[i] in ["-c", "--chip"]:
                cfg.chip = _argv[i + 1]
            elif argv[i] in ["-u", "--upload"]:
                cfg.upload += _argv[i + 1]
            elif argv[i] in ["-h", "--help"]:
                Configuration.help()
            i += 1
        return cfg


class Flasher(Runnable):
    _erase = None
    _write = None
    cfg = None

    def __init__(self, cfg):
        self.cfg = cfg
        base = "esptool.py --chip " + cfg.chip + " --port " + cfg.port
        if cfg.erase:
            self._erase = base + " erase_flash"
        if cfg.binary is not None:
            self._write = base + " write_flash -z 0x1000 " + cfg.binary

    def write(self):
        return self.run(self._write, success=["Compressed", "Wrote", "Hash of data verified."])

    def erase(self):
        return self.run(self._erase, success=["Chip erase completed successfully"])

    def flash(self):
        if self.cfg.chip is None or self.cfg.port is None:
            print("chip / port not supplied")
            return False
        if self.cfg.erase:
            if self.erase():
                print("erase successful")
            else:
                print("erase failed")
        if self.cfg.binary is not None:
            if self.write():
                print("write successful")
            else:
                print("write failed")


class FileSystem(Runnable):

    def __init__(self, cfg):
        self.base = "ampy -p " + cfg.port

    def put(self, _f):
        if self.run(self.base + " put " + _f):
            print("put", _f)
        sleep(0.5)

    def put_directory(self, directory):
        if not directory.endswith('/'):
            directory += '/'
        _ = listdir(directory)
        print("putting", len(_), "files")
        for f in _:
            self.put(directory + f)
            sleep(1)


def flash(c):
    f = Flasher(c)
    f.flash()


def upload(c):
    f = FileSystem(c)
    f.put_directory("libs")
    f.put_directory("scripts/test")


def main():
    print("parsing args")
    c = Configuration.parse(argv)
    print("flashing")
    flash(c)
    if c.upload is not None:
        print("uploading")
        upload(c)


if __name__ == '__main__':
    main()

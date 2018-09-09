from os import listdir
from subprocess import Popen, PIPE
from sys import argv


class Runnable(object):
    @staticmethod
    def run(cmd, success=None, fail=None, _print=False):
        print cmd
        p = Popen(cmd.split(' '), stdout=PIPE)
        p.wait()
        d = p.stdout.read()
        if _print:
            print d
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
    port = None
    chip = None
    binary = None
    erase = None

    def __init__(self, *args, **kwargs):
        self.port = kwargs.get("port")
        if self.port is None:
            self.port = "/dev/ttyUSB0"
        self.chip = kwargs.get("chip")
        if self.chip is None:
            self.chip = "esp32"
        self.binary = kwargs.get("binary")
        if self.binary is None:
            self.binary = "firmware/esp32-20180627-v1.9.4-225-gd8dc918d.bin"
        self.erase = kwargs.get("erase")
        if self.erase is None:
            self.erase = True

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
            print "chip / port not supplied"
            return False
        if self.cfg.erase:
            if self.erase():
                print "erase successful"
            else:
                print "erase failed"
        if self.cfg.binary is not None:
            if self.write():
                print "write successful"
            else:
                print "write failed"


class FileSystem(Runnable):

    def __init__(self, cfg):
        self.base = "ampy -p " + cfg.port

    def put(self, _f):
        if self.run(self.base + " put " + _f):
            print "put", _f

    def put_directory(self, directory):
        if not directory.endswith('/'):
            directory += '/'
        _ = listdir(directory)
        print "putting", len(_), "files"
        for f in _:
            self.put(directory + f)


if __name__ == '__main__':
    print "parsing args"
    c = Configuration.parse(argv)
    print "init flasher"
    f = Flasher(c)
    f.flash()
    print "init fs"
    f = FileSystem(c)
    f.put_directory("libs")
    f.put_directory("scripts/test")

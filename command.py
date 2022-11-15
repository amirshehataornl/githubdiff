import sys, os, shlex, subprocess, threading, ctypes
from util import prformat, fg, bg

class Command(threading.Thread):
    def __init__(self, cmd, wait_event = None, fake=False,
                 verbose=False, dump_file=None):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.thread_id = threading.get_ident()
        self.rc = 0
        self.rc_output = ''
        self.wait_event = wait_event
        self.subprocess = None
        self.fake = fake
        self.verbose = verbose
        self.dump_file = dump_file

    def exec_cmd(self):
        if self.verbose:
            prformat(fg.green+fg.bold, self.cmd)
        if not self.fake:
            args = shlex.split(self.cmd)
            try:
                self.subprocess = subprocess.Popen(args, stderr=subprocess.STDOUT,
                        stdout=subprocess.PIPE)
            except Exception as e:
                prformat(fg.bold+fg.red, "Failed ---> %s" % self.cmd)
                raise e
            t = self.subprocess.communicate()[0],self.subprocess.returncode

            cmd_out = t[0].decode("utf-8", errors="ignore")

            out = "\n"+"rc = "+str(t[1])+"\n"+cmd_out
            if self.verbose:
                prformat(fg.orange, out)

            # write raw output in dump file
            if self.dump_file:
                self.dump_file.write(self.cmd+"\n")
                self.dump_file.write(out)

            return int(t[1]), cmd_out
        else:
            return 0, ""

    def run(self):
        self.rc, self.rc_output = self.exec_cmd()

        if self.wait_event:
            self.wait_event.set()

    def raise_exception(self):
        self.subprocess.terminate()
        self.subprocess.kill()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(self.thread_id,
                        ctypes.py_object(SystemExit))
        if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(self.thread_id, 0)

import time, yaml

reset = '\033[0m'
bold = '\033[01m'
disable = '\033[02m'
underline = '\033[04m'
reverse = '\033[07m'
strikethrough = '\033[09m'
invisible = '\033[08m'

class fg:
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'
    bold = '\033[1m'

class bg:
    black = '\033[40m'
    red = '\033[41m'
    green = '\033[42m'
    orange = '\033[43m'
    blue = '\033[44m'
    purple = '\033[45m'
    cyan = '\033[46m'
    lightgrey = '\033[47m'

class ATFDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(ATFDumper, self).increase_indent(flow, False)

def get_today():
    info = time.localtime()
    today = "%d-%d-%d" % (info.tm_year, info.tm_mon, info.tm_mday)
    return today

def get_now():
    info = time.localtime()
    time_info = "%d.%d" % (info.tm_hour, info.tm_min)
    return time_info

def prformat(color, text):
    print(color, text, reset)

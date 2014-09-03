import logging
import logging.handlers

log = logging.getLogger("sysloger")
log.setLevel(logging.DEBUG)
#log.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - [%(name)s] - %(levelname)s - %(filename)s - %(lineno)d - %(message)s")

# Log to syslog
sysloghandler = logging.handlers.SysLogHandler(address = '/dev/log')
sysloghandler.setLevel(logging.DEBUG)
sysloghandler.setFormatter(formatter)
log.addHandler(sysloghandler)

# Log to file
filehandler = logging.FileHandler("debug.txt", "w")
filehandler.setLevel(logging.DEBUG)
filehandler.setFormatter(formatter)
log.addHandler(filehandler)

# Log to stdout too
streamhandler = logging.StreamHandler()
streamhandler.setLevel(logging.DEBUG)
streamhandler.setFormatter(formatter)
log.addHandler(streamhandler)

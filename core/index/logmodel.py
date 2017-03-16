import logging
import datetime

# the parameter is "/yourpath/20160626.log"
# it is an absolute path,such as "/home/xxx/yyy/20160626.log"
def createlogger(filename):
	nowstr=datetime.datetime.now().strftime("%Y-%m-%d")
	logger=logging.getLogger(nowstr)
	handler=logging.FileHandler(filename)
	formatter=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	logger.setLevel(10)
	return logger

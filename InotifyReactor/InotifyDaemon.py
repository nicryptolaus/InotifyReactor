#!/usr/bin/env python

import signal
from InotifyReactor import *

class InotifyDaemon(multiprocessing.Process):

  def __init__(self, directory = "/tmp", eventMask = IN_CLOSE_WRITE,
      queueSize = 64):

    super(InotifyDaemon, self).__init__()

    self.directory = directory
    self.eventMask = eventMask
    self.eventQueue = multiprocessing.Queue(queueSize)
    self.processId = os.getpid()
    self.logger = Logger.create(self.__class__.__name__)

  def run(self):
    self.logger.info("Starting reactor")

    try:
      reactor = InotifyReactor(queue=self.eventQueue)
      reactor.add_watch(self.directory, self.eventMask)
      self.logger.info("Watching {0} for events {1}".format(
        self.directory, Inotify.EventMask(self.eventMask)))
      reactor.run()
    except Exception as e:
      self.logger.error("Encountered an exception: {0}".format(e))
      pass
    finally:
      self.logger.info("Shutting down reactor")
      reactor.shutdown()

if __name__ == '__main__':

  # Ignore SIGINT
  signal.signal(signal.SIGINT, signal.SIG_IGN)

  d = InotifyDaemon()
  d.start()
  d.join()
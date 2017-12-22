from time import sleep
from os import environ

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.types import SubscribeOptions
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet.task import LoopingCall

from autobahn import wamp

from config import APP_DOMAIN_NAME


MODULE_NAME = 'camera'

BASE_NAME = APP_DOMAIN_NAME + '.' + MODULE_NAME


class Component(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        self.tick = False
        def on_trigger(a):
            print("Got camera capture event: {}".format(a))
            sleep(1)
            self.publish(u'{}.captured'.format(BASE_NAME), 'images/icon.png')

        yield self.subscribe(on_trigger, u'{}.capture'.format(BASE_NAME))
        self._tick_loop = LoopingCall(self._tick)
        self._tick_loop.start(6.5)

    def _tick(self):
        print("publish: {}.heartbeat".format(BASE_NAME))
        self.publish(u'{}.heartbeat'.format(BASE_NAME), self.tick)
        self.tick = not self.tick

    def onDisconnect(self):
        print("disconnected")
        reactor.stop()


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"test",
    )
    runner.run(Component)

from time import sleep
from os import environ

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.types import SubscribeOptions
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet.task import LoopingCall

from autobahn import wamp

from config import APP_DOMAIN_NAME
from camera_twisted import MODULE_NAME as CAMERA_MODULE_NAME

MODULE_NAME = 'calculate'

BASE_NAME = APP_DOMAIN_NAME + '.' + MODULE_NAME


class Calculate:

    def __init__(self, instance):
        self.instance = instance

    def __call__(self, a):
        print("Captured image: {}".format(a))
        for i in range(5):
            print('  calculate running')
            sleep(1)
        image_name = 'images/image.png'
        pub_name = u'{}.finished'.format(BASE_NAME)
        print('publish: {}'.format(pub_name, image_name))
        self.instance.publish(u'{}.finished'.format(BASE_NAME), {'time_used': 12,
                                                         'image': image_name,
                                                         'result': [('T1', 23), ('T2', 5)]})

class Component(ApplicationSession):
    
    @inlineCallbacks
    def onJoin(self, details):
        self.tick = False
        
        def call(a):
            print("Captured image: {}".format(a))
            for i in range(5):
                print('  calculate running')
                sleep(1)
            image_name = 'images/image.png'
            pub_name = u'{}.finished'.format(BASE_NAME)
            print('publish: {}'.format(pub_name, image_name))
            self.publish(u'{}.finished'.format(BASE_NAME), {'time_used': 12,
                                                             'image': image_name,
                                                             'result': [('T1', 23), ('T2', 5)]})
        # yield self.subscribe(Calculate(self), u'{}.{}.captured'.format(APP_DOMAIN_NAME, CAMERA_MODULE_NAME))       
        yield self.subscribe(call, u'{}.{}.captured'.format(APP_DOMAIN_NAME, CAMERA_MODULE_NAME))           
        self._tick_loop = LoopingCall(self._tick)
        self._tick_loop.start(6.1)

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

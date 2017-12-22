from time import sleep
from os import environ

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.types import SubscribeOptions
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet.task import LoopingCall

from autobahn import wamp

from config import APP_DOMAIN_NAME
from calculate_twisted import MODULE_NAME as CALCULATE_MODULE_NAME

MODULE_NAME = 'lora'

BASE_NAME = APP_DOMAIN_NAME + '.' + MODULE_NAME


class LoRaSend:

    def __init__(self, instance):
        self.instance = instance
        
    def __call__(self, a):
        print("Got send event: {}".format(a))
        for i in range(5):
            print('  send lora running')
            sleep(1)
        image_name = 'images/image.png'
        pub_name = u'{}.sent'.format(BASE_NAME)
        print('publish: {} {}'.format(pub_name, image_name))
        self.instance.publish(pub_name, {'image': image_name,
                                         'payload': 'DFECACCAS*#(E)(9qw0e98qwe'})

class Component(ApplicationSession):
    
    @inlineCallbacks
    def onJoin(self, details):
        self.tick = False
        def call(a):
            print("Got send event: {}".format(a))
            for i in range(5):
                print('  send lora running')
                sleep(1)
            image_name = 'images/image.png'
            pub_name = u'{}.sent'.format(BASE_NAME)
            print('publish: {} {}'.format(pub_name, image_name))
            self.publish(pub_name, {'image': image_name,
                                             'payload': 'DFECACCAS*#(E)(9qw0e98qwe'})        
        #yield self.subscribe(LoRaSend(self), u'{}.{}.finished'.format(APP_DOMAIN_NAME, CALCULATE_MODULE_NAME))           
        yield self.subscribe(call, u'{}.{}.finished'.format(APP_DOMAIN_NAME, CALCULATE_MODULE_NAME))           
        self._tick_loop = LoopingCall(self._tick)
        self._tick_loop.start(6.8)
    
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
from bpy.app import timers
from functools import partial


class Simulate:
    @staticmethod
    def press(ctx, mouse, key):
        ctx.window.event_simulate(key, 'PRESS', x=mouse[0], y=mouse[1])
    
    @staticmethod
    def release(ctx, mouse, key):
        ctx.window.event_simulate(key, 'PRESS', x=mouse[0], y=mouse[1])
    
    @staticmethod
    def press_and_release(ctx, mouse, key, time=0.05):
        # Wnd.event_simulate()
        Simulate.press(ctx, mouse, key)
        timers.register(partial(Simulate.release, ctx, mouse, key), first_interval=time)

# TODO. support args and kwargs.
class Event:
    def __init__(self):
        self.callbacks = []
    
    def set_callbacks(self, *args):
        for arg in args:
            self.callbacks.append(arg)
    
    def add_callback(self, call):
        self.callbacks.append(call)
        
    def remove_callbacks(self):
        self.callbacks.clear()

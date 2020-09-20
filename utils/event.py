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
        
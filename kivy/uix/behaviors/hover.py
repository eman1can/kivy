'''
Hover Behavior
=====================

The :class:`~kivy.uix.behaviors.hover.HoverBehavior`
`mixin <https://en.wikipedia.org/wiki/Mixin>`_ class provides
hovering behavior. You can combine this
class with other widgets, such as an :class:`~kivy.uix.image.Image`, to provide
hovering callbacks. This class must be used with a widget inherited class. Otherwise
 it will not have the backend for hovering.

For an overview of behaviors, please refer to the :mod:`~kivy.uix.behaviors`
documentation.

Example
-------

The following example adds hover behavior to an image to make an image that changes when you hover over it::

    from kivy.app import App
    from kivy.lang import Builder
    from kivy.uix.image import Image
    from kivy.uix.relativelayout import RelativeLayout
    from kivy.uix.behaviors import HoverBehavior


    class MyHoverImage(HoverBehavior, Image):
        def __init__(self, **kwargs):
            super(MyHoverImage, self).__init__(**kwargs)
            self.source = 'atlas://data/images/defaulttheme/checkbox_off'

        def on_hover_state(self, widget, value):
            if value == 'inside':
                self.source = 'atlas://data/images/defaulttheme/checkbox_on'
            else:
                self.source = 'atlas://data/images/defaulttheme/checkbox_off'


    class SampleApp(App):
        def build(self):
            layout = RelativeLayout()
            Builder.load_string("""
<MyHoverImage>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.size
            pos: self.pos
""")
            layout.add_widget(MyHoverImage(size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5}))
            return layout


    SampleApp().run()
'''

__all__ = ('HoverBehavior', )

from kivy.clock import Clock
from kivy.config import Config
from kivy.properties import OptionProperty, NumericProperty, ReferenceListProperty
from time import time


class HoverBehavior(object):
    '''
        This `mixin <https://en.wikipedia.org/wiki/Mixin>`_ class provides
        :class:`~kivy.uix.button.Button` behavior. Please see the
        :mod:`button behaviors module <kivy.uix.behaviors.button>` documentation
        for more information.

        :Events:
            `on_enter`
                Fired when the widget is first hovered over
            `on_exit`
                Fired when the hover leaves the widgets bounds or the widget gets hidden

        '''

    hover_x = NumericProperty(0)
    hover_y = NumericProperty(0)
    hover_width = NumericProperty(0)
    hover_height = NumericProperty(0)
    hover_rect = ReferenceListProperty(hover_x, hover_y, hover_width, hover_height)

    hover_state = OptionProperty('outside', options=('outside', 'inside'))
    '''The state of the hover, must be one of 'outside' or 'inside'.
        The state is 'inside' only when the widget is being hovered over,
        is not disabled and has a parent otherwise its 'normal'.

        :attr:`state` is an :class:`~kivy.properties.OptionProperty` and defaults
        to 'outside'.
        '''

    last_x = NumericProperty(0)
    last_y = NumericProperty(0)
    last_pos = ReferenceListProperty(last_x, last_y)
    '''The last position that the widget was successfully hovered on.
        '''

    min_state_time = NumericProperty(0)
    '''The minimum period of time which the widget must remain in the
    `'inside'` state.

    .. versionadded:: 1.9.1

    :attr:`min_state_time` is a float and defaults to 0.035. This value is
    taken from :class:`~kivy.config.Config`.
    '''

    layer = NumericProperty(0)

    def __init__(self, **kwargs):
        kwargs['hover'] = True
        self.register_event_type('on_enter')
        self.register_event_type('on_exit')
        if 'min_state_time' not in kwargs:
            self.min_state_time = float(Config.get('graphics', 'min_state_time'))
        super(HoverBehavior, self).__init__(**kwargs)
        self.__state_event = None
        self.__hover_time = None
        self.fbind('state', self.cancel_event)
        self.last_layer = self.layer
        self.hover_subscribe(self, self.layer)

    def on_layer(self, *args):
        self.hover_unsubscribe(self, self.last_layer)
        self.last_layer = self.layer
        self.hover_subscribe(self, self.layer)

    def _do_enter(self):
        self.hover_state = 'inside'

    def _do_exit(self, *args):
        self.hover_state = 'outside'

    def cancel_event(self, *args):
        if self.__state_event:
            self.__state_event.cancel()
            self.__state_event = None

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def collide_point(self, x, y):
        if self.hover_x != 0 or self.hover_y != 0 or self.hover_width != 0 or self.hover_height != 0:
            x, y = self.to_local(x, y)
            # print(f'{self.hover_x} <= {x} <= {self.hover_x + self.hover_width} | {self.hover_y} <= {y} <= {self.hover_y + self.hover_height}')
            return self.hover_x <= x <= self.hover_x + self.hover_width and self.hover_y <= y <= self.hover_y + self.hover_height
        return super().collide_point(x, y)

    def on_move_hover(self, x, y):
        if self.parent is None:
            return
        x, y = self.parent.get_local(x, y)
        # print(f'{self.x} <= {x} <= {self.right} | {self.y} <= {y} <= {self.top}')
        hover = self.collide_point(x, y)
        # hover = super().on_move_hover(x, y)
        if hover:
            self.last_pos = x, y
            if self.hover_state == 'outside':
                self.__hover_time = time()
                self._do_enter()
                self.dispatch('on_enter')
        elif self.hover_state == 'inside':
            self.last_pos = x, y

            hovertime = time() - self.__hover_time
            if hovertime < self.min_state_time:
                self.__state_event = Clock.schedule_once(self._do_exit, self.min_state_time - hovertime)
            else:
                self._do_exit()
            self.dispatch('on_exit')
        return hover

    def trigger_action(self, duration=0.1):
        '''Trigger whatever action(s) have been bound to the button by calling
        both the on_press and on_release callbacks.

        This is similar to a quick button press without using any touch events,
        but note that like most kivy code, this is not guaranteed to be safe to
        call from external threads. If needed use
        :class:`Clock <kivy.clock.Clock>` to safely schedule this function and
        the resulting callbacks to be called from the main thread.

        Duration is the length of the press in seconds. Pass 0 if you want
        the action to happen instantly.

        .. versionadded:: 1.8.0
        '''
        self._do_enter()
        self.dispatch('on_enter')

        def trigger_release(dt):
            self._do_exit()
            self.dispatch('on_exit')
        if not duration:
            trigger_release(0)
        else:
            Clock.schedule_once(trigger_release, duration)

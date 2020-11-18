'''
HoverButton Behavior
=====================

The :class:`~kivy.uix.behaviors.hoverbutton.HoverButtonBehavior`
`mixin <https://en.wikipedia.org/wiki/Mixin>`_ class provides
:class:`~kivy.uix.hoverbutton.HoverButton` behavior. You can combine this
class with other widgets, such as an :class:`~kivy.uix.image.Image`, to provide
alternative hoverbuttons that preserve Kivy hoverbutton behavior.

For an overview of behaviors, please refer to the :mod:`~kivy.uix.behaviors`
documentation.

Example
-------

The following example adds hoverbutton behavior to an image to make a checkbox
that behaves like a hoverbutton::

    from kivy.app import App
    from kivy.uix.image import Image
    from kivy.uix.behaviors import ToggleButtonBehavior


    class MyButton(ToggleButtonBehavior, Image):
        def __init__(self, **kwargs):
            super(MyButton, self).__init__(**kwargs)
            self.source = 'atlas://data/images/defaulttheme/checkbox_off'

        def on_state(self, widget, value):
            if value == 'down':
                self.source = 'atlas://data/images/defaulttheme/checkbox_on'
            else:
                self.source = 'atlas://data/images/defaulttheme/checkbox_off'


    class SampleApp(App):
        def build(self):
            return MyButton()


    SampleApp().run()
'''

__all__ = ('HoverButtonBehavior', )

from kivy.properties import OptionProperty
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.behaviors.hover import HoverBehavior


class HoverButtonBehavior(ButtonBehavior, HoverBehavior):
    state = OptionProperty('normal', options=('normal', 'down', 'hover_normal', 'hover_down'))

    def __init__(self, **kwargs):
        super(HoverButtonBehavior, self).__init__(**kwargs)

    def _do_press(self):
        # You should always be inside the collision to detect this. So always go to hover_down
        self.state = 'hover_down'
        print('hover')

    def _do_enter(self):
        super()._do_enter()
        if self.state.startswith('hover_'):
            return
        self.state = f'hover_{self.state}'

    def _do_release(self, *args):
        # We could be outside the box
        if self.state.startswith('hover_'):
            self.state = 'hover_normal'
        else:
            self.state = 'normal'

    def _do_exit(self, *args):
        super()._do_exit()
        # We might be down or up
        if self.state.startswith('hover_'):
            self.state = self.state[len('hover_'):]
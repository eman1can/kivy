'''
Pixel Perfect Collision Behavior
=====================

The :class:`~kivy.uix.behaviors.pixelperfectcollision.PixelPerfectCollisionBehavior`
`mixin <https://en.wikipedia.org/wiki/Mixin>`_ class provides
pixel perfect collision behavior using a collision mask. You can combine this
class with other widgets, such as an :class:`~kivy.uix.button.Button`, to provide
customized collision.

For an overview of behaviors, please refer to the :mod:`~kivy.uix.behaviors`
documentation.

Example
-------

The following example adds PPC behavior to an button to make an button that changes when you hover over it::

    from kivy.app import App
    from kivy.resources import resource_find, resource_add_path
    from kivy.uix.button import Button
    from kivy.uix.behaviors import PixelPerfectCollisionBehavior


    class PPCButton(PixelPerfectCollisionBehavior, Button):
        def __init__(self, **kwargs):
            super(PPCButton, self).__init__(**kwargs)
            resource_add_path('C:\\users\\ethan\\pycharmprojects\\kivy\\kivy\\data\\images\\')
            self.collision_source = resource_find('core_collision.png')


    class SampleApp(App):
        def build(self):
            return PPCButton()


    SampleApp().run()

'''

__all__ = ('PixelPerfectCollisionBehavior', )

from kivy.core.image import Image as CoreImage
from kivy.properties import ObjectProperty, StringProperty


class PixelPerfectCollisionBehavior(object):
    collision_source = StringProperty(None, allownone=True)
    '''The collision source is the file to load the collision
    mask from. The collision mask should be a png or other image
    file that supports the alpha layer. Any transparent pixels
    will count as no collision. Any opaque pixels will trigger
    a collision. The mask is scaled to fit the widget.
        '''

    __collision_mask = ObjectProperty(None, allownone=True)
    '''The collision mask is used to detect the collision point against.
    If the collision mask is None then no collision will be possible.
        '''
    def __init__(self, **kwargs):
        super(PixelPerfectCollisionBehavior, self).__init__(**kwargs)

    def on_collision_source(self, instance, value):
        if value is None:
            return
        try:
            self.__collision_mask = CoreImage(value, keep_data=True)
        except:
            self.__collision_mask = None

    def collide_point(self, x, y):
        if self.__collision_mask is None:
            # print("No collision mask")
            return False
        if not super().collide_point(x, y):
            # print("Not inside the widget")
            return False
        try:
            # print(x, y)
            # print(self.x, self.y, self.right, self.top)
            wscale = (self.__collision_mask.width / self.width)
            hscale = (self.__collision_mask.height / self.height)
            # print(wscale, hscale)
            # print(x, self.x)
            # print(y, self.y)
            # print((x - self.x) * wscale, (self.height - (y - self.y)) * hscale)
            # print(self.__collision_mask.width, self.__collision_mask.height)
            color = self.__collision_mask.read_pixel((x - self.x) * wscale, (self.height - (y - self.y)) * hscale)
            # print(color)
        except Exception as e:
            color = 0, 0, 0, 0
        if color[-1] > 0:
            print(self.x, self.y, 'collide')
            return True

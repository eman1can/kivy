
__all__ = ('PPCHoverPathButton', 'PPCHoverPathToggleButton', )

from kivy.properties import StringProperty
from kivy.uix.behaviors import PixelPerfectCollisionBehavior
from kivy.uix.hoverbutton import HoverButton
from kivy.uix.hovertogglebutton import HoverToggleButton


class HoverPathButton(HoverButton):
    '''PPCHoverPathButton class, see module documentation for more information.
    '' vsersionadded:: 2.0.0rc3
        Added the hover button class with the path variable to load images
    '''

    path = StringProperty('')
    '''The relative path to search for images
        '''
    def on_path(self, instance, value):
        # TODO Make this change on wether the string is atlassed or not.
        self.background_normal = value + '.normal.png'
        self.background_down = value + '.down.png'
        self.background_hover_normal = value + '.hover.png'
        self.background_hover_down = value + '.hover.down.png'
        self.background_disabled_normal = value + '.disabled.normal.png'
        self.background_disabled_down = value + '.disabled.down.png'


class HoverPathToggleButton(HoverToggleButton):
    '''PPCHoverPathButton class, see module documentation for more information.
    '' vsersionadded:: 2.0.0rc3
        Added the hover button class with the path variable to load images
    '''

    path = StringProperty('')
    '''The relative path to search for images
        '''
    def on_path(self, instance, value):
        # TODO Make this change on wether the string is atlassed or not.
        self.background_normal = value + '.normal.png'
        self.background_down = value + '.down.png'
        self.background_hover_normal = value + '.hover.png'
        self.background_hover_down = value + '.hover.down.png'
        self.background_disabled_normal = value + '.disabled.normal.png'
        self.background_disabled_down = value + '.disabled.down.png'


class PPCHoverPathButton(PixelPerfectCollisionBehavior, HoverPathButton):
    '''PPCHoverPathButton class, see module documentation for more information.
    '' vsersionadded:: 2.0.0rc3
        Added the hover button class with the path variable to load images
    '''
    def on_path(self, instance, value):
        super().on_path(instance, value)
        self.collision_source = value + '.collision.png'


class PPCHoverPathToggleButton(PixelPerfectCollisionBehavior, HoverPathToggleButton):
    '''PPCHoverPathToggleButton class, see module documentation for more information.
        '' vsersionadded:: 2.0.0rc3
            Added the hover button class with the path variable to load images
        '''
    def on_path(self, instance, value):
        super().on_path(instance, value)
        self.collision_source = value + '.collision.png'

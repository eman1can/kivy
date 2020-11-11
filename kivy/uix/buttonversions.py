
__all__ = ('PPCHoverPathButton', 'PPCHoverPathToggleButton', )

from kivy.properties import StringProperty
from kivy.uix.behaviors import PixelPerfectCollisionBehavior
from kivy.uix.hoverbutton import HoverButton
from kivy.uix.hovertogglebutton import HoverToggleButton


class HoverPathButton(PixelPerfectCollisionBehavior, HoverButton):
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


class PPCHoverPathButton(PixelPerfectCollisionBehavior, HoverButton):
    '''PPCHoverPathButton class, see module documentation for more information.
    '' vsersionadded:: 2.0.0rc3
        Added the hover button class with the path variable to load images
    '''

    path = StringProperty('')
    '''The relative path to search for images
        '''
    def on_path(self, instance, value):
        # TODO Make this change on wether the string is atlassed or not.
        self.collision_source = value + '.collision.png'
        self.background_normal = value + '.normal.png'
        self.background_down = value + '.down.png'
        self.background_hover_normal = value + '.hover.png'
        self.background_hover_down = value + '.hover.down.png'
        self.background_disabled_normal = value + '.disabled.normal.png'
        self.background_disabled_down = value + '.disabled.down.png'


class PPCHoverPathToggleButton(PixelPerfectCollisionBehavior, HoverToggleButton):
    '''PPCHoverPathToggleButton class, see module documentation for more information.
        '' vsersionadded:: 2.0.0rc3
            Added the hover button class with the path variable to load images
        '''

    path = StringProperty('')
    '''The relative path to search for images
        '''

    def on_path(self, instance, value):
        # TODO Make this change on wether the string is atlassed or not.
        self.collision_source = value + '.collision.png'
        self.background_normal = value + '.normal.png'
        self.background_down = value + '.down.png'
        self.background_hover_normal = value + '.hover.png'
        self.background_hover_down = value + '.hover.down.png'
        self.background_disabled_normal = value + '.disabled.normal.png'
        self.background_disabled_down = value + '.disabled.down.png'

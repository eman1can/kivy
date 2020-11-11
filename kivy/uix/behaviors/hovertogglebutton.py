'''
HoverToggleButton Behavior
=====================

The :class:`~kivy.uix.behaviors.hovertogglebutton.HoverToggleButton`
`mixin <https://en.wikipedia.org/wiki/Mixin>`_ class provides
:class:`~kivy.uix.togglebutton.ToggleButton` behavior combined with
:class:`~kivy.uix.hover.Hover` behavior. You can combine this
class with other widgets, such as an :class:`~kivy.uix.image.Image`, to provide
alternative togglebuttons that preserve Kivy togglebutton behavior.

For an overview of behaviors, please refer to the :mod:`~kivy.uix.behaviors`
documentation.
'''

__all__ = ('HoverToggleButtonBehavior', )

from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.behaviors import HoverButtonBehavior
from kivy.uix.behaviors.button import ButtonBehavior
from weakref import ref


class HoverToggleButtonBehavior(HoverButtonBehavior):
    '''This `mixin <https://en.wikipedia.org/wiki/Mixin>`_ class provides
    :mod:`~kivy.uix.togglebutton` behavior. Please see the
    :mod:`togglebutton behaviors module <kivy.uix.behaviors.togglebutton>`
    documentation for more information.

    .. versionadded:: 1.8.0
    '''

    __groups = {}

    group = ObjectProperty(None, allownone=True)
    '''Group of the button. If `None`, no group will be used (the button will be
    independent). If specified, :attr:`group` must be a hashable object, like
    a string. Only one button in a group can be in a 'down' state.

    :attr:`group` is a :class:`~kivy.properties.ObjectProperty` and defaults to
    `None`.
    '''

    allow_no_selection = BooleanProperty(True)
    '''This specifies whether the widgets in a group allow no selection i.e.
    everything to be deselected.

    .. versionadded:: 1.9.0

    :attr:`allow_no_selection` is a :class:`BooleanProperty` and defaults to
    `True`
    '''

    def __init__(self, **kwargs):
        self._previous_group = None
        super(HoverToggleButtonBehavior, self).__init__(**kwargs)

    def on_group(self, *largs):
        groups = HoverToggleButtonBehavior.__groups
        if self._previous_group:
            group = groups[self._previous_group]
            for item in group[:]:
                if item() is self:
                    group.remove(item)
                    break
        group = self._previous_group = self.group
        if group not in groups:
            groups[group] = []
        r = ref(self, HoverToggleButtonBehavior._clear_groups)
        groups[group].append(r)

    def _release_group(self, current):
        if self.group is None:
            return
        group = self.__groups[self.group]
        for item in group[:]:
            widget = item()
            if widget is None:
                group.remove(item)
            if widget is current:
                continue
            if widget.state.startswith('hover_'):
                widget.state = 'hover_normal'
            else:
                widget.state = 'normal'

    def _do_press(self):
        if not self.allow_no_selection and self.group and self.state.endswith('down'):
            return

        self._release_group(self)
        if self.state.startswith('hover_'):
            self.state = 'hover_normal' if self.state == 'hover_down' else 'hover_down'
        else:
            self.state = 'normal' if self.state == 'down' else 'down'

    def _do_release(self, *args):
        pass


    @staticmethod
    def _clear_groups(wk):
        # auto flush the element when the weak reference have been deleted
        groups = HoverToggleButtonBehavior.__groups
        for group in list(groups.values()):
            if wk in group:
                group.remove(wk)
                break

    @staticmethod
    def get_widgets(groupname):
        '''Return a list of the widgets contained in a specific group. If the
        group doesn't exist, an empty list will be returned.

        .. note::

            Always release the result of this method! Holding a reference to
            any of these widgets can prevent them from being garbage collected.
            If in doubt, do::

                l = ToggleButtonBehavior.get_widgets('mygroup')
                # do your job
                del l

        .. warning::

            It's possible that some widgets that you have previously
            deleted are still in the list. The garbage collector might need
            to release other objects before flushing them.
        '''
        groups = HoverToggleButtonBehavior.__groups
        if groupname not in groups:
            return []
        return [x() for x in groups[groupname] if x()][:]

'''
HoverToggle button
=============

.. image:: images/togglebutton.jpg
    :align: right

The :class:`HoverToggle` widget acts like a checkbox. When you touch or click
it, the state toggles between 'normal' and 'down' (as opposed to a
:class:`Button` that is only 'down' as long as it is pressed).

Toggle buttons can also be grouped to make radio buttons - only one button in
a group can be in a 'down' state. The group name can be a string or any other
hashable Python object::

    btn1 = HoverToggleButton(text='Male', group='sex',)
    btn2 = HoverToggleButton(text='Female', group='sex', state='down')
    btn3 = HoverToggleButton(text='Mixed', group='sex')

Only one of the buttons can be 'down'/checked at the same time.

To configure the HoverToggleButton, you can use the same properties that you can use
for a :class:`~kivy.uix.button.Button` class.

'''

__all__ = ('HoverToggleButton', )

from kivy.uix.hoverbutton import HoverButton
from kivy.uix.behaviors import HoverToggleButtonBehavior


class HoverToggleButton(HoverToggleButtonBehavior, HoverButton):
    '''Toggle button class, see module documentation for more information.
    '''

    pass

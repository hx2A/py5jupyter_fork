# *****************************************************************************
#
#   Part of the py5jupyter (& py5) library
#   Copyright (C) 2022 Jim Schmitz
#
#   This library is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published by
#   the Free Sotware Foundation, either version 2.1 of the License, or (at
#   your option) any later version.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
#   General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this library. If not, see <https://www.gnu.org/licenses/>.
#
# *****************************************************************************
from ipywidgets import DOMWidget
from traitlets import Unicode, CUnicode, Bytes
from ._frontend import module_name, module_version


class Py5SketchPortal(DOMWidget):
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('Py5SketchPortalView').tag(sync=True)
    _model_name = Unicode('Py5SketchPortalModel').tag(sync=True)

    # Define the custom state properties to sync with the front-end
    value = Bytes(help="The frame image as bytes.").tag(sync=True)
    format = Unicode('jpeg', help="The format of the image.").tag(sync=True)
    width = CUnicode(help="Width of the image in pixels. Use layout.width "
                          "for styling the widget.").tag(sync=True)
    height = CUnicode(help="Height of the image in pixels. Use layout.height "
                           "for styling the widget.").tag(sync=True)

    def __init__(self, sketch, *args, **kwargs):
        super(Py5SketchPortal, self).__init__(*args, **kwargs)
        self.sketch = sketch
        self._last_event_button = 0
        self.on_msg(self._handle_frontend_event)

    # # Events
    def _handle_frontend_event(self, _, content, buffers):
        import py5
        from py5 import Py5MouseEvent, Py5KeyEvent

        event_type = content.get("event", "")
        event_x = int(content.get("x", 0))
        event_y = int(content.get("y", 0))
        event_mod = content.get("mod", 0)

        if event_type.startswith('mouse'):
            event_button = bool((b := content.get("buttons", 0)) & 1) * py5.LEFT or bool(b & 4) * py5.CENTER or bool(b & 2) * py5.RIGHT

            if event_type == "mouse_enter":
                self.sketch._instance.fakeMouseEvent(Py5MouseEvent.ENTER, event_mod, event_x, event_y, event_button, 0)
            elif event_type == "mouse_down":
                self.sketch._instance.fakeMouseEvent(Py5MouseEvent.PRESS, event_mod, event_x, event_y, event_button, 1)
            elif event_type == "mouse_move":
                self.sketch._instance.fakeMouseEvent(Py5MouseEvent.MOVE, event_mod, event_x, event_y, event_button, 0)
            elif event_type == "mouse_up":
                self.sketch._instance.fakeMouseEvent(Py5MouseEvent.RELEASE, event_mod, event_x, event_y, self._last_event_button, 1)
            elif event_type == "mouse_leave":
                self.sketch._instance.fakeMouseEvent(Py5MouseEvent.EXIT, event_mod, event_x, event_y, event_button, 0)

        elif event_type.startswith("key"):
            event_key = content.get("key", "")
            event_repeat = content.get("repeat", False)

            if event_type == "key_down":
                self.sketch._instance.fakeKeyEvent(Py5KeyEvent.PRESS, event_mod, event_key, event_repeat)
            elif event_type == "key_press":
                self.sketch._instance.fakeKeyEvent(Py5KeyEvent.TYPE, event_mod, event_key, event_repeat)
            elif event_type == "key_up":
                self.sketch._instance.fakeKeyEvent(Py5KeyEvent.RELEASE, event_mod, event_key, event_repeat)

        self._last_event_button = event_button

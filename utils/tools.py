from Xlib import X
from Xlib.display import Display

def get_active_window_title():
    display = Display()
    root = display.screen().root
    active_window_id = root.get_full_property(
        display.intern_atom('_NET_ACTIVE_WINDOW'), X.AnyPropertyType
    ).value[0]
    
    active_window = display.create_resource_object('window', active_window_id)
    window_name = active_window.get_full_property(
        display.intern_atom('_NET_WM_NAME'), X.AnyPropertyType
    )
    
    if window_name:
        return window_name.value
    return None


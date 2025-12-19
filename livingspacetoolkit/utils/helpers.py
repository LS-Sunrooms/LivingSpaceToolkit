from functools import wraps

from PySide6.QtWidgets import QWidget

def temporary_change(
    object_attr: str,
    method_name: str,
    before_value: bool,
    after_value: bool,
):
    """
    Decorator for instance methods.

    Calls:
        getattr(self.<object_attr>, method_name)(before_value)
    before the method, and
        getattr(self.<object_attr>, method_name)(after_value)
    after the method.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            obj = getattr(self, object_attr)
            method = getattr(obj, method_name)

            method(before_value)
            try:
                return func(self, *args, **kwargs)
            finally:
                method(after_value)

        return wrapper
    return decorator


def set_strikethrough(widget: QWidget, enabled: bool):
    font = widget.font()
    font.setStrikeOut(enabled)
    widget.setFont(font)

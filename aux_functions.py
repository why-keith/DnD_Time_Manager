def window_centre(position: tuple[float, float], size: tuple[float, float]) -> tuple[float, float]:
    """Calculates the centre point of a window from its position and size.

    Args:
        position: Top-left corner of the window as (x, y) in pixels.
        size: Width and height of the window as (w, h) in pixels.

    Returns:
        The (x, y) coordinates of the window's centre.
    """
    centre=[s/2+p for p,s in zip(position,size)]
    return tuple(centre)

def TL_from_centre(parent_centre: tuple[float, float], child_size: tuple[float, float]) -> tuple[float, float]:
    """Calculates the top-left position needed to centre a child window over a parent.

    Args:
        parent_centre: Centre coordinates of the parent window as (x, y).
        child_size: Width and height of the child window as (w, h).

    Returns:
        The (x, y) top-left coordinates for the child window.
    """
    position=[c-s/2 for c,s in zip(parent_centre,child_size)]
    return tuple(position)

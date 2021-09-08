def window_centre(position,size):
    """
    Calculates a window's centre from it's position and size

    Parameters
    ----------
    position : tuple(x,y)
        position of the window in pixels.
    size : TYPE
        size of the window in pixels.

    Returns
    -------
    centre : tuple(x,y)
        the coordinates of the window's centre.

    """
    centre=[s/2+p for p,s in zip(position,size)]
    return tuple(centre)

def TL_from_centre(parent_centre, child_size):
    """
    Calculates the requires location of a windows top-left corner, so that its
    centre and that of the parent window are aligned

    Parameters
    ----------
    parent_centre : tuple(x,y)
        coordinates of the parent window's centre.
    child_size : tuple(x,y)
        dimensions of the child window.

    Returns
    -------
    position : tuple(x,y)
        coordinates of the child window's top-left corner.

    """
    position=[c-s/2 for c,s in zip(parent_centre,child_size)]
    return tuple(position)
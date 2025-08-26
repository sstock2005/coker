import modules.constants

def get_middle_h(width: int) -> int:
    """Window helper function to calculate the horizontal center position of coker's window relative to the given image width.

    Args:
        width (int): Should usually be `pygame.rect.width`.

    Returns:
        int: Horizontally center position of coker's window relative to the given image width.
    """
    
    return (modules.constants.WINDOW_WIDTH // 2) - (width // 2)

def get_middle_v(height: int) -> int:
    """Window helper function to calculate the vertical center position of coker's window relative to the given image height.

    Args:
        height (int): Should usually be `pygame.rect.height`.

    Returns:
        int: Horizontally center position of coker's window relative to the given image height.
    """
    
    return (modules.constants.WINDOW_HEIGHT // 2) - (height // 2)
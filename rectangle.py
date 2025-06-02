# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

# Rectangle C typedef:
# double x;
# double y;
# double width;
# double height;
# const char* mode; // NULL for left, "centered" for centered

def get_rectangle(input_rectangle: tuple[float, float, float, float, str | None]) -> tuple[float, float, float, float]:
    """Turns a rectangle "struct" into a rectangle tuple formatted (x, y, width, height)
    
    Args:
        input_rectangle (tuple[float, float, float, float, str | None]): The rectangle "struct"
    
    Returns:
        tuple[float, float, float, float]: A rectangle tuple formatted (x, y, width, height)
    """
    if len(input_rectangle) == 4:
        return input_rectangle
    
    # Unpack the tuple and process it
    x, y, width, height, mode = input_rectangle
    if mode is None:
        return (x, y, width, height)
    match mode:
        case "centered":
            x -= width // 2
        case _:
            raise ValueError(f"Unknown rectangle mode: {mode}")
    
    return (x, y, width, height)

def point_in_rectange(point: tuple[int, int], input_rectangle: tuple[float, float, float, float, str | None]) -> bool:
    """Checks if the given point is inside the specified rectangle
    
    Args:
        point (tuple[int, int]): The point as x, y
        input_rectangle (tuple[float, float, float, float, str | None]): The rectangle
    
    Returns:
        bool: True if the point is in the input_rectangle, False if not
    """
    true_rectangle = get_rectangle(input_rectangle)

    return (true_rectangle[0] <= point[0] <= true_rectangle[0] + true_rectangle[2] and \
            true_rectangle[1] <= point[1] <= true_rectangle[1] + true_rectangle[3])
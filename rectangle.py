# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

# Rectangle C typedef:
# double x;
# double y;
# double width;
# double height;
# const char* mode; // NULL for left, "centered" for centered

def get_rectangle(button_rectangle: tuple[float, float, float, float, str | None]) -> tuple[float, float, float, float]:
    """Turns a rectangle "struct" into a rectangle tuple formatted (x, y, width, height)
    
    Args:
        button_rectangle (tuple[float, float, float, float, str | None]): The rectangle "struct"
    
    Returns:
        tuple[float, float, float, float]: A rectangle tuple formatted (x, y, width, height)
    """
    if len(button_rectangle) == 4:
        return button_rectangle
    
    # Unpack the tuple and process it
    x, y, width, height, mode = button_rectangle
    if mode is None:
        return (x, y, width, height)
    match mode:
        case "centered":
            x -= width // 2
        case _:
            raise ValueError(f"Unknown rectangle mode: {mode}")
    
    return (x, y, width, height)
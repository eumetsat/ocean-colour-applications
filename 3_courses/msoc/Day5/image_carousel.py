import ipywidgets as widgets
from PIL import Image
import io

def create_image_carousel(image_paths, width=800, height=600):
    """
    Create a fixed-size image carousel using ipywidgets.

    Parameters
    ----------
    image_paths : list of str
        List of paths to images on disk.
    width : int
        Width of display area in pixels.
    height : int
        Height of display area in pixels.

    Returns
    -------
    widget.VBox
        The carousel widget.
    """

    def load_and_resize(path):
        img = Image.open(path)

        # Convert transparent images to RGB (JPEG cannot store alpha)
        if img.mode == "RGBA":
            img = img.convert("RGB")

        # Resize while keeping aspect ratio
        img.thumbnail((width, height))

        # Convert to JPEG bytes for ipywidgets.Image
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        return buffer.getvalue()

    # --- INITIAL STATE ---
    index = 0
    img_widget = widgets.Image(
        value=load_and_resize(image_paths[index]),
        format="jpg",
        layout=widgets.Layout(width=f"{width}px", height=f"{height}px")
    )

    prev_button = widgets.Button(description="⟵ Previous")
    next_button = widgets.Button(description="Next ⟶")

    # --- BUTTON ACTIONS ---
    def on_prev(b):
        nonlocal index
        index = (index - 1) % len(image_paths)
        img_widget.value = load_and_resize(image_paths[index])

    def on_next(b):
        nonlocal index
        index = (index + 1) % len(image_paths)
        img_widget.value = load_and_resize(image_paths[index])

    prev_button.on_click(on_prev)
    next_button.on_click(on_next)

    # Layout
    return widgets.VBox([img_widget, widgets.HBox([prev_button, next_button])])

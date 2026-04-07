import ternary
import matplotlib.pyplot as plt
import numpy as np

def plot_ternary(component_a, component_b, component_c, 
                 labels=('Component A', 'Component B', 'Component C'),
                 title='Ternary Diagram',
                 scale=100,
                 marker='o',
                 color='blue',
                 size=50,
                 alpha=0.6,
                 figsize=(10, 8),
                 axes_colors=('black', 'black', 'black'),
                 colorby=None,
                 cmap='viridis',
                 colorbar_label=None,
                 fontsize=15,
                 ax=None,
                 clabel=None):
    """
    Plot a ternary diagram with three components.
    
    Parameters:
    -----------
    component_a : array-like
        Values for component A
    component_b : array-like
        Values for component B
    component_c : array-like
        Values for component C
    labels : tuple of str, optional
        Labels for (A, B, C) axes
    title : str, optional
        Plot title
    scale : int, optional
        Scale for ternary coordinates (default: 100)
    marker : str, optional
        Matplotlib marker style
    color : str or array-like, optional
        Point color(s)
    size : float or array-like, optional
        Point size(s)
    alpha : float, optional
        Point transparency
    figsize : tuple, optional
        Figure size
    axes_colors : tuple of str, optional
        Colors for (A, B, C) axis labels (default: ('black', 'black', 'black'))
    colorby : array-like, optional
        Values to use for coloring points (if None, uses 'color' parameter)
    cmap : str, optional
        Colormap name for colorby values (default: 'viridis')
    colorbar_label : str, optional
        Label for the colorbar (if colorby is provided)
    
    Returns:
    --------
    fig, tax : matplotlib figure and ternary axes objects
    """
    # Convert to numpy arrays
    a = np.array(component_a)
    b = np.array(component_b)
    c = np.array(component_c)
    
    # Normalize to sum to scale
    total = a + b + c
    a_norm = (a / total) * scale
    b_norm = (b / total) * scale
    c_norm = (c / total) * scale
    
    # Create points list
    points = list(zip(a_norm, b_norm, c_norm))
    
    # Create figure and ternary axes
    if ax:
        fig, tax = ternary.figure(ax=ax, scale=100)
    else:
        fig, tax = ternary.figure(scale=scale)
        fig.set_size_inches(figsize)
    
    # Get the matplotlib axes to turn off frame
    ax = tax.get_axes()
    ax.axis('off')
    
    # Set up the diagram
    tax.boundary(linewidth=2.0)
    tax.gridlines(multiple=scale/10, color="gray", linewidth=0.5)
    
    # Left axis (Component C)
    tax.left_axis_label(f"{labels[2]} (%)", offset=0.16, color=axes_colors[2], fontsize=fontsize)
    # Right axis (Component B)
    tax.right_axis_label(f"{labels[1]} (%)", offset=0.16, color=axes_colors[1], fontsize=fontsize)
    # Bottom axis (Component A)
    tax.bottom_axis_label(f"{labels[0]} (%)", offset=0.02, color=axes_colors[0], fontsize=fontsize)
    
    # Add tick labels in black
    tax.ticks(axis='lbr', linewidth=1, multiple=scale/10, offset=0.025, 
              tick_formats="%.0f", fontsize=fontsize)
    
    # Plot scatter points
    if colorby is not None:
        # Convert colorby values to RGBA colors
        colorby_array = np.array(colorby)
        norm = plt.Normalize(vmin=colorby_array.min(), vmax=colorby_array.max())
        cmap_obj = plt.get_cmap(cmap)
        rgba_colors = cmap_obj(norm(colorby_array))
        
        scatter = tax.scatter(points, marker=marker, color=rgba_colors,
                              s=size, alpha=alpha)
        
        # Add colorbar using ScalarMappable
        sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap_obj)
        sm.set_array([])   # required for colorbar
        cbar = plt.colorbar(sm, ax=tax.get_axes(), pad=0.1, label=clabel)
        if colorbar_label:
            cbar.set_label(colorbar_label, rotation=270, labelpad=20)
    else:
        # Use single color
        tax.scatter(points, marker=marker, color=color, s=size, alpha=alpha)
    
    # Add title
    tax.set_title(title, fontsize=16, pad=20)
    
    # Clear default matplotlib ticks
    tax.clear_matplotlib_ticks()
    
    plt.tight_layout()
    
    return fig, tax

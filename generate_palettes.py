import json
import os
import matplotlib.pyplot as plt

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4))

def draw_palette_on_ax(ax, name, colors):
    """Draw color palette directly on provided axis (used in grid)"""
    num_colors = len(colors)
    for i, (label, hex_color) in enumerate(colors.items()):
        rgb = hex_to_rgb(hex_color)
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=rgb))
        ax.text(i + 0.5, -0.15, label, ha='center', va='top', fontsize=9, color='white', rotation=30)
    ax.set_xlim(0, num_colors)
    ax.set_ylim(-0.3, 1)
    ax.set_title(name, fontsize=12, color='white')
    ax.axis('off')
    ax.set_facecolor('#111')

def plot_theme_palette(name, colors):
    """Creates a standalone fig with theme palette"""
    num_colors = len(colors)
    fig, ax = plt.subplots(figsize=(num_colors * 1.5, 2))
    draw_palette_on_ax(ax, name, colors)
    plt.tight_layout()
    return fig

def plot_theme_palette(name, colors):
    """Draw a color palette row for a theme"""
    num_colors = len(colors)
    fig, ax = plt.subplots(figsize=(num_colors * 1.5, 2))
    for i, (label, hex_color) in enumerate(colors.items()):
        rgb = hex_to_rgb(hex_color)
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=rgb))
        ax.text(i + 0.5, -0.1, label, ha='center', va='top', fontsize=9, color='white')
    ax.set_xlim(0, num_colors)
    ax.set_ylim(-0.2, 1)
    ax.axis('off')
    plt.title(name, fontsize=14, color='white')
    fig.patch.set_facecolor('#111')
    plt.tight_layout()
    return fig

def generate_all_palettes(theme_file, output_dir='palettes'):
    with open(theme_file, 'r') as f:
        themes = json.load(f)

    os.makedirs(output_dir, exist_ok=True)

    for theme_name, theme_data in themes.items():
        colors = theme_data.get("colors", {})
        fig = plot_theme_palette(theme_name, colors)
        output_path = os.path.join(output_dir, f"{theme_name}.png")
        plt.savefig(output_path, dpi=200)
        plt.close()
        print(f"Saved palette: {output_path}")

def generate_all_palettes_grid(theme_file, output_dir='palettes'):
    with open(theme_file, 'r') as f:
        themes = json.load(f)

    os.makedirs(output_dir, exist_ok=True)
    all_figures = []

    for theme_name, theme_data in themes.items():
        colors = theme_data.get("colors", {})
        
        # Save individual image
        fig, ax = plt.subplots(figsize=(len(colors) * 1.5, 2))
        draw_palette_on_ax(ax, theme_name, colors)
        output_path = os.path.join(output_dir, f"{theme_name}.png")
        fig.savefig(output_path, dpi=200)
        plt.close(fig)
        print(f"Saved: {output_path}")
        
        all_figures.append((theme_name, colors))

    # Generate combined grid
    combined_rows = len(all_figures)
    max_colors = max(len(c) for _, c in all_figures)
    fig_height = 2.5 * combined_rows
    fig_width = max_colors * 1.6

    fig, axs = plt.subplots(nrows=combined_rows, ncols=1, figsize=(fig_width, fig_height))

    if combined_rows == 1:
        axs = [axs]  # handle single row case

    for ax, (theme_name, colors) in zip(axs, all_figures):
        draw_palette_on_ax(ax, theme_name, colors)

    fig.patch.set_facecolor('#111')
    plt.tight_layout()
    grid_path = os.path.join(output_dir, "all_palettes.png")
    fig.savefig(grid_path, dpi=200)
    plt.close(fig)
    print(f"Saved combined palette grid: {grid_path}")


# Run this if the script is executed directly
if __name__ == "__main__":
    generate_all_palettes_grid("themes.json")
    generate_all_palettes("themes.json")

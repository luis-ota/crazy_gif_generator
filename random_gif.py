#!/usr/bin/env python3
# /// script
# dependencies = [
#     "numpy",
#     "pillow",
#     "chafa.py",
#     "wand"
# ]
# ///

import numpy as np
from PIL import Image, ImageDraw
from chafa import Canvas, CanvasConfig, PixelType, PixelMode  # Added PixelMode
import time
import io
from chafa.loader import Loader
import os
import tempfile
import sys
import argparse

class CustomLoader(Loader):
    def __init__(self, source):
        if isinstance(source, Image.Image):  # Check if it's a Pillow image instance.
            with tempfile.NamedTemporaryFile(suffix=f".{source.format or 'png'}", delete=False) as tmp_file:
                temp_path = tmp_file.name
                source.save(temp_path)
                super().__init__(temp_path)
                os.remove(temp_path)
                return
        elif isinstance(source, str):  # Assume it's a file path.
            super().__init__(source)
        else:
            raise ValueError("Unsupported source type. Provide a file path or a Pillow image instance.")
            
class Display:
    def __init__(self, file, size):
        self.file = file
        self.config = CanvasConfig()

        self.config.height = size
        self.config.width = size

        image = CustomLoader(self.file)

        self.config.calc_canvas_geometry(
            image.width,
            image.height,
            11 / 24
        )

        # Create canvas
        canvas = Canvas(self.config)

        # Load the image

        # Draw to the canvas
        canvas.draw_all_pixels(
            image.pixel_type,
            image.get_pixels(),
            image.width, image.height,
            image.rowstride
    )

        
        self.output = canvas.print().decode()
        print(f"\033[2J\033[H{self.output}", end="", flush=True)
        


def rotate_3d(points, angle_x=0, angle_y=0, angle_z=0):
    """Rotate points in 3D space."""
    rot_x = np.array([
        [1, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x)],
        [0, np.sin(angle_x), np.cos(angle_x)]
    ])
    rot_y = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)]
    ])
    rot_z = np.array([
        [np.cos(angle_z), -np.sin(angle_z), 0],
        [np.sin(angle_z), np.cos(angle_z), 0],
        [0, 0, 1]
    ])
    rotation_matrix = rot_z @ rot_y @ rot_x
    rotated = [np.dot(rotation_matrix, point) for point in points]
    return rotated

def project_3d_to_2d(points, width, height, scale=50):
    """Project 3D points onto a 2D canvas."""
    projected = []
    for x, y, z in points:
        factor = scale / (z + scale + 1)  # Perspective projection
        px = int(width / 2 + x * factor)
        py = int(height / 2 - y * factor)
        projected.append((px, py))
    return projected

def draw_random_cube(draw, width, height):
    """Draw a random 3D cube."""
    size = np.random.randint(10, min(width, height) // 4)
    center_x, center_y = np.random.randint(size, width - size), np.random.randint(size, height - size)
    vertices = [
        [-size, -size, -size], [size, -size, -size], [size, size, -size], [-size, size, -size],
        [-size, -size, size], [size, -size, size], [size, size, size], [-size, size, size]
    ]
    angle_x, angle_y, angle_z = np.random.uniform(0, np.pi), np.random.uniform(0, np.pi), np.random.uniform(0, np.pi)
    rotated = rotate_3d(vertices, angle_x, angle_y, angle_z)
    translated = [(x + center_x - width / 2, y + center_y - height / 2, z) for x, y, z in rotated]
    projected = project_3d_to_2d(translated, width, height)
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Back face
        (4, 5), (5, 6), (6, 7), (7, 4),  # Front face
        (0, 4), (1, 5), (2, 6), (3, 7)  # Connecting edges
    ]
    for start, end in edges:
        draw.line([projected[start], projected[end]], fill=(255, 255, 255), width=1)

def draw_random_tesseract(draw, width, height):
    """Draw a random 2D projection of a tesseract."""
    size = np.random.randint(10, min(width, height) // 4)
    center_x, center_y = np.random.randint(size, width - size), np.random.randint(size, height - size)
    vertices_4d = [((i & 1) * 2 - 1, ((i >> 1) & 1) * 2 - 1, ((i >> 2) & 1) * 2 - 1, ((i >> 3) & 1) * 2 - 1) for i in range(16)]
    vertices_3d = [(x * size, y * size, z * size) for x, y, z, w in vertices_4d]
    angle_x, angle_y, angle_z = np.random.uniform(0, np.pi), np.random.uniform(0, np.pi), np.random.uniform(0, np.pi)
    rotated = rotate_3d(vertices_3d, angle_x, angle_y, angle_z)
    translated = [(x + center_x - width / 2, y + center_y - height / 2, z) for x, y, z in rotated]
    projected = project_3d_to_2d(translated, width, height)
    edges = [(i, j) for i in range(16) for j in range(i + 1, 16) if bin(i ^ j).count('1') == 1]
    for start, end in edges:
        draw.line([projected[start], projected[end]], fill=(0, 255, 0), width=1)



def generate_random_shape_frame(width=400, height=400):
    """Generate a frame with random shapes, cubes, and tesseracts."""
    img = Image.new("RGB", (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    for _ in range(np.random.randint(3, 6)):
        color = tuple(np.random.randint(0, 256, 3))
        shape_type = np.random.choice(['rect', 'ellipse', 'polygon', 'cube', 'tesseract'])
        
        if shape_type == 'rect':
            x1, y1 = np.random.randint(0, width), np.random.randint(0, height)
            x2, y2 = np.random.randint(x1, width), np.random.randint(y1, height)
            draw.rectangle([x1, y1, x2, y2], fill=color)
        elif shape_type == 'ellipse':
            x1, y1 = np.random.randint(0, width), np.random.randint(0, height)
            x2, y2 = np.random.randint(x1, width), np.random.randint(y1, height)
            draw.ellipse([x1, y1, x2, y2], fill=color)
        elif shape_type == 'polygon':
            num_points = np.random.randint(3, 10)
            points = [(np.random.randint(0, width), np.random.randint(0, height)) for _ in range(num_points)]
            points.append(points[0])  # Close the polygon
            draw.polygon(points, fill=color)
        elif shape_type == 'cube':
            draw_random_cube(draw, width, height)
        elif shape_type == 'tesseract':
            draw_random_tesseract(draw, width, height)
    
    return img
    

    

    

def display_animated_shapes(num_frames=20, fps=5, size=50):
    """Display animation using chafa.py"""
    config = CanvasConfig()
    config.width = 60
    config.height = 30
    
    canvas = Canvas(config)
    
    try:
        while True:
            for _ in range(num_frames):
                frame = generate_random_shape_frame(size*2, size)
                Display(frame, size)
                time.sleep(1/fps)
                
    except KeyboardInterrupt:
        print("\033[2J\033[HAnimation stopped.")

def create_gif(output_path="random_shapes.gif", size=50, frame_count=20, duration=100):
    """Generate multiple frames and save them as a GIF."""
    frames = []
    for _ in range(frame_count):
        frame = generate_random_shape_frame(size*2, size)
        Display(frame, size)
        frames.append(frame)
    
    # Save frames as a GIF
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,  # Duration of each frame in milliseconds
        loop=0  # Loop forever
    )
    print(f"GIF saved to {output_path}")

if __name__ == "__main__":
   # Create argument parser
    parser = argparse.ArgumentParser(description="Generate a random shape GIF.")
    
    # Add arguments
    parser.add_argument('-o', '--output', type=str, required=False, help="Output filename (e.g., 'output.gif')")
    parser.add_argument('-S', '--size', type=int, required=False, default=50, help="Size of the image >= 50")
    parser.add_argument('-f', '--frames', type=int, default=5, help="Number of frames in the GIF")
    parser.add_argument('-d', '--duration', type=int, default=100, help="Duration of each frame in milliseconds")
    parser.add_argument('-s', '--speed', type=float, default=1.0, help="Speed factor for adjusting frame duration (1.0 = normal speed, >1 = faster, <1 = slower)")
    
    # Parse arguments
    args = parser.parse_args()

    if args.size < 50:
        print("Size must be >= 50")
        sys.exit(1)
    
    # Default FPS is 10
    target_fps = 10
    
    # Calculate the duration per frame to achieve the target FPS
    duration_per_frame = round(1000 / target_fps)
    
    # Apply speed factor (if speed > 1, frames will appear faster, < 1 slower)
    adjusted_duration = round(duration_per_frame / args.speed)
    
    if args.output:
        create_gif(args.output, args.size, args.frames, adjusted_duration)
        sys.exit(0)
        
    display_animated_shapes(num_frames=args.frames, fps=target_fps, size=args.size)
    

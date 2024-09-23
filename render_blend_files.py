import bpy
import os
import sys

def render_blend_file(blend_file_path, output_file_path):
    # Open the blend file
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)
    
    # Set the render output settings
    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.filepath = output_file_path

    # Render the animation
    bpy.ops.render.render(animation=True)

def main():
    # Directories
    input_dir = "./blender_source"
    output_dir = "./blender_mp4"

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Absolute paths
    input_dir = os.path.abspath(input_dir)
    output_dir = os.path.abspath(output_dir)

    # Iterate over all .blend files in input_dir
    for filename in os.listdir(input_dir):
        if filename.endswith('.blend'):
            blend_file = os.path.join(input_dir, filename)
            base_name = os.path.splitext(filename)[0]
            output_file = os.path.join(output_dir, base_name + ".mp4")
            print(f"Rendering {blend_file} to {output_file}")
            render_blend_file(blend_file, output_file)

if __name__ == "__main__":
    main()

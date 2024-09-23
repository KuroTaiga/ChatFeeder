import bpy
import os
import sys

def batch_render_blend_files(source_folder, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get all .blend files in the source folder
    blend_files = [f for f in os.listdir(source_folder) if f.endswith('.blend')]

    for file_name in blend_files:
        blend_file_path = os.path.join(source_folder, file_name)
        output_file_name = os.path.splitext(file_name)[0] + ".mp4"
        output_file_path = os.path.join(output_folder, output_file_name)

        # Open the Blender file
        bpy.ops.wm.open_mainfile(filepath=blend_file_path)

        # Set render settings
        scene = bpy.context.scene
        scene.render.engine = 'BLENDER_EEVEE'  # Change to 'CYCLES' if needed

        # Set the output format to MP4
        scene.render.image_settings.file_format = 'FFMPEG'
        scene.render.ffmpeg.format = 'MPEG4'
        scene.render.ffmpeg.codec = 'H264'
        scene.render.ffmpeg.constant_rate_factor = 'HIGH'
        scene.render.ffmpeg.ffmpeg_preset = 'GOOD'

        # Set resolution and frame rate if needed
        scene.render.resolution_x = 1920
        scene.render.resolution_y = 1080
        scene.render.fps = 30

        # Set the output file path
        scene.render.filepath = output_file_path

        # Render the animation
        bpy.ops.render.render(animation=True)

        print(f"Rendered and saved {output_file_name}")

if __name__ == "__main__":
    # Parse command line arguments
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # Get all args after "--"

    if len(argv) < 2:
        print("Usage: blender -b -P batch_blend_to_mp4.py -- <source_folder> <output_folder>")
        sys.exit(1)

    source_folder = argv[0]
    output_folder = argv[1]

    batch_render_blend_files(source_folder, output_folder)

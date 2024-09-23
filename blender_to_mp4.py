import bpy
import os

# Source folder with Blender files
source_folder = "./blender_source"
# Destination folder for the MP4 files
output_folder = "./blender_mp4"

# Make sure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate through all files in the source folder
for file_name in os.listdir(source_folder):
    if file_name.endswith(".blend"):
        # Full path to the Blender file
        blend_file_path = os.path.join(source_folder, file_name)
        
        # Create the output file path (same name as the .blend but with .mp4)
        output_file_name = os.path.splitext(file_name)[0] + ".mp4"
        output_file_path = os.path.join(output_folder, output_file_name)
        
        # Open the Blender file
        bpy.ops.wm.open_mainfile(filepath=blend_file_path)
        
        # Set the rendering engine (optional)
        bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'  # Use 'CYCLES' if using Cycles

        
        # Set the output file format to MP4
        bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
        bpy.context.scene.render.ffmpeg.format = 'MPEG4'
        bpy.context.scene.render.ffmpeg.codec = 'H264'
        bpy.context.scene.render.ffmpeg.constant_rate_factor = 'HIGH'
        
        # Set the resolution, frame rate, and output path
        bpy.context.scene.render.resolution_x = 1920  # Set resolution width
        bpy.context.scene.render.resolution_y = 1080  # Set resolution height
        bpy.context.scene.render.fps = 30  # Set frame rate
        bpy.context.scene.render.filepath = output_file_path
        
        # Render the animation
        bpy.ops.render.render(animation=True,write_still = True)
        
        print(f"Rendered {file_name} to {output_file_name}")

# Optional: Save the final state (if you need to save the project files)
# bpy.ops.wm.save_as_mainfile(filepath=os.path.join(source_folder, "final_output.blend"))

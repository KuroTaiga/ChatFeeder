import bpy
import os
import sys
import shutil

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
    count = 0
    # Iterate over all .blend files in input_dir
    for filename in os.listdir(input_dir):
        if filename.endswith('.blend'):
            blend_file = os.path.join(input_dir, filename)
            base_name = os.path.splitext(filename)[0]
            output_file = os.path.join(output_dir, base_name + ".mp4")
            if (base_name+".mp4")in os.listdir(output_dir):
                count+=1
                print(f"{count} already done {base_name}")
            else:
                print(f"Rendering {blend_file} to {output_file}")
                render_blend_file(blend_file, output_file)
def cherryPick():
    input_dir = "./blender_mp4"
    final_dir = "./blender_pics_final"
    output_dir = "./blender_rule_source"
    os.makedirs(output_dir, exist_ok=True)
    input_dir = os.path.abspath(input_dir)
    final_dir = os.path.abspath(final_dir)
    output_dir = os.path.abspath(output_dir)
    count = 0
    base_name = ""
    act_list = []
    for filename in os.listdir(input_dir):
        base_name = os.path.splitext(filename)[0]
        act_list.append(base_name)
        
    for filename in os.listdir(final_dir):
        base_name =  os.path.splitext(filename)[0]
        if base_name in act_list:
            count+=1
            shutil.copy(src=os.path.join(final_dir,filename),dst=os.path.join(output_dir,filename))
            print(f"Act: {base_name}, Count: {count}")


if __name__ == "__main__":
    #main()
    cherryPick()

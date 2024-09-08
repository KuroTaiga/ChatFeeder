import bpy
import os

# 设置输入和输出文件夹路径
input_folder = './blender_source'
output_folder_clean = './blender_pics_final'
output_folder_3pics = './blender_pics'

# 确保输出文件夹存在
if not os.path.exists(output_folder_clean):
    os.makedirs(output_folder_clean)
if not os.path.exists(output_folder_3pics):
    os.makedirs(output_folder_3pics)

# 获取所有 .blend 文件
blend_files = [f for f in os.listdir(input_folder) if f.endswith('.blend')]

for blend_file in blend_files:
    # 打开 .blend 文件
    blend_path = os.path.join(input_folder, blend_file)
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    
    # 设置输出格式为 PNG
    bpy.context.scene.render.image_settings.file_format = 'PNG'

    # 获取总帧数
    total_frames = bpy.context.scene.frame_end
    
    # 定义需要渲染的帧百分比
    percentages = [0.1, 0.5, 0.9]
    frames = [int(total_frames * p) for p in percentages]

    rendered_images = []
    
    # 渲染每个指定帧
    for frame in frames:
        bpy.context.scene.frame_set(frame)
        output_image_path = os.path.join(output_folder_3pics, f"{os.path.splitext(blend_file)[0]}_{frame}.png")
        bpy.context.scene.render.filepath = output_image_path
        bpy.ops.render.render(write_still=True)
        rendered_images.append(output_image_path)

    # 组合图片
    if len(rendered_images) == 3:
        from PIL import Image
        
        images = [Image.open(img) for img in rendered_images]
        widths, heights = zip(*(i.size for i in images))
        
        total_width = sum(widths)
        max_height = max(heights)
        
        new_image = Image.new('RGB', (total_width, max_height))
        
        x_offset = 0
        for img in images:
            new_image.paste(img, (x_offset, 0))
            x_offset += img.width
        
        final_image_path = os.path.join(output_folder_clean, f"{os.path.splitext(blend_file)[0]}_concatenated.png")
        new_image.save(final_image_path)

print("All images have been rendered and concatenated successfully!")

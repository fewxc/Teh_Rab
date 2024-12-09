from PIL import Image, ImageDraw, ImageOps, ImageFont
import os
import math

def create_collage(image_paths, output_path, title):
    gray_color = (200, 200, 200) # Серый фон
    border_size = 10 # Размер рамки
    title_height = 100 # Высота заголовка
    cell_size = 200 # Размер ячеек

    images = []
    for path in image_paths:
        img = Image.open(path)
        # Обрезка и изменение размера изображений
        img = ImageOps.fit(img, (cell_size, cell_size), Image.Resampling.LANCZOS)
        images.append(img)

    # Размеры коллажа
    num_images = len(images)
    grid_columns = math.ceil(math.sqrt(num_images))
    grid_rows = math.ceil(num_images / grid_columns)

    collage_width = grid_columns * (cell_size + border_size) - border_size
    collage_height = grid_rows * (cell_size + border_size) + title_height

    # Пустой коллаж
    collage = Image.new('RGB', (collage_width, collage_height), gray_color)
    draw = ImageDraw.Draw(collage)

    # Размер заголовка
    font_size = 40
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0,0), title, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    text_x = (collage_width - text_width) // 2
    text_y = (title_height - text_height) // 2
    draw.text((text_x, text_y), title, fill="black", font=font)

    # Расположение изображений на коллаже
    for idx, img in enumerate(images):
        row, col = divmod(idx, grid_columns)
        x_offset = col * (cell_size + border_size)
        y_offset = row * (cell_size + border_size) + title_height
        collage.paste(img, (x_offset,y_offset))

    # Сохранение
    collage.save(output_path)
    print(f"Коллаж сщхранен: {output_path}")

    if __name__=="__main__":
        # Папка с изображениями
        image_dir = r"C:\Users\карио\Desktop\KOLAZH\images"
        # Имя итогового файла
        output_file = r"C:\Users\карио\Desktop\KOLAZH\result\collage.jpg"
        # Заголовок
        title = "OMG"

        if not os.path.exists(image_dir):
            print (f"Папка {image_dir} не существует! Попробуйте изменить путь.")
            exit()
                   
        image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir)
                       if f.lower().endswith(('jpg', 'jpeg', 'png'))]
        
    if len(image_paths) == 0:
        print("В указанной папке нет изображений форматов jpg, jpeg, png")
        exit()

    # Создание коллажа
    create_collage(image_paths, output_file, title)
import cv2


def crop_image(image, relative_coords):
    # 解析字符串为浮点数
    x1_rel, y1_rel, x2_rel, y2_rel = map(float, relative_coords.split(','))

    # 获取图像的高度和宽度
    height, width = image.shape[:2]

    # 计算绝对坐标
    x1 = int(x1_rel * width)
    y1 = int(y1_rel * height)
    x2 = int(x2_rel * width)
    y2 = int(y2_rel * height)

    # 裁切图像
    cropped_image = image[y1:y2, x1:x2]

    return cropped_image


def distance_ruler(image, num_ticks):
    marked_image = image.copy()
    height, width = marked_image.shape[:2]
    # 绘制坐标轴
    cv2.line(marked_image, (0, height // 2), (width, height // 2), (0, 0, 255), height // 1000)  # X轴
    cv2.line(marked_image, (width // 2, 0), (width // 2, height), (0, 0, 255), width // 1000)  # Y轴

    # 绘制刻度
    num_ticks = 10  # 刻度数量
    for i in range(num_ticks + 1):
        # X轴刻度
        x = int(i * (width / num_ticks))
        cv2.line(marked_image, (x, height // 2 - 5), (x, height // 2 + 5), (0, 0, 255), height // 100)
        # Y轴刻度
        y = int(i * (height / num_ticks))
        cv2.line(marked_image, (width // 2 - 5, y), (width // 2 + 5, y), (0, 0, 255), width // 100)

    font_scale = 14  # 字体大小
    for i in range(num_ticks + 1):
        # X轴标签
        x_label = f"{i / num_ticks:.1f}"
        cv2.putText(marked_image, x_label, (int(i * (width / num_ticks)), height // 2 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), 5)
        # Y轴标签
        y_label = f"{i / num_ticks:.1f}"
        cv2.putText(marked_image, y_label, (width // 2 + 10, int(i * (height / num_ticks))),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), 5)
    return marked_image


def bounding_box(image, relative_coords):
    edited_image = image.copy()
    # 解析字符串为浮点数
    x1_rel, y1_rel, x2_rel, y2_rel = map(float, relative_coords.split(','))

    # 获取图像的高度和宽度
    height, width = image.shape[:2]

    # 计算绝对坐标
    x1 = int(x1_rel * width)
    y1 = int(y1_rel * height)
    x2 = int(x2_rel * width)
    y2 = int(y2_rel * height)

    cv2.line(edited_image, (x1, y1), (x2, y1), (0, 0, 255), height // 100)
    cv2.line(edited_image, (x1, y2), (x2, y2), (0, 0, 255), height // 100)
    cv2.line(edited_image, (x1, y1), (x1, y2), (0, 0, 255), height // 100)
    cv2.line(edited_image, (x2, y1), (x2, y2), (0, 0, 255), height // 100)

    return edited_image
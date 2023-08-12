import base64
import numpy as np
import cv2

class ConversionError(Exception):
    pass

def get_buffer_image(base64img: str):
    if base64img.startswith("data:image/"):
        base64img = base64img.split(";")[1].split(",")[1]
    image_data = base64.b64decode(base64img)
    nparr = np.frombuffer(image_data, np.uint8)

    image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

    # 이미지를 JPG 형식으로 인코딩하여 메모리 버퍼에 저장
    success, jpg_buffer = cv2.imencode(".jpg", image)
    if (success):
        return jpg_buffer
    raise ConversionError("Failed to encode image as JPG.")


def get_base64_from_buffer(buffer):
    return base64.b64encode(buffer).decode()

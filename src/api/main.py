from fastapi import FastAPI
from pydantic import BaseModel, validator, ValidationError
from fastapi.middleware.cors import CORSMiddleware

from image_extension.core import start_process

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Img2imgRequestBody(BaseModel):
    base_image: str
    roop_image: str
    face_index: int

    @validator('base_image', 'roop_image')
    def validate_blank(cls, v):
        if not bool(v):
            raise ValidationError("image should not blank")
        return v


class Img2ImgResponse(BaseModel):
    image: str

    @validator('image')
    def validate_blank(cls, v):
        if not bool(v):
            raise ValidationError("image should not blank")
        return v


@app.post("/api/v1/img2img")
def img2img_api(req: Img2imgRequestBody) -> Img2ImgResponse:
    image = start_process(
        req.base_image,
        req.roop_image,
        req.face_index
    )

    return Img2ImgResponse(image=image)

from fastapi import FastAPI, File
from fastapi.responses import FileResponse,JSONResponse
from db.models import Property
from services.property_service import PropertyService
from loguru import logger
from helpers.inputs import GeoJsonBody

app = FastAPI()

@app.get('/properties')
def properties():
    return JSONResponse(PropertyService.list_properties())

@app.get('/display/{id}')
def get_image(id: str) -> FileResponse:
    logger.info(f'Request get display id: {id}')
    filename = PropertyService.get_or_download_image(id)
    return FileResponse(filename, media_type="image/jpeg")


@app.post('/find')
def find(geo_json: GeoJsonBody):
    res = PropertyService.find_distance(geo_json)
    return res
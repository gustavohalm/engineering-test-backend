from unittest import result

from matplotlib import dviread
from helpers.inputs import GeoJsonBody
from db.models import Property
import os.path
from client.client import download_image
from db.db import db_conn
from loguru import logger
import pandas as pd
from sqlalchemy import func, select

class PropertyService():
    def __init__(self):
        PropertyService.__init__(self)
    
    @staticmethod
    def list_properties():
        logger.info('getting all properties')
        properties = db_conn.query(Property).all()        
        return [p.serialize for p in properties]

    @staticmethod
    def get_or_download_image(id):
        logger.info(f'Get or downloading image')
        file_name = f'/tmp/{id}.jpeg'
        if not os.path.isfile(file_name):
            property = db_conn.query(Property).filter(Property.id == id).first()
            download_image(property.image_url, file_name)
        return file_name

    @staticmethod
    def find_distance(geo_json: GeoJsonBody):
        logger.info(f'looking for distance {geo_json.__dict__}')
        geom = f'{geo_json.location.type.upper()}({geo_json.location.coordinates[0]} {geo_json.location.coordinates[1]})'
        s = select([Property], func.ST_DWithin(Property.geocode_geo, geom, geo_json.distance) )
        # properties = [ p.serialize for p in db_conn.query(Property).all()]
        # # result = db_conn.query(Property).filter(Property.geocode_geo.ST_DWithain(geo_json.location.__dict__, geo_json.distance ))
        # properties = pd.DataFrame(properties)
        # logger.info(f'properties df {properties}')
        # result = db_conn.execute(s)
        # logger.info(f'result {result}')
        # for row in result:
        #     print('row',row)
        properties = db_conn.query(Property).filter(func.ST_DWithin(Property.geocode_geo, geom, geo_json.distance)).all()
        logger.info(f'properties {properties}')       
        return [p.serialize for p in properties]
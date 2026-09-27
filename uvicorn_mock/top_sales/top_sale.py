import decimal
import json
import random
import time
import uuid
import datetime
import sys
import httpx
from pathlib import Path
import faker

current_dir = Path(__file__).resolve().parent
generic_path = str(current_dir / "generic")

if generic_path not in sys.path:
    sys.path.insert(0, generic_path)

import grpc
from google.protobuf import wrappers_pb2
import asyncio
from pydantic import BaseModel
from concurrent import futures
from google.protobuf.json_format import MessageToDict
import generic.MarketData_pb2
import generic.MarketData_pb2_grpc
import generic.QutesStreamService_pb2
import generic.QutesStreamService_pb2_grpc
import generic.qoi_pb2_grpc
import generic.qoi_pb2
from typing import Union
from fastapi import FastAPI
from fastapi import Request
from modeles.otp_model import OTP
from starlette.responses import JSONResponse

app = FastAPI()
faker = faker.Faker("RU-ru")


@app.post("/")
async def post_method():
    return JSONResponse({"some":"data"})


class QuotesStreamService(generic.QutesStreamService_pb2_grpc.QuotesStreamServiceServicer):

    async def getDataStream(self, request, context):
        pass


class CatalogOfInstrumentsService(generic.qoi_pb2_grpc.CatalogOfInstrumentsServiceServicer):
    async def SubscribeSecurityData(self, request, context):
        pass


async def serve_quotes():
    server = grpc.aio.server()
    generic.QutesStreamService_pb2_grpc.add_QuotesStreamServiceServicer_to_server(QuotesStreamService(), server)
    server.add_insecure_port('[::]:9095')
    await server.start()
    await server.wait_for_termination()


async def server_qoi():
    server = grpc.aio.server()
    generic.qoi_pb2_grpc.add_CatalogOfInstrumentsServiceServicer_to_server(CatalogOfInstrumentsService(), server)
    server.add_insecure_port('[::]:9090')
    await server.start()
    await server.wait_for_termination()


@app.on_event("startup")
async def startup_event():
    import asyncio
    asyncio.create_task(serve_quotes())
    asyncio.create_task(server_qoi())

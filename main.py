from fastapi import FastAPI, BackgroundTasks, Response
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from io import BytesIO
from backend.directions import direction_main
from backend.charts import create_img


app = FastAPI()


origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# @app.get("/")
# async def root():
#     csv_file = "test/sample_addresses.csv"
#     df = pd.read_csv(csv_file)
#     values = df.values.tolist()
#     response = await direction_main(address_pairs=values)
#     return JSONResponse(content=response)


@app.get('/')
async def get_chart():

    csv_file = "test/sample_addresses.csv"
    df = pd.read_csv(csv_file)
    df.reset_index(inplace=True)
    values = df.values.tolist()
    response = await direction_main(address_pairs=values)
    df = pd.DataFrame.from_dict(response)
    chart = create_img(df)

    buffer = BytesIO()
    chart.savefig(buffer, format="png")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")
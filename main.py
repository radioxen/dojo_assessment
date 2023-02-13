from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse
import pandas as pd
from io import BytesIO
from backend.directions import direction_main
from backend.charts import create_img
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")


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

@app.get("/")
async def main():
    content = """
<body>
<form action="/chart" enctype="multipart/form-data" method="post">
<input name="file" type="file" single>
<input type="submit">
</body>
    """
    return HTMLResponse(content=content)


@app.post("/chart")
async def get_chart(file: UploadFile):

    contents = file.file.read()
    buffer = BytesIO(contents)
    df = pd.read_csv(buffer)
    buffer.close()
    file.file.close()
    df.reset_index(inplace=True)
    values = df.values.tolist()
    response = await direction_main(address_pairs=values)
    df = pd.DataFrame.from_dict(response)
    chart = create_img(df)

    buffer = BytesIO()
    chart.savefig(buffer, format="png")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")

from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
#from starlette import *
import uvicorn, aiohttp, asyncio
from io import BytesIO

from fastai import *
from fastai.vision import *

#classes = ['black', 'grizzly', 'teddys']
# Should be :
#classes = ['iron_man','spider_man','captain_america']
# But appears to be (on result) :
#classes = ['captain_america','iron_man','spider_man']
#Reformatted, it gives :
classes = ['Captain America','Iron Man','Spider Man']

# Functions

# This function rearranges a dirty suite of numbers with exponents into a list of clean pourcentages
def formatOutputPourcentages(my_string):
    #my_string = str(my_string)
    my_string = my_string.split("[")[1].split("]")[0]
    return ["{0:.3%}".format(float(s)).zfill(7) for s in my_string.split(", ") if float(s)]

# This function adds the corresponding classes to pourcentages and returns a string
def formatOutput(my_string):
    my_array = formatOutputPourcentages(my_string)
    result = ""
    increment = 0
    for afloat in my_array:
        result += classes[increment] + " : " + str(afloat)+"/"
        increment+=1
    return result

# This function reformat iron_man into Iron Man, for example
def formatResultStringIntoCustomizedString(my_string):
    switcher = {
        "captain_america": "Captain America",
        "iron_man": "Iron Man",
        "spider_man": "Spider Man"
    }
    return switcher.get(my_string, "Catégorie invalide")

# export_file_url = 'https://www.dropbox.com/s/v6cuuvddq73d1e0/export.pkl?raw=1'
#export_file_url = 'https://www.dropbox.com/s/6bgq8t6yextloqp/export.pkl?raw=1'
export_file_name = 'export.pkl'


path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))

async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f: f.write(data)

async def setup_learner():
    #await download_file(export_file_url, path/export_file_name)
    try:
        #learn = load_learner(path, export_file_name)
        learn = load_learner(path, 'models/'+export_file_name)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

@app.route('/')
def index(request):
    html = path/'view'/'index.html'
    return HTMLResponse(html.open().read())

@app.route('/analyze', methods=['POST'])
async def analyze(request):
    data = await request.form()
    img_bytes = await (data['file'].read())
    img = open_image(BytesIO(img_bytes))
    #prediction = learn.predict(img)[0]
    prediction_object = learn.predict(img)
    #return JSONResponse({'result': str(prediction_object)})
    result = str(learn.predict(img)[0])

    return JSONResponse({'result': "result/"+formatResultStringIntoCustomizedString(result)+"/"+str(formatOutput(str(learn.predict(img)[2])))})

if __name__ == '__main__':
    if 'serve' in sys.argv: uvicorn.run(app=app, host='0.0.0.0', port=5042)

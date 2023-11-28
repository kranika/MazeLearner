import json, logging , time, requests, re,  os,math,cairo
from typing import *
from dotenv import load_dotenv

# global resource paths
IMAGE_PATH='res/img'
FONT_PATH='res/fonts'
JS_PATH='res/js'

# Load any environment variables from .env
load_dotenv()

#configure logging
logging.basicConfig(filename='log.txt', level=logging.INFO)

#create a surface to draw pacman 
# surface=cairo.ImageSurface(cairo.FORMAT_RGB24,600,400)
# ctx=cairo.Context(surface)
# ctx.set_source_rgb(.33, .33, .33)
# ctx.stroke() 



def list_to_json(word_list:list,file_name:str)->None:
    # Convert list to JSON array
    json_array = {str(i): word for i, word in enumerate(word_list)}
    output_file=f'{file_name}.json'

    # Open the file in write mode
    with open(output_file, 'w') as output_file:
        # Write the JSON data to the file
        json.dump(json_array, output_file, indent=2)
   
     # Log a message with a timestamp
    timestamp = time.ctime()
    log_message = f"{timestamp} - File {file_name}.json created successfully"
    logging.info(log_message)


def read_json(file_name:str)->Dict[int,str]:
    # read the file path
    #change to the dict that works
    with open(f'{file_name}.json') as json_file:
        data = json.load(json_file)
        return data


# this function removes html tags from a string 
def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# this function defines a word using wordnik api
def defineWord(word:str):
    
    #wordnik only accesses word as lowercase
    word=word.lower()

    # Access your wordnik API key
    wordnik_api_key = os.getenv("WORDNIK_API_KEY")

    url='https://api.wordnik.com/v4/word.json/{}/definitions'.format(word)
    params={
        'limit':200,
        'partOfSpeech':'noun',
        'includeRelated':'false',
        'sourceDictionaries':'wiktionary',
        'useCanonical':'false',
        'includeTags':'false',
        'api_key':f'{wordnik_api_key}'
    }
    response=requests.get(url,params=params)
    try:
        return remove_html_tags(response.json()[0]['text'])
    except KeyError:
        return response.json()['message']




# # this function takes custom circle params
# #the context is passed because this function is called from outside this function
# def draw_circle(x, y, r,start_angle:int,end_angle:int,ctx=ctx,)->None :
#     # ,red=.33, green=.67, blue=0
#      # Set the circle's center coordinates (x, y) and radius (r)
#      #start angle is where your arc starts 
#      #end angle is where your arc ends 
#     ctx.arc(x, y, r, (start_angle)* math.pi, (end_angle)* math.pi)
#     ctx.set_source_rgb(1, 0, 0)
#     ctx.fill()


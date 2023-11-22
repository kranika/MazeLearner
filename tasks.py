import json, logging , time, requests, re,  os
from typing import *
from dotenv import load_dotenv

# Load any environment variables from .env
load_dotenv()

#configure logging
logging.basicConfig(filename='log.txt', level=logging.INFO)


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


word_list =[
  'ujamaa','mzee','zaire','boep','marabi' ,'thebe','hoodia','vly','ouabain', 'kaama','harmel', 'tenrec', 'tanrec', 
  'kierie', 'loiasis', 'mhorr',   'dika','laura',   'VOUDOU','vaudoux', 'VODUN','tampan', 'dagga', 'boet', 'abuna',
  'khamsin', 'KAMSEEN', 'KAMSIN', 'KHAMSEEN','VODOUN',  'VOODOO','vervet', 'whenwe','SCIROCCO',  'sirocco', 'SIROC',
'VODOU','ackee', 'akee','zorille', 'zoril', 'zorilla','pesewa','cedi', 'bwana', 'matatu', 'benga', 'kelim', 'kilim', 'indaba',  'kitenge', 'tajine', 'quango', 'tilapia', 
  'reedbuck', 'ngwee', 'inkosi', 'lekgotla', 'ASSaGAI', 'BATELEUR', 'wenge', 'braai', 'ka', 'stoep', 'kabaka', 
  'kaftan', 'toea', 'kikoi', 'boerewors', 'obi', 'ASSEGAI', 'ubuntu', 'kora', 'naira', 'duyker', 'AMAKHOSI',
   'kwanza', 'amakosi', 'boubou', 'mbira', 'skollie', 'buchu', 'kraal', 'tsotsi', 'aoudad', 'makuta', 'kente', 
   'iroko', 'INkhosi', 'zimb', 'volk', 'obeah', 'zareba', 'fundi', 'dashiki', 'kloof', 'guereza', 'kipunji',
    'tarboosh', 'kwacha',  'soukous', 'duiker', 'razzia', 'waragi', 'nyala', 'kalimba', 'quagga','boma',
     'jomo',  'likuta', 'matooke', 'pronk', 'lwei', 'ouguiya', 'kufi',  'kgotla', 'MATAMBALA', 'GUMBO', 'potto', 'gombo', 'bredie',
     'sosatie', 'couscous', 'fynbos', 'mitumba', 'matoke', 'tambala', 'manyatta', 'injera', 'alma', 'bumster',
      'shweshwe', 'kobo', 'mzungu',  'nakfa','djembe' ,'kniphofia','kanga','shamba','nerine','safari', 
      'raffia','sultana', 'jambok','sjambok','askari','springbok','rooinek', 'hieratic', 'rooikat', 'donga', 'robusta',
      'maloti', 'mielie', 'loti', 'mealie','laager','spaza', 'mooli','pula','hoodia','ZOMBIe','BUSHBUCK', 'boshbok',
      'nyala', 'STEENBUCK', 'STEENBOK', 'steinbok','STEINBOCK', 'khaya', 'WHYDAH',  'WHIDAH',
      
      
]

# create a json file from the list above
# list_to_json(word_list,'words')

# print(defineWord('kipunji'))
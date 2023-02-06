"""Implements Vana API for querying accounts that have Dreambooth trained models. """

import requests
import json

# prompts: https://mpost.io/best-100-stable-diffusion-prompts-the-most-beautiful-ai-text-to-image-prompts/

# get email code via email 
def get_email_code(email):
    api_url = "https://api.vana.com/api/v0/auth/create-login"
    d = {"email": email}     
    headers = {"Content-Type":"application/json"}
    response = requests.post(api_url, data=json.dumps(d), headers=headers)
    if response.status_code==200:
        print("Check your email to get the code")
    else:
        print("Something went wrong. ")
    # if response is [200]
    #print(response)
    #print("returning response")
    #return response  

    
# get access token
def get_access_token(email,code):
    api_url = "https://api.vana.com/api/v0/auth/login"
    d = {"email": email,
         "code": code}     
    headers = {"Content-Type":"application/json"}
    response = requests.post(api_url, data=json.dumps(d), headers=headers)
    token = response.json()['token']
    #print(response)
    #print("Add to:\ntokens[user] = ") 

    return token     
    
    
# Get list of exhibits 
def get_list_of_exhibits(token):
    api_url = "https://api.vana.com/api/v0/account/exhibits"
    headers = {"Content-Type":"application/json",
               "Authorization":"Bearer {}".format(token)}
    response = requests.get(api_url, headers=headers)
    #print(response)
    exhibits = response.json()['exhibits']
    return exhibits


# generate some images on vana 
def generate_vana_images(emails,user,tokens, prompt=None, exhibit_name=None):
    prompt = "very complex hyper-maximalist overdetailed cinematic tribal fantasy closeup macro portrait of a heavenly beautiful young royal dragon queen {target_token} with long platinum blonde windblown hair and dragon scale wings, Magic the gathering, pale wet skin and dark eyes and red lipstick ,flirting smiling passion seductive, vibrant high contrast, by andrei riabovitchev, tomasz alen kopera,moleksandra shchaslyva, peter mohrbacher, Omnious intricate, octane, moebius, arney freytag, Fashion photo shoot, glamorous pose, trending on ArtStation, dramatic lighting, ice, fire and smoke, orthodox symbolism Diesel punk, mist, ambient occlusion, volumetric lighting, Lord of the rings, BioShock, glamorous, emotional, tattoos,shot in the photo studio, professional studio lighting, backlit, rim lighting, Deviant-art, hyper detailed illustration, 8k" if prompt is None else prompt
    exhibit_name = "tribal_fantasy"  if exhibit_name is None else exhibit_name

    api_url = "https://api.vana.com/api/v0/jobs/text-to-image"
    d = {"email": emails[user],
         "prompt": prompt,
         "exhibit_name":exhibit_name}     
    headers = {"Content-Type":"application/json",
               "Authorization":'Bearer {}'.format(tokens[user])}
    response = requests.post(api_url, data=json.dumps(d), headers=headers)
    print(response)
    print("Returning response.")
    return response 

# get links to images
def get_image_links(token,exhibit=None):
    exhibit = "black-and-white" if exhibit is None else exhibit

    api_url = "https://api.vana.com/api/v0/account/exhibits/" + exhibit 
    headers = {"Content-Type":"application/json",
               "Authorization":"Bearer {}".format(token)}
    response = requests.get(api_url, headers=headers)
    #print(response)
    if not response.status_code == 200:
        print("something went wrong")
         
    image_links = response.json()['urls']
    return image_links
    
# download images 
def download_images(image_links, user="",exhibit="", folder="", only_one=False):
    
    def download_image(url, savename):
        img_data = requests.get(url).content
        with open(savename, 'wb') as handler:
            handler.write(img_data)
    
    folder = "" if folder=="" else folder+"/"
    prefix = user + "-" + exhibit + "-" if user!="" and exhibit!="" else ""
    if only_one:
        image_links = [image_links[0]]
    L = len(image_links)
    paths = []
    for i, url in enumerate(image_links):
        savename = folder+prefix + str(i) + ".png"
        download_image(url,savename)
        paths.append(savename)
    return paths
    
def example():
    # example request 
    api_url = "https://jsonplaceholder.typicode.com/todos"
    todo = {"userId": 1, "title": "Buy milk", "completed": False}
    headers =  {"Content-Type":"application/json"}
    response = requests.post(api_url, data=json.dumps(todo), headers=headers)
    print(response.json())


if __name__=="__main__":
    
    # emails 
    emails = {"vitoria":"anavitoria_rodrigueslima@fas.harvard.edu",
              "nemo":"nemoshi@gse.harvard.edu", 
              "cat":"vito.rodrigueslima@gmail.com"}
    

    tokens = {"vitoria":"",
            "nemo":"", 
            "cat":""}
    
    # get codes 
    #get_email_code(emails['nemo'])
    #get_email_code(emails['cat'])
    
    from IPython import embed; embed()
    #get_access_token(emails['nemo'],code)
    #get_access_token(emails['cat'],code)
    #get_access_token(emails['vitoria'],code)
    

    # GET ACCESS TOKEN MANUALLY
    # api_url = "https://api.vana.com/api/v0/auth/login"
    # d = {"email": emails['cat'],
    #      "code": str(160343)}     
    # headers = {"Content-Type":"application/json"}
    # response = requests.post(api_url, data=json.dumps(d), headers=headers)
    # print(response)
    # print(response.json())
    # token = response.json()['token']

    
    
    get_list_of_exhibits(tokens['nemo'])
    get_list_of_exhibits(tokens['cat'])
    get_list_of_exhibits(tokens['vitoria'])
    
    
    exhibits = ['cosmic', 'cyberpunk', 'black-and-white']
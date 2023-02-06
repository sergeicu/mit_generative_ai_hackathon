import requests
import json

# prompts: https://mpost.io/best-100-stable-diffusion-prompts-the-most-beautiful-ai-text-to-image-prompts/

def download_image(url, savename):
    img_data = requests.get(url).content
    with open(savename, 'wb') as handler:
        handler.write(img_data)



# get email code via email 
def get_email_code(emails,user):
    api_url = "https://api.vana.com/api/v0/auth/create-login"
    d = {"email": emails[user]}     
    headers = {"Content-Type":"application/json"}
    response = requests.post(api_url, data=json.dumps(d), headers=headers)
    print(response)
    print("returning response")
    return response  

    
# get access token
def get_access_token(emails,user,code):
    api_url = "https://api.vana.com/api/v0/auth/login"
    d = {"email": emails[user],
         "code": code}     
    headers = {"Content-Type":"application/json"}
    response = requests.post(api_url, data=json.dumps(d), headers=headers)
    token = response.json()['token']
    print(response)
    print("Add to:\ntokens[user] = ") 

    return token     
    
    
# Get list of exhibits 
def get_list_of_exhibits(tokens,user):
    api_url = "https://api.vana.com/api/v0/account/exhibits"
    headers = {"Content-Type":"application/json",
               "Authorization":"Bearer {}".format(tokens[user])}
    response = requests.get(api_url, headers=headers)
    print(response)
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
def get_image_links(tokens,user,exhibit=None):
    exhibit = "black-and-white" if exhibit is None else exhibit

    api_url = "https://api.vana.com/api/v0/account/exhibits/" + exhibit 
    headers = {"Content-Type":"application/json",
               "Authorization":"Bearer {}".format(tokens[user])}
    response = requests.get(api_url, headers=headers)
    print(response)
    
    image_links = response.json()['urls']
    return image_links
    
# download images 
def download_images(image_links, user="",exhibit="", folder=""):
    folder = "" if folder=="" else folder+"/"
    prefix = user + "-" + exhibit + "-" if user!="" and exhibit!="" else ""
    L = len(image_links)
    for i, url in enumerate(image_links):
        savename = folder+prefix + str(i) + ".png"
        download_image(url,savename)
        print(savename)
    
def example():
    # example request 
    api_url = "https://jsonplaceholder.typicode.com/todos"
    todo = {"userId": 1, "title": "Buy milk", "completed": False}
    headers =  {"Content-Type":"application/json"}
    response = requests.post(api_url, data=json.dumps(todo), headers=headers)
    print(response.json())



if __name__=='__main__':

    from IPython import embed; embed()
    
    # tokens
    tokens = {"vitoria":"eyJhbGciOiJSUzI1NiJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6InZhbmEtdXNlciIsIngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsidmFuYS11c2VyIl0sIngtaGFzdXJhLXVzZXItaWQiOiI0NDNjY2E4YS0xZWQ1LTRlYTQtOTdiYy04MjAxNTdkYTMwNmMifSwiZW1haWwiOiJhbmF2aXRvcmlhX3JvZHJpZ3Vlc2xpbWFAZmFzLmhhcnZhcmQuZWR1IiwiaWF0IjoxNjc0Nzk4NDg4LCJzdWIiOiI0NDNjY2E4YS0xZWQ1LTRlYTQtOTdiYy04MjAxNTdkYTMwNmMiLCJpc3MiOiJodHRwczovL2FwaS52YW5hLmNvbS8iLCJhdWQiOiJhcGkudmFuYS5jb20iLCJleHAiOjE2NzQ4ODQ4ODh9.CCw9yze6cemRO7hS7_kG9kFfXSUCHt-uekf2EHdRMBV__rSuugAVKNXRlKdVhKxyTxrJ2LnbNg5RUNXeYA8ZYkb4updmMvBSL5vyPZxoZHs21LDX9rHNuKjYMHE79rLaN1W1a2ThYGW_1kzg8cLP0hFieCdSBi-JQEtzLf8C7kivM1uowjpXCT-55svWPWoeKcPnTXIZL_-AxV6f5eXIujOd2CIIf7G0XryrPEO2KjJG41DWD6FY4GKmXXYSpNmB0O0woYzEDzqCXZ39PCN-R6Z0gAuclR0-6Z4TDv9JbGRLeYLd_GXe_hjVsuBqdgflNrPsrsQUSbOmfQ-Ya53nqg",
              "nemo":"", 
              "cat":""}

    # emails 
    emails = {"vitoria":"anavitoria_rodrigueslima@fas.harvard.edu",
              "nemo":"nemoshi@gse.harvard.edu", 
              "cat":"vito.rodrigueslima@gmail.com"}

    # set user 
    user = 'vitoria'


# ~/w/code/sd/experiments/sd/vana/webui
# conda activate ldm
# which python 

import sys 
import os 

import numpy as np
import gradio as gr
import vana_api2 as v 
import generate_mask as g

import torch
from diffusers import StableDiffusionImg2ImgPipeline
from diffusers import StableDiffusionInpaintPipeline


def sepia(input_img):
    sepia_filter = np.array([
        [0.393, 0.769, 0.189], 
        [0.349, 0.686, 0.168], 
        [0.272, 0.534, 0.131]
    ])
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    return sepia_img


def greet(name, is_morning, temperature):
    salutation = "Good morning" if is_morning else "Good evening"
    greeting = f"{salutation} {name}. It is {temperature} degrees today"
    celsius = (temperature - 32) * 5 / 9
    return greeting, round(celsius, 2)



if __name__ == "__main__":

    ###
    # [hidden] Init 
    ###

    # emails 
    emails = {"vitoria":"anavitoria_rodrigueslima@fas.harvard.edu",
              "nemo":"nemoshi@gse.harvard.edu", 
              "cat":"vito.rodrigueslima@gmail.com"}
    

    tokens = {"vitoria":"eyJhbGciOiJSUzI1NiJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6InZhbmEtdXNlciIsIngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsidmFuYS11c2VyIl0sIngtaGFzdXJhLXVzZXItaWQiOiI0NDNjY2E4YS0xZWQ1LTRlYTQtOTdiYy04MjAxNTdkYTMwNmMifSwiZW1haWwiOiJhbmF2aXRvcmlhX3JvZHJpZ3Vlc2xpbWFAZmFzLmhhcnZhcmQuZWR1IiwiaWF0IjoxNjc0Nzk4NDg4LCJzdWIiOiI0NDNjY2E4YS0xZWQ1LTRlYTQtOTdiYy04MjAxNTdkYTMwNmMiLCJpc3MiOiJodHRwczovL2FwaS52YW5hLmNvbS8iLCJhdWQiOiJhcGkudmFuYS5jb20iLCJleHAiOjE2NzQ4ODQ4ODh9.CCw9yze6cemRO7hS7_kG9kFfXSUCHt-uekf2EHdRMBV__rSuugAVKNXRlKdVhKxyTxrJ2LnbNg5RUNXeYA8ZYkb4updmMvBSL5vyPZxoZHs21LDX9rHNuKjYMHE79rLaN1W1a2ThYGW_1kzg8cLP0hFieCdSBi-JQEtzLf8C7kivM1uowjpXCT-55svWPWoeKcPnTXIZL_-AxV6f5eXIujOd2CIIf7G0XryrPEO2KjJG41DWD6FY4GKmXXYSpNmB0O0woYzEDzqCXZ39PCN-R6Z0gAuclR0-6Z4TDv9JbGRLeYLd_GXe_hjVsuBqdgflNrPsrsQUSbOmfQ-Ya53nqg",
            "nemo":"eyJhbGciOiJSUzI1NiJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6InZhbmEtdXNlciIsIngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsidmFuYS11c2VyIl0sIngtaGFzdXJhLXVzZXItaWQiOiJkN2Y4YmVjMy1jNzU5LTQxN2QtODMwZS1iNDYwZjlhNzVhMTQifSwiZW1haWwiOiJuZW1vc2hpQGdzZS5oYXJ2YXJkLmVkdSIsImlhdCI6MTY3NDgzNTMxMywic3ViIjoiZDdmOGJlYzMtYzc1OS00MTdkLTgzMGUtYjQ2MGY5YTc1YTE0IiwiaXNzIjoiaHR0cHM6Ly9hcGkudmFuYS5jb20vIiwiYXVkIjoiYXBpLnZhbmEuY29tIiwiZXhwIjoxNjc0OTIxNzEzfQ.vR2L4fzjS-c-5WtH1SS-9Wy3koLIfHfVK1GmU6ErFM23r__O_UTlnwT8Xuv3sOUsSkAmj37PRBSD4UY7az2H-YmNHGPrmPsbHHnegcIqcQEUPtk6Hm3GsEYO4K9OoFscTSy78ktWDkZ6DmaZqqw3z97qhYwM7BFqslS_Ml5k-1GJOS-I2-cSx9dq08TjJ3h9rF7NtsDsh3vRSPXkP_kixZKLS0MPiv6cbIOU-uPy9zWxANJXkIxYuVGWhz-F1Fzw1Yn5hs1ezf7J139F8z4qaDWKyHvjdan4pcu5oLkInt2XUjmhbZpJqPxHLoCIayjwrEZmyL2eCG924A70A5wLEA", 
            "cat":"eyJhbGciOiJSUzI1NiJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6InZhbmEtdXNlciIsIngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsidmFuYS11c2VyIl0sIngtaGFzdXJhLXVzZXItaWQiOiIwNDcxODBhZi01YTUyLTQ4ZDQtOTY5Zi1iYTJlOTBmYzc2ODYifSwiZW1haWwiOiJ2aXRvLnJvZHJpZ3Vlc2xpbWFAZ21haWwuY29tIiwiaWF0IjoxNjc0ODM1NTMwLCJzdWIiOiIwNDcxODBhZi01YTUyLTQ4ZDQtOTY5Zi1iYTJlOTBmYzc2ODYiLCJpc3MiOiJodHRwczovL2FwaS52YW5hLmNvbS8iLCJhdWQiOiJhcGkudmFuYS5jb20iLCJleHAiOjE2NzQ5MjE5MzB9.SSkD4KnMe7jVDq8kGGuLRdfjv3p8zn1ooeJccZ6RcuRFlvZPHoSomMhikJLZXu8hHutj0jt854KOGVtnA8bTHxlXLV23Rmk08jXp0KI6d0VjKqmcQDQQoJJArajYW0WfsYEHc6m34Ck1DayRPw-8Z8P8zMMhRKs1M0zyEG0UyCoIKVrE2Dkn8fZyWW2oF8yfi9YG-95ueyMP-R4LIqeUImX1zLdJDuCBu5arcmRNBgaEYXp09xmZXrzFekaqCvmgpxZ1RVZK2BEzbhEI11m2Xczr7v8GhXSJ-kCjFhfmtAI827ZUO0SNLNlSkfN8WZNB4xW1OaHaMrmGpe7zg4eE2w"}

    exhibits = ['cosmic', 'cyberpunk', 'black-and-white']

    demo = gr.Interface(
        fn=greet,
        inputs=["text", "checkbox", gr.Slider(0, 100)],
        outputs=["text", "number"],
    )
    #demo.launch()



    ###
    # [hidden] Load models here 
    ###
    
    # clipseg
    model_clipseg = g.load_clipseg()

    debug=False
    if debug:
        print("warning: skipping all steps. Pls uncomment")
        path1="nemo1.png"
        path2="cat2.png"
        prompt1=['person']
        prompt2=['cat']    
        # prompt2 = [identity2]
        rgba1,rgb1,mask1 = g.process_image(path1, prompt1, model_clipseg)
        #rgba2,original2,mask2 = g.process_image(path2, prompt2, model_clipseg)
        rgba2,rgb2,mask2 = g.process_image(path1, prompt1, model_clipseg)

        # create mask images & images  
        #rgba = g.put_images_together_rgba(rgba1,rgba2)
        rgba,rgb = g.put_images_together([rgba1,rgba2], [rgb1,rgb2], [mask1,mask2])
        
    
    
    #from IPython import embed; embed()
    
    # SD 1.5 
    device = "cuda"
    #pipe = StableDiffusionImg2ImgPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        "runwayml/stable-diffusion-inpainting",
        revision="fp16",
        torch_dtype=torch.float16,
    )    
    pipe.to(device)
    
    ###
    # type your emails [2boxes, pet tick box] -> Get Codes 
    ###
    #v.get_email_code(email)
    code=""
    identity1="person" # "person" or "cat"
    identity2="cat" # "person" or "cat"
    
    
    
    ###
    # type yours codes [2 boxes] -> Get Exhibits 
    ###
    #token1 = v.get_access_token(email,code)
    exhibits = v.get_list_of_exhibits(tokens['cat'])
    savedir =""
    exhibit = exhibits[1]

    
    ###
    # Select exhibit (dropdown list) -> Select 
    ###
    
    image_links1 = v.get_image_links(tokens['vitoria'],exhibit=exhibit)
    image_links2 = v.get_image_links(tokens['cat'],exhibit=exhibit)
    path1 = v.download_images(image_links1, user="1",exhibit=exhibit, folder=savedir, only_one=True)[0]
    path2 = v.download_images(image_links2, user="2",exhibit=exhibit, folder=savedir, only_one=True)[0]

    ###
    # Type prompt / Select from drop down -> Generate 
    ###
        
    # process image 
    assert identity1 in ['person', 'cat']
    prompt1 = [identity1]
    assert identity2 in ['person', 'cat']
    prompt2 = [identity2]    
    path1="nemo1.png"
    path2="cat1.png"
    rgba1,original1,mask1 = g.process_image(path1, prompt1, model_clipseg)
    rgba2,original2,mask2 = g.process_image(path2, prompt2, model_clipseg)

    # create mask images & images  
    rgba = g.put_images_together_rgba(rgba1,rgba2)
    rgb = g.put_images_together_rgb(original1,original2)
    #mask = g.put_images_together_rgb(mask1,mask2)

    # debug (save outputs)
    rgba.save("out-"+"rgba.png")
    rgb.save("out-"+"rgb.png")
    #rgba1.save("out-"+"rgba1.png")
    #original1.save("out-"+"original1.png")
    #mask1.save("out-"+"mask2.png")
    #rgba2.save("out-"+"rgba2.png")
    #original2.save("out-"+"original2.png")
    #mask2.save("out-"+"mask2.png")

    # send these to the model 
    from IPython import embed; embed()
    prompt = "A cyberpunk fantasy landscape, trending on artstation"
    #images = pipe(prompt=prompt, image=rgb, mask_image=rgba, strength=0.75, guidance_scale=7.5).images
    from PIL import Image 
    rgba=Image.open("test8.png")
    rgb = Image.open("test9.png")
    mask=Image.fromarray(np.tile(np.array(rgba)[:,:,3:], (1,1,4)))
    #rgba=Image.fromarray(np.tile(np.array(rgba)[:,:,3:], (1,1,4)))
    #rgba=Image.fromarray(np.tile(np.array(rgba)[:,:,3:], (1,1,4)))
    #rgba = Image.fromarray(np.concatenate((np.array(rgb),np.array(rgba)[:,:,3:]),axis=2),'RGBA')
    #images = pipe(prompt=prompt, image=rgba, mask_image=rgba,guidance_scale=15.).images
    images = pipe(prompt=prompt, image=rgba, mask_image=mask,guidance_scale=15.).images
    images[0].save("test9-"+"fantasy_landscape.png")    
    
    


    
    rgba=Image.open("test8.png")
    rgb = Image.open("test9.png")
    mask=Image.fromarray(np.tile(np.array(rgba)[:,:,3:], (1,1,3)))
    mask2=Image.fromarray(np.full((512,512,3), 255).astype(np.uint8) - np.tile(np.array(rgba)[:,:,3:], (1,1,3)))
    
    mask.save("test_mask.png")
    mask2.save("test_mask2.png")
    #rgba=Image.fromarray(np.tile(np.array(rgba)[:,:,3:], (1,1,4)))
    #rgba=Image.fromarray(np.tile(np.array(rgba)[:,:,3:], (1,1,4)))
    #rgba = Image.fromarray(np.concatenate((np.array(rgb),np.array(rgba)[:,:,3:]),axis=2),'RGBA')
    #images = pipe(prompt=prompt, image=rgba, mask_image=rgba,guidance_scale=15.).images
    images = pipe(prompt=prompt, image=rgb, mask_image=mask2,guidance_scale=15.).images
    images[0].save("test9-"+"fantasy_landscape.png")    

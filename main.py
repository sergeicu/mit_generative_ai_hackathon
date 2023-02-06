"""Application built for a MIT Generative AI Hackathon (hosted by Vana). 
See powerpoint 

"""

import numpy as np

# third party 
import torch
from PIL import Image

from diffusers import StableDiffusionInpaintPipeline

# custom 
import vana_api as v 
import generate_mask as g

if __name__ == "__main__":

    ###
    # Init 
    ###


    # all of these emails are associated with a VANA account, which provides custom Dreambooth trained person models
    emails = {"vitoria":"anavitoria_rodrigueslima@fas.harvard.edu",
              "nemo":"nemoshi@gse.harvard.edu", 
              "cat":"vito.rodrigueslima@gmail.com"}
    

    tokens = {"vitoria":"unique_token",
            "nemo":"unique_token", 
            "cat":"unique_token"}

    exhibits = ['cosmic', 'cyberpunk', 'black-and-white']

    code=""
    identity1="person" 
    identity2="cat" 
    savedir =""
    assert identity1 in ['person', 'cat']
    prompt1 = [identity1]
    assert identity2 in ['person', 'cat']
    prompt2 = [identity2]    



    ###
    # Get Clipseg and Stable Diffusion 
    ###


    # clipseg
    model = g.load_clipseg()

    # Stable Diffusion 
    device = "cuda"
    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        "runwayml/stable-diffusion-inpainting",
        revision="fp16",
        torch_dtype=torch.float16,
    )    
    pipe.to(device)
    
    
    ###
    # Get exhibits 
    ###
    
    exhibits = v.get_list_of_exhibits(tokens['cat'])
    
    
    # [demo only] Loop n times
    for ii in range(0,3):
                
        # [demo only] 
        user = 'vitoria' if ii ==1 else 'nemo'
        exhibit = exhibits[ii+1]

        ###
        # Download images 
        ###
        
        image_links1 = v.get_image_links(tokens[user],exhibit=exhibit)
        image_links2 = v.get_image_links(tokens['cat'],exhibit=exhibit)
        path1 = v.download_images(image_links1, user="1",exhibit=exhibit, folder=savedir, only_one=True)[0]
        path2 = v.download_images(image_links2, user="2",exhibit=exhibit, folder=savedir, only_one=True)[0]

        ###
        # Create joint images and mask
        ###
            
        rgba,rgb = g.process_images(path1,path2,prompt1,prompt2,model)
        mask2=Image.fromarray(np.full((512,512,3), 255).astype(np.uint8) - np.tile(np.array(rgba)[:,:,3:], (1,1,3)))
        
        ###
        # Generate images
        ###
        
        # generate   
        prompt = "A cyberpunk fantasy landscape, trending on artstation"
        images = pipe(prompt=prompt, image=rgb, mask_image=mask2,guidance_scale=15.).images
        images[0].save("u"+str(ii)+"-fantasy_landscape.png")    
        
        # save intermediate results 
        mask2.save("u"+str(ii)+"-mask.png")
        rgba.save("u"+str(ii)+"-rgba.png")
        rgb.save("u"+str(ii)+"-rgb.png")

        from IPython import embed; embed()    


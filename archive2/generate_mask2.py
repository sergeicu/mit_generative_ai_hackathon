import os 
import sys 

from PIL import Image 

import numpy as np 


import torch
from models.clipseg import CLIPDensePredT
from PIL import Image
from torchvision import transforms


def load_clip():
    # load model
    model = CLIPDensePredT(version='ViT-B/16', reduce_dim=64)
    model.eval();

    # non-strict, because we only stored decoder weights (not CLIP weights)
    model.load_state_dict(torch.load('weights/rd64-uni.pth', map_location=torch.device('cpu')), strict=False);
    
    return model 

def get_image(path):
    assert os.path.exists(path), f"Image path is wrong. {path}"
    # load and normalize image
    input_image = Image.open(path)

    # or load from URL...
    # image_url = 'https://farm5.staticflickr.com/4141/4856248695_03475782dc_z.jpg'
    # input_image = Image.open(requests.get(image_url, stream=True).raw)

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        transforms.Resize((352, 352)),
    ])
    img = transform(input_image).unsqueeze(0)    
    return img

def predict(img, prompts,model):
    # predict
    with torch.no_grad():
        preds = model(img.repeat(len(prompts),1,1,1), prompts)[0]
        
    # save as image 
    ims = []
    for i in preds:
        im = i.numpy()


        # turn into an image 
        im3 = np.tile(np.squeeze(im),(3,1,1))
        im4 = np.moveaxis(im3,0,-1)
        im5=im4.astype(np.uint8)
        image = Image.fromarray(im5)
        
        ims.append(image)
    return ims[0]  

def create_rgba(img1r,img1mr, invert=True):
    img1mra = np.array(img1mr)[:,:,0:1] 
    if invert:
        img1mra = np.full(img1mra.shape, 255.) - img1mra
        img1mra = img1mra.astype(np.uint8)
    img1ra = np.array(img1r)
    img1_full = np.concatenate((img1ra,img1mra),axis=-1)
    return Image.fromarray(img1_full,'RGBA')    

# put images together 
def put_images_together2(img1mr,img2mr):    
    a = np.zeros((512,512,4))
    a = a.astype(np.uint8)   
    #from IPython import embed; embed() 
    a[128:384, 0:256,:] = np.array(img1mr)
    a[128:384, 256:,:] = np.array(img2mr)
    ap = Image.fromarray(a)
    
    return ap

def load_clipseg():
    # load model
    model = CLIPDensePredT(version='ViT-B/16', reduce_dim=64)
    model.eval();

    # non-strict, because we only stored decoder weights (not CLIP weights)
    model.load_state_dict(torch.load('weights/rd64-uni.pth', map_location=torch.device('cpu')), strict=False);
    
    return model 


# put images together 
def put_images_together(img1mr,img2mr):    
    a = np.zeros((512,512,3))
    a = a.astype(np.uint8)    
    a[128:384, 0:256,:] = np.array(img1mr)
    a[128:384, 256:,:] = np.array(img2mr)
    ap = Image.fromarray(a)
    
    return ap

def process_images(path1,path2,prompt1,prompt2,model):
    
    
    # get images 
    img1 = Image.open(path1)
    img2 = Image.open(path2)    
    
    # predict segmentations 
    img1_torch = get_image(path1)
    img1m = predict(img1_torch, prompt1,model)
    img2_torch = get_image(path2)
    img2m = predict(img2_torch, prompt2,model)
    
    # resize  
    img1r = img1.resize((256,256))
    img2r = img2.resize((256,256))
    img1mr = img1m.resize((256,256))
    img2mr = img2m.resize((256,256))

    # add random noise  
    noise = np.random.randint(0,255,(256,256,3))
    np.array(img1r) + noise
    
    # create RGBA images (image + mask)
    img1_full = create_rgba(img1r,img1mr,invert=True)
    img2_full = create_rgba(img2r,img2mr,invert=True)
    
    rgba = put_images_together2(img1_full,img2_full)
    rgb = put_images_together(img1r,img2r)
    
    
    return rgba,rgb

if __name__ == '__main__':
    
    # load model 
    model = load_clip()

    # get paths 
    path1 = 'nemo1.png'
    prompt1= ['person']
    path2 = 'cat1.png'
    prompt2= ['cat']
    
    # get images 
    img1 = Image.open(path1)
    img2 = Image.open(path2)    
    
    # predict segmentations 
    img1_torch = get_image(path1)
    img1m = predict(img1_torch, prompt1)
    img2_torch = get_image(path2)
    img2m = predict(img2_torch, prompt2)
    
    # resize  
    img1r = img1.resize((256,256))
    img2r = img2.resize((256,256))
    img1mr = img1m.resize((256,256))
    img2mr = img2m.resize((256,256))

    # add random noise  
    noise = np.random.randint(0,255,(256,256,3))
    np.array(img1r) + noise
    
    # create RGBA images (image + mask)
    img1_full = create_rgba(img1r,img1mr,invert=True)
    img2_full = create_rgba(img2r,img2mr,invert=True)

    # fill images with stuff 
    #from IPython import embed; embed()
    
    
    
    # create mask images & images  
    put_images_together2(img1_full,img2_full).save("test8_new.png")
    put_images_together(img1r,img2r).save("test9_new.png")
    



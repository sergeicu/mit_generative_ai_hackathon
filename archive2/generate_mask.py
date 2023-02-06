import os 
import sys 

from PIL import Image 

import numpy as np 

sys.path.append("/home/ch215616/w/code/sd/experiments/sd/sd/clipseg")

import torch
from models.clipseg import CLIPDensePredT
from PIL import Image
from torchvision import transforms


def load_clipseg():
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
def put_images_together_rgba(img1mr,img2mr):    
    a = np.zeros((512,512,4))
    a = a.astype(np.uint8)    
    a[128:384, 0:256,:] = np.array(img1mr)
    a[128:384, 256:,:] = np.array(img2mr)
    ap = Image.fromarray(a)
    
    return ap


# put images together 
def put_images_together_rgb(img1r,img2r):    
    a = np.zeros((512,512,3))
    a = a.astype(np.uint8)    
    a[128:384, 0:256,:] = np.array(img1r)
    a[128:384, 256:,:] = np.array(img2r)
    ap = Image.fromarray(a)


    
    return ap


# put images together 
def put_images_together(rgbas,rgbs,masks, addnoise=True):    

    rgba1,rgba2 = rgbas
    rgb1,rgb2 = rgbs
    mask1, mask2 = masks 
    from IPython import embed; embed()
    
    # rgba
    rgba = np.zeros((512,512,4))
    rgba = rgba.astype(np.uint8)    
    rgba[128:384, 0:256,:] = np.array(rgba1)
    rgba[128:384, 256:,:] = np.array(rgba2)

    # rgb
    rgb = np.zeros((512,512,3))
    rgb = rgb.astype(np.uint8)    
    rgb[128:384, 0:256,:] = np.array(rgb1)
    rgb[128:384, 256:,:] = np.array(rgb2)

    # put together mask 
    mask = np.full((512,512,3),255)
    mask = mask.astype(np.uint8)    
    mask[128:384, 0:256,:] = np.array(mask1)
    mask[128:384, 256:,:] = np.array(mask2)


    # add noise 
    addnoise=False
    print("warning addnoise is false")
    input("proceed?")
    if addnoise:
        noise = np.random.randint(0,255,(512,512,3))
        noise = noise.astype(np.uint8)
        
        # get mask 
        m = rgba[:,:,-1]
        ib = np.where(np.logical_and(m>0, m<255)) # inbetween
        m[ib] = 0
        Image.fromarray(m).save("out_mask_test.png")
        
        mask_f = rgba[:,:,-1].astype(np.float)
        ib = np.where(np.logical_and(mask_f>0, mask_f<255)) # inbetween
        m[ib] = 0
        zr = np.where(mask_f==0)
        new = np.full(mask_f.shape,255)
        new[zr] = 0 
        Image.fromarray(new.astype(np.uint8)).save("out_mask_test.png")

        
        rgba_p.save("out_rgba_p.png")
        m = rgba[:,:,-1]
        Image.fromarray(np.moveaxis(np.tile(m,(3,1,1)), 0,-1).astype(np.uint8)).save("out_rgba_ch4.png")
        rgba = noise[zr]
        
        
    
    # turn to pil 
    rgba_p = Image.fromarray(rgba)    
    rgb_p = Image.fromarray(rgb)    
    mask_p = Image.fromarray(mask)
    
    # debug 
    debug = True
    if debug:
        rgba_p.save("out_rgba.png")
        rgb_p.save("out_rgb.png")
        mask_p.save("out_mask.png")
        mask1.save("out_mask_small.png")
        

    return rgba,rgb


def process_image(path1, prompt, model):
    
    assert isinstance(prompt,list)
    assert os.path.exists(path1)

    # get images 
    img1 = Image.open(path1)
    
    # predict segmentations 
    img1_torch = get_image(path1)
    img1m = predict(img1_torch, prompt, model)
    
    # resize  
    #from IPython import embed; embed()
    #img1m.save("out_img1m.png")
    #np.histogram(np.array(img1mr))
    
    img1r = img1.resize((256,256))
    img1mr = img1m.resize((256,256))
    #img1mr_a = np.array(img1mr).astype(np.float)
    #ib = np.where(np.logical_and(img1mr_a>0, img1mr_a<255)) # inbetween
    #img1mr_a[ib] = 0
    #img1mr = Image.fromarray(img1mr_a.astype(np.uint8))
        
    # create RGBA images (image + mask)
    img1_full = create_rgba(img1r,img1mr,invert=True)

    return img1_full,img1r,img1mr

if __name__ == '__main__':
    
    # load model 
    model = load_clipseg()
    
    # process image 
    rgba1,original1,mask1 = process_image(path1, prompt1)
    rgba2,original2,mask2 = process_image(path2, prompt2)


    # create mask images & images  
    rgba = put_images_together2(rgba1,rgba2)
    rgb = put_images_together(original1,original2)
    
    
    
    
    
    

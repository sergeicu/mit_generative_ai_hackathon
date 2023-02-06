import os 
import sys 

from PIL import Image 

import numpy as np 



def load_data_mask_v(path):    
    """Load PNG or numpy array and resize to 256x256"""
    
    if path.endswith("png"):
        # load with PIL and resize 
        image = Image.open(path)
        image = image.resize((256,256))
        return image
    
    if path.endswith("npy"):
        seg = np.load(path)
        
        # get clean segmentation 
        seg[seg>1] = 0 

        # resize segmentation to 512x512 
        seg_e = np.expand_dims(seg,0)
        seg_t = np.tile(seg_e,(3,1,1))
        seg_uint = np.moveaxis(seg_t,0,-1).astype(np.uint8)    
        image = Image.fromarray(seg_uint*255)
        seg_r = image.resize((256,256))

        return seg_r 


def load_data_image_v(path):    
    """Load PNG or numpy array and resize to 256x256"""
    
    if path.endswith("png"):
        # load with PIL and resize 
        image = Image.open(path)
        image = image.resize((256,256))
        return image
    
    if path.endswith("npy"):
        seg_uint = np.load(path).astype(np.uint8)
        
        # # get clean segmentation 
        # seg[seg>1] = 0 

        # resize segmentation to 512x512 
        # seg_e = np.expand_dims(seg,0)
        # seg_t = np.tile(seg_e,(3,1,1))
        # seg_uint = np.moveaxis(seg_t,0,-1).astype(np.uint8)    
        image = Image.fromarray(seg_uint*255)
        seg_r = image.resize((256,256))

        return seg_r 



if __name__ == '__main__':
    
    
    # if result is a numpy array -> resize to 256x256 
    seg_path = 'segmentation_cat.npy'
    image_path = 'image_cat.npy'
    image = load_data_image_v(image_path)
    seg = load_data_mask_v(seg_path)
    
    seg.save("test3s.png")
    image.save("test3i.png")
    
    seg = np.load(seg_path)
    image = np.load(image_path)
    tag = 1 








    # get object min max... 
    image.save("test2.png")
    seg_r.save("test.png")
    segn = np.array(seg_r)
    #nz = np.where(segn>254)
    nz = np.where(seg==1)
    rx = min(nz[0]), max(nz[0])
    ry = min(nz[1]), max(nz[1])
    #rz = min(nz[2]), max(nz[2])
    
    from IPython import embed; embed()
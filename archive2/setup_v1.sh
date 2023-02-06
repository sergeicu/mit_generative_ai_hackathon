



# convert stable diffusion to diffusers - https://github.com/huggingface/diffusers/blob/main/scripts/convert_original_stable_diffusion_to_diffusers.py
installed diffusers via pip and locally via (in vana/models)
git clone https://github.com/huggingface/diffusers.git 
# and here 
https://github.com/jsksxs360/bin2ckpt/blob/main/convert.py


# convert 
cd ~/w/code/sd/experiments/sd/vana/
python convert_diffusers_to_sd.py --model_path models/cat/ --checkpoint_path models/cat.ckpt

# link 
cd ~/w/code/sd/experiments/sd
ln -sf /lab-share/Rad-Warfield-e2/Groups/Imp-Recons/serge/code/sd/experiments/s20230126_vana/models/cat.ckpt cat.ckpt sd/models/ldm/stable-diffusion-v1/cat.ckpt
$ ln -sf /lab-share/Rad-Warfield-e2/Groups/Imp-Recons/serge/code/sd/experiments/s20230126_vana/models/nemo.ckpt sd/models/ldm/stable-diffusion-v1/nemo.ckpt

# use this tag
jianthisisdefinitelymeyes cat
jianthisisdefinitelymeyes person
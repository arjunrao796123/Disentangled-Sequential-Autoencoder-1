from disVAE import FullQDisentangledVAE
import torch
import torchvision
vae = FullQDisentangledVAE(frames=8, f_dim=64, z_dim=32, hidden_dim=512, conv_dim=1024)
device = torch.device('cuda:0')
vae.to(device)
checkpoint = torch.load('disentangled-vae.model')
vae.load_state_dict(checkpoint['state_dict'])
vae.eval()

for imageset in ('set1', 'set2', 'set3', 'set4', 'set5', 'set6'):
    print(imageset)
    path = './test/similarity-f/'+imageset+'/'
    image1 = torch.load(path + 'image1.sprite')
    image2 = torch.load(path + 'image2.sprite')
    image1 = image1.to(device)
    image2 = image2.to(device)
    image1 = torch.unsqueeze(image1,0)
    image2= torch.unsqueeze(image2,0)
    with torch.no_grad():
        conv1 = vae.encode_frames(image1)
        conv2 = vae.encode_frames(image2)

        _,_,image1_f = vae.encode_f(conv1)
        print(image1_f.shape)
        image1_f = image1_f.view(64)

        _,_,image2_f = vae.encode_f(conv2)
        image2_f = image2_f.view(64)
        similarity = image1_f.dot(image2_f) / (image1_f.norm(2) * image2_f.norm(2))
        print(similarity)
    




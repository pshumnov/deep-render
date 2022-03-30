# Applying deep learning algorithms to rendering and post-processing of 3D scenes

This project implements rendering of 3D indoor scenes using deep learning algorithms such as convolutional neural networks (CNN) and conditional generative adversarial networks (CGAN). The pix2pix model is used to generate the final frame render having a G-buffer as input.

<img src="https://user-images.githubusercontent.com/65417507/160793998-e25d12e0-4798-4f66-93e3-7c06b6d16d39.png" alt="result" width="500"/>

The program receives 3 images as input:
- depth buffer
- normals
- albedo

<img src="https://user-images.githubusercontent.com/65417507/160797728-0abc2235-c7db-46d6-90b3-4893a9504852.png" alt="app" width="900"/>


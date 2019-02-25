import matplotlib.pyplot as plt
import numpy as np

from skimage.transform import rescale, resize


def main():
    
    path_in = "/scratch/Downloads_local/641px-Sint-Baafskathedraal_(St._Bavo's_Cathedral)_Ghent_Belgium_October.jpg"
    path_in = "/home/lameeus/Pictures/elephant.jpg"
    im = plt.imread(path_in)/255
    
    scale = 1   # .2
    im = rescale(im, scale)
    
    h, w, _ = im.shape
    
    im_triangle = np.zeros(im.shape)
    
    h_tr = int(30*scale)
    degr60 = np.pi/3    # 60 degree
    degr30 = np.pi/6    # 30 degrees

    w_tr_half = h_tr/np.tan(degr60)
    
    # # horizontal, a and b: y = ax+delta_b
    # # every 10 pixels, there is a new line
    # line1 = [1, h_tr]
    # line2 = [np.tan(angle), 2*h_tr]
    # line3 = [-np.tan(angle), 2*h_tr]
    
    h_grid = np.ceil(h/h_tr).astype(int)
    w_grid = np.ceil(w/w_tr_half).astype(int) + 1 # always need one extra
    
    values = np.zeros((h_grid, w_grid, 3))
    nnn = np.zeros((h_grid, w_grid))
    
    # TODO paralize: calculate i_h, i_w for all at once

    def get_triangle_coord(h_i, w_i):
        
        # TODO for uneven start with up triangle, for even start with down triangle
        
        h_part = h_i % h_tr
        
        bool_even = ((h_i//h_tr) % 2) == 0
        
        # TODO do other side of triangles, now parallelograms
        
        # calc = (-np.tan(angle)*w_i - h_part)/(2*h_tr) + 1
        # i_w = int(np.floor( calc ))
        
        # i_w = (w%(2*w_tr_half))/h_part + 1  #-h_part
        
        # seems a bit off, but going in the right direction!
        calc_tl2br = (h_part * -np.sin(degr30) + w_i * np.cos(degr30))/h_tr + 1
        
        calc_bl2tr = (h_part* np.sin(degr30) + w_i * np.cos(degr30))/h_tr

        if bool_even:
            # shift everything
            calc_tl2br -= .5
            calc_bl2tr -= .5
        
        # i_w = int(np.floor(calc_tl2br))
        # i_w = int(np.floor(calc_bl2tr))
        i_w = int(np.floor(calc_tl2br)) + int(np.floor(calc_bl2tr))
        
        i_h = h_i // h_tr
        
        return i_h, i_w   # TODO
    
    for h_i in range(h):
        print('{} / {}'.format(h_i, h))
        for w_i in range(w):
            
            i_h, i_w = get_triangle_coord(h_i, w_i)
            
            # print(i_h, h_i, w_i)
            # print(h_grid, w_grid)
            
            values[i_h, i_w, :] += im[h_i, w_i, :]
            nnn[i_h, i_w] += 1
            
    for h_i in range(h):
        print('{} / {}'.format(h_i, h))
        for w_i in range(im.shape[1]):
            i_h, i_w = get_triangle_coord(h_i, w_i)
            
            im_triangle[h_i, w_i, :] = values[i_h, i_w, :]/nnn[i_h, i_w]

    plt.figure()
    plt.imshow(im_triangle)
    plt.show()

    im_alias = rescale(im_triangle, .5)
    im_alias = rescale(im_alias, 2)
    plt.figure()
    plt.imshow(im_alias)
    plt.show()
    
    plt.imsave("/scratch/Downloads_local/triangles",im_triangle, vmin=0, vmax=1)
    
    return 1


if __name__ == '__main__':
    main()

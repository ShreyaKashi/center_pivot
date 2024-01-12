import os
import cv2
import numpy as np
import pickle
import statistics
import matplotlib.pyplot as plt 

dir_path = "/home/kashis/Desktop/misc/Capstone/GIS-AI project/Pivot GIS Project/images"

for file in os.listdir(dir_path):
    if file.endswith('.png'):
        img = cv2.imread(os.path.join(dir_path, file))
        # plt.imshow(img)
        # plt.show()
        pink_color = [191, 30, 219]
        Y, X = np.where(np.all(img==pink_color, axis=2))

        print(X,Y)
        assert len(X) and len(Y)


        pkl_file = open(os.path.join(dir_path, file.split('.png')[0] + '.pkl'), 'rb')
        pkl_file_path = os.path.join(dir_path, file.split('.png')[0] + '.pkl')
        old_data = pickle.load(pkl_file)
        old_data['center_x'] = statistics.median(X)
        old_data['center_y'] = statistics.median(Y)

        with open(pkl_file_path, 'wb') as fp:
            pickle.dump(old_data, fp)

    # if file.endswith('.pkl'):
    #     pkl_file = open(os.path.join(dir_path, file), 'rb')
    #     old_data = pickle.load(pkl_file)
    #     print()

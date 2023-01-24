#%%
# CVAT file analysis
import numpy as np
from matplotlib import image
import os
import matplotlib.pyplot as plt
from pycocotools.coco import COCO
import skimage.io as io
import statistics

Dict = {'T1': '06_08_22', 'T2': '06_23_22', 'T3': '07_08_22', 'T4': '07_15_22', \
            'T5': '07_30_22', 'T6': '08_03_22', 'T7': '08_31_22'}

def json_enumerator(idx_file, idx_type):

    Json_files = 'C:/Users/Students/Box/Research/IoT4ag/Project_ Water Stress' \
        +'/Data Collection/Almond/Multispectral/Json_files/'

    Img_files = 'C:/Users/Students/Box/Research/IoT4ag/Project_ Water Stress' \
    + '/Data Collection/Almond/Multispectral/'

    index_all = list([])

    for i in range(len(Dict)):
        Index_all_date = index_capture(idx_file, idx_type, Img_files, Json_files, list(Dict.keys())[i])
        index_all.append(Index_all_date)

    return index_all

def index_capture(idx_file, idx_type, Img_files, Json_files, Tx):

    Json_path = Json_files + Tx + '.json'
    image_path = Img_files + Dict[Tx] + '/index_map' + idx_file

    coco = COCO(Json_path)
    img_ids = coco.getImgIds()
    annotation_ids = coco.getAnnIds(img_ids)
    annotations = coco.loadAnns(annotation_ids) 
    print("{} is being extracted for trees in {}...".format(idx_type, Tx))
    
    index_all_date = list([])
    for i in range(len(annotations)):
        # image_id = coco.loadImgs(annotations[i]["id"])[0]
        # im_id = image_id["id"]
        im_id = annotations[i]["id"]
        entity_id = annotations[i]["category_id"]
        entity = coco.loadCats(entity_id)[0]["name"]
        print("idx={}: image {}: {}".format(i, im_id ,entity))


        # print(image_path)
        # image_meta = coco.loadImgs(annotations[i]["image_id"])[0]   
        # image_path = os.path.join(TRAIN_IMAGES_DIRECTORY, image_meta["file_name"])

        masks = coco.annToMask(annotations[i])
        segmentation = np.where(masks == True)
        print(len(segmentation[0]))

        I = io.imread(image_path)
        index_array = I[(segmentation[0],segmentation[1])]

        arr = np.array(index_array)
        mean_val = statistics.mean(arr)
        median_val = statistics.median(arr)
        stdev = statistics.stdev(arr)

        temp_dict = {'idx': i, 'image_id': im_id, 'pixels_numbers': len(segmentation[0]) ,\
            'spec_idx': idx_type,'test_number': entity, 'pixel_array': index_array, 'mean':mean_val,\
                'median':median_val, 'stdev': stdev}
        index_all_date.append([temp_dict])

        # print(Index_a)
        # return Index_array
    return index_all_date

#### Calling Functions
NDVI = json_enumerator('/NDVI.tif', 'NDVI')
GNDVI = json_enumerator('/GNDVI.tif', 'GNDVI')
OSAVI = json_enumerator('/OSAVI.tif', 'OSAVI')
LCI = json_enumerator('/LCI.tif', 'LCI')
NDRE = json_enumerator('/NDRE.tif', 'NDRE')

#%%
#### SAVE data
import pandas as pd
idxes = NDVI, GNDVI, OSAVI, LCI, NDRE

tmp0 = []
tmp1 = []
tmp2 = []
tmp3 = []
tmp4 = []
tmp5 = []
tmp6 = []
for x in range(len(idxes)):
    for i in range(len(idxes[x])):
        for j in range(len(idxes[x][i])):
            spec = idxes[x][i][j][0]['spec_idx']    # captures the type of spectral index
            id = idxes[x][i][j][0]['image_id']      # captures the Image number
            Tnum = idxes[x][i][j][0]['test_number'] # captures the Test Number
            data = idxes[x][i][j][0]['pixel_array'] # captures the pixel arrays
            mean_val = idxes[x][i][j][0]['mean']
            median_val =idxes[x][i][j][0]['median']
            stdev_val = idxes[x][i][j][0]['stdev']

            tmp0.append(spec)
            tmp1.append(id)
            tmp2.append(Tnum)
            tmp3.append(data)
            tmp4.append(mean_val)
            tmp5.append(median_val)
            tmp6.append(stdev_val)

df = pd.DataFrame({'spec_idx':tmp0, 'image_id': tmp1, 'test_number': tmp2, 'pixel_array':tmp3,\
    'mean':tmp4, 'median':tmp5, 'stdev':tmp6})
df.to_json('pistachio_im_indexes.json')




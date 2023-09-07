import json
import os
import glob
TRAIN_PATH = "data/coco/train_txts.txt"
TEST_PATH = "data/coco/valid_txts.txt"
root = "data/coco"

"""
├── data
        │   ├── my_dataset
        │   │   ├── img_dir
        │   │   │   ├── train
        │   │   │   │   ├── xxx{img_suffix}
        │   │   │   │   ├── yyy{img_suffix}
        │   │   │   │   ├── zzz{img_suffix}
        │   │   │   ├── val
        │   │   ├── ann_dir
        │   │   │   ├── train
        │   │   │   │   ├── xxx{seg_map_suffix}
        │   │   │   │   ├── yyy{seg_map_suffix}
        │   │   │   │   ├── zzz{seg_map_suffix}
        │   │   │   ├── val
"""


#the following functions work in the case of dataset structured as follow:
"""
├── data
        │   ├── my_dataset
        │   │   ├── train
        │   │   │   ├── images
        │   │   │   ├── labels
        │   │   ├── valid
        │   │   │   ├── images
        │   │   │   ├── labels
"""

def create_COCO_annotation_file(data_path, output_path):
    """
    Args:
    data_path: path to a text file containing images paths along with their labels paths
    in the form: "img_path lbl_path" in every line
    output_path: the path where to save the json file in COCO format
    """
    images = []
    anns = []
    
    with open(data_path, 'r') as f:
        data = f.read().splitlines()
    dataset = []
    counter = 0
    for idx, example in enumerate(data):
        image_path, annotations_path = example.split()

        with open(annotations_path, 'r') as f:
            annotations = f.read().splitlines()
            
        for ann in annotations:
            cls, x, y, w, h = ann.split()
            x = float(x)
            y = float(y)
            w = float(w)
            h = float(h)
            cls = int(cls)
            anns.append({
                'image_id': idx,
                'iscrowd': 0,
                'area': w*h,
                'category_id': cls,
                'bbox': [x,y,w,h],
                'id': counter
            })

            counter += 1

        images.append({
            'file_name': image_path.split("images/")[-1],
            'width': 640,
            'height': 640,
            'id': idx
        })
        
    dataset = {
        'images': images,
        'annotations': anns,
        'categories': [
            {'id': 0, 'name': 'oil'},
		
        ]
    }
    with open(output_path, 'w') as f:
        json.dump(dataset, f)

def create_COCO_annotations(root_of_txt_files,out_dir='', train_folder="train", valid_folder = "valid"):
    if out_dir=='':
        out_dir = root_of_txt_files
    train_path = os.path.join(root_of_txt_files,f"{str(train_folder)}.txt")
    valid_path = os.path.join(root_of_txt_files,f"{str(valid_folder)}.txt")
    train_json = os.path.join(out_dir,f"{str(train_folder)}.json")
    valid_json = os.path.join(out_dir,f"{str(valid_folder)}.json")
    create_COCO_annotation_file(train_path,train_json)
    create_COCO_annotation_file(valid_path,valid_json)

def create_data_path_text_file(path, out_dir, folder):
    output_txt = os.path.join(out_dir,f"{str(folder)}.txt")
    train_imgs = sorted(glob.glob(path+"/images/*"))
    train_labels = sorted(glob.glob(path + "/labels/*"))
    print(train_imgs[0])
    print(train_labels[0])
    with open(output_txt, 'w') as f:
        for i in range(len(train_imgs)):
            if i !=0:
                f.write("\n")
            f.write(train_imgs[i]+" "+ train_labels[i])
def create_data_path_text(root, out_dir, train_folder="train", valid_folder = "valid"):
    train_path = os.path.join(root, train_folder)
    valid_path = os.path.join(root, valid_folder)
    create_data_path_text_file(train_path, out_dir, train_folder)
    create_data_path_text_file(valid_path, out_dir, valid_folder)

def renumber_img_lbl(root=''):
    """
    Sorts images and labels and renames them
    """
    #get directories of images of labels
    tr_img = os.path.join(root, "train/images")
    tr_lbl = os.path.join(root, "train/labels")
    v_img = os.path.join(root, "valid/images")
    v_lbl = os.path.join(root, "valid/labels")
    #get paths of images and labels
    ls_tr_img = sorted(glob.glob(tr_img+"/*.jpg"))
    ls_tr_lbl = sorted(glob.glob(tr_lbl+"/*.txt"))
    ls_v_img = sorted(glob.glob(v_img+"/*.jpg"))
    ls_v_lbl = sorted(glob.glob(v_lbl+"/*.txt"))
    def _rename(ls, folder, extension):
        for i,im in enumerate(ls):
            os.rename(im, folder+f"/{i}"+extension)
    _rename(ls_tr_img, tr_img , '.jpg')
    _rename(ls_tr_lbl,tr_lbl, '.txt')
    _rename(ls_v_img, v_img, '.jpg')
    _rename(ls_v_lbl, v_lbl, '.txt')

def main():
    root = "data/coco"
    # renumber_img_lbl(root)
    
    create_data_path_text(root,root, train_folder="train", valid_folder = "valid")
    create_COCO_annotations(root,root, train_folder="train", valid_folder = "valid")

if __name__=="__main__":
    main()
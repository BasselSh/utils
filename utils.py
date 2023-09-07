from typing import List, Dict
import numpy as np

def xywh2xyxy(bbox:np.ndarray) -> np.ndarray:
    x,y,w,h = bbox
    x1,x2 = int(x-w/2), int(x+w/2)
    y1,y2 = int(y-h/2), int(y+h/2)
    return np.array([x1,y1,x2,y2])



# 实验编号

## 消融实验

消融实验数据根目录为:`./experimentData/val`

| 模型                  | 编号 | 
| ------------------- | --------- | 
| YOLOv8n(base)         | val    |   
| base + SIoU | val2    | 
| base + EMA | val3    | 
| base + GN | val4    | 
| base + SIoU + EMA | val5    | 
| base + SIoU + GN | val6    | 
| base + GN + EMA | val7    | 
| 完全改良模型 | val8    | 


## 对比实验

对比实验数据根目录为:`./experimentData/val`

| 模型 | Crack-seg数据集编号 | Roboflow-Crack数据集编号 |
|------|---------------------|--------------------------|
| YOLOv8n(base) | val | val19 |
| 完全改良模型 | val8 | val20 |
| YOLOv5nu | val9 | val21 |
| YOLOv8S | val10 | val22 |
| YOLOv8m | val11 | val23 |
| YOLOv8l | val12 | val24 |
| YOLOv8x | val13 | val25 |
| YOLO11n | val14 | val26 |
| YOLO26n | val15 | val27 |
| YOLO26s | val16 | val28 |
| YOLO26m | val17 | val29 |
| RT-DETR-L | val18 | val30 |

## 原始训练数据

原始训练数据根目录为:`./experimentData/oriData`

| 模型 | 训练数据编号 |
|------|:-------------------:|
| YOLOv8n(base) | train |
| base + SIoU | train2 |
| base + EMA | train3 |
| base + GN | train4 |
| base + SIoU + EMA | train5 |
| base + SIoU + GN | train6 |
| base + GN + EMA | train7 |
| 完全改良模型 | train8 |
| YOLOv5nu | train9 |
| YOLOv8S | train10 |
| YOLOv8m | train11 |
| YOLOv8l | train12 |
| YOLOv8x | train13 |
| YOLO11n | train14 |
| YOLO26n | train15 |
| YOLO26s | train16 |
| YOLO26m | train17 |
| RT-DETR-L | train18 |
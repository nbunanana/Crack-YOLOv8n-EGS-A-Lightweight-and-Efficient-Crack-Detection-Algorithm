# Crack-YOLOv8n-EGS: A Lightweight and Efficient Crack Detection Algorithm

> Based on YOLOv8, the EMA attention mechanism, Group Normalization, and SIoU loss function are introduced to achieve efficient detection of cracks on building surfaces.

## Table of Contents

- [Introduction](#introduction)
- [Environment Configuration](#environment-configuration)
- [Dataset](#dataset)
- [Model Structure](#model-structure)
- [Installation](#installation)
- [Training](#training)
- [Evaluation](#evaluation)
- [Inference](#inference)
- [Experimental Results](#experimental-results)
- [Citation](#citation)
- [Acknowledgements](#acknowledgements)
- [License](#license)


## Introduction

Aiming at the problems of insufficient bounding box regression accuracy of YOLOv8n in crack detection, instability in small-batch training, and inadequate feature extraction for slender targets, an improved algorithm is proposed: an EMA attention module is embedded in the P3 path of the Neck network to enhance multi-scale features; GN replaces BN to eliminate statistical jitter; the SIoU loss function is adopted to introduce angle cost to optimize the localization of slender cracks. Experiments on the Crack-Seg dataset show that the three modules have complementary effects. The model's mAP\@0.5 reaches 73.24%, and mAP\@0.5:0.95 reaches 51.45%, which are 8.58 and 8.46 percentage points higher than the baseline respectively. On the Roboflow-Crack dataset, mAP50 reaches 60.58%, and mAP50-95 reaches 25.91%, which are 9.23 and 7.56 percentage points higher than the baseline respectively. The number of parameters increases by only 0.0024M, and the average inference speed reaches 220 FPS, achieving a balance between detection accuracy and complexity.


## Environment Configuration

| Item     | Version/Configuration                |
| -------- | ------------------------------------ |
| OS       | Windows 11                           |
| Python   | 3.11                                 |
| PyTorch  | 2.11.0 + CUDA 12.8                   |
| GPU      | NVIDIA GeForce RTX 5060 Laptop 8GB   |
| Dependencies | See [requirements.txt](requirements.txt) |


## Dataset
### 1. Crack-seg Dataset

- Data source: officially collected by Ultralytics[^1]
- Number of classes: 1 (crack)
- Train/val/test split: 7:1:2

  Directory structure:

  ```
  datasets/crack-seg/
  ├── images/
  │   ├── train/
  │   ├── val/
  │   └── test/
  └── labels/
  │   ├── train/
  │   ├── val/
  │   └── test/
  └── crack-seg.yaml
  ```


### 2. Roboflow-Crack Dataset

- Dataset name: robotflow_crack
- Data source: open-source dataset from the Roboflow platform[^2]
- Number of classes: 1 (crack)
- Train/val/test split: 0:0:1

  Directory structure:

  ```
  datasets/robotflow_crack/
  ├── images/
  │   └── test/
  └── labels/
  │   └── test/
  └── robotflow_crack.yaml
  ```


## Model Structure

- Base model: YOLOv8n
- Improvements:
  - Introduce EMA attention mechanism (code location: `ultralytics-main/ultralytics/nn/modules/attention.py`)[^3]
  - Introduce SIoU loss function (code location: `ultralytics-main/ultralytics/utils/metrics.py#L170`)[^4]
  - Introduce Group Normalization (code location: `ultralytics-main/ultralytics/nn/modules/conv.py#L93-L111`)[^5]
  - Model configuration file: `ultralytics-main/ultralytics/cfg/models/v8/yolov8-ema-crack.yaml`

Model structure diagram:

![Improved Model Architecture](./png/改进模型架构图.png)


## Installation

```bash
# 1. Clone the repository
git@github.com:nbunanana/Research-on-Crack-Detection-Algorithm-Based-on-Improved-YOLOv8.git

# 2. Create conda environment
conda create -n conda_env python=3.11
conda activate conda_env

# 3. Install dependencies
pip install -r requirements.txt
```


## Training

```bash
yolo detect train \
  data=crack-seg.yaml \
  model=ultralytics/cfg/models/v8/yolov8-ema-crack.yaml \
  pretrained=yolov8n.pt \
  epochs=300 \
  imgsz=640 \
  batch=16 \
  device=0
```

- Training results are saved in `runs/detect/train-X/`
- Final weights: `runs/detect/train-X/weights/best.pt`


## Evaluation

```bash
# Method 1: YOLO command line
yolo detect val model=runs/detect/train-X/weights/best.pt data=crack-seg.yaml split=test imgsz=640

# Method 2: Use the evaluation script provided by the project (outputs metrics + FPS)
python ./test/getresult.py --model train-X --data crack-seg.yaml --split test
```


## Inference

```bash
# Inference on a single image
yolo predict model=runs/detect/train-X/weights/best.pt source="image_path.jpg" conf=0.25

# Inference on an entire folder
yolo predict model=runs/detect/train-X/weights/best.pt source="image_folder_path/" conf=0.25
```

Results are saved in `runs/detect/predict-X`.


## Experimental Results

The experimental results are located in `./experimentData/`. For specific numbering, see [experimentData/README.md](./experimentData/README.md).


## Citation

If you use this project in your research, please cite:

```bibtex
[To be filled: BibTeX entry for this paper/project]
```

Please also cite the original Ultralytics project:

```bibtex
@article{yolo26,
  title={Ultralytics YOLO26: Unified Real-Time End-to-End Vision Models},
  author={Jocher, Glenn and Qiu, Jing and Liu, Mengyu and Lyu, Shuai and Akyon, Fatih Cagatay and Kalfaoglu, Muhammet Esat},
  year={2026},
  doi={10.48550/arXiv.2606.03748},
  url={https://arxiv.org/abs/2606.03748}
}
```


## Acknowledgements

- Thanks to [HuOldBig](https://github.com/HuOldBig) for technical guidance
- Thanks to [Ultralytics](https://github.com/ultralytics/ultralytics) for the YOLOv8 open-source framework and dataset
- Thanks to [Roboflow](https://universe.roboflow.com) for the dataset search service


## License

Copyright (c) 2026 YuChunDing, Anhui Jianzhu University

This project is a secondary development based on Ultralytics, licensed under [AGPL-3.0](LICENSE).


## References

[^1]: Ultralytics. Crack-Seg: A crack segmentation dataset for computer vision\[DB/OL]. (2023)\[2026-06-28].<https://github.com/ultralytics/assets/releases/download/v0.0.0/crack-seg.zip>.

[^2]: Roboflow. Crack v2: A crack detection dataset for computer vision\[DB/OL]. (2026-07-05)\[2026-07-12].<https://universe.roboflow.com/s-workspace-bb4fj/crack-detection-ypnwo-bn3zg>.

[^3]: OUYANG D L, HE S, ZHANG G Z, et al. Efficient multi-scale attention module with cross-spatial learning[C]//ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2023: 1-5. DOI: 10.1109/ICASSP49357.2023.10096516.

[^4]: GEVORGYAN Z. SIoU loss: More powerful learning for bounding box regression[J]. arXiv preprint arXiv:2205.12740, 2022.

[^5]: WU Y X, HE K M. Group normalization[C]//Proceedings of the European Conference on Computer Vision (ECCV). Munich: Springer, 2018: 3-19. DOI: 10.1007/978-3-030-01261-8_1.

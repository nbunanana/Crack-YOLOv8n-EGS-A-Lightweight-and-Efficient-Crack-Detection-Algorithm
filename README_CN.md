# Crack-YOLOv8n-EGS：一种轻量高效的裂缝检测算法

> 在YOLOv8基础上引入EMA注意力机制、Group Normalization、SIoU损失函数,实现建筑物表面裂缝的高效检测。

## 目录

- [项目简介](#项目简介)
- [环境配置](#环境配置)
- [数据集](#数据集)
- [模型结构](#模型结构)
- [安装](#安装)
- [训练](#训练)
- [评估](#评估)
- [推理](#推理)
- [实验结果](#实验结果)
- [引用](#引用)
- [致谢](#致谢)
- [开源协议](#开源协议)


## 项目简介

针对裂缝检测中YOLOv8n框回归精度不足、小批量训练不稳定及细长目标特征提取不充分等问题，提出一种改进算法：在Neck网络P3路径嵌入EMA注意力模块增强多尺度特征；以GN替代BN消除统计抖动；采用SIoU损失函数引入角度成本优化细长裂缝定位。Crack-Seg数据集上的实验表明，三个模块具有互补效应，模型 mAP\@0.5 达 73.24%，mAP\@0.5:0.95 达 51.45%，较基线提升 8.58 和 8.46 个百分点。在 Roboflow-Crack 数据集上 mAP50 达到 60.58%，mAP50−95 达到 25.91%，较基线提升 9.23 和 7.56 个百分点。参数量仅增加 0.0024M，推理速度平均达到 220 帧/s，实现了检测精度与复杂度的平衡。


## 环境配置

| 项目      | 版本/配置                              |
| ------- | ---------------------------------- |
| 操作系统    | Windows 11                         |
| Python  | 3.11                               |
| PyTorch | 2.11.0 + CUDA 12.8                 |
| GPU     | NVIDIA GeForce RTX 5060 Laptop 8GB |
| 依赖      | 见 [requirements.txt](requirements.txt)               |


## 数据集
### 1.Crack-seg数据集

- 数据来源:ultralytics官方采集[^1]
- 类别数:1(裂缝)
- 训练/验证/测试划分:7:1:2

  目录结构:

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


### 1.robotflow_crack数据集

- 数据集名称:robotflow_crack
- 数据来源:robotflow平台开源数据集[^2]
- 类别数:1(裂缝)
- 训练/验证/测试划分:0:0:1

  目录结构:

  ```
  datasets/robotflow_crack/
  ├── images/
  │   └── test/
  └── labels/
  │   └── test/
  └── robotflow_crack.yaml
  ```


## 模型结构

- 基础模型:YOLOv8n
- 改进点:
  - 引入EMA注意力机制(代码位置:`ultralytics-main/ultralytics/nn/modules/attention.py`)[^3]
  - 引入SIoU损失函数(代码位置:`ultralytics-main/ultralytics/utils/metrics.py#L170`)[^4]
  - 引入Group Normalization(代码位置:`ultralytics-main/ultralytics/nn/modules/conv.py#L93-L111`)[^5]
  - 模型配置文件:`ultralytics-main/ultralytics/cfg/models/v8/yolov8-ema-crack.yaml`

模型结构图:

![改进模型架构图](./png/改进模型架构图.png)


## 安装

```bash
# 1. 克隆仓库
git@github.com:nbunanana/Research-on-Crack-Detection-Algorithm-Based-on-Improved-YOLOv8.git

# 2. 创建 conda 环境
conda create -n conda_env python=3.11
conda activate conda_env

# 3. 安装依赖
pip install -r requirements.txt
```


## 训练

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

- 训练结果保存在 `runs/detect/train-X/`
- 最终权重:`runs/detect/train-X/weights/best.pt`


## 评估

```bash
# 方式一:YOLO 命令行
yolo detect val model=runs/detect/train-X/weights/best.pt data=crack-seg.yaml split=test imgsz=640

# 方式二:使用项目提供的评估脚本(输出指标 + FPS)
python ./test/getresult.py --model train-X --data crack-seg.yaml --split test
```


## 推理

```bash
# 推理单张图片
yolo predict model=runs/detect/train-X/weights/best.pt source="图片路径.jpg" conf=0.25

# 推理整个文件夹
yolo predict model=runs/detect/train-X/weights/best.pt source="图片文件夹路径/" conf=0.25
```

结果保存在 `runs/detect/predict-X`。


## 实验结果

实验结果位于`./experimentData/`中,具体编号见[README.md](./experimentData/README.md)


## 引用

如果在研究中使用了本项目,请引用:

```bibtex
[待填写:本论文/项目的 BibTeX 条目]
```

同时请引用 Ultralytics 原项目:

```bibtex
@article{yolo26,
  title={Ultralytics YOLO26: Unified Real-Time End-to-End Vision Models},
  author={Jocher, Glenn and Qiu, Jing and Liu, Mengyu and Lyu, Shuai and Akyon, Fatih Cagatay and Kalfaoglu, Muhammet Esat},
  year={2026},
  doi={10.48550/arXiv.2606.03748},
  url={https://arxiv.org/abs/2606.03748}
}
```


## 致谢

- 感谢 [HuOldBig](https://github.com/HuOldBig) 提供的技术指导
- 感谢 [Ultralytics](https://github.com/ultralytics/ultralytics) 提供的 YOLOv8 开源框架以及数据集
- 感谢 [Robotflow](https://universe.roboflow.com) 提供的数据集搜索服务


## 开源协议

Copyright (c) 2026 YuChunDing, Anhui Jianzhu University

本项目基于 Ultralytics 二次开发,遵循 [AGPL-3.0](LICENSE) 协议


## 参考文献

[^1]: Ultralytics. Crack-Seg: A crack segmentation dataset for computer vision\[DB/OL]. (2023)\[2026-06-28].<https://github.com/ultralytics/assets/releases/download/v0.0.0/crack-seg.zip>.

[^2]: Roboflow. Crack v2: A crack detection dataset for computer vision\[DB/OL]. (2026-07-05)\[2026-07-12].<https://universe.roboflow.com/s-workspace-bb4fj/crack-detection-ypnwo-bn3zg>.

[^3]: OUYANG D L, HE S, ZHANG G Z, et al. Efficient multi-scale attention module with cross-spatial learning[C]//ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2023: 1-5. DOI: 10.1109/ICASSP49357.2023.10096516.

[^4]: GEVORGYAN Z. SIoU loss: More powerful learning for bounding box regression[J]. arXiv preprint arXiv:2205.12740, 2022.

[^5]: WU Y X, HE K M. Group normalization[C]//Proceedings of the European Conference on Computer Vision (ECCV). Munich: Springer, 2018: 3-19. DOI: 10.1007/978-3-030-01261-8_1.


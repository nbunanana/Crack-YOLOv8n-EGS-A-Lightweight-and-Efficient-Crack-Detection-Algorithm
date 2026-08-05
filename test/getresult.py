from ultralytics import YOLO
import argparse
from pathlib import Path
from datetime import datetime


def save_result(metrics, fps, val_dir,train_num, model_name, data_name, split_name, params, flops):
    """保存评估指标到 YOLO 自动创建的 val 目录下"""
    save_path = Path(val_dir) / f"results.yaml"
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"train_num：{train_num}\n")
        f.write(f"Model: {model_name}\n")
        f.write(f"Dataset: {data_name}\n")
        f.write(f"Split: {split_name}\n")
        f.write(f"Precision: {metrics.box.mp:.4f}\n")
        f.write(f"Recall: {metrics.box.mr:.4f}\n")
        f.write(f"mAP50: {metrics.box.map50:.4f}\n")
        f.write(f"mAP50-95: {metrics.box.map:.4f}\n")
        f.write(f"Params(M): {params / 1e6:.4f}\n")
        f.write(f"FLOPs(G): {flops:.1f}\n")
        f.write(f"FPS: {fps:.2f} 帧/s\n")
    print(f"指标已保存到: {save_path}")


def get_val_save_dir(args_name="val"):
    """获取最新的 val/val-X 目录"""
    base_dir = Path("runs/detect")
    base_dir.mkdir(parents=True, exist_ok=True)

    existing = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith(args_name)]
    if not existing:
        return base_dir / args_name

    existing.sort(key=lambda x: x.name)
    return existing[-1]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='模型评估')
    parser.add_argument('--model', type=str, default='train-35', help='训练目录名称，如 train-9')
    parser.add_argument('--data', type=str, default='robotflow_crack2.yaml', help='数据集名称')
    parser.add_argument('--split', type=str, default='test', help='评估集名称，默认 test')
    parser.add_argument('--imgsz', type=int, default=640, help='输入图像尺寸，默认 640')
    args = parser.parse_args()

    train_dir = f'../ultralytics-main/runs/detect/{args.model}'
    model_path = f'{train_dir}/weights/best.pt'

    model = YOLO(model_path)

    # 记录运行 val 前的 val 目录列表
    base_dir = Path("../ultralytics-main/runs/detect")
    before_val = set(base_dir.glob("val*")) if base_dir.exists() else set()

    metrics = model.val(data=args.data, imgsz=args.imgsz, split=args.split)

    # 找出运行 val 后新增的 val 目录
    after_val = set(base_dir.glob("val*"))
    new_val_dirs = after_val - before_val

    if new_val_dirs:
        val_dir = sorted(new_val_dirs, key=lambda x: x.name)[-1]
    else:
        val_dir = get_val_save_dir("val")

    print(f"YOLO 验证结果目录: {val_dir}")
    print("=" * 60)

    # 获取模型信息（verbose=True 才会返回元组，verbose=False 返回 None）
    info = model.info(verbose=True)
    params, flops = info[1], info[3]  # (layers, params, gradients, flops)
    yaml_file = getattr(model.model, "yaml_file", "") or model.model.yaml.get("yaml_file", "")
    model_name = Path(yaml_file).stem if yaml_file else args.model

    print(f"Precision: {metrics.box.mp:.4f}")
    print(f"Recall: {metrics.box.mr:.4f}")
    print(f"mAP50: {metrics.box.map50:.4f}")
    print(f"mAP50-95: {metrics.box.map:.4f}")
    print(f"Params(M): {params / 1e6:.4f}")
    print(f"FLOPs(G): {flops:.1f}")
    print("=" * 60)

    # 计算 FPS
    preprocess = metrics.speed['preprocess']
    inference = metrics.speed['inference']
    postprocess = metrics.speed['postprocess']
    total_ms = preprocess + inference + postprocess
    fps = 1000 / total_ms

    print(f"推理速度统计:")
    print(f"  预处理:   {preprocess:.1f} ms")
    print(f"  模型推理: {inference:.1f} ms")
    print(f"  后处理:   {postprocess:.1f} ms")
    print(f"  端到端:   {total_ms:.1f} ms")
    print(f"  FPS:      {fps:.2f} 帧/s")
    print("=" * 60)

    save_result(metrics, fps, val_dir, args.model, model_name, args.data, args.split, params, flops)

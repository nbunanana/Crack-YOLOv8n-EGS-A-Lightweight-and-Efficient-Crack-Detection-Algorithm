from ultralytics import YOLO
import time

if __name__ == '__main__':
    # 加载模型
    model = YOLO('./ultralytics-main/runs/detect/train-44/weights/best.pt')

    # 验证并获取指标
    results = model.val(data='DeepCrack.yaml', imgsz=640, device=0)

    # 从 results 中提取速度（单位：毫秒）
    preprocess = results.speed['preprocess']      # 1.2
    inference = results.speed['inference']          # 2.6
    postprocess = results.speed['postprocess']     # 0.8

    # 计算 FPS
    total_ms = preprocess + inference + postprocess
    fps = 1000 / total_ms

    print("=" * 40)
    print(f"推理速度统计:")
    print(f"  预处理:   {preprocess:.1f} ms")
    print(f"  模型推理: {inference:.1f} ms")
    print(f"  后处理:   {postprocess:.1f} ms")
    print(f"  端到端:   {total_ms:.1f} ms")
    print(f"  FPS:      {fps:.2f} 帧/s")
    print("=" * 40)
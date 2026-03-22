from ultralytics import YOLO
import torch
import os
import multiprocessing


def main():

    print("CUDA Available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("GPU:", torch.cuda.get_device_name(0))
    else:
        raise RuntimeError("❌ GPU not detected! Install CUDA PyTorch first.")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    data_path = os.path.join(BASE_DIR, "dataset_circuit", "data2.yaml")
    test_image = os.path.join(BASE_DIR, "dataset_circuit", "images", "val", "EM-02_MAIN SWITCHBOARD_page_68.png")

    print("📂 Dataset:", data_path)
    print("🖼️ Test Image:", test_image)


    model = YOLO("yolov8l.pt")

    model.train(
        data=data_path,
        epochs=150,
        imgsz=1024,
        batch=32,
        device=0,

        workers=4,

        amp=True,
        cache=True,

        optimizer="AdamW",
        lr0=0.003,

        degrees=3,
        translate=0.05,
        scale=0.3,
        shear=0.0,
        fliplr=0.3,
        flipud=0.0,
        mosaic=0.5,

        project="runs/detect",
        name="circuit_model",

        pretrained=True,
        verbose=True
    )


    metrics = model.val()
    print("\n📊 Evaluation Results:")
    print(metrics)

    best_model_path = os.path.join(
        BASE_DIR,
        "runs",
        "detect",
        "circuit_model",
        "weights",
        "best.pt"
    )

    model = YOLO(best_model_path)


    results = model(
        test_image,
        imgsz=1024,
        conf=0.25,
        save=True
    )

    print("✅ Training + Testing Completed!")



if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
from imageai.Detection.Custom import DetectionModelTrainer
mylist = ["aeroplane", "apple", "backpack", "banana", "baseball bat", "baseball glove", "bear", "bed", "bench", "bicycle", "bird", "boat", "book", "bottle", "bowl", "broccoli", "bus", "cake", "car", "carrot", "cat", "cell phone", "chair", "clock", "cow", "cup", "diningtable", "dog", "donut", "elephant", "fire hydrant", "fork", "frisbee", "giraffe", "hair drier", "handbag", "horse", "hot dog", "keyboard", "kite", "knife", "laptop",
          "microwave", "motorbike", "mouse", "orange", "oven", "parking meter", "person", "pizza", "pottedplant", "refrigerator", "remote", "sandwich", "scissors", "sheep", "sink", "skateboard", "skis", "snowboard", "sofa", "spoon", "sports ball", "stop sign", "suitcase", "surfboard", "teddy bear", "tennis racket", "tie", "toaster", "toilet", "toothbrush", "traffic light", "train", "truck", "tvmonitor", "umbrella", "vase", "wine glass", "zebra"]
trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory="E:\Moodboard\datasets")
trainer.setTrainConfig(object_names_array=mylist, batch_size=4,
                       num_experiments=200, train_from_pretrained_model="yolov3.pt")
trainer.trainModel()
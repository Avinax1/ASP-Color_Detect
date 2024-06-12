from inference import get_model

model = get_model(model_id="yolov8n-640")

results = model.infer("https://media.roboflow.com/inference/people-walking.jpg")
import numpy as np
import supervision as sv
import pygame


def callback(frame: np.ndarray, _: int, model, tracker, box_annotator, label_annotator, trace_annotator, names, sound_files, animal_log) -> np.ndarray:
    pygame.mixer.init()
    results = model.infer(frame)[0]
    detections = sv.Detections.from_inference(results)
    detections = tracker.update_with_detections(detections)

    labels = [
        f"#{tracker_id} {names[class_id]}"
        for class_id, tracker_id
        in zip(detections.class_id, detections.tracker_id)
    ]
    if len(detections.confidence) > 0 and detections.confidence[0] > 0.8:
        if(len(detections.class_id)>0 and detections.class_id[0] == 0 or 1):
            class_id = detections.class_id[0]
            print(class_id);
            annotated_frame = box_annotator.annotate(frame.copy(), detections=detections)
            annotated_frame = label_annotator.annotate(annotated_frame, detections=detections, labels=labels)
            return trace_annotator.annotate(annotated_frame, detections=detections), class_id
    else:
        return frame, None




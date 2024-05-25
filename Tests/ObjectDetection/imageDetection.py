# Instalar detecto dentro del programa a través del comando pip3 install detecto

import cv2
from detecto import core, visualize

cap = cv2.VideoCapture(0)

ret, frame = cap.read()

cap.release()

frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Poner todos los archivos png y xml en una sola carpeta
dataset = core.Dataset("/Users/myriamfm/Downloads/imagesDetecto")

# Entrenamiento del modelo
dataset = core.Dataset("/Users/myriamfm/Downloads/imagesDetecto")
model = core.Model.load("/Users/myriamfm/Downloads/imagesDetecto/pruebasSLB.pth", ['stomach', 'liver', 'brain'])

# Especificar el path o el directorio de la imagen a probar
predictions = model.predict(frame_rgb)

# Formato de predicciones: (labels, boxes, scores)
labels, boxes, scores = predictions

print(labels)
print(boxes)
print(scores)

visualize.show_labeled_image(frame_rgb, boxes, labels)

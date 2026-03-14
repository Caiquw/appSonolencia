from datetime import datetime
import database
import cv2
import mediapipe as mp
import numpy as np
import time
import threading
from playsound import playsound
from report import gerar_relatorio_html
from email_sender import enviar_relatorio


funcionario_atual = "João Silva"  
evento_inicio = None
ear_acumulado = []



mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,          
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Índices dos pontos dos olhos (MediaPipe)
# Olho direito (íris direita): 33, 246, 161, 160, 159, 158, 157, 173
# Olho esquerdo (íris esquerda): 263, 466, 388, 387, 386, 385, 384, 398
# Para simplificar, usamos apenas 6 pontos por olho (formato EAR clássico):
RIGHT_EYE = [33, 160, 158, 133, 153, 144]   # pontos verticais e horizontais
LEFT_EYE = [362, 385, 387, 263, 373, 380]

def tocar_alarme():
    threading.Thread(target=playsound, args=("alarme.mp3",), daemon=True).start()

# Função para calcular EAR (Eye Aspect Ratio)
def eye_aspect_ratio(eye_landmarks):
    # eye_landmarks: lista de 6 pontos (x,y) na ordem: p1, p2, p3, p4, p5, p6
    # EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
    p1, p2, p3, p4, p5, p6 = eye_landmarks
    vertical1 = np.linalg.norm(p2 - p6)
    vertical2 = np.linalg.norm(p3 - p5)
    horizontal = np.linalg.norm(p1 - p4)
    ear = (vertical1 + vertical2) / (2.0 * horizontal + 1e-6)  # +1e-6 para evitar divisão por zero
    return ear


EAR_THRESHOLD = 0.13        # Valor abaixo do qual consideramos olho fechado (ajuste conforme necessidade)
CONSECUTIVE_FRAMES = 120     # Número de frames consecutivos com olhos fechados para disparar alerta
frame_counter = 0           # Contador de frames fechados consecutivos


cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Converte BGR para RGB (MediaPipe)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    # Converte de volta para BGR para exibição com OpenCV
    frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

    
    ear = None

    if results.multi_face_landmarks:
        # Pega o primeiro rosto detectado
        face_landmarks = results.multi_face_landmarks[0]

        # Extrai coordenadas (x, y) dos pontos dos olhos
        h, w, _ = frame.shape
        left_eye_points = []
        right_eye_points = []

        for idx in LEFT_EYE:
            lm = face_landmarks.landmark[idx]
            left_eye_points.append((lm.x * w, lm.y * h))
        for idx in RIGHT_EYE:
            lm = face_landmarks.landmark[idx]
            right_eye_points.append((lm.x * w, lm.y * h))

        # Converte para arrays numpy
        left_eye = np.array(left_eye_points, dtype=np.float32)
        right_eye = np.array(right_eye_points, dtype=np.float32)

        # Calcula EAR para cada olho
        ear_left = eye_aspect_ratio(left_eye)
        ear_right = eye_aspect_ratio(right_eye)
        ear = (ear_left + ear_right) / 2.0   # EAR médio

        # Desenha os pontos dos olhos (opcional, para visualização)
        for (x, y) in left_eye:
            cv2.circle(frame, (int(x), int(y)), 1, (0, 255, 0), -1)
        for (x, y) in right_eye:
            cv2.circle(frame, (int(x), int(y)), 1, (0, 255, 0), -1)

    # Lógica de sonolência

 # Lógica de sonolência
    if ear is not None:
        if ear < EAR_THRESHOLD:
            frame_counter += 1
            ear_acumulado.append(ear)

            if frame_counter == CONSECUTIVE_FRAMES:
                evento_inicio = datetime.now()
                tocar_alarme()

            if frame_counter >= CONSECUTIVE_FRAMES:
                cv2.putText(frame, "SONOLENCIA DETECTADA!", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        else:
            if evento_inicio is not None:
                fim = datetime.now()
                duracao = (fim - evento_inicio).total_seconds()
                ear_medio = sum(ear_acumulado) / len(ear_acumulado)
                database.registrar_evento(
                    funcionario_atual, evento_inicio, fim, duracao, ear_medio
                )
                evento_inicio = None
                ear_acumulado = []
            frame_counter = 0

        # Textos que aparecem quando rosto é detectado
        cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(frame, f"Frames: {frame_counter}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(frame, "Rosto: DETECTADO", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    else:
        frame_counter = 0
        # Texto de diagnóstico — sempre visível quando sem rosto
        cv2.putText(frame, "Rosto: NAO DETECTADO", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Mostra o frame
    cv2.imshow('Detector de Sonolencia', frame)
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# Após o loop principal:
cap.release()
cv2.destroyAllWindows()

# Gera e envia relatório ao encerrar o sistema


print("Gerando relatório final...")
arquivo = gerar_relatorio_html()
enviar_relatorio(arquivo)
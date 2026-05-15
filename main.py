from datetime import datetime
import database
import cv2
import mediapipe as mp
import numpy as np
import time
import threading
from playsound import playsound
from email_sender import enviar_relatorio
from analise_dados import gerando_relatorio_excel
from login import abrir_login

funcionario_atual = None

def iniciar_sistema(nome):
    global funcionario_atual
    funcionario_atual = nome
    print(f"Funcionario logado: {nome}")


abrir_login(iniciar_sistema)

if funcionario_atual is None:
    print("Login cancelado")
    exit()

evento_inicio= None
ear_acumulado = []

cap = cv2.VideoCapture(0)



"""
funcionario_atual = "João Silva"  
evento_inicio = None
ear_acumulado = []
"""

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,          
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

RIGHT_EYE = [33, 160, 158, 133, 153, 144]   
LEFT_EYE = [362, 385, 387, 263, 373, 380]

def tocar_alarme():
    threading.Thread(target=playsound, args=("alarme.mp3",), daemon=True).start()


def eye_aspect_ratio(eye_landmarks):
    p1, p2, p3, p4, p5, p6 = eye_landmarks
    vertical1 = np.linalg.norm(p2 - p6)
    vertical2 = np.linalg.norm(p3 - p5)
    horizontal = np.linalg.norm(p1 - p4)
    ear = (vertical1 + vertical2) / (2.0 * horizontal + 1e-6) 
    return ear


EAR_THRESHOLD = 0.13        
CONSECUTIVE_FRAMES = 160     
frame_counter = 0           


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
        
        face_landmarks = results.multi_face_landmarks[0]

        
        h, w, _ = frame.shape
        left_eye_points = []
        right_eye_points = []

        for idx in LEFT_EYE:
            lm = face_landmarks.landmark[idx]
            left_eye_points.append((lm.x * w, lm.y * h))
        for idx in RIGHT_EYE:
            lm = face_landmarks.landmark[idx]
            right_eye_points.append((lm.x * w, lm.y * h))

        
        left_eye = np.array(left_eye_points, dtype=np.float32)
        right_eye = np.array(right_eye_points, dtype=np.float32)

        
        ear_left = eye_aspect_ratio(left_eye)
        ear_right = eye_aspect_ratio(right_eye)
        ear = (ear_left + ear_right) / 2.0   # EAR médio

        
        for (x, y) in left_eye:
            cv2.circle(frame, (int(x), int(y)), 1, (0, 255, 0), -1)
        for (x, y) in right_eye:
            cv2.circle(frame, (int(x), int(y)), 1, (0, 255, 0), -1)

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

        cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(frame, f"Frames: {frame_counter}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(frame, "Rosto: DETECTADO", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    else:
        frame_counter = 0
        cv2.putText(frame, "Rosto: NAO DETECTADO", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow('Detector de Sonolencia', frame)
            
    if cv2.waitKey(1) & 0xFF == ord('q'):  
        gerando_relatorio_excel()
        break

cap.release()
cv2.destroyAllWindows()


print("Enviando relatório excel...")

arquivo = 'relatorio_sonolencia.xlsx'
enviar_relatorio(arquivo)
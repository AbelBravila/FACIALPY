from fastapi import FastAPI, UploadFile, File
import face_recognition

app = FastAPI()

# Cargar rostro autorizado
known_image = face_recognition.load_image_file("usuario.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

@app.get("/")
def home():
    return {"mensaje": "Servidor FastAPI funcionando en Railway 🚂"}

@app.post("/validar_rostro/")
async def validar_rostro(file: UploadFile = File(...)):
    try:
        img = face_recognition.load_image_file(file.file)
        encodings = face_recognition.face_encodings(img)

        if len(encodings) == 0:
            return {"autenticado": False, "mensaje": "No se detectó rostro"}

        match = face_recognition.compare_faces([known_encoding], encodings[0])
        return {"autenticado": match[0]}
    except Exception as e:
        return {"autenticado": False, "error": str(e)}

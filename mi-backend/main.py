from fastapi import FastAPI, UploadFile, File
from deepface import DeepFace
import tempfile

app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "Servidor FastAPI funcionando en Railway 🚂"}

@app.post("/validar_rostro/")
async def validar_rostro(file: UploadFile = File(...)):
    try:
        # Guardar imagen temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Comparar contra la imagen base "usuario.jpg"
        result = DeepFace.verify(img1_path=tmp_path, img2_path="usuario.jpg", model_name="Facenet")

        return {"autenticado": bool(result["verified"])}
    except Exception as e:
        return {"autenticado": False, "error": str(e)}

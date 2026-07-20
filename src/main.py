from fastapi import FastAPI 
import uvicorn


app = FastAPI()

@app.get("/")
def root():
    return {"message": "watermark message"}

@app.get("/health")
def health():
    return {"status": "ok"}

def main():
    uvicorn.run("src.main:app", host="127.0.0.1", port=8080, reload = True)


if __name__ == "__main__":
    main()



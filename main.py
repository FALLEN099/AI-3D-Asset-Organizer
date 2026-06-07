import os
import json
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Cấu hình Gemini AI
API_KEY = os.getenv("GEMINI_API_KEY")
model = None

genai.configure(api_key=API_KEY) # type: ignore
model = genai.GenerativeModel('gemini-2.5-flash-lite') # type: ignore


class InputData(BaseModel):
    inputData: str

@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")

@app.post("/api/organize")
async def organize_assets(data: InputData):
    # Validate input rỗng
    if not data.inputData or not data.inputData.strip():
        raise HTTPException(status_code=400, detail="Dữ liệu đầu vào không được để trống.")

    try:
        prompt = f"""
        Bạn là một trợ lý quản lý dự án 3D. Hãy phân tích danh sách các asset/phòng sau đây:
        "{data.inputData}"
        
        Trả về kết quả dưới dạng JSON với cấu trúc sau (chỉ trả về JSON, không thêm markdown hay text phụ):
        {{
          "metadata": {{
            "projectName": "Tên dự án dự đoán",
            "totalAssets": "Tổng số lượng loại asset"
          }},
          "assets": [
            {{
              "originalName": "tên gốc",
              "quantity": "số lượng sản phẩm này (kiểu số nguyên, nếu không đề cập hoặc text thô thì mặc định là 1)",
              "category": "Phân loại (vd: phòng ngủ, khu vực công cộng, kỹ thuật...)",
              "suggestedSlug": "ten-file-goi-y-theo-chuan-slug"
            }}
          ],
          "suggestions": [
            "Đề xuất 2–3 ý để cải thiện về cách tổ chức hoặc đặt tên nhằm tối ưu việc quản lý "
          ]
        }}
        """
        
        response = model.generate_content(prompt) # type: ignore
        text_output = response.text.strip()
        
        # Xử lý text để đảm bảo parse JSON an toàn (loại bỏ markdown code block nếu có)
        if text_output.startswith("```json"):
            text_output = text_output[7:-3].strip()
        elif text_output.startswith("```"):
            text_output = text_output[3:-3].strip()
            
        return json.loads(text_output)

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="AI trả về định dạng không hợp lệ.")
    except Exception as e:
        print(f"Lỗi AI: {e}")
        raise HTTPException(status_code=500, detail="Lỗi khi xử lý từ AI API. Vui lòng thử lại sau.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


## 1.Chức năng đã làm
- **Giao diện nhập liệu**: Frontend tĩnh bằng HTML/JS
- **Backend API**: Xây dựng bằng Python với framework FastAPI xử lý request POST đồng bộ. 
- **Tích hợp AI**: Sử dụng SDK `google-generativeai`. Tính năng bao gồm việc định dạng prompt để xuất ra JSON.
---

## 2. Lỗi/Điểm chưa hợp lý về UI/UX/Luồng thao tác -> Đề xuất cải thiện

| 1 | **Không có tính năng chỉnh sửa kết quả sau khi AI trả về** (người dùng bị thụ động với kết quả của AI). -> Chuyển đổi bảng kết quả HTML tĩnh thành một Data-Grid (ví dụ dùng các thẻ `<input>` trực tiếp trên bảng) để  có thể tinh chỉnh lại `slug` hoặc `category` bị phân loại sai trước khi chốt luồng.
| 2 | **Thiếu cơ chế Export dữ liệu** (phân loại xong nhưng không lấy ra dùng ở hệ thống phần mềm 3D được). -> Thêm nút "Export to JSON" / "Export to CSV" để tải file về
| 3 | **Giới hạn Token**. Cần Phải mua API Key của google

---

## 3. Cách dùng AI trong quá trình làm bài

- **AI Tool đã dùng**: Gemini / ChatGPT.
- **Mục đích sử dụng**: 
  - Phân tích và Phân loại (Classification): Tự động nhận diện danh sách các asset hoặc phòng do người dùng nhập vào để phân loại chúng vào các nhóm phù hợp (ví dụ: phòng ngủ, khu vực công cộng, kỹ thuật...).

  - Trích xuất dữ liệu (Data Extraction): Dự đoán tên tổng thể của dự án (projectName) và đếm số lượng asset từ văn bản thô nhập vào.

  - Chuẩn hóa dữ liệu (Normalization): Chuyển đổi tên gốc thành dạng "slug" (suggestedSlug) thân thiện với hệ thống tệp tin hoặc URL.

  - Đưa ra giải pháp / Tư vấn (Recommendation): Gợi ý 2–3 ý tưởng để tối ưu hóa việc quản lý và tổ chức asset dựa trên kinh nghiệm cấu trúc dự án.

- **Prompt mẫu đã sử dụng với AI**:
    "Bạn là một trợ lý quản lý dự án 3D. Hãy phân tích danh sách các asset/phòng sau đây:
    '{dữ_liệu_đầu_vào_của_user}'

    Trả về kết quả dưới dạng JSON với cấu trúc sau (chỉ trả về JSON, không thêm markdown hay text phụ):
    {
    "metadata": {
    "projectName": "Tên dự án dự đoán",
    "totalAssets": "Tổng số lượng asset"
    },
    "assets": [
    {
    "originalName": "tên gốc",
    "category": "Phân loại (vd: phòng ngủ, khu vực công cộng, kỹ thuật...)",
    "suggestedSlug": "ten-file-goi-y-theo-chuan-slug"
    }
    ],
    "suggestions": [
    "Đề xuất 2–3 ý để cải thiện về cách tổ chức hoặc đặt tên nhằm tối ưu việc quản lý"
    ]
    }"

- **Cách kiểm tra lại output của AI**: 
  - 1. Kiểm tra tính chính xác của dữ liệu
        Cần đối chiếu kết quả JSON của AI với danh sách gốc xem có bị "ảo tưởng" (hallucination) hoặc sót thông tin không:

        Kiểm tra số lượng (Total Assets): Input vào 5 phòng, trường totalAssets trong JSON phải bằng 5. Nếu AI đếm ra 4 hoặc 6 là sai.

        Kiểm tra tính toàn vẹn (Lossless): Mọi asset  nhập vào ở inputData đều phải xuất hiện đầy đủ trong danh sách assets (thông qua trường originalName). AI không được tự ý "vứt bỏ" phòng nào của bạn.

        Kiểm tra logic phân loại (Category): Ví dụ Input "Phòng ngủ Master" mà AI xếp vào nhóm kỹ thuật là sai logic. Nó phải thuộc nhóm phòng ngủ hoặc không gian riêng tư.
  - 2. Kiểm tra tính chuẩn hóa kỹ thuật
        Tiêu chuẩn Slug (suggestedSlug): Kiểm tra xem AI có chuyển đổi đúng quy tắc không.Đúng chuẩn: Không dấu, không viết hoa, khoảng trắng thay bằng dấu gạch ngang -, không chứa ký tự đặc biệt.Ví dụ: "Phòng ngủ Master tầng 2" phải thành "phong-ngu-master-tang-2". Nếu AI trả về "phong_ngu Master" hoặc giữ nguyên dấu là AI làm sai quy chuẩn.


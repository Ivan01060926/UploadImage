import gradio as gr
from io import BytesIO
import requests
from PIL import Image
import os

def send_to_line(filepaths):
    url = 'https://notify-api.line.me/api/notify'
    line_token = 'Cf4wpfze99AsLIeVMHgWuZTYisjZu0OrGYcLgOOms7w'
    headers = {'Authorization': f'Bearer {line_token}'}

    results = []  # 存放每張圖片的發送結果

    for filepath in filepaths:
        # 讀取圖片文件
        with Image.open(filepath) as image:
            buffered = BytesIO()
            image.save(buffered, format="PNG")  # 儲存為 PNG 格式
            buffered.seek(0)

            # 建立表單資料和圖片文件
            filename = os.path.basename(filepath)
            data = {'message': os.path.splitext(filename)[0]}
            files = {'imageFile': buffered}

            # 發送 POST 請求到 LINE Notify
            response = requests.post(url, headers=headers, data=data, files=files)
            results.append(f'{data["message"]}圖片已發送' if response.status_code == 200 else f'失敗: {response.text}')

    # 返回發送結果並清空檔案選擇
    return results, []

# 建立 Gradio UI
with gr.Blocks() as demo:
    with gr.Row():
        image_input = gr.File(
            label="上傳圖片", type="filepath", file_count="multiple"
        )  # 允許多選
    send_button = gr.Button("發送到 LINE")
    output_text = gr.Textbox(label="結果")  # 用於顯示發送結果

    # 按鈕點擊事件：支援發送後重置檔案選擇
    send_button.click(
        fn=send_to_line, 
        inputs=image_input, 
        outputs=[output_text, image_input]  # 更新結果和清空檔案輸入
    )

if __name__ == "__main__":
    # Render 要求應用監聽 0.0.0.0 並使用環境變數 PORT
    port = int(os.environ.get('PORT', 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
    
demo.launch()

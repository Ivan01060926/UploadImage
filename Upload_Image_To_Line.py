import gradio as gr
import os
import requests
from io import BytesIO
from PIL import Image

def send_images_from_folder(folder_path):
    url = 'https://notify-api.line.me/api/notify'
    line_token = 'wx3JjnPVDfLWX3y0m4ZVSzmGVAdZjXU9He8UItwOjhh'
    headers = {'Authorization': f'Bearer {line_token}'}
    
    folder_path = folder_path or 'D:\\測試圖2'
    # 遍歷資料夾中的所有檔案
    result = ""
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_path = os.path.join(folder_path, filename)
            
            # 將圖片讀入並轉為 BytesIO 格式
            with Image.open(file_path) as img:
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                buffered.seek(0)
            
            # 發送圖片到 LINE Notify
            data = {'message': f'發送圖片: {filename}'}
            files = {'imageFile': buffered}
            response = requests.post(url, headers=headers, data=data, files=files)
            
            # 回報傳送結果
            if response.status_code == 200:
                result += f'{filename} 已成功發送\n'
            else:
                result += f'{filename} 發送失敗: {response.text}\n'
    
    return result

# 建立 Gradio UI
with gr.Blocks() as demo:
    with gr.Row():
        folder_input = gr.Textbox(label="資料夾路徑", placeholder="D:\測試圖2")
    send_button = gr.Button("發送資料夾中的圖片到 LINE")
    output_text = gr.Textbox(label="結果")

    # 點擊按鈕後執行函數
    send_button.click(fn=send_images_from_folder, inputs=folder_input, outputs=output_text)

demo.launch()
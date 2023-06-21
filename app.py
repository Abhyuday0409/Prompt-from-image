from aiohttp import web
import aiohttp
import jinja2
import os
from model import generate_prompt_from_image  # Import the function from the model module
import base64

async def handle_upload(request):
    reader = await request.multipart()
    field = await reader.next()
    assert field.name == 'file'
    filename = field.filename
    size = 0
    temp_image_path = "temp.jpg"  # Temporary path to save the uploaded image
    with open(temp_image_path, 'wb') as f:
        while True:
            chunk = await field.read_chunk()  # Read the file in chunks
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    prompt = generate_prompt_from_image(temp_image_path)

    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("result.html")

    # Read the image file as a base64-encoded string
    with open(temp_image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    output = template.render(prompt=prompt, image_data=encoded_image)

    return web.Response(text=output, content_type="text/html")

async def init_app():
    app = web.Application()
    app.router.add_post('/upload-image', handle_upload)
    return app

if __name__ == '__main__':
    app = init_app()
    web.run_app(app, host='0.0.0.0', port=8000)

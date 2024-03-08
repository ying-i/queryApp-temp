from flask import Flask, render_template, request
import base64
from gradio_client import Client
import os

app = Flask(__name__)
client = Client("yiyii/generate-story")

# Gradio python client Doc: For certain inputs, such as images, you should pass in the filepath or URL to the file.
# save the uploaded image temporarily on my server and then pass the file path to the Gradio API.
# Define a folder to store temporary images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image = request.files["image"] #image_file is a binary file
        temperature = float(request.form["temperature"])
        max_new_tokens = float(request.form["max_new_tokens"])
        top_p = float(request.form["top_p"])
        repetition_penalty = float(request.form["repetition_penalty"])

         # Save the uploaded image temporarily
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)

        # # to solve TypeError: Object of type FileStorage is not JSON serializable
        # # Convert image bytes to base64 string
        # image_data = base64.b64encode(image.read()).decode('utf-8')

        # read the binary file(image_file) and convert it to base64 encoding (before sending it to the API)
        # image_file_content = base64.b64encode(image_file.read()).decode()
       
        print("Image file content:", image_path)
        print("Temperature:", temperature)
        print("Max new tokens:", max_new_tokens)
        print("Top-p:", top_p)
        print("Repetition penalty:", repetition_penalty)

        result = client.predict(
                image_path,	# filepath  in 'Upload Image' Image component
                temperature,	# float (numeric value between 0.0 and 1.0) in 'Temperature' Slider component
                max_new_tokens,	# float (numeric value between 0 and 3000) in 'Max new tokens' Slider component
                top_p,	# float (numeric value between 0.0 and 1) in 'Top-p (nucleus sampling)' Slider component
                repetition_penalty,	# float (numeric value between 1.0 and 2.0) in 'Repetition penalty' Slider component
                api_name="/predict"
        )

        # Optionally, remove the temporary image after processing
        os.remove(image_path)

        return render_template("index.html",result=result)
    return render_template("index.html",result=None)
    #Flask automatically looks for templates in the templates folder,
    #when you call the render_template() function in your Flask application.

if __name__ == "__main__":
    app.run(debug=True)


# running on http://127.0.0.1:5000/
# pip show gradio_client


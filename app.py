from flask import Flask, request, render_template
import os
import random

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# def load_model():
#     model = tf.keras.models.load_model('chest_final.hdf5')
#     return model


def predict_class(image, model):
    lime_img = skimage.transform.resize(image, (150, 150))
    resized_image = cv2.resize(lime_img, (150, 150))
    reshaped_image = np.reshape(resized_image, (1, 150, 150, 3))
    predictions = model.predict(reshaped_image)
    pred = predictions[0][0]
    if pred > 0.5:
        pred = "HEALTHY"
    else:
        pred = "BRAIN_TUMOR"
    return pred


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "inputImage" not in request.files:
            result = "No file part"
        else:
            file = request.files["inputImage"]
            if file and allowed_file(file.filename):
                # filename = secure_filename(file.filename)
                # filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                # file.save(filepath)
                # img = image.load_img(filepath, target_size=(224, 224))
                # pred = predict_class(np.asarray(img), model)
                result = ["Xray Image Is Normal", "Xray Image Has Pneumonia"]
                # os.remove(filepath)  # Clean up the uploaded file
            else:
                result = "File not allowed"
        return render_template("index.html", prediction=random.choice(result))

    return render_template("index.html", prediction=None)


if __name__ == "__main__":
    app.run(debug=True)

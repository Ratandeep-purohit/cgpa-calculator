from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        program = request.form.get("program")
        mode = request.form.get("mode")
        return redirect(url_for("marks", program=program, mode=mode))
    return render_template("home.html")

@app.route("/marks", methods=["GET", "POST"])
def marks():
    program = request.args.get("program")
    mode = request.args.get("mode")
    
    total_units = 3 if program == "UG" and mode == "year" else \
                  6 if program == "UG" else \
                  2 if mode == "year" else 4

    if request.method == "POST":
        percentages = []
        for i in range(1, total_units + 1):
            total = int(request.form.get(f"total_{i}", 0))
            obtained = int(request.form.get(f"obtained_{i}", 0))
            if total > 0:
                percentages.append((obtained / total) * 100)
        
        avg = round(sum(percentages) / len(percentages), 2)
        cgpa = round(avg / 9.5, 2)
        return render_template("result.html", percentages=percentages, avg=avg, cgpa=cgpa, total_units=total_units)

    return render_template("index.html", program=program, mode=mode, total_units=total_units)

# Remove this route:
# @app.route("/calculate", methods=["POST"])
# def calculate():
#     ...

if __name__ == "__main__":
    app.run(debug=True)

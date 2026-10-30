# Import Flask class, jsonify for JSON responses, and request to access incoming request data
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory list acting as our "database" of students
student = [
    {"name": "John Doe","id": 20,"major": "Computer Science"},
    {"name": "Jane Smith","id": 22,"major": "Mathematics"},
    {"name": "Michael Johnson","id": 21,"major": "Physics"},
    {"name": "Emily Davis","id": 19,"major": "Biology"},
    {"name": "Stacy Brown","id": 23,"major": "Chemistry"}
]


# GET all students

@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(student)

# GET one student by id
@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    for students in student:
        if students["id"] == id:
            return jsonify(students)
    return jsonify({"message": "Student not found"}), 404

# POST - Add a new student
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()
    # Convert id to integer to prevent it from being saved as a string
    data["id"] = int(data["id"])
    student.append(data)
    return jsonify({"message": "Student added", "student": student})

# PUT - Update an existing student
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    found = next((s for s in student if s["id"] == student_id), None)

    if not found:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()
    found["name"] = data.get("name", found["name"])
    # Convert id to integer when updating
    found["id"] = int(data.get("id", found["id"]))
    found["major"] = data.get("major", found["major"])
    return jsonify(found)

# DELETE - Remove a student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    global student
    student = [s for s in student if s["id"] != student_id]
    return jsonify({"message": "Student deleted"})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

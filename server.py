import json
import socket

# Grading scheme lookup table matching the lab prompt
GRADING_SCALE = {
    4.0: {"letter": "A", "percent": "93-100"},
    3.7: {"letter": "A-", "percent": "90-92"},
    3.3: {"letter": "B+", "percent": "87-89"},
    3.0: {"letter": "B", "percent": "83-86"},
    2.7: {"letter": "B-", "percent": "80-82"},
    2.3: {"letter": "C+", "percent": "77-79"},
    2.0: {"letter": "C", "percent": "73-76"},
    1.7: {"letter": "C-", "percent": "70-72"},
    1.3: {"letter": "D+", "percent": "67-69"},
    1.0: {"letter": "D", "percent": "65-66"},
    0.0: {"letter": "F", "percent": "Below 65"},
}


def save_student_record(data):
    try:
        try:
            with open("students.json", "r") as f:
                records = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            records = []

        records.append(data)

        with open("students.json", "w") as f:
            json.dump(records, f, indent=4)

        return (
            f"SUCCESS: Saved record for {data.get('name')} (Roll: {data.get('roll_number')})"
        )
    except Exception as e:
        return f"ERROR: Failed to save record ({str(e)})"


def get_grade_info(grade_points):
    try:
        gp = float(grade_points)
        if gp in GRADING_SCALE:
            info = GRADING_SCALE[gp]
            return f"Letter Grade: {info['letter']} | Percent Grade: {info['percent']}"
        return "ERROR: Grade Points not found in scale."
    except ValueError:
        return "ERROR: Invalid numerical value for Grade Points."


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 5000))
    server.listen(5)
    print("Server running on 127.0.0.1:5000...")

    try:
        while True:
            conn, addr = server.accept()
            raw_data = conn.recv(1024).decode("utf-8")

            if not raw_data:
                conn.close()
                continue

            try:
                payload = json.loads(raw_data)
                task_type = payload.get("task")

                if task_type == 1:
                    response = save_student_record(payload.get("student", {}))
                elif task_type == 2:
                    response = get_grade_info(payload.get("grade_points"))
                else:
                    response = "ERROR: Unknown task."
            except json.JSONDecodeError:
                response = "ERROR: Invalid JSON request."

            print(f"[{addr[0]}:{addr[1]}] -> {response}")

            conn.send(response.encode("utf-8"))
            conn.close()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server.close()


if __name__ == "__main__":
    start_server()

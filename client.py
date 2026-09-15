import json
import socket


def send_request(data):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", 5000))
        client.send(json.dumps(data).encode("utf-8"))
        response = client.recv(1024).decode("utf-8")
        client.close()
        return response
    except ConnectionRefusedError:
        return "ERROR: Server is not running."


def main():
    while True:
        print("\n=== Student Record System ===")
        print("1. Enter Student Details (Task 1)")
        print("2. Lookup Grading Scheme by Grade Points (Task 2)")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            name = input("Enter Student Name: ").strip()
            roll_no = input("Enter Roll Number: ").strip()
            marks = input("Enter Marks: ").strip()

            payload = {
                "task": 1,
                "student": {
                    "name": name,
                    "roll_number": roll_no,
                    "marks": marks,
                },
            }
            response = send_request(payload)
            print(f"\nServer Response: {response}")

        elif choice == "2":
            gp = input(
                "Enter Grade Points (e.g., 4, 3.7, 3.3, 3, 2.7...): "
            ).strip()

            payload = {"task": 2, "grade_points": gp}
            response = send_request(payload)
            print(f"\nServer Response: {response}")

        elif choice == "3":
            print("Exiting client.")
            break
        else:
            print("Invalid selection. Try again.")


if __name__ == "__main__":
    main()

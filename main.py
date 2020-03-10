import json


def get_users_choice():
    users_input = input("Enter your choice: ")
    return users_input


def is_valid_name(student_name):  # student_name = "ali"
    for character in student_name:
        if character.isalpha() or character.isspace():
            is_valid = True
        else:
            return False
    return is_valid


def is_valid_cnic(cnic):  # cnic = "12-3452345671-1"
    cnic = cnic.strip()
    if len(cnic) == 13:
        if cnic.isdigit():
            return True
        else:
            return False
    else:
        return False


def is_mobile_valid(mobile_number):  # mobile_number = "0334-1128322"
    mobile_number = mobile_number.strip()
    if len(mobile_number) == 12:
        if "-" in mobile_number:
            if mobile_number.count("-") > 1:
                return False
            else:
                if mobile_number[4] == "-":
                    parts = mobile_number.split("-")  # parts = ["0334","1128322"]
                    if parts[0].isdigit() and parts[1].isdigit():
                        return True
                    else:
                        return False
                else:
                    return False
        else:
            return False
    else:
        return False


def is_address_valid(address):  # address = "a-85"
    address = address.strip()
    if len(address) >= 4:
        for character in address:
            if character in " #()-\:',./" or character.isalpha() or character.isdigit():
                is_valid = True
            else:
                return False
        return is_valid
    else:
        return False


def is_cnic_unique(cnic):
    is_unique = True
    with open("students_data.json") as f:
        data = json.load(f)
        for course in ["ai", "bc", "cc"]:
            for student_id in data[course].keys():  # data[course].keys() = []
                if data[course][student_id]["cnic"] == cnic:
                    return False
                else:
                    is_unique = True
        return is_unique


def generate_id(courses, course_number):
    student_id = courses[course_number]["prefix"]  # "AI"
    with open("students_data.json", "r") as f:
        data = json.load(f)
        prefix = courses[course_number]["prefix"].lower()
        list_of_students = data[prefix].keys()  # list_of_students = []
        number_of_students = len(list_of_students)
        if number_of_students == 0:
            student_id = student_id + " " + "1"
            return student_id
        else:
            numbers = []
            for key in list_of_students:  # key = "AI 1" 1
                numbers.append(int(key.split()[-1]))
            max_number = max(numbers)
            new_number = max_number + 1

            student_id = student_id + " " + str(new_number)
            return student_id


def show_courses():
    print("\nSelect any 1 from the following courses:")
    print("\nEnter 1 for Artificial Intelligence")
    print("Enter 2 for Blockchain")
    print("Enter 3 for Cloud Computing\n")
    course_number = get_users_choice()
    return course_number


def add_student():
    courses = {
        "1": {"prefix": "AI", "course_name": "Artificial Intelligence"},
        "2": {"prefix": "BC", "course_name": "Blockchain"},
        "3": {"prefix": "CC", "course_name": "Cloud Computing"},
    }

    while True:
        print("\n*** ADD STUDENT ***")
        course_number = show_courses()

        if course_number in courses.keys():  # keys = ["1","2","3"]
            print("\nCourse:", courses[course_number]["course_name"])
            student_name, father_name, mobile_number, cnic, address = take_input("add")
            break
        else:
            print(f"\n\tInvalid Course Number '{course_number}'!")
            continue

    student_id = generate_id(courses, course_number)
    student = {
        "course": courses[course_number]["course_name"],
        "name": student_name,
        "father name": father_name,
        "mobile no": mobile_number,
        "cnic": cnic,
        "address": address
    }

    with open("students_data.json") as f:
        data = json.load(f)
    with open("students_data.json", "w") as f:
        data[courses[course_number]["prefix"].lower()][student_id] = student
        json.dump(data, f)
        print("\n\t*** Student Added Successfully :) ***")


def get_formatted_cnic(cnic):  # cnic = "1234512345671"
    part1 = cnic[:5]
    part2 = cnic[5:12]
    cnic = part1 + "-" + part2 + "-" + cnic[-1]
    return cnic


def take_mobile_address():
    while True:
        mobile_number = input("Mobile No: ")
        if is_mobile_valid(mobile_number):
            address = input("Address: ")
            if is_address_valid(address):
                break
            else:
                print(f"\n\tInvalid Address '{address}'!")
                continue
        else:
            print(f"\n\tInvalid Mobile No. '{mobile_number}'!")
            continue
    return mobile_number, address


def take_input(operation, student_id=""):  # student_id = "AI 1"
    while True:
        student_name = input("Name: ")
        if is_valid_name(student_name):
            father_name = input("Father Name: ")
            if is_valid_name(father_name):
                cnic = input("B. Form / CNIC: ")
                if is_valid_cnic(cnic):
                    cnic = get_formatted_cnic(cnic)
                    if is_cnic_unique(cnic):
                        mobile_number, address = take_mobile_address()
                        break
                    else:
                        if operation == "update":
                            with open("students_data.json") as f:
                                data = json.load(f)
                                if data[student_id.split()[0].lower()][student_id]["cnic"] == cnic:
                                    mobile_number, address = take_mobile_address()
                                    break
                                else:
                                    print(f"\n\tB. Form / CNIC '{cnic}' already exists!")
                                    continue
                        else:
                            print(f"\n\tB. Form / CNIC '{cnic}' already exists!")
                            continue
                else:
                    print(f"\n\tInvalid B. Form / CNIC '{cnic}'!")
                    continue
            else:
                print(f"\n\tInvalid Name '{father_name}'!")
                continue
        else:
            print(f"\n\tInvalid Name '{student_name}'!")
            continue

    return student_name, father_name, mobile_number, cnic, address


def is_id_found():
    student_id = input("Enter ID: ")
    with open("students_data.json") as f:
        data = json.load(f)
        for course_name in ["ai", "bc", "cc"]:
            for std_id in data[course_name].keys():
                if student_id == std_id:
                    return True, data, course_name, student_id
                else:
                    not_exist = True
        if not_exist:
            return False, None, None, student_id


def update_student():
    print("*** UPDATE STUDENT ***")
    is_found, data, course_name, student_id = is_id_found()
    if is_found:
        student_name, father_name, mobile_number, cnic, address = take_input("update", student_id)
        with open("students_data.json", "w") as f:
            data[course_name][student_id]["name"] = student_name
            data[course_name][student_id]["father name"] = father_name
            data[course_name][student_id]["mobile no"] = mobile_number
            data[course_name][student_id]["cnic"] = cnic
            data[course_name][student_id]["address"] = address

            json.dump(data, f)
            print("\n\t*** Student Updated Successfully :) ***")
    else:
        print(f"\n\tInvalid ID '{student_id}'!")


def delete_single_student():
    is_found, data, course_name, student_id = is_id_found()
    if is_found:
        data[course_name].pop(student_id)
        with open("students_data.json", "w") as f:
            json.dump(data, f)
            print("\n\t*** Student Deleted Successfully :) ***")
    else:
        print(f"\n\tInvalid ID '{student_id}'!")


def delete_students(course_name):
    with open("students_data.json") as f:
        data = json.load(f)
        if len(data[course_name]) > 0:
            data[course_name] = {}
            with open("students_data.json", "w") as f:
                json.dump(data, f)
                print(f"\n\t*** Deleted Students of {course_name.upper()} :) ***")
        else:
            print(f"\n\tNo students in '{course_name.upper()}'!")


def delete_course_students():
    course_number = show_courses()
    if course_number == "1":
        delete_students("ai")
    elif course_number == "2":
        delete_students("bc")
    elif course_number == "3":
        delete_students("cc")
    else:
        print("\n\tInvalid Choice!")


def delete_all_students():
    password = input("Enter Password: ")
    with open("students_data.json") as f:
        data = json.load(f)
        if data["admin_password"] == password:
            data["ai"] = {}
            data["bc"] = {}
            data["cc"] = {}
            with open("students_data.json", "w") as f:
                json.dump(data, f)
                print("*** Deleted All Students of All Courses Successfully :) ***")
        else:
            print(f"\n\tInvalid Password '{password}'!\n")


def delete_student():
    print("*** DELETE STUDENT ***")
    print("1. Enter 1 to Delete a Single Student")
    print("2. Enter 2 to Delete All Students of a Course")
    print("3. Enter 3 to Delete All Students of All Courses")
    users_choice = get_users_choice()
    if users_choice == "1":
        delete_single_student()
    elif users_choice == "2":
        delete_course_students()
    elif users_choice == "3":
        delete_all_students()
    else:
        print("\n\tInvalid Input!")


def is_student_available():
    with open("students_data.json") as f:
        data = json.load(f)
        number_of_students = 0
        for course in ["ai", "bc", "cc"]:
            number_of_students = number_of_students + len(data[course])

        if number_of_students > 0:
            return True
        else:
            return False


def view_single_student():
    is_found, data, course_name, student_id = is_id_found()
    if is_found:
        print(f"\n*** Student Bearing ID '{student_id}' ***\n")
        for key, value in data[course_name][student_id].items():
            print(key.upper() if key == "cnic" else key.title(), ":", value.title())

        print("\n*** Student Retrieved Successfully :) ***\n")
    else:
        print(f"\n\tInvalid ID '{student_id}'!\n")


def view_students(course_name, call_print):
    with open("students_data.json") as f:
        data = json.load(f)
        if len(data[course_name]) > 0:
            print(f"\n*** Students of {course_name.upper()} ***\n")
            print("ID | Name | Father Name | CNIC | Mobile No | Address\n")
            for student_id, student in data[course_name].items():
                print(student_id, "|", student["name"].title(), "|", student["father name"].title(), "|",
                      student["cnic"], "|",
                      student["mobile no"], "|", student["address"].title())
            if call_print:
                print("\n*** Students Retrieved Successfully :) ***\n")
        else:
            print(f"\n\tNo students in '{course_name.upper()}'!")


def view_course_students():
    course_number = show_courses()
    if course_number == "1":
        view_students("ai", True)
    elif course_number == "2":
        view_students("bc", True)
    elif course_number == "3":
        view_students("cc", True)
    else:
        print("\n\tInvalid Choice!")


def view_all_students():
    for course_name in ["ai", "bc", "cc"]:
        view_students(course_name, False)
    print("\n*** Students Retrieved Successfully :) ***\n")


def view_student():
    print("*** VIEW STUDENT ***")
    print("1. Enter 1 to View a Single Student")
    print("2. Enter 2 to View All Students of a Course")
    print("3. Enter 3 to View All Students of All Courses")
    users_choice = get_users_choice()
    if users_choice == "1":
        view_single_student()
    elif users_choice == "2":
        view_course_students()
    elif users_choice == "3":
        view_all_students()
    else:
        print("\n\tInvalid Input!")


def start():
    import os
    exists = os.path.exists(os.getcwd() + r"\students_data.json")
    if not exists:
        with open("students_data.json", "w") as f:
            data = {
                "admin_password": "admin123",
                "ai": {},
                "bc": {},
                "cc": {}
            }
            json.dump(data, f)

    while True:
        print("*** STUDENT MANAGEMENT SYSTEM ***")
        print("1. Enter 1 To Add")
        print("2. Enter 2 To Update")
        print("3. Enter 3 To Delete")
        print("4. Enter 4 To View")
        print("5. Enter 5 To Exit")
        print("*********************************")
        users_choice = get_users_choice()
        if users_choice == "1":
            add_student()
        elif users_choice == "2":
            if is_student_available():
                update_student()
            else:
                print("\n\tNothing to Update!")
        elif users_choice == "3":
            if is_student_available():
                delete_student()
            else:
                print("\n\tNothing to Delete!")
        elif users_choice == "4":
            if is_student_available():
                view_student()
            else:
                print("\n\tNothing to Show!")
        elif users_choice == "5":
            print("\n\t*** Saving your work ***")
            print("\n\tTHANK YOU :)")
            break
        else:
            print("\n\tInvalid Input!")


start()

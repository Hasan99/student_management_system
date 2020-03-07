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
        print("data:", data, "type:", type(data))
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


def add_student():
    courses = {
        "1": {"prefix": "AI", "course_name": "Artificial Intelligence"},
        "2": {"prefix": "BC", "course_name": "Blockchain"},
        "3": {"prefix": "CC", "course_name": "Cloud Computing"},
    }

    while True:
        print("\n*** ADD STUDENT ***")
        print("\nSelect any 1 from the following courses:")
        print("\nEnter 1 for Artificial Intelligence")
        print("Enter 2 for Blockchain")
        print("Enter 3 for Cloud Computing\n")
        course_number = get_users_choice()

        if course_number in courses.keys():  # keys = ["1","2","3"]
            print("\nCourse:", courses[course_number]["course_name"])
            student_name, father_name, mobile_number, cnic, address = take_input("add")
        else:
            print(f"Invalid Course Number '{course_number}'")
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
        print("\n*** Student Added Successfully :) ***")


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
                print(f"Invalid Address '{address}'")
                continue
        else:
            print(f"Invalid Mobile No. '{mobile_number}'")
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
                    else:
                        if operation == "update":
                            with open("students_data.json") as f:
                                data = json.load(f)
                                if data[student_id.split()[0].lower()][student_id]["cnic"] == cnic:
                                    mobile_number, address = take_mobile_address()
                                    break
                                else:
                                    print(f"B. Form / CNIC '{cnic}' already exists!")
                                    continue
                        else:
                            print(f"B. Form / CNIC '{cnic}' already exists!")
                            continue
                else:
                    print(f"Invalid B. Form / CNIC '{cnic}'")
                    continue
            else:
                print(f"Invalid Name '{father_name}'")
                continue
        else:
            print(f"Invalid Name '{student_name}'")
            continue

    return student_name, father_name, mobile_number, cnic, address


def update_student():
    flag = False
    print("*** UPDATE STUDENT ***")
    student_id = input("Enter ID: ")
    with open("students_data.json") as f:
        data = json.load(f)
        for course_name in data.keys():
            for std_id in data[course_name].keys():
                if student_id == std_id:
                    student_name, father_name, mobile_number, cnic, address = take_input("update", student_id)
                    not_exist = False
                    flag = True
                    break
                else:
                    not_exist = True
            if flag:
                break
        if not_exist:
            print(f"Invalid ID '{student_id}'")
        else:
            with open("students_data.json", "w") as f:
                # course = data[course_name][student_id]["course"]
                data[course_name][student_id]["name"] = student_name
                data[course_name][student_id]["father name"] = father_name
                data[course_name][student_id]["mobile no"] = mobile_number
                data[course_name][student_id]["cnic"] = cnic
                data[course_name][student_id]["address"] = address

                json.dump(data, f)
                print("*** Student Updated Successfully :) ***")


def delete_student():
    print("*** DELETE STUDENT ***")
    print("1. Enter 1 to Delete a Single Student")
    print("2. Enter 2 to Delete All Students of a Course")
    print("3. Enter 3 to Delete All Students of All Courses")
    users_choice = get_users_choice()
    if users_choice == "1":
        print("Delete a Single Student")
    elif users_choice == "2":
        print("Delete All Students of a Course")
    elif users_choice == "3":
        print("Delete All Students of All Courses")
    else:
        print("Invalid Input!")


def start():
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
            update_student()
        elif users_choice == "3":
            delete_student()
        elif users_choice == "4":
            print("View")
        elif users_choice == "5":
            print("\n\tTHANK YOU :)")
            break
        else:
            print("Invalid Input!")


start()

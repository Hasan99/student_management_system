def get_users_choice():
    users_input = input("Enter your choice: ")
    return users_input


def is_valid_name(student_name):  # student_name = "123 ali"
    for character in student_name:
        if character.isalpha() or character.isspace():
            return True
        else:
            return False


def add_student():
    courses = {
        "1": "Artificial Intelligence",
        "2": "Blockchain",
        "3": "Cloud Computing"
    }
    print("\n*** ADD STUDENT ***")
    print("\nSelect any 1 from the following courses:")
    print("\nEnter 1 for Artificial Intelligence")
    print("Enter 2 for Blockchain")
    print("Enter 3 for Cloud Computing\n")

    while True:
        course_number = get_users_choice()

        if course_number in courses.keys():  # keys = ["1","2","3"]
            print("\nCourse:", courses[course_number])
            student_name = input("Name: ")
            if is_valid_name(student_name):
                father_name = input("Father Name: ")
                if is_valid_name(father_name):
                    print("in if")
                    pass
                else:
                    print(f"Invalid Name '{father_name}'")
                    continue
            else:
                print(f"Invalid Name '{student_name}'")
                continue
        else:
            print(f"Invalid Course Number '{course_number}'")
            continue

    # cnic = input("B. Form / CNIC: ")
    # mobile_number = input("Mobile No: ")
    # address = input("Address: ")
    print("\n*** Student Added Successfully :) ***")


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
        print("Update")
    elif users_choice == "3":
        print("Delete")
    elif users_choice == "4":
        print("View")
    elif users_choice == "5":
        print("\n\tTHANK YOU :)")
        break
    else:
        print("Invalid Input!")

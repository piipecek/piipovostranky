from website.paths import acga_students_xlsx_path
import openpyxl
import czech_sort


def get_students_from_xlsx() -> dict:
    if not acga_students_xlsx_path().exists():
        return {}
    workbook = openpyxl.load_workbook(acga_students_xlsx_path())
    sheet = workbook.active
    students = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        surname, name, email, class_name = row
        students.append({"full_name": name + " " + surname, "name": name, "surname": surname, "email": email, "class": class_name})
    
    order = {"FR": 0, "SO": 1, "JU": 2, "SR": 3}
    students.sort(key=lambda x: (order.get(x["class"][:2], 99), x["class"], czech_sort.key(x["surname"]), czech_sort.key(x["name"])))
    for i, student in enumerate(students):
        student["cislo"] = i + 1
    return students


def get_classes() -> list[str]:
    students = get_students_from_xlsx()
    classes = set(student["class"] for student in students)
    # sort using groups by substrings FR, SO, JU, SR, then by the following (FR1A)
    order = {"FR": 0, "SO": 1, "JU": 2, "SR": 3}
    classes = sorted(classes, key=lambda x: (order.get(x[:2], 99), x))
    return classes
    

def get_students_by_class(class_name: str) -> list[dict]:
    students = get_students_from_xlsx()
    students = [student for student in students if student["class"] == class_name]
    students.sort(key=lambda x: (czech_sort.key(x["surname"]), czech_sort.key(x["name"])))
    for i, student in enumerate(students):
        student["cislo"] = i + 1
    return students
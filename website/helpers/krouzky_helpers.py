from website.paths import acga_students_xlsx_path
import openpyxl


def get_students_from_xlsx() -> dict:
    if not acga_students_xlsx_path().exists():
        return {}
    workbook = openpyxl.load_workbook(acga_students_xlsx_path())
    sheet = workbook.active
    students = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        surname, name, email, class_name = row
        students.append({"full_name": name + " " + surname, "surname": surname, "email": email, "class": class_name})
    students.sort(key=lambda x: (x["class"], x["surname"]))
    for i, student in enumerate(students):
        student["cislo"] = i + 1
    return students

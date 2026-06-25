import pandas as pd
from pathlib import Path

DATA_FOLDER = "data"

students = []
subjects = {}
semesters = set()
grades = []

for file in Path(DATA_FOLDER).glob("*.xlsx"):

    print("Đang xử lý:", file.name)

    df = pd.read_excel(file, header=None)

    current_student = None
    current_semester = None

    for _, row in df.iterrows():

        values = [
            str(x).strip()
            for x in row
            if pd.notna(x)
        ]

        row_text = " ".join(values)

        # Họ tên
        if "Họ và tên:" in row_text:

            name = row_text.split("Họ và tên:")[-1].strip()

            current_student = {
                "MSSV": "",
                "Họ tên": name,
                "Lớp": "",
                "Ngành": ""
            }

        # MSSV
        if "Mã SV:" in row_text and current_student:

            current_student["MSSV"] = (
                row_text
                .split("Mã SV:")[-1]
                .split()[0]
            )

        # Ngành
        if "Ngành:" in row_text and current_student:

            current_student["Ngành"] = (
                row_text
                .split("Ngành:")[-1]
                .split("Lớp:")[0]
                .strip()
            )

        # Lớp
        if "Lớp:" in row_text and current_student:

            current_student["Lớp"] = (
                row_text
                .split("Lớp:")[-1]
                .strip()
            )

            if current_student not in students:
                students.append(current_student.copy())

        # Học kỳ
        if "Học kỳ" in row_text:

            current_semester = row_text
            semesters.add(current_semester)

        # Môn học
        subject = ""tia

        if len(row) > 1 and pd.notna(row[1]):
            subject = str(row[1]).strip()

        if (
            current_student
            and current_semester
            and subject
            and "Trung bình học kỳ" not in subject
        ):

            tc = None
            diem10 = None
            diem4 = None
            diemchu = None

            if len(row) > 8 and pd.notna(row[8]):
                tc = row[8]

            if len(row) > 14 and pd.notna(row[14]):
                diem10 = row[14]

            if len(row) > 15 and pd.notna(row[15]):
                diem4 = row[15]

            if len(row) > 16 and pd.notna(row[16]):
                diemchu = row[16]

            if tc is not None and diem10 is not None:

                subjects[subject] = tc

                grades.append({
                    "MSSV": current_student["MSSV"],
                    "Lớp": current_student["Lớp"],
                    "Học kỳ": current_semester,
                    "Môn học": subject,
                    "Số TC": tc,
                    "Điểm hệ 10": diem10,
                    "Điểm hệ 4": diem4,
                    "Điểm chữ": diemchu
                })

# ===== Xuất Excel =====

with pd.ExcelWriter(
    "university_data.xlsx",
    engine="openpyxl"
) as writer:

    pd.DataFrame(students).drop_duplicates().to_excel(
        writer,
        sheet_name="Students",
        index=False
    )

    pd.DataFrame({
        "Môn học": list(subjects.keys()),
        "Số TC": list(subjects.values())
    }).to_excel(
        writer,
        sheet_name="Subjects",
        index=False
    )

    pd.DataFrame({
        "Học kỳ": sorted(list(semesters))
    }).to_excel(
        writer,
        sheet_name="Semesters",
        index=False
    )

    pd.DataFrame(grades).to_excel(
        writer,
        sheet_name="Grades",
        index=False
    )

print("Đã tạo university_data.xlsx")
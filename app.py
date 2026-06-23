
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

FILE = "university_data.xlsx"

# Đọc dữ liệu một lần khi khởi động
students = pd.read_excel(FILE, sheet_name="Students")
grades = pd.read_excel(FILE, sheet_name="Grades")


@app.route("/", methods=["GET", "POST"])
def index():

    student = None
    semesters = {}
    gpa = None
    message = None

    if request.method == "POST":

        keyword = request.form.get(
            "keyword",
            ""
        ).strip()

        if keyword:

            # Tìm theo MSSV hoặc Họ tên
            student_df = students[
                (students["MSSV"].astype(str) == keyword)
                |
                (
                    students["Họ tên"]
                    .astype(str)
                    .str.contains(
                        keyword,
                        case=False,
                        na=False
                    )
                )
            ]

            if not student_df.empty:

                student = student_df.iloc[0].to_dict()

                mssv = str(student["MSSV"])

                # Lấy bảng điểm
                result = grades[
                    grades["MSSV"]
                    .astype(str)
                    == mssv
                ]

                if not result.empty:

                    # GPA toàn khóa
                    gpa = round(
                        result["Điểm hệ 10"].mean(),
                        2
                    )

                    # Gom theo học kỳ
                    for hk, group in result.groupby("Học kỳ"):

                        semesters[hk] = group[
                            [
                                "Môn học",
                                "Số TC",
                                "Điểm hệ 10"
                            ]
                        ].to_dict("records")

            else:
                message = "Không tìm thấy sinh viên"

    return render_template(
        "index.html",
        student=student,
        semesters=semesters,
        gpa=gpa,
        message=message
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

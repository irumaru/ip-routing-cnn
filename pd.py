import pandas as pd

student_data = [{'name': 'Alice', 'grade': 95, 'subject': 'Math'},
                {'name': 'Bob', 'grade': 87, 'subject': 'English'},
                {'name': 'Charlie', 'grade': 92, 'subject': 'Science'}]

df = pd.DataFrame(student_data)
print(df.loc[:, ["name", "grade"]])

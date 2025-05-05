import customtkinter as ctk  
from tkinter import ttk, messagebox  
from db import Database 
from datetime import datetime 

class StudentGradeApp(ctk.CTk):  
    def __init__(self):  
        super().__init__()  

        self.db = Database("StudentRelational.db")  

        self.title("Student Grade Management System")  
        self.geometry("1400x900")  
        self.configure(fg_color="#2c3e50") 

        self.name = ctk.StringVar()  
        self.index_number = ctk.StringVar()  
        self.course_name = ctk.StringVar()  
        self.grade = ctk.StringVar()  

        self.search_student_var = ctk.StringVar()  
        self.search_course_var = ctk.StringVar()  

        self.selected_grade_id = None  

        self.create_widgets()  
        self.refresh_data()  

    def create_widgets(self):  
        tabview = ctk.CTkTabview(self)  
        tabview.pack(expand=True, fill="both", padx=20, pady=20)  

        tab_students = tabview.add("Students")  
        tab_courses = tabview.add("Courses")  
        tab_grades = tabview.add("Grades")  

        tab_students.columnconfigure((0, 3), weight=1)  
        tab_students.columnconfigure((1, 2), weight=0)  

        ctk.CTkLabel(tab_students, text="Name:").grid(row=0, column=1, sticky="e", padx=10, pady=5)  
        ctk.CTkEntry(tab_students, textvariable=self.name).grid(row=0, column=2, sticky="w", padx=10, pady=5)  

        ctk.CTkLabel(tab_students, text="Index Number:").grid(row=1, column=1, sticky="e", padx=10, pady=5)  
        ctk.CTkEntry(tab_students, textvariable=self.index_number).grid(row=1, column=2, sticky="w", padx=10, pady=5)  

        ctk.CTkButton(tab_students, text="Add Student", command=self.add_student).grid(row=2, column=1, columnspan=2, pady=10)  

        tab_courses.columnconfigure((0, 3), weight=1)  
        tab_courses.columnconfigure((1, 2), weight=0)  

        ctk.CTkLabel(tab_courses, text="Course Name:").grid(row=0, column=1, sticky="e", padx=10, pady=5)  
        ctk.CTkEntry(tab_courses, textvariable=self.course_name).grid(row=0, column=2, sticky="w", padx=10, pady=5)  

        ctk.CTkButton(tab_courses, text="Add Course", command=self.add_course).grid(row=1, column=1, columnspan=2, pady=10)

        tab_grades.columnconfigure((0,1),weight=1)
        self.combo_students=ttk.Combobox(tab_grades,state="readonly")
        self.combo_students.grid(row=0,column=0,padx=10,pady=5,sticky="ew")

        self.combo_courses=ttk.Combobox(tab_grades,state="readonly")
        self.combo_courses.grid(row=0,column=1,padx=10,pady=5,sticky="ew")
        ctk.CTkLabel(tab_grades,text="Grade:").grid(row=1,column=0,sticky="e",padx=10,pady=5)
        ctk.CTkEntry(tab_grades,textvariable=self.grade).grid(row=1,column=1,sticky="ew",padx=10,pady=5)
        ctk.CTkButton(tab_grades,text="Add grade",command=self.add_grade).grid(row=2,column=0,columnspan=2,pady=10)

        ctk.CTkEntry(tab_grades,textvariable=self.search_student_var,placeholder_text="Search student").grid(row=3,column=0,padx=10,pady=5,sticky="ew")
        ctk.CTkEntry(tab_grades,textvariable=self.search_course_var,placeholder_text="Seach course").grid(row=3,column=1,padx=10,pady=5,sticky="ew")

        ctk.CTkButton(tab_grades,text="Filter grades",command=self.filter_grades).grid(row=4,column=0,columnspan=2,pady=5)

        ctk.CTkButton(tab_grades,text="Update grade",command=self.update_grade).grid(row=5,column=0,pady=5)
        ctk.CTkButton(tab_grades,text="Delete grade",command=self.delete_grade).grid(row=5,column=1,pady=5)

        self.tv = ttk.Treeview(tab_grades,columns=(1,2,3,4,5,6),show="headings",height=10)
        self.tv.grid(row=6,column=0,columnspan=2,sticky="nsew",pady=10)
        tab_grades.rowconfigure(6,weight=1)

        self.tv.heading(1,text="ID")
        self.tv.heading(2,text="Students Name")
        self.tv.heading(3,text="Index")
        self.tv.heading(4,text="Course")
        self.tv.heading(5,text="Grade")
        self.tv.heading(6,text="Date")

        self.tv.bind("<Double-1>",self.select_grade) #odje dodati komandu za izbor ocjene

    def refresh_data(self):
        self.combo_students["values"]=[f"{s[0]} - {s[1]} ({s[2]})" for s in self.db.fetch_students()]
        self.combo_courses["values"]=[f"{c[0]} - {c[1]} " for c in self.db.fetch_courses()]

        for i in self.tv.get_children():
            self.tv.delete(i)
        for row in self.db.fetch_grades():
            self.tv.insert("","end",values=row)

    def add_student(self):
        if self.name.get() and self.index_number.get():
            try:
                self.db.add_student(self.name.get(),self.index_number.get())
                self.refresh_data()
                messagebox.showinfo("Uspjesno ste dodali studenta")
                self.name.set("")
                self.index_number.set("")
            except Exception as e:
                messagebox.showerror("Greska",str(e))
    def add_course(self):
        if self.course_name.get():
            try:
                self.db.add_course(self.course_name.get())
                self.refresh_data()
                messagebox.showinfo("Uspjeh","Kurs je dodat")
                self.course_name.set("")
            except Exception as e:
                messagebox.showerror("Greska",str(e))
    def add_grade(self):
        try:
            student_info=self.combo_students.get().split(" - ")[0]
            course_info=self.combo_courses.get().split(" - ")[0]

            student_id=int(student_info)
            course_id=int(course_info)
            grade_value=self.grade.get()
            date=datetime.now().strftime("%Y-%m-%d")
            if grade_value:
                self.db.add_grade(student_id,course_id,grade_value,date)
                self.refresh_data()
                messagebox.showinfo("Uspjeh","Uspjesno dodata ocjena")
                self.grade.set("")
        except Exception as e:
            messagebox.showerror("Greska",str(e))

    def select_grade(self,event):
        selected=self.tv.focus()
        values=self.tv.item(selected,"values")
        if values:
            self.selected_grade_id=int(values[0])
            self.grade.set(values[4])
            student_name=values[1]
            index=values[2]
            course_name=values[3]
            for student in self.combo_students["values"]:
                if f"{student_name} ({index})" in student:
                    self.combo_students.set(student)
                    break
            for course in self.combo_courses["values"]:
                if course_name in course:
                    self.combo_courses.set(course)
                    break

    def update_grade(self):
        if self.selected_grade_id is not None and self.grade.get():
            try:
                new_grade=self.grade.get()
                self.db.update_grade(self.selected_grade_id,new_grade)
                self.refresh_data()
                messagebox.showinfo("Uspjesno","Ocjena je promijenjena")
                self.grade.set("")
                self.selected_grade_id=None
            except Exception as e:
                messagebox.showerror("Greska",str(e))
        else:
            messagebox.showwarning("Izaberi ocjenu","Klikni dva puta na polje")
    def delete_grade(self):
        selected=self.tv.focus()
        values=self.tv.item(selected,"values")
        if values:
            try:
                self.db.delete_grade(values[0])
                self.refresh_data()
                messagebox.showinfo("Uspjeh","Ocjena je obrisana")
            except Exception as e:
                messagebox.showerror("Greska",str(e))
    def search_students(self):
        keyword=self.search_student_var.get()
        students=self.db.search_students(keyword)
        if not students:
            messagebox.showinfo("Nije pronadjeno","Ne postoji taj student")
        self.combo_students["values"]=[f"{s[0]} - {s[1]} ({s[2]})" for s in students]
    def search_courses(self):
        keyword=self.search_course_var.get()
        courses=self.db.search_courses(keyword)
        if not courses:
            messagebox.showinfo("Nije pronadjeno", "Ne postoji taj kurs")
        self.combo_courses["values"]=[f"{c[0]} - {c[1]}" for c in courses]
    def filter_grades(self):
        student_kw=self.search_student_var.get().lower()
        course_kw=self.search_course_var.get().lower()
        for i in self.tv.get_children():
            self.tv.delete(i)
        for row in self.db.fetch_grades():
            student_name=row[1].lower()
            course_name=row[3].lower()
            if (student_kw in student_name) and (course_kw in course_name):
                self.tv.insert("","end",values=row)





            

            





    









if __name__ == "__main__":  
    ctk.set_appearance_mode("dark")  
    ctk.set_default_color_theme("blue") 
    app = StudentGradeApp()  
    app.mainloop() 

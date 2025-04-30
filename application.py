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
        #self.refresh_data()  

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

        ctk.CTkButton(tab_students, text="Add Student", command="").grid(row=2, column=1, columnspan=2, pady=10)  

        tab_courses.columnconfigure((0, 3), weight=1)  
        tab_courses.columnconfigure((1, 2), weight=0)  

        ctk.CTkLabel(tab_courses, text="Course Name:").grid(row=0, column=1, sticky="e", padx=10, pady=5)  
        ctk.CTkEntry(tab_courses, textvariable=self.course_name).grid(row=0, column=2, sticky="w", padx=10, pady=5)  

        ctk.CTkButton(tab_courses, text="Add Course", command="").grid(row=1, column=1, columnspan=2, pady=10)  

        

if __name__ == "__main__":  
    ctk.set_appearance_mode("dark")  
    ctk.set_default_color_theme("blue") 
    app = StudentGradeApp()  
    app.mainloop() 

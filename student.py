import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re

class StudentClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1100x600+120+100")
        self.root.config(bg="white")
        self.root.focus_force()

        # ==== Variables ====
        self.var_roll = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_gender = tk.StringVar()
        self.var_dob = tk.StringVar()
        self.var_contact = tk.StringVar()
        self.var_course = tk.StringVar()
        self.var_admission = tk.StringVar()
        self.var_state = tk.StringVar()
        self.var_city = tk.StringVar()
        self.var_pin = tk.StringVar()
        self.var_search = tk.StringVar()

        self.create_table()

        # === Title ===
        title = tk.Label(self.root, text="Manage Student Details", font=("goudy old style", 20, "bold"), bg="#0f4d7d", fg="white").place(x=10, y=15, width=1070)

        # === Search Bar ===
        search_label = tk.Label(self.root, text=" Roll No :", font=("goudy old style", 15), bg="white").place(x=10, y=60)
        search_entry = tk.Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15), bg="lightyellow").place(x=200, y=60, width=300)
        btn_search = tk.Button(self.root, text="Search", font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2", command=self.search_student).place(x=520, y=60, width=100, height=30)

        # === Content ===
        lbl_roll = tk.Label(self.root, text="Roll No.", font=("goudy old style", 15), bg="white").place(x=10, y=100)
        lbl_name = tk.Label(self.root, text="Name", font=("goudy old style", 15), bg="white").place(x=350, y=100)
        lbl_email = tk.Label(self.root, text="Email", font=("goudy old style", 15), bg="white").place(x=700, y=100)

        txt_roll = tk.Entry(self.root, textvariable=self.var_roll, font=("goudy old style", 15), bg="lightyellow").place(x=120, y=100, width=200)
        txt_name = tk.Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(x=430, y=100, width=240)
        txt_email = tk.Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15), bg="lightyellow").place(x=790, y=100, width=280)

        lbl_gender = tk.Label(self.root, text="Gender", font=("goudy old style", 15), bg="white").place(x=10, y=140)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female", "Other"), state="readonly", justify=tk.CENTER, font=("goudy old style", 15))
        cmb_gender.place(x=120, y=140, width=200)
        cmb_gender.current(0)

        lbl_dob = tk.Label(self.root, text="D.O.B", font=("goudy old style", 15), bg="white").place(x=350, y=140)
        txt_dob = tk.Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 15), bg="lightyellow").place(x=430, y=140, width=240)

        lbl_contact = tk.Label(self.root, text="Contact No", font=("goudy old style", 15), bg="white").place(x=700, y=140)
        txt_contact = tk.Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow").place(x=820, y=140, width=250)

        lbl_course = tk.Label(self.root, text="Course", font=("goudy old style", 15), bg="white").place(x=10, y=180)
        self.course_list = self.fetch_courses()
        cmb_course = ttk.Combobox(self.root, textvariable=self.var_course, values=self.course_list, state="readonly", justify=tk.CENTER, font=("goudy old style", 15))
        cmb_course.place(x=120, y=180, width=200)

        lbl_admission = tk.Label(self.root, text="Admission Date", font=("goudy old style", 15), bg="white").place(x=350, y=180)
        txt_admission = tk.Entry(self.root, textvariable=self.var_admission, font=("goudy old style", 15), bg="lightyellow").place(x=500, y=180, width=170)

        lbl_state = tk.Label(self.root, text="State", font=("goudy old style", 15), bg="white").place(x=700, y=180)
        txt_state = tk.Entry(self.root, textvariable=self.var_state, font=("goudy old style", 15), bg="lightyellow").place(x=770, y=180, width=300)

        lbl_city = tk.Label(self.root, text="City", font=("goudy old style", 15), bg="white").place(x=10, y=220)
        txt_city = tk.Entry(self.root, textvariable=self.var_city, font=("goudy old style", 15), bg="lightyellow").place(x=120, y=220, width=200)

        lbl_pin = tk.Label(self.root, text="Pin Code", font=("goudy old style", 15), bg="white").place(x=350, y=220)
        txt_pin = tk.Entry(self.root, textvariable=self.var_pin, font=("goudy old style", 15), bg="lightyellow").place(x=430, y=220, width=240)

        lbl_address = tk.Label(self.root, text="Address", font=("goudy old style", 15), bg="white").place(x=700, y=220)
        self.txt_address = tk.Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_address.place(x=790, y=220, width=280, height=60)

        # === Buttons ===
        btn_save = tk.Button(self.root, text="Save", font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2", command=self.add_student).place(x=270, y=300, width=100, height=30)
        btn_update = tk.Button(self.root, text="Update", font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2", command=self.update_student).place(x=380, y=300, width=100, height=30)
        btn_delete = tk.Button(self.root, text="Delete", font=("goudy old style", 15), bg="#f44336", fg="white", cursor="hand2", command=self.delete_student).place(x=490, y=300, width=100, height=30)
        btn_clear = tk.Button(self.root, text="Clear", font=("goudy old style", 15), bg="#607d8b", fg="white", cursor="hand2", command=self.clear_fields).place(x=600, y=300, width=100, height=30)

        # === Table Frame ===
        student_frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE)
        student_frame.place(x=0, y=360, relwidth=1, height=180)

        scrolly = tk.Scrollbar(student_frame, orient=tk.VERTICAL)
        scrollx = tk.Scrollbar(student_frame, orient=tk.HORIZONTAL)

        self.student_table = ttk.Treeview(student_frame, columns=("roll", "name", "email", "gender", "dob"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        scrollx.config(command=self.student_table.xview)
        scrolly.config(command=self.student_table.yview)

        self.student_table.heading("roll", text="Roll No")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("dob", text="D.O.B")
        self.student_table["show"] = "headings"

        self.student_table.column("roll", width=100)
        self.student_table.column("name", width=100)
        self.student_table.column("email", width=100)
        self.student_table.column("gender", width=100)
        self.student_table.column("dob", width=100)

        self.student_table.pack(fill=tk.BOTH, expand=1)
        self.student_table.bind("<ButtonRelease-1>", self.get_data)

        self.show_students()

    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com|outlook\.com|vvce\.ac\.in)$'
        return re.match(pattern, email)

    def fetch_courses(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        cur.execute("SELECT name FROM course")
        data = cur.fetchall()
        con.close()
        return [row[0] for row in data]

    def create_table(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS student(
            roll TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            gender TEXT,
            dob TEXT,
            contact TEXT,
            course TEXT,
            admission TEXT,
            state TEXT,
            city TEXT,
            pin TEXT,
            address TEXT)''')
        con.commit()
        con.close()

    def add_student(self):
        required_fields = {
            "Roll No": self.var_roll.get().strip(),
            "Name": self.var_name.get().strip(),
            "Email": self.var_email.get().strip(),
            "Contact": self.var_contact.get().strip(),
        }

        if any(not val for val in required_fields.values()):
            messagebox.showerror("Error", "Please fill all required fields")
            return

        if not self.is_valid_email(self.var_email.get()):
            messagebox.showerror("Invalid Email", "Please enter a valid email address")
            return

        try:
            con = sqlite3.connect("rms.db")
            cur = con.cursor()
            cur.execute("INSERT INTO student VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                self.var_roll.get(), self.var_name.get(), self.var_email.get(), self.var_gender.get(),
                self.var_dob.get(), self.var_contact.get(), self.var_course.get(),
                self.var_admission.get(), self.var_state.get(), self.var_city.get(),
                self.var_pin.get(), self.txt_address.get("1.0", tk.END)))
            con.commit()
            messagebox.showinfo("Success", "Student added successfully")
            self.show_students()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Roll No already exists")
        finally:
            con.close()

    def update_student(self):
        required_fields = {
            "Roll No": self.var_roll.get().strip(),
            "Name": self.var_name.get().strip(),
            "Email": self.var_email.get().strip(),
            "Contact": self.var_contact.get().strip(),
        }

        if any(not val for val in required_fields.values()):
            messagebox.showerror("Error", "Please fill all required fields")
            return

        if not self.is_valid_email(self.var_email.get()):
            messagebox.showerror("Invalid Email", "Please enter a valid email address")
            return

        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        cur.execute('''UPDATE student SET name=?, email=?, gender=?, dob=?, contact=?, course=?, admission=?, state=?, city=?, pin=?, address=? WHERE roll=?''', (
            self.var_name.get(), self.var_email.get(), self.var_gender.get(), self.var_dob.get(),
            self.var_contact.get(), self.var_course.get(), self.var_admission.get(),
            self.var_state.get(), self.var_city.get(), self.var_pin.get(),
            self.txt_address.get("1.0", tk.END), self.var_roll.get()))
        con.commit()
        con.close()
        messagebox.showinfo("Success", "Student record updated")
        self.show_students()

    def delete_student(self):
        if self.var_roll.get() == "":
            messagebox.showerror("Error", "Please select a student to delete")
            return

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this student?")
        if confirm:
            try:
                con = sqlite3.connect("rms.db")
                cur = con.cursor()
                cur.execute("DELETE FROM student WHERE roll=?", (self.var_roll.get(),))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Student deleted successfully")
                self.show_students()
                self.clear_fields()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")

    def clear_fields(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_course.set("")
        self.var_admission.set("")
        self.var_state.set("")
        self.var_city.set("")
        self.var_pin.set("")
        self.txt_address.delete("1.0", tk.END)
        self.var_search.set("")
        self.show_students()

    def get_data(self, event):
        selected_item = self.student_table.focus()
        content = self.student_table.item(selected_item)
        row = content["values"]

        self.var_roll.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_dob.set(row[4])

    def show_students(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        cur.execute("SELECT roll, name, email, gender, dob FROM student")
        rows = cur.fetchall()
        self.student_table.delete(*self.student_table.get_children())
        for row in rows:
            self.student_table.insert('', tk.END, values=row)
        con.close()

    def search_student(self):
        search_term = self.var_search.get()
        if not search_term:
            messagebox.showerror("Error", "Please enter a search term.")
            return
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        query = "SELECT roll, name, email, gender, dob FROM student WHERE roll LIKE ? OR name LIKE ?"
        cur.execute(query, (f"%{search_term}%", f"%{search_term}%"))
        rows = cur.fetchall()
        self.student_table.delete(*self.student_table.get_children())
        for row in rows:
            self.student_table.insert('', tk.END, values=row)
        con.close()

if __name__ == "__main__":
    root = tk.Tk()
    obj = StudentClass(root)
    root.mainloop()

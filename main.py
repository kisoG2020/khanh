from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import csv
from datetime import datetime
import pandas as pd

def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.config(fg='grey')
    entry.bind("<FocusIn>", lambda event: clear_placeholder(entry, placeholder_text))
    entry.bind("<FocusOut>", lambda event: set_placeholder(entry, placeholder_text))

def clear_placeholder(entry, placeholder_text):
    if entry.get() == placeholder_text:
        entry.delete(0, END)
        entry.config(fg='black')

def set_placeholder(entry, placeholder_text):
    if not entry.get():
        entry.insert(0, placeholder_text)
        entry.config(fg='grey')

def save_to_csv():
    data = {
        "Mã": entry_ma.get(),
        "Tên": entry_ten.get(),
        "Ngày sinh": date_entry.get(),
        "Giới tính": "Nam" if gender_var.get() == 1 else "Nữ",
        "Đơn vị": donv.get(),
        "Số CMND": so_entry.get(),
        "Ngày cấp": dat_entry.get(),
        "Nơi cấp": S_entry.get(),
        "Chức danh": T_entry.get()
    }

    with open("employees.csv", mode="a", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(data)

    messagebox.showinfo("Thông báo", "Lưu thông tin thành công!")
    xuli()

def sinhnhat():
    try:
        today = datetime.now().strftime("%d/%m/%Y")
        employees = []
        with open("employees.csv", mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Ngày sinh'][:-5] == today[:-5]:  # So sánh ngày và tháng
                    employees.append(row)

        if employees:
            result = "Nhân viên có sinh nhật hôm nay:\n\n" + "\n".join([row['Tên'] for row in employees])
        else:
            result = "Không có nhân viên nào sinh nhật hôm nay."

        messagebox.showinfo("Kết quả", result)
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "File dữ liệu chưa được tạo!")

def exel():
    try:
        df = pd.read_csv("employees.csv", encoding="utf-8")
        df['Ngày sinh'] = pd.to_datetime(df['Ngày sinh'], format="%d/%m/%Y")
        df.sort_values(by="Ngày sinh", ascending=True, inplace=True)
        output_file = "sorted_employees.xlsx"
        df.to_excel(output_file, index=False)
        messagebox.showinfo("Thông báo", f"Xuất danh sách thành công! File: {output_file}")
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "File dữ liệu chưa được tạo!")
    except ModuleNotFoundError as e:
        messagebox.showerror("Lỗi", str(e))

def xuli():
    entry_ma.delete(0, END)
    entry_ten.delete(0, END)
    date_entry.set_date(datetime.now())
    gender_var.set(0)
    combobox.set("")
    so_entry.delete(0, END)
    dat_entry.set_date(datetime.now())
    S_entry.delete(0, END)
    T_entry.delete(0, END)

# Initialize Tkinter window
window = Tk()
window.title("Thông tin nhân viên")
window.geometry("850x400")

lbl = Label(window, text="Thông tin nhân viên", fg="black", font=("Timenewroman", 23))
lbl.grid(column=0, row=0, columnspan=4, pady=10, sticky="W")

lakh = Checkbutton(window, text="Là khách hàng")
lakh.grid(column=1, row=0, sticky="w")

lanv = Checkbutton(window, text="Là nhân viên")
lanv.grid(column=2, row=0)

# Initialize entry fields with placeholders
entry_ma = Entry(window, width=30)
entry_ma.grid(column=0, row=2, padx=5, pady=5, sticky="W")
add_placeholder(entry_ma, "Nhập mã nhân viên")

entry_ten = Entry(window, width=30, bd=2, relief="groove")
entry_ten.grid(column=1, row=2, padx=5, pady=5, sticky="w")
add_placeholder(entry_ten, "Nhập tên nhân viên")

ngay_sinh = Label(window, text="Ngày sinh", fg="black", font=("Arial", 10))
ngay_sinh.grid(column=2, row=1, sticky="W")
date_entry = DateEntry(window, width=20, foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
date_entry.grid(column=2, row=2, sticky="W")

gt = Label(window, text="Giới tính", fg="black", font=("Arial", 10))
gt.grid(column=3, row=1, sticky="W")
gender_var = IntVar()
chk3 = Radiobutton(window, text="Nam", variable=gender_var, value=1)
chk3.grid(row=2, column=3, padx=10, pady=5, sticky="W")
chk4 = Radiobutton(window, text="Nữ", variable=gender_var, value=2)
chk4.grid(row=2, column=4, padx=10, pady=5, sticky="W")

donvi = Label(window, text="Đơn vị", fg="black", font=("Arial", 10))
donvi.grid(column=0, row=3, sticky="W")
donv = StringVar()
don = ["D24CQCC01-B", "D24CQCC02-B", "D24CQCC03-B", "D24CQCC04-B", "D24CQCC05-B", "D24CQCC06-B"]
combobox = ttk.Combobox(window, textvariable=donv, values=don, width=27, font=("Arial", 12), state="readonly")
combobox.grid(row=4, column=0, padx=5, pady=5, sticky="W")

cm = Label(window, text="Số CMND", fg="black", font=("Arial", 10))
cm.grid(column=1, row=3, sticky="W")
so_entry = Entry(window, width=30)
so_entry.grid(column=1, row=4, sticky="W")
add_placeholder(so_entry, "Nhập số CMND")

ngay_cap = Label(window, text="Ngày cấp", fg="black", font=("Arial", 10))
ngay_cap.grid(column=2, row=3, sticky="W")
dat_entry = DateEntry(window, width=20, foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
dat_entry.grid(column=2, row=4, sticky="W")

chuc_danh = Label(window, text="Chức danh", fg="black", font=("Arial", 10))
chuc_danh.grid(column=0, row=5, sticky="W")
T_entry = Entry(window, width=40)
T_entry.grid(column=0, row=6, sticky="W")
add_placeholder(T_entry, "Nhập chức danh")

noi_cap = Label(window, text="Nơi cấp", fg="black", font=("Arial", 10))
noi_cap.grid(column=1, row=5, sticky="W")
S_entry = Entry(window, width=40)
S_entry.grid(column=1, row=6, sticky="W")
add_placeholder(S_entry, "Nhập nơi cấp")

btn_send = Button(window, text="Send", command=save_to_csv, width=15, height=2)
btn_send.grid(row=7, column=0, padx=10, pady=20)

btn_birthday = Button(window, text="Sinh nhật hôm nay", command=sinhnhat, width=20, height=2)
btn_birthday.grid(row=7, column=1, padx=10, pady=20)

btn_export = Button(window, text="Xuất danh sách", command=exel, width=20, height=2)
btn_export.grid(row=7, column=2, padx=10, pady=20)

window.mainloop()

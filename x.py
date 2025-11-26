# import tkinter as tk
# from tkinter import messagebox
# root = tk.Tk() 
# root.geometry("600x500")  
# root.title("Parking management System")
# root.configure(bg="black")

# label = tk.Label(root, text="🚗Parking Management System",font=("Sans-Serif", 20, "bold"), bg='black', fg='white')
# label.place(relx=0.5, rely=0.03, anchor='center')  

# Label1 = tk.Label(root, text="🏠DashBoard", font=("Sans-Serif", 18, "bold"), bg="black", fg="white")
# Label1.place(relx=0, rely=0.1, anchor='w')


# Button1 = tk.Button(root, text="🏠DashBoard", font=("Sans-Serif", 15, "bold"),width=20, bg="gray20", fg="white",command=lambda:messagebox.showinfo("Dashboard","You are viewing Vehicle dashboard"))
# Button1.place(relx=0.5, rely=0.23, anchor='center')

# Button2=tk.Button(root,text="🚗➡️Vehicle Entry",font=("Sans-Serif", 15, "bold"),width=20,bg="gray20",fg="white",command=lambda:messagebox.showinfo("Vehicle Entry", "New vehicle entry logged successfully!"))
# Button2.place(relx=0.5, rely=0.29, anchor="center")

# Button3 = tk.Button(root, text="🚗⬅️Vehicle Exit", font=("Sans-Serif", 15, "bold"),width=20,bg="gray20",fg="white",command=lambda:messagebox.showinfo("Vehicle Exit","Vehicle exited successfully"))
# Button3.place(relx=0.5,rely=0.35,anchor="center")

# Button4 = tk.Button(root, text="✅❌Check Availabity", font=("Sans-Serif", 15, "bold"),width=20,bg="gray20",fg="white",command=lambda:messagebox.showinfo("Checking parking slot availability"))
# Button4.place(relx=0.5,rely=0.41,anchor="center")


# footer = tk.Label(
#     root,
#     text="© 2025 Parking Management System",
#     font=("Sans-Serif", 9),
#     bg="black",
#     fg="gray"
# )
# footer.place(relx=0.5, rely=0.95, anchor='center')
# root.mainloop()  




# import tkinter as tk
# from tkinter import messagebox
# root = tk.Tk() 
# root.geometry("600x500")  
# root.title("Parking management System")
# root.configure(bg="black")

# label = tk.Label(root, text="🚗Parking Management System",font=("Sans-Serif", 20, "bold"), bg='black', fg='white')
# label.place(relx=0.5, rely=0.03, anchor='center')  

# Label1 = tk.Label(root, text="Main Menu", font=("Sans-Serif", 18, "bold"), bg="black", fg="white")
# Label1.place(relx=0, rely=0.1, anchor='w')


# Button1 = tk.Button(root, text="🏠DashBoard", font=("Sans-Serif", 15, "bold"),width=20, bg="gray20", fg="white",command=lambda:messagebox.showinfo("Dashboard","You are viewing Vehicle dashboard"))
# Button1.Button1 = tk.Button(root, text="🏠DashBoard", font=("Sans-Serif", 15, "bold"),width=20, bg="gray20", fg="white",command=lambda:messagebox.showinfo("Dashboard","You are viewing Vehicle dashboard"))
# Button1.place(relx=0.098, rely=0.23, anchor='center')

# Button2=tk.Button(root,text="🚗➡️Vehicle Entry",font=("Sans-Serif", 15, "bold"),width=20,bg="gray20",fg="white",command=lambda:messagebox.showinfo("Vehicle Entry", "New vehicle entry logged successfully!"))
# Button2.place(relx=0, rely=0.29, anchor="w")

# Button3 = tk.Button(root, text="🚗⬅️Vehicle Exit", font=("Sans-Serif", 15, "bold"),width=20,bg="gray20",fg="white",command=lambda:messagebox.showinfo("Vehicle Exit","Vehicle exited successfully"))
# Button3.place(relx=0,rely=0.35,anchor="w")

# Button4 = tk.Button(root, text="✅❌Check Availabity", font=("Sans-Serif", 15, "bold"),width=20,bg="gray20",fg="white",command=lambda:messagebox.showinfo("Checking parking slot availability"))
# Button4.place(relx=0,rely=0.41,anchor="w")

# E1 = tk.Entry(root,text="Car Number", bg='white', fg='red', font=("Sans-Serif", 10))
# E1.place(relx=0.5, rely=0.23, anchor='w')


# E2 = tk.Entry(root,text="Car Entry Time", bg='white', fg='red', font=("Sans-Serif", 10))
# E2.place(relx=0.5, rely=0.27, anchor='w')


# Button5=tk.Button(root,text="Submit",font=('sans serif',10),bg='white',fg='black',command=lambda:config(entry1.get(),entry2.get))
# Button5.place(relx=0.55,rely=0.33,anchor='w')

# footer = tk.Label(root,text="© 2025 Parking Management System",font=("Sans-Serif", 9),bg="black",fg="gray"
# )
# footer.place(relx=0.5, rely=0.95, anchor='center')
# root.mainloop() 


import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.geometry("600x500")
root.title("Parking Management System")
root.configure(bg="black")


label = tk.Label(root, text="🚗 Parking Management System",font=("Sans-Serif", 20, "bold"), bg='black', fg='white')
label.place(relx=0.5, rely=0.03, anchor='center')

Label1 = tk.Label(root, text="Main Menu",font=("Sans-Serif", 18, "bold"), bg="black", fg="white")
Label1.place(relx=0, rely=0.1, anchor='w')


Button1 = tk.Button(root, text="🏠 DashBoard", font=("Sans-Serif", 15, "bold"),width=20, bg="gray20", fg="white",
                    command=lambda: messagebox.showinfo("Dashboard", "You are viewing Vehicle dashboard"))
Button1.place(relx=0.098, rely=0.23, anchor='center')

Button2 = tk.Button(root, text="🚗 ➡️ Vehicle Entry", font=("Sans-Serif", 15, "bold"),width=20, bg="gray20", fg="white",
                    command=lambda: messagebox.showinfo("Vehicle Entry", "New vehicle entry logged successfully!"))
Button2.place(relx=0, rely=0.29, anchor="w")

Button3 = tk.Button(root, text="🚗 ⬅️ Vehicle Exit", font=("Sans-Serif", 15, "bold"),width=20, bg="gray20", fg="white",
                    command=lambda: messagebox.showinfo("Vehicle Exit", "Vehicle exited successfully"))
Button3.place(relx=0, rely=0.35, anchor="w")

Button4 = tk.Button(root, text="✅❌ Check Availability", font=("Sans-Serif", 15, "bold"),width=20, bg="gray20", fg="white",
                    command=lambda: messagebox.showinfo("Availability", "Checking parking slot availability..."))
Button4.place(relx=0, rely=0.41, anchor="w")

car_label = tk.Label(root, text="Car Number:", bg="black", fg="white", font=("Sans-Serif", 12, "bold"))
car_label.place(relx=0.5, rely=0.20, anchor='w')

E1 = tk.Entry(root, bg='white', fg='red', font=("Sans-Serif", 10))
E1.place(relx=0.5, rely=0.23, anchor='w')


time_label = tk.Label(root, text="Car Entry Time:", bg="black", fg="white", font=("Sans-Serif", 12, "bold"))
time_label.place(relx=0.5, rely=0.27, anchor='w')

E2 = tk.Entry(root, bg='white', fg='red', font=("Sans-Serif", 10))
E2.place(relx=0.5, rely=0.31, anchor='w')

Button5 = tk.Button(root, text="Submit", font=('Sans-Serif', 10, 'bold'),bg='white', fg='black',command=lambda: print(f"Car Number: {E1.get()} | Entry Time: {E2.get()}"))
Button5.place(relx=0.55, rely=0.36, anchor='w')

Label2 = tk.Label(root, text="© 2025 Parking Management System",
                  font=("Sans-Serif", 9), bg="black", fg="gray")
Label2.place(relx=0.5, rely=0.95, anchor='center')

root.mainloop()


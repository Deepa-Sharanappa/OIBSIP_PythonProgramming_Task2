import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os

current_user = None
selected_profile = None

# ---------------- HEALTH SUGGESTION ---------------- #

def get_health_suggestion(bmi):

    if bmi < 18.5:
        return "Increase calories, eat protein foods, strength training."

    elif bmi < 25:
        return "Maintain balanced diet and regular exercise."

    elif bmi < 30:
        return "Reduce sugar intake, cardio exercises recommended."

    else:
        return "Consult doctor, follow structured diet and exercise."


# ---------------- DIET PLAN GENERATOR ---------------- #

def get_diet_plan(bmi):

    if bmi < 18.5:
        return (
            "Breakfast: Oatmeal + Banana + Milk\n"
            "Lunch: Rice + Chicken + Vegetables\n"
            "Dinner: Pasta + Eggs\n"
            "Snacks: Nuts + Smoothies"
        )

    elif bmi < 25:
        return (
            "Breakfast: Eggs + Whole grain toast\n"
            "Lunch: Brown rice + Fish + Salad\n"
            "Dinner: Grilled chicken + Veggies\n"
            "Snacks: Fruits + Yogurt"
        )

    elif bmi < 30:
        return (
            "Breakfast: Oats + Green tea\n"
            "Lunch: Grilled chicken salad\n"
            "Dinner: Vegetable soup\n"
            "Snacks: Apple or almonds"
        )

    else:
        return (
            "Breakfast: Fruit bowl + Green tea\n"
            "Lunch: Quinoa salad\n"
            "Dinner: Steamed vegetables\n"
            "Snacks: Nuts"
        )


# ---------------- REGISTER ---------------- #

def register():

    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "All fields required")
        return

    if os.path.exists("users.csv"):
        with open("users.csv", "r") as file:
            for row in csv.reader(file):
                if row[0] == username:
                    messagebox.showerror("Error", "User already exists")
                    return

    with open("users.csv", "a", newline="") as file:
        csv.writer(file).writerow([username, password])

    messagebox.showinfo("Success", "Registration successful")


# ---------------- LOGIN ---------------- #

def login():

    global current_user

    username = username_entry.get()
    password = password_entry.get()

    if not os.path.exists("users.csv"):
        messagebox.showerror("Error", "No users registered")
        return

    with open("users.csv", "r") as file:
        for row in csv.reader(file):

            if row[0] == username and row[1] == password:

                current_user = username
                open_profile_manager()
                return

    messagebox.showerror("Error", "Invalid credentials")


# ---------------- PROFILE MANAGER ---------------- #

def open_profile_manager():

    login_window.destroy()

    profile_window = tk.Tk()
    profile_window.title("Profile Manager")
    profile_window.geometry("420x420")
    profile_window.configure(bg="#F4F8FB")

    tk.Label(profile_window,
             text="Profile Manager",
             font=("Segoe UI", 16, "bold"),
             bg="#F4F8FB").pack(pady=10)

    name_entry = tk.Entry(profile_window)
    name_entry.pack(pady=5)
    name_entry.insert(0, "Profile Name")

    age_entry = tk.Entry(profile_window)
    age_entry.pack(pady=5)
    age_entry.insert(0, "Age")

    gender_entry = tk.Entry(profile_window)
    gender_entry.pack(pady=5)
    gender_entry.insert(0, "Gender")

    def create_profile():

        name = name_entry.get()
        age = age_entry.get()
        gender = gender_entry.get()

        if name == "" or age == "" or gender == "":
            messagebox.showerror("Error", "Fill all fields")
            return

        filename = f"{current_user}_profiles.csv"

        with open(filename, "a", newline="") as file:
            csv.writer(file).writerow([name, age, gender])

        messagebox.showinfo("Success", "Profile created")
        load_profiles()

    def load_profiles():

        listbox.delete(0, tk.END)

        filename = f"{current_user}_profiles.csv"

        if os.path.exists(filename):

            with open(filename, "r") as file:

                for row in csv.reader(file):
                    listbox.insert(tk.END, row[0])

    def select_profile():

        global selected_profile

        selected_profile = listbox.get(tk.ACTIVE)

        if selected_profile == "":
            messagebox.showerror("Error", "Select profile")
            return

        open_dashboard(profile_window)

    tk.Button(profile_window, text="Create Profile",
              command=create_profile,
              bg="#4CAF50", fg="white").pack(pady=5)

    listbox = tk.Listbox(profile_window)
    listbox.pack(pady=10)

    tk.Button(profile_window, text="Open Profile",
              command=select_profile,
              bg="#2196F3", fg="white").pack(pady=5)

    load_profiles()

    profile_window.mainloop()


# ---------------- DASHBOARD ---------------- #

def open_dashboard(prev_window):

    prev_window.destroy()

    dashboard = tk.Tk()
    dashboard.title("Health Dashboard")
    dashboard.geometry("450x500")
    dashboard.configure(bg="#EEF3F7")

    card = tk.Frame(dashboard, bg="white", bd=0)
    card.place(relx=0.5, rely=0.5, anchor="center",
               width=350, height=420)

    tk.Label(card,
             text=f"{selected_profile} BMI Tracker",
             font=("Segoe UI", 16, "bold"),
             bg="white").pack(pady=10)

    tk.Label(card, text="Weight (kg)", bg="white").pack()
    weight_entry = tk.Entry(card)
    weight_entry.pack(pady=5)

    tk.Label(card, text="Height (m)", bg="white").pack()
    height_entry = tk.Entry(card)
    height_entry.pack(pady=5)

    result_label = tk.Label(card, text="", bg="white",
                            font=("Segoe UI", 10))
    result_label.pack(pady=10)

    def calculate_bmi():

        try:

            weight = float(weight_entry.get())
            height = float(height_entry.get())

            bmi = weight / (height ** 2)

            if bmi < 18.5:
                category = "Underweight"
            elif bmi < 25:
                category = "Normal"
            elif bmi < 30:
                category = "Overweight"
            else:
                category = "Obese"

            suggestion = get_health_suggestion(bmi)
            diet = get_diet_plan(bmi)

            result_label.config(
                text=f"BMI: {bmi:.2f}\nCategory: {category}\n\nSuggestion:\n{suggestion}\n\nDiet Plan:\n{diet}"
            )

            filename = f"{current_user}_{selected_profile}_bmi.csv"

            with open(filename, "a", newline="") as file:
                csv.writer(file).writerow(
                    [datetime.now(), weight, height, bmi])

        except:
            messagebox.showerror("Error", "Invalid input")

    def show_graph():

        try:

            filename = f"{current_user}_{selected_profile}_bmi.csv"

            data = pd.read_csv(filename,
                               header=None,
                               names=["Date", "Weight", "Height", "BMI"])

            data["Date"] = pd.to_datetime(data["Date"])

            plt.figure()
            plt.plot(data["Date"], data["BMI"])
            plt.xlabel("Date")
            plt.ylabel("BMI")
            plt.title("BMI Trend")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

        except:
            messagebox.showerror("Error", "No data available")

    tk.Button(card,
              text="Calculate BMI",
              command=calculate_bmi,
              bg="#1976D2",
              fg="white").pack(pady=8)

    tk.Button(card,
              text="Show BMI Trend",
              command=show_graph,
              bg="#4CAF50",
              fg="white").pack(pady=8)

    dashboard.mainloop()


# ---------------- LOGIN WINDOW ---------------- #

login_window = tk.Tk()
login_window.title("Health Monitor Login")
login_window.geometry("350x260")
login_window.configure(bg="#F4F8FB")

tk.Label(login_window,
         text="Health Monitor Login",
         font=("Segoe UI", 16, "bold"),
         bg="#F4F8FB").pack(pady=10)

tk.Label(login_window, text="Username",
         bg="#F4F8FB").pack()

username_entry = tk.Entry(login_window)
username_entry.pack(pady=5)

tk.Label(login_window, text="Password",
         bg="#F4F8FB").pack()

password_entry = tk.Entry(login_window, show="*")
password_entry.pack(pady=5)

tk.Button(login_window,
          text="Login",
          command=login,
          bg="#2196F3",
          fg="white").pack(pady=6)

tk.Button(login_window,
          text="Register",
          command=register,
          bg="#4CAF50",
          fg="white").pack(pady=6)

login_window.mainloop()

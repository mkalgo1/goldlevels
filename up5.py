import tkinter as tk
from tkinter import ttk, filedialog
import tkinter.messagebox as messagebox
import math
import pyperclip
import sys
import threading
import random

# --- Styles Configuration ---
def configure_styles():
    """Configures the ttk styles for the application."""
    s = ttk.Style()
    
    # Configure a dark theme for frames
    s.configure("Dark.TFrame", background="black")
    s.configure("TNotebook", background="black")
    s.configure("TNotebook.Tab", background="black", foreground="white", font=("Arial", 10, "bold"))
    s.map("TNotebook.Tab", background=[("selected", "#333333")])

    # Main Program Buttons
    s.configure("Yellow.TButton",
                background="#FFD700",  # Gold/Yellow
                foreground="black",
                font=("Arial", 12, "bold"),
                borderwidth=0,
                relief="flat",
                padding=[15, 8]
               )
    s.map("Yellow.TButton",
          background=[("active", "#CCCC00")] # Darker yellow on hover
          )

    # Mini-Program Buttons (Semi-transparent effect)
    s.configure("TransparentYellow.TButton",
                background="#E0C000",  # Lighter yellow to simulate transparency
                foreground="black",
                font=("Arial", 12, "bold"),
                borderwidth=2,
                relief="solid",
                bordercolor="black",
                padding=[15, 8]
               )
    s.map("TransparentYellow.TButton",
          background=[("active", "#CCCC00")],
          foreground=[("active", "black")]
          )

# --- Program Classes ---

class GannBoxProgram(tk.Frame):
    """A Frame containing the GANN BOX calculation program widgets."""
    def __init__(self, master=None):
        super().__init__(master, bg='#333333') # Semi-transparent gray for background effect
        self.last_result = ""
        self.create_widgets()

    def sum_digits(self, n):
        s = sum(int(digit) for digit in str(n))
        return s if s < 10 else self.sum_digits(s)

    def get_gate_value(self, n):
        if n in [1, 4, 7]:
            return 12
        elif n in [2, 5, 8]:
            return 15
        elif n in [3, 6, 9]:
            return 18
        else:
            return None

    def calculate_levels(self, price_level, sentiment):
        try:
            lvl = int(price_level)
            if len(str(lvl)) < 2:
                messagebox.showerror("Invalid Input", "Please enter a price with at least 2 digits.")
                return None

            single_digit_sum = self.sum_digits(lvl)
            gate_value = self.get_gate_value(single_digit_sum)

            if gate_value is None:
                messagebox.showerror("Invalid Input", "The sum of digits did not match any gate.")
                return None

            results = []
            current_lvl = lvl
            for i in range(10):
                if sentiment == 'bullish':
                    current_lvl += gate_value
                else:
                    current_lvl -= gate_value
                results.append(current_lvl)
            return results

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the price.")
            return None

    def create_widgets(self):
        main_frame = tk.Frame(self, padx=20, pady=20, bg=self['bg'])
        main_frame.pack(expand=True, fill="both")

        tk.Label(main_frame, text="Enter Price Level:", bg=self['bg'], fg="white", font=("Arial", 12)).pack(pady=5)
        self.price_entry = tk.Entry(main_frame, font=("Arial", 12), width=20, borderwidth=2, relief="solid")
        self.price_entry.pack(pady=5)

        button_frame = tk.Frame(main_frame, bg=self['bg'])
        button_frame.pack(pady=10)

        bullish_button = ttk.Button(
            button_frame,
            text="Bullish",
            command=lambda: self.update_results('bullish'),
            style="TransparentYellow.TButton"
        )
        bullish_button.pack(side="left", padx=10)

        bearish_button = ttk.Button(
            button_frame,
            text="Bearish",
            command=lambda: self.update_results('bearish'),
            style="TransparentYellow.TButton"
        )
        bearish_button.pack(side="right", padx=10)

        self.results_text = tk.Text(main_frame, height=12, width=30, font=("Arial", 12), wrap=tk.WORD, state=tk.DISABLED, bg=self['bg'], fg="white")
        self.results_text.pack(pady=10)

        copy_button = ttk.Button(
            main_frame,
            text="Copy Results",
            command=self.copy_result,
            style="TransparentYellow.TButton"
        )
        copy_button.pack(pady=5)

    def update_results(self, sentiment):
        price_level = self.price_entry.get()
        calculated_levels = self.calculate_levels(price_level, sentiment)
        
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        
        if calculated_levels:
            results_string = f"{sentiment.capitalize()} Levels:\n"
            for i, level in enumerate(calculated_levels, 1):
                results_string += f"Level {i}: {level}\n"
            self.last_result = results_string
            self.results_text.insert(tk.END, results_string)
        else:
            self.last_result = ""

        self.results_text.config(state=tk.DISABLED)

    def copy_result(self):
        if self.last_result:
            try:
                pyperclip.copy(self.last_result)
                messagebox.showinfo("Copied", "Results copied to clipboard!")
            except pyperclip.PyperclipException:
                messagebox.showerror("Copy Error", "Could not copy to clipboard. Ensure pyperclip is configured.")

class Lvl369Program(tk.Frame):
    """A Frame containing the 369 LVL calculation program widgets."""
    def __init__(self, master=None):
        super().__init__(master, bg='#333333') # Semi-transparent gray
        self.last_result = ""
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self, padx=20, pady=20, bg=self['bg'])
        main_frame.pack(expand=True, fill="both")

        tk.Label(main_frame, text="Enter Price Level:", bg=self['bg'], fg="white").pack(pady=5)
        self.entry_price = tk.Entry(main_frame, width=30, font=("Arial", 12))
        self.entry_price.pack(pady=5)

        button_frame = tk.Frame(main_frame, bg=self['bg'])
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Bullish", command=self.bullish_action, style="TransparentYellow.TButton").pack(side="left", padx=10)
        ttk.Button(button_frame, text="Bearish", command=self.bearish_action, style="TransparentYellow.TButton").pack(side="right", padx=10)

        self.result_label = tk.Label(main_frame, text="Waiting for input...", bg=self['bg'], fg="white", font=("Arial", 14, "bold"))
        self.result_label.pack(expand=True, anchor="center", pady=10)
        
        copy_button = ttk.Button(
            main_frame,
            text="Copy Result",
            command=self.copy_result,
            style="TransparentYellow.TButton"
        )
        copy_button.pack(pady=5)

    def calculate_bullish(self, price_level):
        try:
            price = int(price_level)
            if len(str(price)) < 2:
                messagebox.showerror("Invalid Input", "Please enter a valid price level (a number with at least 2 digits).")
                return None, None, None
            
            last_two_digits = price % 100
            
            new_last_two_digits_3 = last_two_digits + 3
            level_3 = (price // 100) * 100 + new_last_two_digits_3
            
            new_last_two_digits_6 = new_last_two_digits_3 + 6
            level_6 = (price // 100) * 100 + new_last_two_digits_6
            
            new_last_two_digits_9 = new_last_two_digits_6 + 9
            level_9 = (price // 100) * 100 + new_last_two_digits_9
            
            return level_3, level_6, level_9
        
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid price level (a number with at least 2 digits).")
            return None, None, None

    def calculate_bearish(self, price_level):
        try:
            price = int(price_level)
            if len(str(price)) < 2:
                messagebox.showerror("Invalid Input", "Please enter a valid price level (a number with at least 2 digits).")
                return None, None, None
                
            last_two_digits = price % 100
            
            new_last_two_digits_3 = last_two_digits - 3
            level_3 = (price // 100) * 100 + new_last_two_digits_3
            
            new_last_two_digits_6 = new_last_two_digits_3 - 6
            level_6 = (price // 100) * 100 + new_last_two_digits_6
            
            new_last_two_digits_9 = new_last_two_digits_6 - 9
            level_9 = (price // 100) * 100 + new_last_two_digits_9
            
            return level_3, level_6, level_9
        
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid price level (a number with at least 2 digits).")
            return None, None, None
    
    def copy_result(self):
        if self.last_result:
            try:
                pyperclip.copy(self.last_result)
                messagebox.showinfo("Copied", "Results copied to clipboard!")
            except pyperclip.PyperclipException:
                messagebox.showerror("Copy Error", "Could not copy to clipboard. Ensure pyperclip is configured.")

    def bullish_action(self):
        price_level = self.entry_price.get()
        level_3, level_6, level_9 = self.calculate_bullish(price_level)
        if level_3 is not None:
            self.last_result = f"Level 3: {level_3}\nLevel 6: {level_6}\nLevel 9: {level_9}"
            self.result_label.config(text=self.last_result)

    def bearish_action(self):
        price_level = self.entry_price.get()
        level_3, level_6, level_9 = self.calculate_bearish(price_level)
        if level_3 is not None:
            self.last_result = f"Level 3: {level_3}\nLevel 6: {level_6}\nLevel 9: {level_9}"
            self.result_label.config(text=self.last_result)


class RevLvlProgram(tk.Frame):
    """A Frame containing the REV LVL calculation program widgets."""
    def __init__(self, master=None):
        super().__init__(master, bg='#333333') # Semi-transparent gray
        self.last_result = ""
        self.create_widgets()

    def create_widgets(self):
        canvas = tk.Canvas(self, width=100, height=100, bg=self['bg'], highlightthickness=0)
        canvas.pack(pady=10)
        canvas.create_text(
            50, 50, text="$", font=("Arial", 60, "bold"), fill="white"
        )

        price_label = tk.Label(self, text="Enter the price level:", bg=self['bg'], fg="white", font=("Arial", 12))
        price_label.pack(pady=5)

        self.price_entry = tk.Entry(self, font=("Arial", 12), width=20, borderwidth=2, relief="solid")
        self.price_entry.pack(pady=5)

        button_frame = tk.Frame(self, bg=self['bg'])
        button_frame.pack(pady=10)

        bullish_button = ttk.Button(
            button_frame,
            text="Bullish",
            command=self.calculate_bullish,
            style="TransparentYellow.TButton"
        )
        bullish_button.pack(side="left", padx=10)

        bearish_button = ttk.Button(
            button_frame,
            text="Bearish",
            command=self.calculate_bearish,
            style="TransparentYellow.TButton"
        )
        bearish_button.pack(side="right", padx=10)

        self.result_label = tk.Label(self, text="Waiting for input...", bg=self['bg'], fg="white", font=("Arial", 14, "bold"))
        self.result_label.pack(expand=True, anchor="center", pady=10)
    
    def calculate_bullish(self):
        try:
            price = float(self.price_entry.get())
            if price < 0:
                messagebox.showerror("Invalid Input", "Price cannot be negative.")
                return

            x = math.sqrt(price)
            y = x + 2
            final_price = y ** 2
            self.last_result = f"Final Bullish Price: {final_price:.2f}"
            self.result_label.config(text=self.last_result)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the price.")

    def calculate_bearish(self):
        try:
            price = float(self.price_entry.get())
            if price < 0:
                messagebox.showerror("Invalid Input", "Price cannot be negative.")
                return

            x = math.sqrt(price)
            y = x - 2
            final_price = y ** 2
            self.last_result = f"Final Bearish Price: {final_price:.2f}"
            self.result_label.config(text=self.last_result)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the price.")

class MiddleLProgram(tk.Frame):
    """A Frame containing the Middle L calculation program widgets."""
    def __init__(self, master=None):
        super().__init__(master, bg='#333333') # Semi-transparent gray
        self.last_result = ""
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self, padx=20, pady=20, bg=self['bg'])
        frame.pack(expand=True)

        tk.Label(frame, text="Price of High Custom Label:", bg=self['bg'], fg="white").pack(pady=(0, 5))
        self.entry_high = tk.Entry(frame, width=20, font=("Arial", 12))
        self.entry_high.pack(pady=(0, 10))

        tk.Label(frame, text="Price of Low Custom Label:", bg=self['bg'], fg="white").pack(pady=(0, 5))
        self.entry_low = tk.Entry(frame, width=20, font=("Arial", 12))
        self.entry_low.pack(pady=(0, 10))

        calculate_button = ttk.Button(
            frame,
            text="Calculate",
            command=self.calculate_and_display,
            style="TransparentYellow.TButton"
        )
        calculate_button.pack(pady=(10, 15))

        self.result_label = tk.Label(frame, text="Result: ", font=("Arial", 12, "bold"),
                                     padx=10, pady=10, relief="groove", bd=2, bg="#555555", fg="white")
        self.result_label.pack(side=tk.LEFT, padx=(0, 5))

        self.copy_button = ttk.Button(
            frame,
            text="Copy",
            command=self.copy_result,
            style="TransparentYellow.TButton"
        )
        self.copy_button.pack(side=tk.RIGHT)

    def calculate_and_display(self):
        try:
            price_high = float(self.entry_high.get())
            price_low = float(self.entry_low.get())

            if price_high < 0 or price_low < 0:
                messagebox.showerror("Invalid Input", "Prices cannot be negative.")
                return

            result = math.sqrt(price_high * price_low)
            self.last_result = f"Result: {result:.2f}"
            self.result_label.config(text=self.last_result)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")

    def copy_result(self):
        if self.last_result:
            try:
                result_value = self.last_result.split(": ")[1]
                pyperclip.copy(result_value)
                messagebox.showinfo("Copied", f"'{result_value}' copied to clipboard!")
            except (IndexError, pyperclip.PyperclipException):
                messagebox.showerror("Copy Error", "Could not copy to clipboard. Ensure pyperclip is configured.")

class HowToUseProgram(tk.Frame):
    """A frame to display the "how to use" instructions."""
    def __init__(self, master=None):
        super().__init__(master, bg='#333333')
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self, padx=20, pady=20, bg=self['bg'])
        main_frame.pack(expand=True, fill="both")

        instructions_text = """
How to Use the Programs:

1- GANN BOX:
   Just bring a high or low from a 1-hour timeframe (1h TF), copy/paste the price, and put the results on your chart to see how price respects these levels.

2- 369 LVL:
   Same as Gann Box levels, but these levels are for short-term and scalping.

3- REV LVL:
   This method gives you a level where the price is likely to reverse. For example, you can use a high or low from the London session.

4- MID LVL:
   You can use this to scalp retracements. For example, bring a high and low from a 15-minute timeframe (15mins TF) and paste those prices into the program to see how the price reacts to the result.

For more information, contact me on Instagram:
https://www.instagram.com/mk_algo1
"""

        text_widget = tk.Text(
            main_frame,
            wrap=tk.WORD,
            font=("Arial", 12),
            bg=self['bg'],
            fg="white",
            relief="flat",
            state=tk.NORMAL
        )
        text_widget.insert(tk.END, instructions_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(expand=True, fill="both", padx=10, pady=10)


# --- Main Application ---
class Application(tk.Frame):
    """
    A GUI application class that manages all program functionalities
    within a single window, using a central display area.
    """
    def __init__(self, master=None):
        super().__init__(master, bg='black')
        self.master = master
        self.master.title("GANN PROGRAMS")
        self.master.state('zoomed')

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)

        self.grid(row=0, column=0, columnspan=2, rowspan=2, sticky='nsew')
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Main background canvas for stars
        self.bg_canvas = tk.Canvas(self, bg='black', highlightthickness=0)
        self.bg_canvas.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nsew')
        
        # Display frame for programs (now centered)
        self.display_frame = tk.Frame(self.bg_canvas, bg='#333333', relief='raised', borderwidth=2)
        
        self.active_frame = None
        self.create_widgets()
        self.draw_stars()
        
    def draw_stars(self):
        """Draws a random pattern of stars on the background canvas."""
        self.bg_canvas.delete("stars")
        width = self.bg_canvas.winfo_width()
        height = self.bg_canvas.winfo_height()
        
        num_stars = 200
        for _ in range(num_stars):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(1, 3)
            color = random.choice(["#FFFFCC", "#E0E0E0", "#FFD700"]) # Pale yellow, light gray, gold
            self.bg_canvas.create_oval(x, y, x + size, y + size, fill=color, outline=color, tags="stars")
            
    def create_widgets(self):
        """
        Create all the buttons and layout them in the window using grid.
        """
        program_frame = tk.Frame(self, bg='black')
        program_frame.grid(row=0, column=0, sticky='nsw', padx=20, pady=20)

        # Style the main program buttons
        btn_style = {
            "style": "Yellow.TButton",
        }

        btn_gann_box = ttk.Button(
            program_frame,
            text="GANN BOX",
            command=self.show_gann_box,
            **btn_style
        )
        btn_gann_box.pack(pady=5, expand=True)
        self.btn_gann_box = btn_gann_box

        btn_369_lvl = ttk.Button(
            program_frame,
            text="369 LVL",
            command=self.show_lvl_369,
            **btn_style
        )
        btn_369_lvl.pack(pady=5, expand=True)
        self.btn_369_lvl = btn_369_lvl

        btn_rev_lvl = ttk.Button(
            program_frame,
            text="REV LVL",
            command=self.show_rev_lvl,
            **btn_style
        )
        btn_rev_lvl.pack(pady=5, expand=True)
        self.btn_rev_lvl = btn_rev_lvl

        btn_middle_l = ttk.Button(
            program_frame,
            text="MIDDLE L",
            command=self.show_middle_l,
            **btn_style
        )
        btn_middle_l.pack(pady=5, expand=True)
        self.btn_middle_l = btn_middle_l
        
        # Frame for "how to use" button in the bottom left
        instructions_frame = tk.Frame(self, bg='black')
        instructions_frame.grid(row=1, column=0, sticky='sw', padx=20, pady=20)

        btn_how_to_use = ttk.Button(
            instructions_frame,
            text="how to use",
            command=self.show_instructions,
            style="Yellow.TButton"
        )
        btn_how_to_use.pack()

        # Styling for control buttons
        control_frame = tk.Frame(self, bg='black')
        control_frame.grid(row=1, column=1, sticky='se', padx=20, pady=20)

        btn_clear = ttk.Button(
            control_frame,
            text="clear",
            style="Yellow.TButton",
            command=self.clear_action,
        )
        btn_clear.pack(side=tk.LEFT, padx=5)

        btn_save_file = ttk.Button(
            control_frame,
            text="save file",
            style="Yellow.TButton",
            command=self.save_file_action,
        )
        btn_save_file.pack(side=tk.LEFT, padx=5)

        btn_exit = ttk.Button(
            control_frame,
            text="exit",
            style="Yellow.TButton",
            command=self.exit_app,
        )
        btn_exit.pack(side=tk.LEFT, padx=5)

    def show_program(self, program_class):
        """
        Clears the display frame and shows the new program.
        """
        # Destroy existing widgets in the display frame
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        # Place the display frame in the center of the canvas
        self.display_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.5, relheight=0.5)

        # Create and pack the new program frame
        self.active_frame = program_class(self.display_frame)
        self.active_frame.pack(expand=True, fill='both')

    def show_gann_box(self):
        self.show_program(GannBoxProgram)

    def show_lvl_369(self):
        self.show_program(Lvl369Program)

    def show_rev_lvl(self):
        self.show_program(RevLvlProgram)

    def show_middle_l(self):
        self.show_program(MiddleLProgram)
    
    def show_instructions(self):
        self.show_program(HowToUseProgram)

    def clear_action(self):
        self.display_frame.place_forget()
        self.active_frame = None
        messagebox.showinfo("Clear", "Display cleared.")

    def save_file_action(self):
        if not self.active_frame or not hasattr(self.active_frame, 'last_result') or not self.active_frame.last_result:
            messagebox.showerror("Save Error", "No results to save. Please perform a calculation first.")
            return

        results_to_save = self.active_frame.last_result
        if isinstance(results_to_save, bytes):
              results_to_save = results_to_save.decode("utf-8")
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="gann_results.txt"
        )

        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(results_to_save)
                messagebox.showinfo("Success", f"Results successfully saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"An error occurred while saving the file: {e}")

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    configure_styles()
    app = Application(master=root)
    app.mainloop()

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from gurobipy import Model, GRB
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle
import json
from tkinter import filedialog

# Set the appearance mode and default color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class CoveringProblemApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Covering Problem Solver")
        self.geometry("800x900")

        # Create main frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main container
        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        # Demand Points Input
        self.demand_count_label = ctk.CTkLabel(self.main_frame, text="Number of Demand Points:")
        self.demand_count_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.demand_count_entry = ctk.CTkEntry(self.main_frame, width=250)
        self.demand_count_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Facility Points Input
        self.facility_count_label = ctk.CTkLabel(self.main_frame, text="Number of Facilities:")
        self.facility_count_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.facility_count_entry = ctk.CTkEntry(self.main_frame, width=250)
        self.facility_count_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Generate Inputs Button
        self.generate_button = ctk.CTkButton(
            self.main_frame, 
            text="Generate Inputs", 
            command=self.generate_inputs,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.generate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Frames for dynamic inputs
        self.demand_frame = ctk.CTkScrollableFrame(self.main_frame, width=400, height=200)
        self.demand_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.facility_frame = ctk.CTkScrollableFrame(self.main_frame, width=400, height=200)
        self.facility_frame.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

        # Service Level Input
        self.service_level_label = ctk.CTkLabel(self.main_frame, text="Level of Service (S):")
        self.service_level_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.service_level_entry = ctk.CTkEntry(self.main_frame, width=250)
        self.service_level_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # Problem Type Selection
        self.problem_type_label = ctk.CTkLabel(self.main_frame, text="Problem Type:")
        self.problem_type_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.problem_type_var = ctk.StringVar(value="Set Covering")
        self.problem_type_menu = ctk.CTkComboBox(
            self.main_frame, 
            values=["Set Covering", "Max Covering"],
            variable=self.problem_type_var,
            state="readonly",
            width=250,
            command=self.toggle_max_facilities
        )
        self.problem_type_menu.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        # Max Facilities Input (for Max Covering)
        self.max_facilities_label = ctk.CTkLabel(self.main_frame, text="Max Facilities (p):")
        self.max_facilities_entry = ctk.CTkEntry(self.main_frame, width=250)

        # Solve Button
        self.solve_button = ctk.CTkButton(
            self.main_frame, 
            text="Solve", 
            command=self.solve_problem,
            fg_color="#2196F3",
            hover_color="#1976D2"
        )
        self.solve_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.load_test_case_button = ctk.CTkButton(
            self.main_frame, 
            text="Load Test Case", 
            command=self.load_test_case,
            fg_color="#FFC107",
            hover_color="#FFA000"
        )
        self.load_test_case_button.grid(row=2, column=1, padx=10, pady=10)

        # Result Display
        self.result_label = ctk.CTkTextbox(self.main_frame, width=760, height=200)
        self.result_label.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        # Initialize input trackers
        self.demand_entries = []
        self.facility_entries = []

    def load_test_case(self):
        try:
            # Open file dialog to select JSON file
            file_path = filedialog.askopenfilename(
                title="Select Test Case JSON File",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if not file_path:
                return  # User cancelled file selection

            # Read the JSON file
            with open(file_path, 'r') as file:
                test_case = json.load(file)

            # Clear existing inputs
            self.demand_count_entry.delete(0, tk.END)
            self.facility_count_entry.delete(0, tk.END)
            self.service_level_entry.delete(0, tk.END)

            # Set basic parameters
            self.demand_count_entry.insert(0, str(len(test_case.get('demand_points', []))))
            self.facility_count_entry.insert(0, str(len(test_case.get('facility_points', []))))
            
            # Generate input fields
            self.generate_inputs()

            # Populate demand point coordinates
            for i, coord in enumerate(test_case.get('demand_points', [])):
                if i < len(self.demand_entries):
                    self.demand_entries[i].delete(0, tk.END)
                    self.demand_entries[i].insert(0, f"{coord[0]},{coord[1]}")

            # Populate facility point coordinates
            for i, coord in enumerate(test_case.get('facility_points', [])):
                if i < len(self.facility_entries):
                    self.facility_entries[i].delete(0, tk.END)
                    self.facility_entries[i].insert(0, f"{coord[0]},{coord[1]}")

            # Set service level
            self.service_level_entry.delete(0, tk.END)
            self.service_level_entry.insert(0, str(test_case.get('service_level', 1)))

            # Set problem type
            problem_type = test_case.get('problem_type', 'Set Covering')
            self.problem_type_var.set(problem_type)
            self.toggle_max_facilities()

            # Set max facilities if Max Covering
            if problem_type == 'Max Covering':
                max_facilities = test_case.get('max_facilities', '')
                if max_facilities:
                    self.max_facilities_entry.delete(0, tk.END)
                    self.max_facilities_entry.insert(0, str(max_facilities))

            # Optional: Show success message
            messagebox.showinfo("Test Case Loaded", f"Loaded test case from {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load test case: {e}")

    def generate_inputs(self):
        try:
            num_demand = int(self.demand_count_entry.get())
            num_facility = int(self.facility_count_entry.get())

            # Clear existing entries
            for widget in self.demand_frame.winfo_children():
                widget.destroy()
            for widget in self.facility_frame.winfo_children():
                widget.destroy()

            # Reset entry trackers
            self.demand_entries.clear()
            self.facility_entries.clear()

            # Create demand point inputs
            for i in range(num_demand):
                coord_label = ctk.CTkLabel(self.demand_frame, text=f"Demand {i + 1} (x,y):")
                coord_label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
                coord_entry = ctk.CTkEntry(self.demand_frame, width=250)
                coord_entry.grid(row=i, column=1, padx=5, pady=5)
                self.demand_entries.append(coord_entry)

            # Create facility point inputs
            for i in range(num_facility):
                coord_label = ctk.CTkLabel(self.facility_frame, text=f"Facility {i + 1} (x,y):")
                coord_label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
                coord_entry = ctk.CTkEntry(self.facility_frame, width=250)
                coord_entry.grid(row=i, column=1, padx=5, pady=5)
                self.facility_entries.append(coord_entry)

            # Show or hide max facilities entry
            self.toggle_max_facilities()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def toggle_max_facilities(self, *args):
        # Check if max facilities should be shown
        if self.problem_type_var.get() == "Max Covering":
            self.max_facilities_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
            self.max_facilities_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")
        else:
            try:
                self.max_facilities_label.grid_remove()
                self.max_facilities_entry.grid_remove()
            except:
                pass

    def solve_problem(self):
        try:
            # Get level of service
            S = float(self.service_level_entry.get())

            # Get problem type
            problem_type = self.problem_type_var.get()

            # Parse demand points
            demand_points = [
                tuple(map(float, entry.get().split(',')))
                for entry in self.demand_entries
            ]

            # Parse facility points
            facility_points = [
                tuple(map(float, entry.get().split(',')))
                for entry in self.facility_entries
            ]

            # Calculate coverage matrix
            coverage = []
            for i, demand in enumerate(demand_points):
                row = []
                for j, facility in enumerate(facility_points):
                    distance = math.sqrt((demand[0] - facility[0])**2 + (demand[1] - facility[1])**2)
                    row.append(distance <= S)
                coverage.append(row)

            # Define the optimization model
            model = Model("Covering Problem")

            # Add variables
            y = model.addVars(len(facility_points), vtype=GRB.BINARY, name="y")
            z = model.addVars(len(demand_points), vtype=GRB.BINARY, name="z")

            if problem_type == "Max Covering":
                # Get max facilities constraint
                p = int(self.max_facilities_entry.get())

                # Add constraints: limit the number of facilities
                model.addConstr(y.sum() <= p, name="facility_limit")

                # Add constraints: demand coverage
                for i in range(len(demand_points)):
                    model.addConstr(
                        z[i] <= sum(y[j] for j in range(len(facility_points)) if coverage[i][j]),
                        name=f"demand_{i}_coverage"
                    )

                # Set objective: maximize coverage of demand points
                model.setObjective(z.sum(), GRB.MAXIMIZE)
            else:  # Set Covering Problem
                # Add constraints: all demand points must be covered
                for i in range(len(demand_points)):
                    model.addConstr(
                        sum(y[j] for j in range(len(facility_points)) if coverage[i][j]) >= 1,
                        name=f"demand_{i}_coverage"
                    )

                # Set objective: minimize the number of facilities
                model.setObjective(y.sum(), GRB.MINIMIZE)

            # Solve the model
            model.optimize()

            # Extract results
            if model.status == GRB.OPTIMAL:
                covered_demands = [
                    i for i in range(len(demand_points)) if z[i].X > 0.5
                ] if problem_type == "Max Covering" else "All"

                selected_facilities = [
                    j for j in range(len(facility_points)) if y[j].X > 0.5
                ]

                result_text = (
                    f"Optimization Problem Results:\n"
                    f"-------------------------\n"
                    f"Problem Type: {problem_type}\n\n"
                    f"Facility Selection:\n"
                    f"  • Number of Facilities Chosen: {len(selected_facilities)}\n"
                    f"  • Facility Indices: {sorted(selected_facilities)}\n\n"
                    f"Demand Coverage:\n"
                    f"  • {'All demand points covered' if covered_demands == 'All' else f'Demands Covered: {len(covered_demands)} out of {len(demand_points)}'}\n"
                    f"  • {'Indices of Covered Demands: ' + str(covered_demands) if covered_demands != 'All' else ''}"
                )
                
                self.result_label.delete("1.0", tk.END)
                self.result_label.insert(tk.END, result_text)

                # Plot results
                self.plot_results(demand_points, facility_points, selected_facilities, coverage, covered_demands if problem_type == "Max Covering" else None)
            else:
                self.result_label.delete("1.0", tk.END)
                self.result_label.insert(tk.END, "No optimal solution found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def plot_results(self, demand_points, facility_points, selected_facilities, coverage, covered_demands):
        # Create a new window for the plot
        plot_window = ctk.CTkToplevel(self)
        plot_window.title("Solution Visualization")
        plot_window.geometry("600x500")

        # Create the plot with dark background
        fig, ax = plt.subplots(figsize=(8, 6), facecolor='#2C2C2C')

        # Get service level
        S = float(self.service_level_entry.get())

        # Plot demand points
        for i, (x, y) in enumerate(demand_points):
            ax.scatter(x, y, color='blue', label='Demand Points' if i == 0 else "")
            ax.text(x, y, f' D{i+1}', verticalalignment='bottom', color='white')

        # Plot facility points
        for i, (x, y) in enumerate(facility_points):
            color = 'green' if i in selected_facilities else 'red'
            ax.scatter(x, y, color=color, label='Selected Facilities' if i == 0 and i in selected_facilities else 'Facilities' if i == 0 else "")
            ax.text(x, y, f' F{i+1}', verticalalignment='bottom', color='white')
            
            # Coverage radius
            circle = Circle((x, y), S, color=color, alpha=0.2, label='Coverage Radius' if i == 0 else "")
            ax.add_patch(circle)

        # Draw connections between facilities and covered demands
        for i in range(len(demand_points)):
            if covered_demands is None or i in covered_demands:
                for j in selected_facilities:
                    if coverage[i][j]:
                        ax.plot([demand_points[i][0], facility_points[j][0]],
                                [demand_points[i][1], facility_points[j][1]],
                                color='gray', linestyle='solid', linewidth=0.7)

        # Styling for dark theme
        ax.set_facecolor('#2C2C2C')
        ax.set_xlabel("X Coordinate", color='white')
        ax.set_ylabel("Y Coordinate", color='white')
        ax.set_title("Covering Problem Solution", color='white')
        ax.tick_params(colors='white')
        ax.grid(True, color='#444444', linestyle='--', linewidth=0.5)

        for spine in ax.spines.values():
            spine.set_edgecolor('white')

        # Customize legend
        leg = ax.legend(facecolor='#2C2C2C', edgecolor='white', labelcolor='white')

        # Embed the plot in the CustomTkinter window
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=ctk.BOTH, expand=True)

        # Add a close button
        close_button = ctk.CTkButton(
            plot_window, 
            text="Close", 
            command=plot_window.destroy,
            fg_color="#F44336",
            hover_color="#D32F2F"
        )
        close_button.pack(pady=10)

def main():
    # Make sure to install customtkinter and gurobi before running
    app = CoveringProblemApp()
    app.mainloop()

if __name__ == "__main__":
    main()
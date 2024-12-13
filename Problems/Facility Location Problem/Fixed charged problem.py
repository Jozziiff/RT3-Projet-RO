import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from gurobipy import Model, GRB
import math
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
from tkinter import filedialog

# Set the appearance mode and default color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class FacilityLocationApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Facility Location Problem Solver")
        self.geometry("800x900")

        # Create main frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main container
        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        # Problem Type Selection
        self.problem_type_label = ctk.CTkLabel(self.main_frame, text="Problem Type:")
        self.problem_type_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.problem_type = ctk.CTkComboBox(
            self.main_frame, 
            values=["Capacitated", "Non-Capacitated"],
            state="readonly",
            width=250
        )
        self.problem_type.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.problem_type.set("Capacitated")

        # Demand Points Input
        self.demand_count_label = ctk.CTkLabel(self.main_frame, text="Number of Demand Points:")
        self.demand_count_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.demand_count_entry = ctk.CTkEntry(self.main_frame, width=250)
        self.demand_count_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Facility Points Input
        self.facility_count_label = ctk.CTkLabel(self.main_frame, text="Number of Facilities:")
        self.facility_count_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.facility_count_entry = ctk.CTkEntry(self.main_frame, width=250)
        self.facility_count_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.load_test_case_button = ctk.CTkButton(
            self.main_frame, 
            text="Load Test Case", 
            command=self.load_test_case,
            fg_color="#FF9800",
            hover_color="#F57C00"
        )
        self.load_test_case_button.grid(row=3, column=1, padx=10, pady=10)

        # Generate Inputs Button
        self.generate_button = ctk.CTkButton(
            self.main_frame, 
            text="Generate Inputs", 
            command=self.generate_inputs,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.generate_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Frames for dynamic inputs
        self.demand_frame = ctk.CTkScrollableFrame(self.main_frame, width=400, height=200)
        self.demand_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        self.facility_frame = ctk.CTkScrollableFrame(self.main_frame, width=400, height=200)
        self.facility_frame.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

        # Budget Constraint
        self.budget_var = ctk.BooleanVar(value=False)
        self.budget_checkbox = ctk.CTkCheckBox(
            self.main_frame, 
            text="Enable Budget Constraint", 
            variable=self.budget_var,
            command=self.toggle_budget_input
        )
        self.budget_checkbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.budget_label = ctk.CTkLabel(self.main_frame, text="Budget:")
        self.budget_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")

        self.budget_entry = ctk.CTkEntry(self.main_frame, width=250, state="disabled")
        self.budget_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        # Alpha Input
        self.alpha_label = ctk.CTkLabel(self.main_frame, text="Shipping Cost Factor (α):")
        self.alpha_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")

        self.alpha_entry = ctk.CTkEntry(self.main_frame, width=250)
        self.alpha_entry.grid(row=7, column=1, padx=10, pady=10, sticky="w")


        

        # Solve Button
        self.solve_button = ctk.CTkButton(
            self.main_frame, 
            text="Solve", 
            command=self.solve_problem,
            fg_color="#2196F3",
            hover_color="#1976D2"
        )
        self.solve_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        # Result Display
        self.result_label = ctk.CTkTextbox(self.main_frame, width=760, height=200)
        self.result_label.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

        # Initialize input trackers
        self.demand_entries = []
        self.demand_quantity_entries = []
        self.facility_entries = []
        self.fixed_cost_entries = []
        self.capacity_entries = []
    def load_test_case(self):
        try:
            # Open file dialog to select JSON file
            file_path = filedialog.askopenfilename(
                title="Select Test Case JSON",
                filetypes=[("JSON files", "*.json")]
            )
            
            if not file_path:
                return  # User cancelled file selection
            
            # Load the JSON file
            with open(file_path, 'r') as file:
                test_case = json.load(file)
            
            # Clear existing inputs
            self.demand_count_entry.delete(0, tk.END)
            self.facility_count_entry.delete(0, tk.END)
            self.alpha_entry.delete(0, tk.END)
            
            # Set problem type
            self.problem_type.set(test_case.get("problem_type", "Capacitated"))
            
            # Set number of demand and facility points
            self.demand_count_entry.insert(0, str(len(test_case.get("demand_points", []))))
            self.facility_count_entry.insert(0, str(len(test_case.get("facility_points", []))))
            
            # Generate input fields
            self.generate_inputs()
            
            # Set alpha value
            self.alpha_entry.insert(0, str(test_case.get("alpha", 1.0)))
            
            # Set budget constraint
            if "budget" in test_case:
                self.budget_checkbox.select()
                self.budget_entry.configure(state="normal")
                self.budget_entry.delete(0, tk.END)
                self.budget_entry.insert(0, str(test_case["budget"]))
            else:
                self.budget_checkbox.deselect()
                self.budget_entry.configure(state="disabled")
            
            # Populate demand points and quantities
            for i, (point, quantity) in enumerate(zip(test_case.get("demand_points", []), test_case.get("demand_quantities", []))):
                self.demand_entries[i].delete(0, tk.END)
                self.demand_entries[i].insert(0, f"{point[0]},{point[1]}")
                self.demand_quantity_entries[i].delete(0, tk.END)
                self.demand_quantity_entries[i].insert(0, str(quantity))
            
            # Populate facility points, fixed costs, and capacities
            for i, (point, fixed_cost) in enumerate(zip(test_case.get("facility_points", []), test_case.get("fixed_costs", []))):
                self.facility_entries[i].delete(0, tk.END)
                self.facility_entries[i].insert(0, f"{point[0]},{point[1]}")
                self.fixed_cost_entries[i].delete(0, tk.END)
                self.fixed_cost_entries[i].insert(0, str(fixed_cost))
                
                # Populate capacities for capacitated problems
                if self.problem_type.get() == "Capacitated" and "capacities" in test_case:
                    self.capacity_entries[i].delete(0, tk.END)
                    self.capacity_entries[i].insert(0, str(test_case["capacities"][i]))
            
            messagebox.showinfo("Success", "Test case loaded successfully!")
        
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
            self.demand_quantity_entries.clear()
            self.facility_entries.clear()
            self.fixed_cost_entries.clear()
            self.capacity_entries.clear()

            # Create demand point inputs
            for i in range(num_demand):
                coord_label = ctk.CTkLabel(self.demand_frame, text=f"Demand {i + 1} (x,y):")
                coord_label.grid(row=i*2, column=0, padx=5, pady=5, sticky="w")
                coord_entry = ctk.CTkEntry(self.demand_frame, width=150)
                coord_entry.grid(row=i*2, column=1, padx=5, pady=5)
                self.demand_entries.append(coord_entry)

                quantity_label = ctk.CTkLabel(self.demand_frame, text=f"Quantity {i + 1}:")
                quantity_label.grid(row=i*2, column=2, padx=5, pady=5, sticky="w")
                quantity_entry = ctk.CTkEntry(self.demand_frame, width=150)
                quantity_entry.grid(row=i*2, column=3, padx=5, pady=5)
                self.demand_quantity_entries.append(quantity_entry)

            # Create facility point inputs
            for i in range(num_facility):
                coord_label = ctk.CTkLabel(self.facility_frame, text=f"Facility {i + 1} (x,y):")
                coord_label.grid(row=i*3, column=0, padx=5, pady=5, sticky="w")
                coord_entry = ctk.CTkEntry(self.facility_frame, width=150)
                coord_entry.grid(row=i*3, column=1, padx=5, pady=5)
                self.facility_entries.append(coord_entry)

                cost_label = ctk.CTkLabel(self.facility_frame, text=f"Fixed Cost {i + 1}:")
                cost_label.grid(row=i*3, column=2, padx=5, pady=5, sticky="w")
                cost_entry = ctk.CTkEntry(self.facility_frame, width=150)
                cost_entry.grid(row=i*3, column=3, padx=5, pady=5)
                self.fixed_cost_entries.append(cost_entry)

                if self.problem_type.get() == "Capacitated":
                    capacity_label = ctk.CTkLabel(self.facility_frame, text=f"Capacity {i + 1}:")
                    capacity_label.grid(row=i*3+1, column=0, padx=5, pady=5, sticky="w")
                    capacity_entry = ctk.CTkEntry(self.facility_frame, width=150)
                    capacity_entry.grid(row=i*3+1, column=1, padx=5, pady=5)
                    self.capacity_entries.append(capacity_entry)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def toggle_budget_input(self):
        """Enable or disable the budget entry based on checkbox state."""
        if self.budget_var.get():
            self.budget_entry.configure(state="normal")
        else:
            self.budget_entry.configure(state="disabled")

    def solve_problem(self):
        try:
            # Parse demand points (implementation from original code)
            demand_points = [
                tuple(map(float, entry.get().split(',')))
                for entry in self.demand_entries
            ]

            # Parse facility points
            facility_points = [
                tuple(map(float, entry.get().split(',')))
                for entry in self.facility_entries
            ]

            # Parse fixed costs and alpha
            fixed_costs = [float(entry.get()) for entry in self.fixed_cost_entries]
            alpha = float(self.alpha_entry.get())

            # Parse budget constraint
            use_budget = self.budget_var.get()
            budget = float(self.budget_entry.get()) if use_budget else None

            # Parse capacities (if enabled)
            capacitated = self.problem_type.get() == "Capacitated"
            capacities = [float(entry.get()) for entry in self.capacity_entries] if capacitated else None

            # Parse demand quantities
            demand_quantities = [float(entry.get()) for entry in self.demand_quantity_entries]

            # Calculate shipping costs
            shipping_costs = [
                [alpha * math.sqrt((d[0] - f[0])**2 + (d[1] - f[1])**2)
                 for f in facility_points] for d in demand_points
            ]

            # Define the optimization model (same as original code)
            model = Model("Facility Location Problem")

            # Add decision variables
            select = model.addVars(len(facility_points), vtype=GRB.BINARY, name="select")
            assign = model.addVars(len(demand_points), len(facility_points), vtype=GRB.CONTINUOUS, name="assign")

            # Objective function: Minimize total costs
            model.setObjective(
                sum(fixed_costs[j] * select[j] for j in range(len(facility_points))) +
                sum(shipping_costs[i][j] * assign[i, j] for i in range(len(demand_points)) for j in range(len(facility_points))),
                GRB.MINIMIZE
            )

            # Constraints: Each demand must be fully satisfied
            for i in range(len(demand_points)):
                model.addConstr(
                    sum(assign[i, j] for j in range(len(facility_points))) == demand_quantities[i],
                    name=f"demand_fulfillment_{i}"
                )

            # Constraints: Shipping only allowed from selected facilities
            for i in range(len(demand_points)):
                for j in range(len(facility_points)):
                    model.addConstr(assign[i, j] <= demand_quantities[i] * select[j], name=f"shipping_constraint_{i}_{j}")

            # Capacitated constraints (if enabled)
            if capacitated:
                for j in range(len(facility_points)):
                    model.addConstr(
                        sum(assign[i, j] for i in range(len(demand_points))) <= capacities[j] * select[j],
                        name=f"capacity_constraint_{j}"
                    )

            # Budget constraint (if enabled)
            if use_budget:
                model.addConstr(
                    sum(fixed_costs[j] * select[j] for j in range(len(facility_points))) <= budget,
                    name="budget_constraint"
                )

            # Solve the model
            model.optimize()

            # Extract results
            if model.status == GRB.OPTIMAL:
                selected_facilities = [j for j in range(len(facility_points)) if select[j].X > 0.5]
                assignments = {
                    i: [j for j in range(len(facility_points)) if assign[i, j].X > 0.001]
                    for i in range(len(demand_points))
                }

                # Build a more detailed result text
                result_text = "Facilities Chosen:\n"
                for j in selected_facilities:
                    result_text += f"Facility {j+1} at {facility_points[j]} (Fixed Cost: {fixed_costs[j]})\n"
                
                result_text += "\nAssignments:\n"
                for i, assigned_facilities in assignments.items():
                    result_text += f"Demand Point {i+1} at {demand_points[i]} (Quantity: {demand_quantities[i]})\n"
                    for j in assigned_facilities:
                        result_text += f"  Assigned to Facility {j+1} at {facility_points[j]} with Shipping Cost: {shipping_costs[i][j] * demand_quantities[i]}\n"

                self.result_label.delete("1.0", tk.END)
                self.result_label.insert(tk.END, result_text)
                
                # Call plot results 
                self.plot_results(demand_points, facility_points, selected_facilities, assignments)
            else:
                self.result_label.delete("1.0", tk.END)
                self.result_label.insert(tk.END, "No optimal solution found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def plot_results(self, demand_points, facility_points, selected_facilities, assignments):
        # Create a new window for the plot
        plot_window = ctk.CTkToplevel(self)
        plot_window.title("Solution Visualization")
        plot_window.geometry("600x500")

        # Create the plot
        fig, ax = plt.subplots(figsize=(8, 6), facecolor='#2C2C2C')
        for i, (x, y) in enumerate(demand_points):
            ax.scatter(x, y, color='blue', label='Demand Points' if i == 0 else "")
            ax.text(x, y, f' D{i+1}', verticalalignment='bottom')

        # Plot facility points
        for i, (x, y) in enumerate(facility_points):
            color = 'green' if i in selected_facilities else 'red'
            ax.scatter(x, y, color=color, label='Selected Facilities' if i == 0 and i in selected_facilities else 'Facilities' if i == 0 else "")
            ax.text(x, y, f' F{i+1}', verticalalignment='bottom')

        # Draw arrows for assignments
        for i, demand in enumerate(demand_points):
            for j in assignments[i]:
                facility = facility_points[j]
                ax.add_patch(FancyArrow(
                    demand[0], demand[1],
                    facility[0] - demand[0], facility[1] - demand[1],
                    color='gray', width=0.005, length_includes_head=True
                ))

        ax.set_facecolor('#2C2C2C')
        ax.set_xlabel("X Coordinate", color='white')
        ax.set_ylabel("Y Coordinate", color='white')
        ax.set_title("Facility Location Problem Solution", color='white')
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
    app = FacilityLocationApp()
    app.mainloop()

if __name__ == "__main__":
    main()
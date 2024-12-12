import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from gurobipy import GRB, Model, quicksum
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.spatial.distance import euclidean
import json

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModernTSPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TSP_ZELLO")
        self.root.geometry("800x800")

        # Create main container with scrolling
        self.main_container = ctk.CTkScrollableFrame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title Label
        self.title_label = ctk.CTkLabel(
            self.main_container, 
            text="TSP Route Optimizer",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=10)

        # Dropdown for number of cities with label
        self.cities_frame = ctk.CTkFrame(self.main_container)
        self.cities_frame.pack(fill=tk.X, pady=10)
        
        self.num_cities_label = ctk.CTkLabel(
            self.cities_frame,
            text="Number of Locations:",
            font=ctk.CTkFont(size=14)
        )
        self.num_cities_label.pack(side=tk.LEFT, padx=10)
        
        self.num_cities_var = tk.IntVar(value=3)
        self.num_cities_menu = ctk.CTkOptionMenu(
            self.cities_frame,
            values=[str(i) for i in range(3, 16)],
            command=self.update_location_inputs,
            variable=self.num_cities_var
        )
        self.num_cities_menu.pack(side=tk.LEFT, padx=10)

        # Frame for coordinates and constraints
        self.input_frame = ctk.CTkFrame(self.main_container)
        self.input_frame.pack(fill=tk.X, pady=10)

        # Constraints Section
        self.constraints_frame = ctk.CTkFrame(self.main_container)
        self.constraints_frame.pack(fill=tk.X, pady=10)

        # Restricted Routes
        self.restricted_routes_label = ctk.CTkLabel(
            self.constraints_frame,
            text="Restricted Routes (e.g., 1-2, 3-4):",
            font=ctk.CTkFont(size=14)
        )
        self.restricted_routes_label.pack(pady=5)
        
        self.restricted_routes_var = tk.StringVar(value="")
        self.restricted_routes_entry = ctk.CTkEntry(
            self.constraints_frame,
            textvariable=self.restricted_routes_var,
            width=200
        )
        self.restricted_routes_entry.pack(pady=5)

        # Max Distance
        self.max_distance_label = ctk.CTkLabel(
            self.constraints_frame,
            text="Max Distance Between Locations:",
            font=ctk.CTkFont(size=14)
        )
        self.max_distance_label.pack(pady=5)
        
        self.max_distance_var = tk.DoubleVar(value=100.0)
        self.max_distance_entry = ctk.CTkEntry(
            self.constraints_frame,
            textvariable=self.max_distance_var,
            width=200
        )
        self.max_distance_entry.pack(pady=5)

        # Vehicle Count
        self.vehicle_count_label = ctk.CTkLabel(
            self.constraints_frame,
            text="Number of Vehicles:",
            font=ctk.CTkFont(size=14)
        )
        self.vehicle_count_label.pack(pady=5)
        
        self.vehicle_count_var = tk.IntVar(value=1)
        self.vehicle_count_menu = ctk.CTkOptionMenu(
            self.constraints_frame,
            values=[str(i) for i in range(1, 6)],
            variable=self.vehicle_count_var
        )
        self.vehicle_count_menu.pack(pady=5)

        # Priority Weight
        self.priority_weight_label = ctk.CTkLabel(
            self.constraints_frame,
            text="Priority Weight (0-1):",
            font=ctk.CTkFont(size=14)
        )
        self.priority_weight_label.pack(pady=5)
        
        self.priority_weight_var = tk.DoubleVar(value=0.5)
        self.priority_weight_entry = ctk.CTkEntry(
            self.constraints_frame,
            textvariable=self.priority_weight_var,
            width=200
        )
        self.priority_weight_entry.pack(pady=5)

        # Buttons Frame
        self.buttons_frame = ctk.CTkFrame(self.main_container)
        self.buttons_frame.pack(fill=tk.X, pady=10)

        # Configuration Buttons
        self.save_button = ctk.CTkButton(
            self.buttons_frame,
            text="Save Configuration",
            command=self.save_config,
            width=150
        )
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.load_button = ctk.CTkButton(
            self.buttons_frame,
            text="Load Configuration",
            command=self.load_config,
            width=150
        )
        self.load_button.pack(side=tk.LEFT, padx=10)

        # Solve Button
        self.solve_button = ctk.CTkButton(
            self.main_container,
            text="Solve TSP",
            command=self.solve_tsp,
            width=200,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.solve_button.pack(pady=20)

        self.coordinates_inputs = []
        self.location_name_inputs = []
        self.priority_inputs = []
        self.update_location_inputs()

    def update_location_inputs(self, event=None):
        # Clear previous inputs
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        self.coordinates_inputs = []
        self.location_name_inputs = []
        self.priority_inputs = []

        # Add new input fields
        for i in range(self.num_cities_var.get()):
            row_frame = ctk.CTkFrame(self.input_frame)
            row_frame.pack(pady=5, padx=10, fill=tk.X)

            # Location name
            name_label = ctk.CTkLabel(
                row_frame,
                text=f"Location {i + 1}:",
                font=ctk.CTkFont(size=12)
            )
            name_label.pack(side=tk.LEFT, padx=5)
            
            name_input = ctk.CTkEntry(row_frame, width=100)
            name_input.pack(side=tk.LEFT, padx=5)
            self.location_name_inputs.append(name_input)

            # Coordinates
            coord_label = ctk.CTkLabel(
                row_frame,
                text="(x, y):",
                font=ctk.CTkFont(size=12)
            )
            coord_label.pack(side=tk.LEFT, padx=5)
            
            x_input = ctk.CTkEntry(row_frame, width=70)
            y_input = ctk.CTkEntry(row_frame, width=70)
            x_input.pack(side=tk.LEFT, padx=2)
            y_input.pack(side=tk.LEFT, padx=2)
            self.coordinates_inputs.append((x_input, y_input))

            # Priority
            priority_label = ctk.CTkLabel(
                row_frame,
                text="Priority:",
                font=ctk.CTkFont(size=12)
            )
            priority_label.pack(side=tk.LEFT, padx=5)
            
            priority_var = tk.IntVar(value=1)
            priority_menu = ctk.CTkOptionMenu(
                row_frame,
                values=[str(i) for i in range(1, 6)],
                variable=priority_var,
                width=70
            )
            priority_menu.pack(side=tk.LEFT, padx=5)
            self.priority_inputs.append(priority_var)

    def display_tsp_result(self, coordinates, best_route, min_distance, location_names):
        result_window = ctk.CTkToplevel(self.root)
        result_window.title("TSP Result")
        result_window.geometry("600x400")

        # Display optimal distance
        distance_label = ctk.CTkLabel(
            result_window,
            text=f"Optimal Distance: {min_distance:.2f}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        distance_label.pack(pady=10)

        # Display route order with priorities
        route_text = "Optimal Route:\n"
        for i, loc_idx in enumerate(best_route):
            priority = self.priority_inputs[loc_idx].get()
            route_text += f"{i+1}. {location_names[loc_idx]} (Priority: {priority})"
            if i < len(best_route) - 1:
                route_text += " → \n"
        
        text_widget = ctk.CTkTextbox(result_window, height=300, width=500)
        text_widget.insert("1.0", route_text)
        text_widget.configure(state="disabled")
        text_widget.pack(pady=10, padx=20)

    def show_tsp_graph(self, coordinates, best_route, location_names):
        graph_window = ctk.CTkToplevel(self.root)
        graph_window.title("TSP Graph")
        graph_window.geometry("800x600")

        # Use dark background for the plot
        plt.style.use('dark_background')
        
        fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
        ordered_coords = [coordinates[i] for i in best_route]
        x, y = zip(*ordered_coords)

        # Plot route with enhanced styling
        ax.plot(x, y, color='#00bfff', linewidth=2, zorder=1)

        # Plot points with priority-based colors
        for i, coord in enumerate(ordered_coords):
            priority = self.priority_inputs[best_route[i]].get()
            color = plt.cm.RdYlBu(priority/5.0)
            ax.scatter(coord[0], coord[1], color=color, s=100, zorder=2, edgecolor='white')
            ax.text(coord[0], coord[1], f"{location_names[best_route[i]]}\n(P:{priority})",
                   fontsize=8, ha='right', va='bottom', color='white')

        # Add legend for priority levels
        priority_patches = [plt.scatter([], [], color=plt.cm.RdYlBu(p/5.0), label=f'Priority {p}')
                          for p in range(1, 6)]
        ax.legend(handles=priority_patches, title='Priority Levels',
                 bbox_to_anchor=(1.05, 1), loc='upper left')

        ax.set_title("Optimal TSP Route with Priorities", color='white', pad=20)
        ax.set_xlabel("X Coordinate", color='white')
        ax.set_ylabel("Y Coordinate", color='white')
        ax.grid(True, linestyle='--', alpha=0.3, color='gray')

        # Style the plot
        ax.set_facecolor('#2b2b2b')
        fig.patch.set_facecolor('#2b2b2b')

        plt.tight_layout()

        # Embed the figure
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # The save_config, load_config, and solve_tsp_with_gurobi methods remain unchanged
    def save_config(self):
        """Save current configuration to JSON file"""
        try:
            config = {
                'num_cities': self.num_cities_var.get(),
                'restricted_routes': self.restricted_routes_var.get(),
                'max_distance': self.max_distance_var.get(),
                'vehicle_count': self.vehicle_count_var.get(),
                'priority_weight': self.priority_weight_var.get(),
                'locations': []
            }

            for i, ((x_input, y_input), name_input, priority_input) in enumerate(
                    zip(self.coordinates_inputs, self.location_name_inputs, self.priority_inputs)):
                location_data = {
                    'name': name_input.get(),
                    'x': float(x_input.get()) if x_input.get() else 0,
                    'y': float(y_input.get()) if y_input.get() else 0,
                    'priority': priority_input.get()
                }
                config['locations'].append(location_data)

            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")]
            )
            
            if filename:
                with open(filename, 'w') as f:
                    json.dump(config, f, indent=4)
                messagebox.showinfo("Success", "Configuration saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Error saving configuration: {str(e)}")

    def load_config(self):
        """Load configuration from JSON file"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json")]
            )
            
            if filename:
                with open(filename, 'r') as f:
                    config = json.load(f)

                self.num_cities_var.set(config['num_cities'])
                self.restricted_routes_var.set(config['restricted_routes'])
                self.max_distance_var.set(config['max_distance'])
                self.vehicle_count_var.set(config['vehicle_count'])
                self.priority_weight_var.set(config.get('priority_weight', 0.5))

                self.update_location_inputs()

                for i, location in enumerate(config['locations']):
                    if i < len(self.coordinates_inputs):
                        x_input, y_input = self.coordinates_inputs[i]
                        name_input = self.location_name_inputs[i]
                        priority_input = self.priority_inputs[i]
                        
                        name_input.delete(0, "end")
                        name_input.insert(0, location['name'])
                        
                        x_input.delete(0, "end")
                        x_input.insert(0, str(location['x']))
                        
                        y_input.delete(0, "end")
                        y_input.insert(0, str(location['y']))
                        
                        priority_input.set(location.get('priority', 1))

                messagebox.showinfo("Success", "Configuration loaded successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Error loading configuration: {str(e)}")

    def solve_tsp(self):
        try:
            # Collect location names, coordinates, and priorities
            coordinates = []
            location_names = []
            priorities = []
            for name_input, (x_input, y_input), priority_var in zip(
                    self.location_name_inputs, self.coordinates_inputs, self.priority_inputs):
                try:
                    name = name_input.get()
                    x = float(x_input.get())
                    y = float(y_input.get())
                    priority = int(priority_var.get())
                    location_names.append(name)
                    coordinates.append((x, y))
                    priorities.append(priority)
                except ValueError:
                    messagebox.showerror("Input Error", "All coordinates must be valid numbers and priorities must be integers.")
                    return

            num_cities = len(coordinates)

            # Compute the distance matrix
            distance_matrix = np.zeros((num_cities, num_cities))
            for i in range(num_cities):
                for j in range(num_cities):
                    if i != j:
                        distance_matrix[i][j] = euclidean(coordinates[i], coordinates[j])

            # Show loading indicator
            self.solve_button.configure(state="disabled", text="Solving...")
            self.root.update()

            # Solve TSP using Gurobi with priorities
            best_route, min_distance = self.solve_tsp_with_gurobi(distance_matrix, num_cities, priorities)

            # Reset button state
            self.solve_button.configure(state="normal", text="Solve TSP")

            # Display the result
            self.display_tsp_result(coordinates, best_route, min_distance, location_names)

            # Show the matplotlib graph
            self.show_tsp_graph(coordinates, best_route, location_names)

        except Exception as e:
            # Reset button state
            self.solve_button.configure(state="normal", text="Solve TSP")
            messagebox.showerror("Error", str(e))

    def solve_tsp_with_gurobi(self, distance_matrix, num_cities, priorities):
        try:
            # Create a Gurobi model with a time limit
            model = Model("VRP")
            model.setParam('TimeLimit', 60)
            model.setParam('MIPGap', 0.05)

            num_vehicles = self.vehicle_count_var.get()
            priority_weight = self.priority_weight_var.get()
            
            # Create binary variables for edges with vehicle dimension
            x = model.addVars(num_cities, num_cities, num_vehicles, vtype=GRB.BINARY, name="x")
            
            # Time variables to track visit order
            t = model.addVars(num_cities, num_vehicles, vtype=GRB.CONTINUOUS, name="t")
            
            # Objective: minimize weighted sum of distance and priority-based waiting time
            distance_obj = quicksum(
                distance_matrix[i][j] * x[i, j, k]
                for i in range(num_cities)
                for j in range(num_cities)
                for k in range(num_vehicles)
                if i != j
            )
            
            priority_obj = quicksum(
                t[i, k] * (6 - priorities[i])  # Higher priority locations should be visited earlier
                for i in range(num_cities)
                for k in range(num_vehicles)
            )
            
            model.setObjective(
                (1 - priority_weight) * distance_obj + priority_weight * priority_obj,
                GRB.MINIMIZE
            )

            # Each non-depot city must be visited exactly once
            for j in range(1, num_cities):
                model.addConstr(
                    quicksum(
                        x[i, j, k]
                        for i in range(num_cities)
                        for k in range(num_vehicles)
                        if i != j
                    ) == 1
                )

            # Flow conservation
            for k in range(num_vehicles):
                for j in range(num_cities):
                    model.addConstr(
                        quicksum(x[i, j, k] for i in range(num_cities) if i != j) ==
                        quicksum(x[j, i, k] for i in range(num_cities) if i != j)
                    )

            # Vehicle depot constraints
            for k in range(num_vehicles):
                model.addConstr(quicksum(x[0, j, k] for j in range(1, num_cities)) == 1)
                model.addConstr(quicksum(x[i, 0, k] for i in range(1, num_cities)) == 1)

            # Time constraints
            M = num_cities  # Big M constant
            for k in range(num_vehicles):
                model.addConstr(t[0, k] == 0)  # Start from depot at time 0
                for i in range(num_cities):
                    for j in range(1, num_cities):
                        if i != j:
                            model.addConstr(
                                t[j, k] >= t[i, k] + 1 - M * (1 - x[i, j, k])
                            )

            # Add restricted routes if specified
            restricted_routes = self.restricted_routes_var.get()
            if restricted_routes:
                try:
                    restrictions = [
                        tuple(map(int, route.split('-'))) 
                        for route in restricted_routes.strip().split(',')
                    ]
                    for i, j in restrictions:
                        if 1 <= i <= num_cities and 1 <= j <= num_cities:
                            for k in range(num_vehicles):
                                model.addConstr(x[i - 1, j - 1, k] == 0)
                                model.addConstr(x[j - 1, i - 1, k] == 0)
                except ValueError:
                    raise ValueError("Invalid restricted routes format")

            # Maximum distance constraints
            max_distance = self.max_distance_var.get()
            if max_distance > 0:
                for k in range(num_vehicles):
                    model.addConstr(
                        quicksum(
                            distance_matrix[i][j] * x[i, j, k]
                            for i in range(num_cities)
                            for j in range(num_cities)
                            if i != j
                        ) <= max_distance
                    )

            # Optimize
            model.optimize()

            if model.status == GRB.OPTIMAL or model.status == GRB.TIME_LIMIT:
                solution = model.getAttr('x', x)
                
                # Extract routes
                all_routes = []
                for k in range(num_vehicles):
                    route = []
                    current = 0
                    while True:
                        route.append(current)
                        next_city = None
                        for j in range(num_cities):
                            if j != current and solution[current, j, k] > 0.5:
                                next_city = j
                                break
                        if next_city is None or next_city == 0:
                            route.append(0)
                            break
                        current = next_city
                    if len(route) > 2:
                        all_routes.append(route)
                
                combined_route = [0]
                for route in all_routes:
                    combined_route.extend(route[1:])
                
                return combined_route, model.objVal
            else:
                raise ValueError(f"Optimization failed with status {model.status}")

        except Exception as e:
            raise Exception(f"Optimization error: {str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = ModernTSPApp(root)
    root.mainloop()
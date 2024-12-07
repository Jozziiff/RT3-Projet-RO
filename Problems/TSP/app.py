import tkinter as tk
from tkinter import ttk, messagebox
from gurobipy import GRB, Model, quicksum
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.spatial.distance import euclidean

class TSPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced TSP Solver")

        # Dropdown to select the number of cities
        self.num_cities_label = tk.Label(root, text="Select Number of Locations:")
        self.num_cities_label.pack()
        self.num_cities_var = tk.IntVar(value=3)
        self.num_cities_menu = ttk.Combobox(root, textvariable=self.num_cities_var, values=list(range(3, 16)))
        self.num_cities_menu.pack()
        self.num_cities_menu.bind("<<ComboboxSelected>>", self.update_location_inputs)

        # Frame for coordinates and constraints
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10)

        # Options for additional constraints
        self.restricted_routes_label = tk.Label(root, text="Restricted Routes (e.g., 1-2, 3-4):")
        self.restricted_routes_label.pack()
        self.restricted_routes_var = tk.StringVar(value="")
        self.restricted_routes_entry = tk.Entry(root, textvariable=self.restricted_routes_var)
        self.restricted_routes_entry.pack()

        self.max_distance_label = tk.Label(root, text="Max Distance Between Locations:")
        self.max_distance_label.pack()
        self.max_distance_var = tk.DoubleVar(value=100.0)
        self.max_distance_entry = tk.Entry(root, textvariable=self.max_distance_var)
        self.max_distance_entry.pack()

        self.vehicle_count_label = tk.Label(root, text="Number of Vehicles:")
        self.vehicle_count_label.pack()
        self.vehicle_count_var = tk.IntVar(value=1)
        self.vehicle_count_menu = ttk.Combobox(root, textvariable=self.vehicle_count_var, values=list(range(1, 6)))
        self.vehicle_count_menu.pack()

        # Checkbox for time window constraints
        self.time_window_var = tk.BooleanVar()
        self.time_window_check = tk.Checkbutton(root, text="Enable Time Windows", variable=self.time_window_var, command=self.update_time_window_fields)
        self.time_window_check.pack()

        # Button to calculate TSP
        self.solve_button = tk.Button(root, text="Solve TSP", command=self.solve_tsp)
        self.solve_button.pack(pady=5)

        self.coordinates_inputs = []
        self.location_name_inputs = []
        self.time_window_inputs = []
        self.update_location_inputs()  # Initialize input fields

    def update_location_inputs(self, event=None):
        # Clear previous inputs
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        self.coordinates_inputs = []
        self.location_name_inputs = []
        self.time_window_inputs = []

        # Add new input fields based on the number of cities
        for i in range(self.num_cities_var.get()):
            row_frame = tk.Frame(self.input_frame)
            row_frame.pack(pady=5)

            tk.Label(row_frame, text=f"Location {i + 1} Name:").pack(side=tk.LEFT)
            name_input = tk.Entry(row_frame, width=10)
            name_input.pack(side=tk.LEFT, padx=5)
            self.location_name_inputs.append(name_input)

            tk.Label(row_frame, text=f"Coordinates (x, y):").pack(side=tk.LEFT)
            x_input = tk.Entry(row_frame, width=10)
            y_input = tk.Entry(row_frame, width=10)
            x_input.pack(side=tk.LEFT, padx=5)
            y_input.pack(side=tk.LEFT, padx=5)
            self.coordinates_inputs.append((x_input, y_input))

            if self.time_window_var.get():
                tk.Label(row_frame, text="Time Window (Start-End):").pack(side=tk.LEFT)
                start_time = tk.Entry(row_frame, width=5)
                end_time = tk.Entry(row_frame, width=5)
                start_time.pack(side=tk.LEFT, padx=2)
                end_time.pack(side=tk.LEFT, padx=2)
                self.time_window_inputs.append((start_time, end_time))

    def update_time_window_fields(self):
        # Toggle time window fields
        self.update_location_inputs()

    def solve_tsp(self):
        try:
            # Collect location names and coordinates
            coordinates = []
            location_names = []
            for name_input, (x_input, y_input) in zip(self.location_name_inputs, self.coordinates_inputs):
                try:
                    name = name_input.get()
                    x = float(x_input.get())
                    y = float(y_input.get())
                    location_names.append(name)
                    coordinates.append((x, y))
                except ValueError:
                    messagebox.showerror("Input Error", "All coordinates must be valid numbers.")
                    return

            num_cities = len(coordinates)

            # Collect time windows if enabled
            time_windows = []
            if self.time_window_var.get():
                for start_input, end_input in self.time_window_inputs:
                    try:
                        start = float(start_input.get())
                        end = float(end_input.get())
                        time_windows.append((start, end))
                    except ValueError:
                        messagebox.showerror("Input Error", "Time windows must be valid numbers.")
                        return

            # Compute the distance matrix
            distance_matrix = np.zeros((num_cities, num_cities))
            for i in range(num_cities):
                for j in range(num_cities):
                    if i != j:
                        distance_matrix[i][j] = euclidean(coordinates[i], coordinates[j])

            # Solve TSP using Gurobi
            best_route, min_distance = self.solve_tsp_with_gurobi(distance_matrix, num_cities, time_windows)

            # Display the result
            self.display_tsp_result(coordinates, best_route, min_distance, location_names)

            # Show the matplotlib graph directly
            self.show_tsp_graph(coordinates, best_route, location_names)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def solve_tsp_with_gurobi(self, distance_matrix, num_cities, time_windows):
        try:
        # Create a Gurobi model with a time limit
            model = Model("VRP")
            model.setParam('TimeLimit', 60)
            model.setParam('MIPGap', 0.05)

            num_vehicles = self.vehicle_count_var.get()
            
            # Create binary variables for edges with vehicle dimension
            # x[i,j,k] = 1 if vehicle k travels from i to j
            x = model.addVars(num_cities, num_cities, num_vehicles, vtype=GRB.BINARY, name="x")
            
            # Time of arrival at each city
            t = model.addVars(num_cities, num_vehicles, vtype=GRB.CONTINUOUS, name="t")
            
            # Objective: minimize total distance across all vehicles
            model.setObjective(
                quicksum(
                    distance_matrix[i][j] * x[i, j, k]
                    for i in range(num_cities)
                    for j in range(num_cities)
                    for k in range(num_vehicles)
                    if i != j
                ),
                GRB.MINIMIZE
            )

            # Constraints for multiple vehicles
            # Each city must be visited exactly once by one vehicle (except depot)
            for j in range(1, num_cities):
                model.addConstr(
                    quicksum(
                        x[i, j, k]
                        for i in range(num_cities)
                        for k in range(num_vehicles)
                        if i != j
                    ) == 1
                )

            # Flow conservation: vehicle entering a city must leave it
            for k in range(num_vehicles):
                for j in range(num_cities):
                    model.addConstr(
                        quicksum(x[i, j, k] for i in range(num_cities) if i != j) ==
                        quicksum(x[j, i, k] for i in range(num_cities) if i != j)
                    )

            # Each vehicle must start and end at depot (city 0)
            for k in range(num_vehicles):
                model.addConstr(quicksum(x[0, j, k] for j in range(1, num_cities)) == 1)
                model.addConstr(quicksum(x[i, 0, k] for i in range(1, num_cities)) == 1)

            # Time window constraints if enabled
            if time_windows:
                M = sum(sum(row) for row in distance_matrix)  # Big M constant
                
                # Set initial time at depot
                for k in range(num_vehicles):
                    model.addConstr(t[0, k] == 0)
                
                # Time window constraints for each city
                for i in range(num_cities):
                    for k in range(num_vehicles):
                        if time_windows[i][0] is not None:
                            model.addConstr(t[i, k] >= time_windows[i][0])
                        if time_windows[i][1] is not None:
                            model.addConstr(t[i, k] <= time_windows[i][1])

                # Time precedence constraints with vehicle tracking
                for i in range(num_cities):
                    for j in range(num_cities):
                        if i != j:
                            for k in range(num_vehicles):
                                model.addConstr(
                                    t[j, k] >= t[i, k] + distance_matrix[i][j] -
                                    M * (1 - x[i, j, k])
                                )

            # Subtour elimination using MTZ formulation adapted for multiple vehicles
            u = model.addVars(
                num_cities, num_vehicles, lb=0, 
                ub=num_cities-1, vtype=GRB.CONTINUOUS, name="u"
            )
            
            for k in range(num_vehicles):
                model.addConstr(u[0, k] == 0)
                for i in range(1, num_cities):
                    for j in range(1, num_cities):
                        if i != j:
                            model.addConstr(
                                u[i, k] - u[j, k] + num_cities * x[i, j, k] <= num_cities - 1
                            )

            # Parse restricted routes
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

            # Optimize with error handling
            model.optimize()

            if model.status == GRB.OPTIMAL or model.status == GRB.TIME_LIMIT:
                # Extract solutions for all vehicles
                solution = model.getAttr('x', x)
                all_routes = []
                total_distance = 0
                
                # Extract route for each vehicle
                for k in range(num_vehicles):
                    route = []
                    current = 0  # Start at depot
                    while True:
                        route.append(current)
                        next_city = None
                        for j in range(num_cities):
                            if j != current and solution[current, j, k] > 0.5:
                                next_city = j
                                break
                        if next_city is None or next_city == 0:
                            route.append(0)  # Return to depot
                            break
                        current = next_city
                    if len(route) > 2:  # Only add non-empty routes
                        all_routes.append(route)
                
                # Combine routes for visualization
                combined_route = [0]  # Start at depot
                for route in all_routes:
                    combined_route.extend(route[1:])
                
                return combined_route, model.objVal
            else:
                raise ValueError(f"Optimization failed with status {model.status}")

        except Exception as e:
            raise Exception(f"Optimization error: {str(e)}")


    def display_tsp_result(self, coordinates, best_route, min_distance, location_names):
        result_window = tk.Toplevel(self.root)
        result_window.title("TSP Result")

        # Display optimal distance
        tk.Label(result_window, text=f"Optimal Distance: {min_distance:.2f}").pack(pady=5)

        # Display route order
        route_order = " -> ".join(location_names[i] for i in best_route)
        tk.Label(result_window, text=f"Optimal Route: {route_order}").pack(pady=5)

    def show_tsp_graph(self, coordinates, best_route, location_names):
        graph_window = tk.Toplevel(self.root)
        graph_window.title("TSP Graph")

        # Create the figure
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        ordered_coords = [coordinates[i] for i in best_route]
        x, y = zip(*ordered_coords)
        ax.plot(x, y, marker='o')
        for i, coord in enumerate(ordered_coords):
            ax.text(coord[0], coord[1], location_names[best_route[i]], fontsize=8)
        ax.set_title("Optimal TSP Route")
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.grid()

        # Embed the figure into the window
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas._tkcanvas.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = TSPApp(root)
    root.mainloop()
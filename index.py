import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import Button, Entry, Frame, OptionMenu, Text, font, Canvas, ttk
import heapq
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import timeit
import numpy as np
import pandas as pd
import tkinter.messagebox as messagebox
from collections import deque

# Create window
window = tk.Tk()
window.title("ASEMETH : Ateraa Search Methods Programs")
window.state('zoomed')

result_text = None
resultTitle = None

# Options Frame Left
options_frame = tk.Frame(window, bg='#ffffff')
options_frame.pack(side=tk.LEFT)
options_frame.pack_propagate(False)
options_frame.configure(width=350, height=1024)

# Add a title label to options_frame
title_label = tk.Label(options_frame, text="ASEMETH", font=("Times", 24), bg='#ffffff')
title_label.pack(pady=20)  # Adjust the padding as needed
subtitle_label = tk.Label(options_frame, text="Ateraa Search Methods Programs", font=("Times", 14), bg='#ffffff')
subtitle_label.pack(pady=0.01)

# Create a black line below the subtitle label
line_canvas = tk.Canvas(options_frame, width=350, height=2, bg='black', highlightthickness=0)
line_canvas.pack(pady=(25, 0))

# Main Frame Right
main_frame = tk.Frame(window)
main_frame.pack(side=tk.LEFT, expand=True, fill="both")  # Expand and fill the available space
main_frame.pack_propagate(False)
main_frame.configure(width=1185, height=1024)

# Read coordinates from a CSV file
def read_coordinates(file_path):
    coordinates = pd.read_csv(file_path, header=None, names=['City', 'Latitude', 'Longitude'])
    return coordinates.set_index('City').to_dict(orient='index')

coordinates = read_coordinates('coordinates.csv')

fig, ax = plt.subplots(figsize=(16, 10))  # Increase the figure size for a larger map
node_color = 'black'

adjacencies = {}
canvas = None

def display_map(coordinates, start_town=None, end_town=None):
    global adjacencies, canvas

    node_color = 'black'

    # Iterate through the cities and create rectangles based on latitude and longitude
    for city, coord in coordinates.items():
        lat = coord['Latitude']
        lon = coord['Longitude']

        # Convert latitude and longitude to x and y coordinates
        x = lon
        y = lat

        if city == start_town:
            node_color = 'blue'  # Set the color for the starting city
        elif city == end_town:
            node_color = 'red'  # Set the color for the ending city
        else:
            node_color = 'black'

        # Make all node circles the same color
        ax.plot(x, y, 'o', markersize=10, alpha=0.5, color=node_color, label=city)

        # Display the city name on the node
        # Adjust the y-coordinate of the label to move it slightly higher
        label_y_offset = 0.03  # Adjust this value as needed
        plt.text(x, y + label_y_offset, city, fontsize=7, ha='center', va='bottom')
        
        if city in adjacencies:
            for adjacent_city in adjacencies[city]:
                if adjacent_city in coordinates:
                    adj_coords = coordinates[adjacent_city]
                    adj_x, adj_y = adj_coords['Longitude'], adj_coords['Latitude']
                    plt.plot([x, adj_x], [y, adj_y], linestyle='-', color='black', alpha=0.2)
    
    plt.title("Display Route Map", y=1.05)
    inform_text = "Blue = Start Town, Red = End Town, Black = Visited Town"
    plt.text(0.5, 1.02, inform_text, fontsize=12, ha='center', va='center', transform=ax.transAxes)
    
    # Remove the rectangular frame
    ax.axis('off')
    
    # Make a separate Tkinter canvas to embed the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Define a variable to keep track of whether the route is currently displayed
displayedRoute = False

# Store the current route to this variable
route = []

# Create a canvas in the main_frame
canvas = Canvas(main_frame, bg='white')
canvas.pack(fill="both", expand=True)  # Fill and expand the canvas to the available space
canvas.configure(height=1024)

# Call the function to display the map
display_map(coordinates)

# Main Menu
main_menu = tk.Menu(window)
window.config(menu=main_menu)

def reset_app():
    global selected_search_method, textbox1, textbox2, result_text, resultTitle # Reference result_text as a global variable

    # Clear the text fields
    if textbox1 is not None:
        textbox1.delete(0, tk.END)
    if textbox2 is not None:
        textbox2.delete(0, tk.END)

    # Reset the selected search method
    if selected_search_method is not None:
        selected_search_method.set("Choose Search Method")

    # Remove the results text box from the frame, if it exists
    if result_text is not None:
        result_text.destroy()
        result_text = None

    # Remove the resultTitle label from the frame, if it exists
    if resultTitle is not None:
        resultTitle.destroy()
        resultTitle = None
    

main_menu.add('command', label='Reset', command=reset_app)
main_menu.add('command', label='Exit', command=window.quit)

textbox1 = None
textbox2 = None
selected_search_method = None

# Options Frame Contains
def searchInput():
    label1 = tk.Label(options_frame, text='Starting State', bg='#ffffff', font=('Times', 12))
    label1.pack(pady=(25,0), padx=(0, 175))

    global textbox1
    textbox1 = Entry(options_frame, font=('Times', 12), width=30)
    textbox1.pack(pady=(10,0), padx=(0, 20))

    label2 = tk.Label(options_frame, text='Goal State', bg='#ffffff', font=('Times', 12))
    label2.pack(pady=(15,0), padx=(0, 195))
    
    global textbox2
    textbox2 = Entry(options_frame, font=('Times', 12), width=30)
    textbox2.pack(pady=(10,0), padx=(0, 20))

    # Create a black line below the subtitle label
    line_canvas2 = tk.Canvas(options_frame, width=350, height=2, bg='black', highlightthickness=0)
    line_canvas2.pack(pady=(30, 0))

searchInput()

# Create a search button
def perform_search():
    global result_text, resultTitle, displayedRoute, route  # Reference the global result_text variable
    start_town = textbox1.get()
    end_town = textbox2.get()

    # Validate user input
    if not validate_input(start_town, end_town):
        return

    # Get the selected search method
    input_search_method = selected_search_method.get()

    # Remove the results text box from the frame, if it exists
    if result_text is not None:
        result_text.destroy()
        result_text = None

    # Remove the resultTitle label from the frame, if it exists
    if resultTitle is not None:
        resultTitle.destroy()
        resultTitle = None

    resultTitle = tk.Label(options_frame, text='The Result', bg='#ffffff', font=('Times', 12))
    resultTitle.pack(pady=(25,0), padx=(0, 200))

    if start_town not in adjacencies or end_town not in adjacencies:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Invalid town names. Please try again.")
        return

    input_search_method = selected_search_method.get()
    result_text = Text(options_frame, font=('Times', 12), width=40, height=10, bg='#ffffff', highlightthickness=0, borderwidth=0)
    result_text.pack(pady=(10, 0), padx=(40, 20))

    ax.clear()
    display_map(coordinates, start_town, end_town)
    displayedRoute = False

    if input_search_method == 'Breadth-First Search':
        # Measure execution time using timeit
        start_time = timeit.default_timer()
        route = breadth_first_search(start_town, end_town, adjacencies)
        end_time = timeit.default_timer()
        
        if route:
            # Plot the cities in the route and connect them with lines
            plot_route(route)
            # Set displayedRoute to True to indicate that the route is displayed
            displayedRoute = True
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Shortest Route (BFS): {' -> '.join(route)}\n")
            result_text.insert(tk.END, f"Total Distance: {len(route) - 1} nodes\n")
            result_text.insert(tk.END, f"Total Distance: {total_distance(route, coordinates):.2f} kilometers\n")
            result_text.insert(tk.END, f"Time Taken: {end_time - start_time:.6f} seconds")
        else:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "No route found.")
    
    elif input_search_method == 'Depth-First Search':
        # Measure execution time using timeit
        start_time = timeit.default_timer()
        route = depth_first_search(start_town, end_town, adjacencies)
        end_time = timeit.default_timer()

        if route:
            # Plot the cities in the route and connect them with lines
            plot_route(route)
            # Set displayedRoute to True to indicate that the route is displayed
            displayedRoute = True
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Shortest Route (Depth-First Search): {' -> '.join(route)}\n")
            result_text.insert(tk.END, f"Total Distance: {len(route) - 1} nodes\n")
            result_text.insert(tk.END, f"Total Distance: {total_distance(route, coordinates):.2f} kilometers\n")
            result_text.insert(tk.END, f"Time Taken: {end_time - start_time:.6f} seconds")
        else:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "No route found using Depth-First Search.")

    elif input_search_method == 'ID-Depth First Search':
        # Measure execution time using timeit
        start_time = timeit.default_timer()
        route = iterative_deepening_dfs(start_town, end_town, adjacencies)
        end_time = timeit.default_timer()

        if route:
            # Plot the cities in the route and connect them with lines
            plot_route(route)
            # Set displayedRoute to True to indicate that the route is displayed
            displayedRoute = True
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Shortest Route (Iterative Deepening DFS): {' -> '.join(route)}\n")
            result_text.insert(tk.END, f"Total Distance: {len(route) - 1} nodes\n")
            result_text.insert(tk.END, f"Total Distance: {total_distance(route, coordinates):.2f} kilometers\n")
            result_text.insert(tk.END, f"Time Taken: {end_time - start_time:.6f} seconds")
        else:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "No route found using Iterative Deepening DFS.")

    elif input_search_method == 'Best-First Search':
        # Calculate the heuristic value for the current and goal cities
        heuristic_value = heuristic_distance(start_town, end_town, coordinates)

        # Measure execution time using timeit
        start_time = timeit.default_timer()
        route = best_first_search(start_town, end_town, heuristic_value, adjacencies, coordinates)
        end_time = timeit.default_timer()

        if route:
            # Plot the cities in the route and connect them with lines
            plot_route(route)
            # Set displayedRoute to True to indicate that the route is displayed
            displayedRoute = True
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Shortest Route (Best-First Search): {' -> '.join(route)}\n")
            result_text.insert(tk.END, f"Total Distance: {len(route) - 1} nodes\n")
            result_text.insert(tk.END, f"Total Distance: {total_distance(route, coordinates):.2f} kilometers\n")
            result_text.insert(tk.END, f"Time Taken: {end_time - start_time:.6f} seconds")
        else:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "No route found using Best-First Search.")
    
    elif input_search_method == 'A* Search':
        # Calculate the heuristic value for the current and goal cities
        heuristic_value = heuristic_distance(start_town, end_town, coordinates)

        # Measure execution time using timeit
        start_time = timeit.default_timer()
        route = a_star_search(start_town, end_town, adjacencies, heuristic_value, coordinates)
        end_time = timeit.default_timer()

        if route:
            # Plot the cities in the route and connect them with lines
            plot_route(route)
            # Set displayedRoute to True to indicate that the route is displayed
            displayedRoute = True
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Shortest Route (A* Search): {' -> '.join(route)}\n")
            result_text.insert(tk.END, f"Total Distance: {len(route) - 1} nodes\n")
            result_text.insert(tk.END, f"Total Distance: {total_distance(route, coordinates):.2f} kilometers\n")
            result_text.insert(tk.END, f"Time Taken: {end_time - start_time:.6f} seconds")
        else:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "No route found using A* Search.")

def plot_route(route):
    route_coordinates = [coordinates[city] for city in route]
    route_x, route_y = zip(*[(coords['Longitude'], coords['Latitude']) for coords in route_coordinates])
    
    # Plot lines connecting the cities in the route
    ax.plot(route_x, route_y, 'o-', markersize=10, alpha=0.5, color=node_color, label='Route')
    
    # Display the city names on the nodes
    for x, y, city in zip(route_x, route_y, route):
        label_y_offset = 0.03  # Adjust this value as needed
        plt.text(x, y + label_y_offset, city, fontsize=7, ha='center', va='bottom')

    # Set the title at the top
    plt.title("Display Route Map", y=1.05)

    # Add additional text below the title
    inform_text = "Blue = Start Town, Red = End Town, Black = Visited Town"
    plt.text(0.5, 1.02, inform_text, fontsize=12, ha='center', va='center', transform=ax.transAxes)

    # Remove the rectangular frame
    ax.axis('off')

def searchMethodOption():
    global selected_search_method  # Access the global variable
    
    label3 = tk.Label(options_frame, text='Search Methods', bg='#ffffff', font=('Times', 12))
    label3.pack(pady=(25,0), padx=(0, 175))
    
    # Create a ComboBox
    combo = ttk.Combobox(
        options_frame, 
        values=["Breadth-First Search", "Depth-First Search", "ID-Depth First Search", "Best-First Search", "A* Search"], 
        font=('Times', 12), width=28, state="readonly")
    combo.set("Choose Search Method")  # Set the default value
    combo.pack(pady=(10, 0), padx=(0, 26))

    # Create a search button
    search_button = Button(options_frame, text="Start Search", command=perform_search)
    search_button.pack(pady=(20, 0), padx=(0,20))

    # Set the global variable to the selected value
    selected_search_method = combo
    return search_button

search_button = searchMethodOption()
search_button.pack(pady=(20, 20), padx=(0,20))

def validate_input(start_town, end_town):
    if not start_town or not end_town:
        messagebox.showerror("Input Error", "Please enter both starting and ending towns.")
        return False
    elif start_town not in adjacencies or end_town not in adjacencies:
        messagebox.showerror("Input Error", "Invalid town names. Please check your input.")
        return False
    return True

# Create a black line below the subtitle label
line_canvas2 = tk.Canvas(options_frame, width=350, height=2, bg='black', highlightthickness=0)
line_canvas2.pack(pady=(30, 0))

#Search Method Program Section

## Read adjacency data from a txt file
def read_adjacencies(file_path):
    adjacencies = {}
    with open(file_path, 'r') as file:
        for line in file:
            c1, c2 = line.split()
            adjacencies.setdefault(c1, []).append(c2)
            adjacencies.setdefault(c2, []).append(c1)
    return adjacencies

adjacencies = read_adjacencies('Adjacencies.txt')

# Calculate the distance between two coordinates using Haversine formula
def haversine_distance(lat1, lon1, lat2, lon2):
    #Earth Radius in kilometers
    R = 6371.0
    # Convert lat and longit from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    # Differences in latitude and longitude
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    # Haversine formula
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# Calculate the total distance for a given route
def total_distance(route, coordinates):
    total = 0
    for i in range(1, len(route)):
        city1, city2 = route[i - 1], route[i]
        lat1, lon1 = coordinates[city1]['Latitude'], coordinates[city1]['Longitude']
        lat2, lon2 = coordinates[city2]['Latitude'], coordinates[city2]['Longitude']
        total += haversine_distance(lat1, lon1, lat2, lon2)
    return total

# Calculate the heuristic distance between two cities
def heuristic_distance(city1, city2, coordinates):
    lat1, lon1 = coordinates[city1]['Latitude'], coordinates[city1]['Longitude']
    lat2, lon2 = coordinates[city2]['Latitude'], coordinates[city2]['Longitude']
    #Calculate the straight-line (Euclidean) distance
    return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)

# Function to perform a breadth-first search
def breadth_first_search(start, end, adjacencies):
    visited = set()
    queue = deque([[start]])

    while queue:
        path = queue.popleft()
        current_town = path[-1]

        if current_town == end:
            return path

        if current_town not in visited:
            visited.add(current_town)
            for neighbor in adjacencies[current_town]:
                new_path = path + [neighbor]
                queue.append(new_path)

    return None

# Function to perform a depth-first search
def depth_first_search(start, end, adjacencies):
    def dfs_recursive(current_town, path, visited):
        visited.add(current_town)

        if current_town == end:
            return path

        for neighbor in adjacencies[current_town]:
            if neighbor not in visited:
                new_path = dfs_recursive(neighbor, path + [neighbor], visited)
                if new_path:
                    return new_path

    if start not in adjacencies or end not in adjacencies:
        return None

    return dfs_recursive(start, [start], set())

# Function to perform iterative deepening depth-first search (IDDFS)
def iterative_deepening_dfs(start, end, adjacencies):
    def depth_limited_dfs(node, goal, depth_limit, visited):
        if node == goal:
            return [node]
        if depth_limit <= 0:
            return None

        visited.add(node)
        for neighbor in adjacencies[node]:
            if neighbor not in visited:
                path = depth_limited_dfs(neighbor, goal, depth_limit - 1, visited)
                if path is not None:
                    return [node] + path

        return None

    max_depth = 1
    while True:
        visited = set()
        path = depth_limited_dfs(start, end, max_depth, visited)
        if path is not None:
            return path
        max_depth += 1

        return None

# Function to perform a best-first search
def best_first_search(start, end, heuristic_value, adjacencies, coordinates):
    frontier = [(0, start)]  # Priority queue with (priority, city) tuples
    came_from = {}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)  # Get the city with the lowest estimated cost
        if current == end:
            # Reconstruct the path from start to end
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor in adjacencies[current]:
            new_cost = cost_so_far[current] + haversine_distance(
                coordinates[current]['Latitude'], coordinates[current]['Longitude'],
                coordinates[neighbor]['Latitude'], coordinates[neighbor]['Longitude']
            )
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic_value  # Use the provided heuristic value
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    return None

# Function to perform A* search
def a_star_search(start, end, adjacencies, heuristic_value, coordinates):
    frontier = [(0, start)]  # Priority queue with (priority, city) tuples
    came_from = {}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)  # Get the city with the lowest estimated cost
        if current == end:
            # Reconstruct the path from start to end
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor in adjacencies[current]:
            new_cost = cost_so_far[current] + haversine_distance(
                coordinates[current]['Latitude'], coordinates[current]['Longitude'],
                coordinates[neighbor]['Latitude'], coordinates[neighbor]['Longitude']
            )
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic_value + heuristic_distance(neighbor, end, coordinates)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    return None

plt.show()

window.mainloop()

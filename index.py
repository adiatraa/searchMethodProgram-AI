import tkinter as tk
from tkinter import Button, Entry, Frame, OptionMenu, Text, font, Canvas, ttk
import time
import itertools
import heapq
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

# Create a canvas in the main_frame
canvas = Canvas(main_frame, bg='white')
canvas.pack(fill="both", expand=True)  # Fill and expand the canvas to the available space
canvas.configure(height=1024)

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
    global result_text, resultTitle  # Reference the global result_text variable
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

    if input_search_method == 'Breadth-First Search':
        # Measure execution time using timeit
        start_time = timeit.default_timer()
        route = breadth_first_search(start_town, end_town, adjacencies)
        end_time = timeit.default_timer()
        
        if route:
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
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Shortest Route (A* Search): {' -> '.join(route)}\n")
            result_text.insert(tk.END, f"Total Distance: {len(route) - 1} nodes\n")
            result_text.insert(tk.END, f"Total Distance: {total_distance(route, coordinates):.2f} kilometers\n")
            result_text.insert(tk.END, f"Time Taken: {end_time - start_time:.6f} seconds")
        else:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "No route found using A* Search.")

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

# def result_text():
    
# result_text()

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

# Read coordinates from a CSV file
def read_coordinates(file_path):
    coordinates = pd.read_csv(file_path, header=None, names=['City', 'Latitude', 'Longitude'])
    return coordinates.set_index('City').to_dict(orient='index')

coordinates = read_coordinates('coordinates.csv')

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

window.mainloop()


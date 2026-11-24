import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================================
# PART 1: DATA STRUCTURES
# ==========================================================

# 1. Singly Linked List -> Stores all confirmed booking records
class BookingNode:
    def __init__(self, customer_name, movie_id):
        self.customer_name = customer_name
        self.movie_id = movie_id
        self.next = None


class BookingLinkedList:
    def __init__(self):
        self.head = None

    def add_booking(self, customer_name, movie_id):
        new_node = BookingNode(customer_name, movie_id)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    def get_all(self):
        records = []
        current = self.head
        while current is not None:
            records.append(f"Customer: {current.customer_name} | Movie ID: {current.movie_id}")
            current = current.next
        return records


# 2. Queue (FIFO) -> Stores waiting list customers
class WaitingQueue:
    def __init__(self):
        self.items = []

    def enqueue(self, customer_name, movie_id):
        self.items.append((customer_name, movie_id))

    def dequeue(self):
        return self.items.pop(0) if self.items else None

    def peek_front(self):
        return self.items[0] if self.items else None

    def get_all(self):
        return [f"{i + 1}. {name} (Movie ID: {m_id})" for i, (name, m_id) in enumerate(self.items)]


# 3. Stack (LIFO) -> Stores recent bookings
class RecentBookingsStack:
    def __init__(self):
        self.items = []

    def push(self, customer_name, movie_id):
        self.items.append((customer_name, movie_id))

    def peek(self):
        return self.items[-1] if self.items else None

    def pop(self):
        return self.items.pop() if self.items else None

    def get_all_top_first(self):
        return [f"Customer: {c} | Movie ID: {m}" for c, m in reversed(self.items)]


# ==========================================================
# PART 2: ALGORITHMS
# ==========================================================

def linear_search_by_name(movie_list, target_name):
    for movie in movie_list:
        if movie["name"].lower() == target_name.lower():
            return movie
    return None


def binary_search_by_id(movie_list, target_id):
    sorted_movies = sorted(movie_list, key=lambda m: m["id"])
    low, high = 0, len(sorted_movies) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_movies[mid]["id"] == target_id:
            return sorted_movies[mid]
        elif sorted_movies[mid]["id"] < target_id:
            low = mid + 1
        else:
            high = mid - 1
    return None


def count_movies_recursive(movie_list):
    if len(movie_list) == 0:
        return 0
    return 1 + count_movies_recursive(movie_list[1:])


# ==========================================================
# PART 3: INITIAL SAMPLE DATA (Python List)
# ==========================================================

movies = [
    {"id": 101, "name": "Avengers", "genre": "Action", "seats": 10},
    {"id": 102, "name": "Titanic", "genre": "Romance", "seats": 8},
    {"id": 103, "name": "Jurassic Park", "genre": "Adventure", "seats": 5},
    {"id": 104, "name": "The Batman", "genre": "Action", "seats": 7},
    {"id": 105, "name": "Frozen", "genre": "Animation", "seats": 6},
]

bookings_list = BookingLinkedList()
waiting_queue = WaitingQueue()
recent_stack = RecentBookingsStack()


# ==========================================================
# PART 4: GUI FUNCTIONS
# ==========================================================

def set_status(message):
    status_var.set(f"  {message}")


def clear_inputs():
    for field in (entry_id, entry_name, entry_genre, entry_seats, entry_customer):
        field.delete(0, tk.END)
    set_status("Input fields cleared.")


def refresh_dsa_views():
    lb_bookings.delete(0, tk.END)
    for item in bookings_list.get_all():
        lb_bookings.insert(tk.END, item)

    lb_waiting.delete(0, tk.END)
    for item in waiting_queue.get_all():
        lb_waiting.insert(tk.END, item)

    lb_recent.delete(0, tk.END)
    for item in recent_stack.get_all_top_first():
        lb_recent.insert(tk.END, item)


def view_movies(subset=None, keep_id=None):
    """Refresh the movie table while optionally keeping the same movie selected."""
    for row in tree.get_children():
        tree.delete(row)
    data = subset if subset is not None else movies
    for m in data:
        item_id = tree.insert("", tk.END, values=(m["id"], m["name"], m["genre"], m["seats"]))
        if keep_id is not None and m["id"] == keep_id:
            tree.selection_set(item_id)
            tree.focus(item_id)
    if subset is None and keep_id is None:
        set_status(f"Displaying all {len(movies)} movies.")


def on_row_select(event):
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, "values")
    if values:
        for field, val in zip((entry_id, entry_name, entry_genre, entry_seats), values):
            field.delete(0, tk.END)
            field.insert(0, val)
        set_status(f"Selected: {values[1]} (ID: {values[0]})")


def add_movie():
    try:
        m_id = int(entry_id.get().strip())
        name = entry_name.get().strip()
        genre = entry_genre.get().strip()
        seats = int(entry_seats.get().strip())
        if not name or not genre or seats < 0:
            messagebox.showwarning("Input Error", "Please enter valid movie details.")
            return
        if binary_search_by_id(movies, m_id):
            messagebox.showwarning("Duplicate ID", f"Movie ID {m_id} already exists.")
            return
        movies.append({"id": m_id, "name": name, "genre": genre, "seats": seats})
        view_movies(keep_id=m_id)
        set_status(f"Added movie '{name}' (ID: {m_id}).")
        messagebox.showinfo("Success", f"Movie '{name}' added.")
    except ValueError:
        messagebox.showerror("Input Error", "Movie ID and Available Seats must be numbers.")


def update_movie():
    try:
        m_id = int(entry_id.get().strip())
        movie = binary_search_by_id(movies, m_id)
        if not movie:
            messagebox.showinfo("Result", "Movie Not Found.")
            return
        if entry_name.get().strip():
            movie["name"] = entry_name.get().strip()
        if entry_genre.get().strip():
            movie["genre"] = entry_genre.get().strip()
        if entry_seats.get().strip():
            seats = int(entry_seats.get().strip())
            if seats < 0:
                messagebox.showwarning("Input Error", "Seats cannot be negative.")
                return
            movie["seats"] = seats
        view_movies(keep_id=m_id)
        set_status(f"Updated Movie ID {m_id}.")
        messagebox.showinfo("Success", f"Movie ID {m_id} updated.")
    except ValueError:
        messagebox.showerror("Input Error", "Movie ID and Available Seats must be numbers.")


def search_by_name():
    target = entry_search.get().strip()
    if not target:
        messagebox.showwarning("Input Error", "Enter a movie name to search.")
        return
    result = linear_search_by_name(movies, target)
    if result:
        view_movies([result], keep_id=result["id"])
        set_status(f"Linear Search found: {result['name']}")
        messagebox.showinfo("Movie Found (Linear Search)",
                            f"ID: {result['id']}\nName: {result['name']}\nGenre: {result['genre']}\nSeats: {result['seats']}")
    else:
        set_status("Movie Not Found.")
        messagebox.showinfo("Result", "Movie Not Found.")


def search_by_id():
    try:
        target_id = int(entry_search.get().strip())
    except ValueError:
        messagebox.showerror("Input Error", "Enter a numeric Movie ID to search.")
        return
    result = binary_search_by_id(movies, target_id)
    if result:
        view_movies([result], keep_id=result["id"])
        set_status(f"Binary Search found: {result['name']} (ID: {target_id})")
        messagebox.showinfo("Movie Found (Binary Search)",
                            f"ID: {result['id']}\nName: {result['name']}\nGenre: {result['genre']}\nSeats: {result['seats']}")
    else:
        set_status("Movie Not Found.")
        messagebox.showinfo("Result", "Movie Not Found.")


def book_ticket():
    customer = entry_customer.get().strip()
    if not customer:
        messagebox.showwarning("Input Error", "Enter a customer name.")
        return
    try:
        m_id = int(entry_id.get().strip())
    except ValueError:
        messagebox.showerror("Input Error", "Select a movie from the table or enter a valid Movie ID.")
        return

    movie = binary_search_by_id(movies, m_id)
    if not movie:
        messagebox.showinfo("Result", "Movie Not Found.")
        return

    if movie["seats"] > 0:
        movie["seats"] -= 1
        bookings_list.add_booking(customer, m_id)
        recent_stack.push(customer, m_id)
        # Keep the same movie selected and update its seat count in the form
        view_movies(keep_id=m_id)
        entry_seats.delete(0, tk.END)
        entry_seats.insert(0, str(movie["seats"]))
        refresh_dsa_views()
        entry_customer.delete(0, tk.END)
        set_status(f"Booking Successful: {customer} -> '{movie['name']}' (Seats left: {movie['seats']})")
        messagebox.showinfo("Booking Successful", f"Ticket booked for {customer} ({movie['name']}).")
    else:
        waiting_queue.enqueue(customer, m_id)
        refresh_dsa_views()
        entry_customer.delete(0, tk.END)
        set_status(f"No Seats Available. {customer} added to Waiting List (Queue).")
        messagebox.showinfo("No Seats Available", f"No seats left for {movie['name']}.\n{customer} has been added to the Waiting List.")


def cancel_latest_booking():
    """Pop the latest booking from the Stack and free 1 seat for that movie."""
    removed = recent_stack.pop()
    if not removed:
        messagebox.showinfo("Cancel Booking", "No recent bookings to cancel.")
        return
    customer, m_id = removed
    movie = binary_search_by_id(movies, m_id)
    if movie:
        movie["seats"] += 1
        view_movies(keep_id=m_id)
        if entry_id.get().strip() == str(m_id):
            entry_seats.delete(0, tk.END)
            entry_seats.insert(0, str(movie["seats"]))
    refresh_dsa_views()
    set_status(f"Canceled booking for {customer} (Movie ID {m_id}). +1 seat freed.")
    messagebox.showinfo("Booking Canceled", f"Canceled {customer}'s booking for Movie ID {m_id}.\n1 seat is now available.")


def view_bookings_popup():
    records = bookings_list.get_all()
    text = "\n".join(records) if records else "No bookings yet."
    messagebox.showinfo("View Bookings (Singly Linked List)", text)


def view_waiting_popup():
    records = waiting_queue.get_all()
    text = "\n".join(records) if records else "Waiting list is empty."
    messagebox.showinfo("Waiting List (Queue - FIFO)", text)


def process_waiting_list():
    front = waiting_queue.peek_front()
    if not front:
        messagebox.showinfo("Waiting List", "No customers in the waiting list.")
        return
    customer, m_id = front
    movie = binary_search_by_id(movies, m_id)
    if movie and movie["seats"] > 0:
        waiting_queue.dequeue()
        movie["seats"] -= 1
        bookings_list.add_booking(customer, m_id)
        recent_stack.push(customer, m_id)
        view_movies(keep_id=m_id)
        refresh_dsa_views()
        set_status(f"Processed Waiting List: {customer} booked '{movie['name']}'.")
        messagebox.showinfo("Booking Successful", f"Seat assigned to {customer} for {movie['name']}.")
    else:
        messagebox.showinfo("No Seats Available", f"Still 0 seats for {customer} (Movie ID {m_id}).\nFree a seat or update seats first.")


def view_latest_booking():
    latest = recent_stack.peek()
    if latest:
        messagebox.showinfo("Recent Bookings (Stack - Peek)", f"Latest Booking:\nCustomer: {latest[0]} | Movie ID: {latest[1]}")
    else:
        messagebox.showinfo("Recent Bookings (Stack)", "No recent bookings.")


def count_movies():
    total = count_movies_recursive(movies)
    set_status(f"Total movies (Recursion): {total}")
    messagebox.showinfo("Count Movies (Recursion)", f"Total movies in system: {total}")


# ==========================================================
# PART 5: GUI WINDOW & LAYOUT
# ==========================================================

root = tk.Tk()
root.title("Movie Ticket Booking System")
root.geometry("860x650")
root.minsize(820, 610)
root.configure(bg="#f4f6f9")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", rowheight=26, font=("Segoe UI", 10))
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#2c3e50", foreground="white")
style.map("Treeview", background=[("selected", "#3498db")])

# Title Header
header = tk.Frame(root, bg="#2c3e50", height=54)
header.pack(fill="x")
tk.Label(header, text="Movie Ticket Booking System", bg="#2c3e50", fg="white",
         font=("Segoe UI", 16, "bold")).pack(pady=11)

# Top Search & Utility Bar
top_bar = tk.Frame(root, bg="#f4f6f9")
top_bar.pack(fill="x", padx=15, pady=(10, 6))

tk.Label(top_bar, text="Search (Name or ID):", bg="#f4f6f9", font=("Segoe UI", 10)).pack(side="left", padx=(0, 6))
entry_search = ttk.Entry(top_bar, width=22)
entry_search.pack(side="left", padx=(0, 8))

ttk.Button(top_bar, text="Search by Name", command=search_by_name).pack(side="left", padx=3)
ttk.Button(top_bar, text="Search by ID", command=search_by_id).pack(side="left", padx=3)
ttk.Button(top_bar, text="View Movies", command=lambda: view_movies()).pack(side="left", padx=3)
ttk.Button(top_bar, text="Count Movies", command=count_movies).pack(side="right", padx=3)

# Movie Table
table_frame = tk.Frame(root, bg="#f4f6f9")
table_frame.pack(fill="both", expand=True, padx=15, pady=5)

columns = ("ID", "Name", "Genre", "Available Seats")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)
for col, width in zip(columns, (90, 270, 190, 130)):
    tree.heading(col, text=col)
    tree.column(col, width=width, anchor="center")

scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scroll.set)
tree.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")
tree.bind("<<TreeviewSelect>>", on_row_select)

# Tabbed Bottom Section
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=15, pady=10)

# --- TAB 1: Manage Movies & Book Ticket ---
tab_main = tk.Frame(notebook, bg="#f4f6f9", padx=10, pady=10)
notebook.add(tab_main, text="  Manage Movies & Book Ticket  ")
tab_main.columnconfigure(0, weight=1)
tab_main.columnconfigure(1, weight=1)

# Left: Add / Update Movie
movie_box = tk.LabelFrame(tab_main, text=" Movie Details (Click a row above to select) ",
                          bg="#f4f6f9", font=("Segoe UI", 10, "bold"), padx=10, pady=8)
movie_box.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

fields = []
for i, label in enumerate(["Movie ID:", "Movie Name:", "Genre:", "Available Seats:"]):
    tk.Label(movie_box, text=label, bg="#f4f6f9", font=("Segoe UI", 10)).grid(row=i, column=0, sticky="e", pady=4, padx=5)
    ent = ttk.Entry(movie_box, width=24)
    ent.grid(row=i, column=1, sticky="w", pady=4, padx=5)
    fields.append(ent)
entry_id, entry_name, entry_genre, entry_seats = fields

m_btns = tk.Frame(movie_box, bg="#f4f6f9")
m_btns.grid(row=4, column=0, columnspan=2, pady=(8, 0))
tk.Button(m_btns, text="Add Movie", command=add_movie, bg="#27ae60", fg="white",
          font=("Segoe UI", 9, "bold"), width=11, relief="flat").pack(side="left", padx=4)
tk.Button(m_btns, text="Update Movie", command=update_movie, bg="#2980b9", fg="white",
          font=("Segoe UI", 9, "bold"), width=12, relief="flat").pack(side="left", padx=4)
tk.Button(m_btns, text="Clear", command=clear_inputs, bg="#7f8c8d", fg="white",
          font=("Segoe UI", 9, "bold"), width=8, relief="flat").pack(side="left", padx=4)

# Right: Book Ticket
book_box = tk.LabelFrame(tab_main, text=" Ticket Booking ",
                         bg="#f4f6f9", font=("Segoe UI", 10, "bold"), padx=10, pady=8)
book_box.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

tk.Label(book_box, text="Customer Name:", bg="#f4f6f9", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="e", pady=8, padx=5)
entry_customer = ttk.Entry(book_box, width=24)
entry_customer.grid(row=0, column=1, sticky="w", pady=8, padx=5)

tk.Button(book_box, text="Book Ticket", command=book_ticket, bg="#e67e22", fg="white",
          font=("Segoe UI", 10, "bold"), relief="flat", pady=5).grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=6)

tk.Button(book_box, text="Cancel Latest Booking (+1 Seat)", command=cancel_latest_booking, bg="#c0392b", fg="white",
          font=("Segoe UI", 9, "bold"), relief="flat", pady=4).grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=4)

tk.Label(book_box, text="How Waiting List works:\n1. Book until a movie reaches 0 seats (or update seats to 0).\n2. Book again -> customer joins the Waiting List (Queue).\n3. Click Cancel Latest Booking (+1 Seat) -> Process Waiting.",
         bg="#f4f6f9", fg="#555", justify="left", font=("Segoe UI", 8)).grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=4)

# --- TAB 2: Live DSA Records Viewer ---
tab_dsa = tk.Frame(notebook, bg="#f4f6f9", padx=10, pady=10)
notebook.add(tab_dsa, text="  DSA Records (Linked List / Queue / Stack)  ")
for col in range(3):
    tab_dsa.columnconfigure(col, weight=1)

# Column 1: Singly Linked List
f_ll = tk.LabelFrame(tab_dsa, text=" Bookings (Singly Linked List) ", bg="#f4f6f9", font=("Segoe UI", 9, "bold"), padx=6, pady=6)
f_ll.grid(row=0, column=0, sticky="nsew", padx=4)
lb_bookings = tk.Listbox(f_ll, height=7, font=("Segoe UI", 9))
lb_bookings.pack(fill="both", expand=True, pady=(0, 6))
ttk.Button(f_ll, text="View Bookings", command=view_bookings_popup).pack(fill="x")

# Column 2: Queue (FIFO)
f_q = tk.LabelFrame(tab_dsa, text=" Waiting List (Queue - FIFO) ", bg="#f4f6f9", font=("Segoe UI", 9, "bold"), padx=6, pady=6)
f_q.grid(row=0, column=1, sticky="nsew", padx=4)
lb_waiting = tk.Listbox(f_q, height=7, font=("Segoe UI", 9))
lb_waiting.pack(fill="both", expand=True, pady=(0, 6))
q_btns = tk.Frame(f_q, bg="#f4f6f9")
q_btns.pack(fill="x")
ttk.Button(q_btns, text="Waiting List", command=view_waiting_popup).pack(side="left", expand=True, fill="x", padx=(0, 2))
ttk.Button(q_btns, text="Process Waiting", command=process_waiting_list).pack(side="left", expand=True, fill="x", padx=(2, 0))

# Column 3: Stack (LIFO)
f_st = tk.LabelFrame(tab_dsa, text=" Recent Bookings (Stack - LIFO) ", bg="#f4f6f9", font=("Segoe UI", 9, "bold"), padx=6, pady=6)
f_st.grid(row=0, column=2, sticky="nsew", padx=4)
lb_recent = tk.Listbox(f_st, height=7, font=("Segoe UI", 9))
lb_recent.pack(fill="both", expand=True, pady=(0, 6))
st_btns = tk.Frame(f_st, bg="#f4f6f9")
st_btns.pack(fill="x")
ttk.Button(st_btns, text="Recent (Peek)", command=view_latest_booking).pack(side="left", expand=True, fill="x", padx=(0, 2))
ttk.Button(st_btns, text="Pop / Cancel", command=cancel_latest_booking).pack(side="left", expand=True, fill="x", padx=(2, 0))

# Bottom Status Bar
status_var = tk.StringVar(value="  Ready. Click a movie row to select it.")
tk.Label(root, textvariable=status_var, bd=1, relief="sunken", anchor="w",
         bg="#e9ecef", fg="#2c3e50", font=("Segoe UI", 9)).pack(side="bottom", fill="x")

view_movies()
refresh_dsa_views()

root.mainloop()
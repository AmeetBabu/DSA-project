import tkinter as tk
from tkinter import ttk, messagebox


class Movie:
    def __init__(self, movie_id, name, genre, seats):
        self.movie_id = int(movie_id)
        self.name = name.strip()
        self.genre = genre.strip()
        self.seats = int(seats)


class BookingNode:
    def __init__(self, customer, movie_id, movie_name):
        self.customer = customer
        self.movie_id = movie_id
        self.movie_name = movie_name
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.length = 0

    def append(self, customer, movie_id, movie_name):
        node = BookingNode(customer, movie_id, movie_name)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node
        self.length += 1

    def to_list(self):
        records = []
        current = self.head
        while current:
            records.append((current.customer, current.movie_id, current.movie_name))
            current = current.next
        return records


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, customer, movie_id, movie_name):
        self.items.append((customer, movie_id, movie_name))

    def dequeue(self):
        if not self.items:
            return None
        return self.items.pop(0)

    def peek(self):
        return self.items[0] if self.items else None

    def to_list(self):
        return list(self.items)


class Stack:
    def __init__(self):
        self.items = []

    def push(self, customer, movie_id, movie_name):
        self.items.append((customer, movie_id, movie_name))

    def peek(self):
        return self.items[-1] if self.items else None

    def pop(self):
        return self.items.pop() if self.items else None

    def to_list(self):
        return list(reversed(self.items))


class MovieBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Ticket Booking System")
        self.root.geometry("1080x680")
        self.root.minsize(900, 600)

        self.movies = [
            Movie(101, "Avengers", "Action", 10),
            Movie(102, "Titanic", "Romance", 8),
            Movie(103, "Jurassic Park", "Adventure", 5),
            Movie(104, "The Batman", "Action", 7),
            Movie(105, "Frozen", "Animation", 6),
        ]
        self.bookings = SinglyLinkedList()
        self.waiting = Queue()
        self.recent = Stack()

        self._build_ui()
        self.refresh_movies()

    def _build_ui(self):
        title = ttk.Label(self.root, text="Movie Ticket Booking System", font=("Segoe UI", 20, "bold"))
        title.pack(pady=(12, 8))

        main = ttk.Frame(self.root, padding=12)
        main.pack(fill="both", expand=True)

        left = ttk.Frame(main)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ttk.Label(left, text="Movies", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        columns = ("id", "name", "genre", "seats")
        self.movie_table = ttk.Treeview(left, columns=columns, show="headings", height=12)
        headings = [("id", "Movie ID"), ("name", "Movie Name"), ("genre", "Genre"), ("seats", "Available Seats")]
        for column, label in headings:
            self.movie_table.heading(column, text=label)
            width = 100 if column != "name" else 180
            self.movie_table.column(column, width=width, anchor="center")
        self.movie_table.pack(fill="both", expand=True)
        self.movie_table.bind("<<TreeviewSelect>>", self.select_movie)

        table_buttons = ttk.Frame(left)
        table_buttons.pack(fill="x", pady=(8, 0))
        ttk.Button(table_buttons, text="View Movies", command=self.refresh_movies).pack(side="left", padx=3)
        ttk.Button(table_buttons, text="View Bookings", command=self.show_bookings).pack(side="left", padx=3)
        ttk.Button(table_buttons, text="Waiting List", command=self.show_waiting).pack(side="left", padx=3)
        ttk.Button(table_buttons, text="Process Waiting", command=self.process_waiting).pack(side="left", padx=3)

        right = ttk.Frame(main, width=320)
        right.pack(side="right", fill="y")

        movie_box = ttk.LabelFrame(right, text="Movie Details", padding=10)
        movie_box.pack(fill="x")
        self.movie_id = tk.StringVar()
        self.movie_name = tk.StringVar()
        self.movie_genre = tk.StringVar()
        self.movie_seats = tk.StringVar()

        fields = [
            ("Movie ID", self.movie_id),
            ("Movie Name", self.movie_name),
            ("Genre", self.movie_genre),
            ("Available Seats", self.movie_seats),
        ]
        for label, var in fields:
            ttk.Label(movie_box, text=label).pack(anchor="w")
            ttk.Entry(movie_box, textvariable=var).pack(fill="x", pady=(0, 5))

        movie_actions = ttk.Frame(movie_box)
        movie_actions.pack(fill="x", pady=(4, 0))
        ttk.Button(movie_actions, text="Add Movie", command=self.add_movie).pack(side="left", expand=True, fill="x", padx=(0, 3))
        ttk.Button(movie_actions, text="Update Movie", command=self.update_movie).pack(side="left", expand=True, fill="x", padx=(3, 0))

        search_box = ttk.LabelFrame(right, text="Search", padding=10)
        search_box.pack(fill="x", pady=10)
        self.search_name = tk.StringVar()
        ttk.Entry(search_box, textvariable=self.search_name).pack(fill="x")
        ttk.Button(search_box, text="Search by Name", command=self.search_by_name).pack(fill="x", pady=(5, 0))
        ttk.Separator(search_box, orient="horizontal").pack(fill="x", pady=7)
        self.search_id = tk.StringVar()
        ttk.Entry(search_box, textvariable=self.search_id).pack(fill="x")
        ttk.Button(search_box, text="Search by ID", command=self.search_by_id).pack(fill="x", pady=(5, 0))

        booking_box = ttk.LabelFrame(right, text="Ticket Booking", padding=10)
        booking_box.pack(fill="x")
        ttk.Label(booking_box, text="Customer Name").pack(anchor="w")
        self.customer_name = tk.StringVar()
        ttk.Entry(booking_box, textvariable=self.customer_name).pack(fill="x", pady=(0, 7))
        ttk.Button(booking_box, text="Book Ticket", command=self.book_ticket).pack(fill="x")

        bottom = ttk.Frame(right)
        bottom.pack(fill="x", pady=10)
        ttk.Button(bottom, text="Recent Bookings", command=self.show_recent).pack(side="left", expand=True, fill="x", padx=(0, 3))
        ttk.Button(bottom, text="Count Movies", command=self.count_movies).pack(side="left", expand=True, fill="x", padx=(3, 0))

        ttk.Button(right, text="Clear Fields", command=self.clear_fields).pack(fill="x")

        self.status = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status, relief="sunken", anchor="w", padding=5)
        status_bar.pack(side="bottom", fill="x")

    def set_status(self, message):
        self.status.set(message)

    def clear_fields(self):
        for var in (self.movie_id, self.movie_name, self.movie_genre, self.movie_seats,
                    self.search_name, self.search_id, self.customer_name):
            var.set("")
        self.movie_table.selection_remove(self.movie_table.selection())

    def refresh_movies(self):
        for row in self.movie_table.get_children():
            self.movie_table.delete(row)
        for movie in self.movies:
            self.movie_table.insert("", "end", iid=str(movie.movie_id), values=(movie.movie_id, movie.name, movie.genre, movie.seats))
        self.set_status(f"Showing {len(self.movies)} movies")

    def select_movie(self, _event=None):
        selected = self.movie_table.selection()
        if not selected:
            return
        movie = self.find_movie_by_id(int(selected[0]))
        if movie:
            self.movie_id.set(str(movie.movie_id))
            self.movie_name.set(movie.name)
            self.movie_genre.set(movie.genre)
            self.movie_seats.set(str(movie.seats))

    def find_movie_by_id(self, movie_id):
        for movie in self.movies:
            if movie.movie_id == movie_id:
                return movie
        return None

    def add_movie(self):
        try:
            movie_id = int(self.movie_id.get().strip())
            seats = int(self.movie_seats.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Movie ID and Available Seats must be numbers.")
            return
        name = self.movie_name.get().strip()
        genre = self.movie_genre.get().strip()
        if not name or not genre:
            messagebox.showerror("Invalid Input", "Movie Name and Genre are required.")
            return
        if seats < 0:
            messagebox.showerror("Invalid Input", "Available Seats cannot be negative.")
            return
        if self.find_movie_by_id(movie_id):
            messagebox.showerror("Duplicate ID", "A movie with this ID already exists.")
            return
        self.movies.append(Movie(movie_id, name, genre, seats))
        self.refresh_movies()
        messagebox.showinfo("Movie Added", f"{name} was added successfully.")

    def update_movie(self):
        try:
            movie_id = int(self.movie_id.get().strip())
            seats = int(self.movie_seats.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Movie ID and Available Seats must be numbers.")
            return
        movie = self.find_movie_by_id(movie_id)
        if not movie:
            messagebox.showerror("Movie Not Found", "No movie exists with that ID.")
            return
        name = self.movie_name.get().strip()
        genre = self.movie_genre.get().strip()
        if not name or not genre:
            messagebox.showerror("Invalid Input", "Movie Name and Genre are required.")
            return
        if seats < 0:
            messagebox.showerror("Invalid Input", "Available Seats cannot be negative.")
            return
        movie.name = name
        movie.genre = genre
        movie.seats = seats
        self.refresh_movies()
        messagebox.showinfo("Movie Updated", f"{name} was updated successfully.")

    def linear_search_by_name(self, name):
        normalized = name.strip().lower()
        for movie in self.movies:
            if normalized in movie.name.lower():
                return movie
        return None

    def search_by_name(self):
        name = self.search_name.get().strip()
        if not name:
            messagebox.showwarning("Search", "Enter a movie name.")
            return
        movie = self.linear_search_by_name(name)
        if movie:
            messagebox.showinfo("Movie Found", f"ID: {movie.movie_id}\nName: {movie.name}\nGenre: {movie.genre}\nAvailable Seats: {movie.seats}")
        else:
            messagebox.showinfo("Movie Not Found", f"No movie matches '{name}'.")

    def binary_search_by_id(self, movie_id):
        sorted_movies = sorted(self.movies, key=lambda movie: movie.movie_id)
        low = 0
        high = len(sorted_movies) - 1
        while low <= high:
            middle = (low + high) // 2
            if sorted_movies[middle].movie_id == movie_id:
                return sorted_movies[middle]
            if sorted_movies[middle].movie_id < movie_id:
                low = middle + 1
            else:
                high = middle - 1
        return None

    def search_by_id(self):
        try:
            movie_id = int(self.search_id.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Movie ID must be a number.")
            return
        movie = self.binary_search_by_id(movie_id)
        if movie:
            messagebox.showinfo("Movie Found", f"ID: {movie.movie_id}\nName: {movie.name}\nGenre: {movie.genre}\nAvailable Seats: {movie.seats}")
        else:
            messagebox.showinfo("Movie Not Found", f"No movie has ID {movie_id}.")

    def book_ticket(self):
        customer = self.customer_name.get().strip()
        if not customer:
            messagebox.showwarning("Booking", "Enter the customer name.")
            return
        selected = self.movie_table.selection()
        if not selected:
            messagebox.showwarning("Booking", "Select a movie from the table.")
            return
        movie = self.find_movie_by_id(int(selected[0]))
        if not movie:
            messagebox.showerror("Booking", "Selected movie was not found.")
            return
        if movie.seats > 0:
            movie.seats -= 1
            self.bookings.append(customer, movie.movie_id, movie.name)
            self.recent.push(customer, movie.movie_id, movie.name)
            self.refresh_movies()
            self.customer_name.set("")
            messagebox.showinfo("Booking Successful", f"Ticket booked for {customer} at {movie.name}.\nSeats left: {movie.seats}")
        else:
            self.waiting.enqueue(customer, movie.movie_id, movie.name)
            messagebox.showinfo("No Seats Available", f"{customer} was added to the waiting list for {movie.name}.")

    def show_bookings(self):
        records = self.bookings.to_list()
        if not records:
            messagebox.showinfo("Bookings", "No bookings have been made.")
            return
        text = "\n".join(f"{i}. {customer} | Movie ID: {movie_id} | {movie_name}" for i, (customer, movie_id, movie_name) in enumerate(records, 1))
        messagebox.showinfo("Booking Records", text)

    def show_waiting(self):
        records = self.waiting.to_list()
        if not records:
            messagebox.showinfo("Waiting List", "The waiting list is empty.")
            return
        text = "\n".join(f"{i}. {customer} | Movie ID: {movie_id} | {movie_name}" for i, (customer, movie_id, movie_name) in enumerate(records, 1))
        messagebox.showinfo("Waiting List", text)

    def process_waiting(self):
        waiting = self.waiting.peek()
        if not waiting:
            messagebox.showinfo("Waiting List", "The waiting list is empty.")
            return
        customer, movie_id, movie_name = waiting
        movie = self.find_movie_by_id(movie_id)
        if not movie:
            self.waiting.dequeue()
            messagebox.showerror("Process Waiting", f"The movie '{movie_name}' no longer exists. The customer was removed.")
            return
        if movie.seats <= 0:
            messagebox.showwarning("No Seats", f"No seat is currently available for {movie.name}.")
            return
        waiting = self.waiting.dequeue()
        customer, movie_id, movie_name = waiting
        movie.seats -= 1
        self.bookings.append(customer, movie_id, movie_name)
        self.recent.push(customer, movie_id, movie_name)
        self.refresh_movies()
        messagebox.showinfo("Waiting Customer Processed", f"Ticket booked for {customer} at {movie.name}.\nSeats left: {movie.seats}")

    def show_recent(self):
        records = self.recent.to_list()
        if not records:
            messagebox.showinfo("Recent Bookings", "No recent bookings.")
            return
        text = "\n".join(f"{i}. {customer} | Movie ID: {movie_id} | {movie_name}" for i, (customer, movie_id, movie_name) in enumerate(records, 1))
        messagebox.showinfo("Recent Bookings (Latest First)", text)

    def count_movies_recursive(self, index=0):
        if index >= len(self.movies):
            return 0
        return 1 + self.count_movies_recursive(index + 1)

    def count_movies(self):
        count = self.count_movies_recursive()
        messagebox.showinfo("Movie Count", f"Total movies: {count}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieBookingApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

from database import Database


class FinanceApp:

    def __init__(self, root):

        self.root = root
        self.db = Database()

        self.root.title("NOVA Finance")
        self.root.geometry("1200x760")
        self.root.minsize(1000, 650)
        self.root.configure(bg="#F4F6FB")

        self.colors = {
            "sidebar": "#17243A",
            "sidebar_light": "#243650",
            "background": "#F4F6FB",
            "white": "#FFFFFF",
            "primary": "#14B8A6",
            "primary_dark": "#0F988A",
            "text": "#17243A",
            "muted": "#8994A7",
            "green": "#16A36A",
            "red": "#E35D6A",
            "border": "#E7EBF2"
        }

        self.setup_styles()
        self.create_layout()
        self.show_dashboard()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_styles(self):

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#17243A",
            rowheight=38,
            fieldbackground="#FFFFFF",
            font=("Segoe UI", 10),
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background="#EEF2F7",
            foreground="#526078",
            font=("Segoe UI", 10, "bold"),
            padding=12,
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[("selected", "#DDF5F1")],
            foreground=[("selected", "#17243A")]
        )

        style.configure(
            "TCombobox",
            padding=8,
            font=("Segoe UI", 10)
        )

    def create_layout(self):

        self.sidebar = tk.Frame(
            self.root,
            bg=self.colors["sidebar"],
            width=220
        )

        self.sidebar.pack(side="left", fill="y")

        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(
            self.root,
            bg=self.colors["background"]
        )

        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        logo = tk.Label(
            self.sidebar,
            text="NOVA",
            font=("Segoe UI", 25, "bold"),
            fg="#FFFFFF",
            bg=self.colors["sidebar"]
        )

        logo.pack(pady=(35, 3))

        subtitle = tk.Label(
            self.sidebar,
            text="FINANCE MANAGER",
            font=("Segoe UI", 8, "bold"),
            fg="#91A0B7",
            bg=self.colors["sidebar"]
        )

        subtitle.pack(pady=(0, 45))

        self.create_nav_button(
            "Dashboard",
            self.show_dashboard
        )

        self.create_nav_button(
            "Transactions",
            self.show_transactions
        )

        footer = tk.Label(
            self.sidebar,
            text="NOVA Finance  |  v1.0",
            font=("Segoe UI", 8),
            fg="#91A0B7",
            bg=self.colors["sidebar"]
        )

        footer.pack(side="bottom", pady=25)

        self.page = tk.Frame(
            self.content,
            bg=self.colors["background"]
        )

        self.page.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=25
        )

    def create_nav_button(self, title, command):

        button = tk.Button(
            self.sidebar,
            text="   " + title,
            command=command,
            anchor="w",
            font=("Segoe UI", 11, "bold"),
            fg="#D5DEEA",
            bg=self.colors["sidebar"],
            activebackground=self.colors["sidebar_light"],
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=20,
            pady=15
        )

        button.pack(fill="x", padx=12, pady=4)

    def clear_page(self):

        for widget in self.page.winfo_children():

            widget.destroy()


    def create_header(self, title, subtitle):

        header = tk.Frame(
            self.page,
            bg=self.colors["background"]
        )

        header.pack(fill="x", pady=(0, 25))

        title_label = tk.Label(
            header,
            text=title,
            font=("Segoe UI", 23, "bold"),
            fg=self.colors["text"],
            bg=self.colors["background"]
        )

        title_label.pack(anchor="w")

        subtitle_label = tk.Label(
            header,
            text=subtitle,
            font=("Segoe UI", 10),
            fg=self.colors["muted"],
            bg=self.colors["background"]
        )

        subtitle_label.pack(anchor="w", pady=(5, 0))

    def create_stat_card(
        self,
        parent,
        title,
        value,
        color
    ):

        card = tk.Frame(
            parent,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=7
        )

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 10),
            fg=self.colors["muted"],
            bg=self.colors["white"]
        ).pack(anchor="w", padx=18, pady=(20, 8))

        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 17, "bold"),
            fg=color,
            bg=self.colors["white"]
        )

        value_label.pack(anchor="w", padx=18, pady=(0, 20))

        return value_label

    def create_table(self, parent, height=8):

        container = tk.Frame(
            parent,
            bg=self.colors["white"]
        )

        container.pack(fill="both", expand=True)

        columns = (
            "ID",
            "Title",
            "Category",
            "Type",
            "Amount",
            "Date"
        )

        table = ttk.Treeview(
            container,
            columns=columns,
            show="headings",
            height=height
        )

        widths = {
            "ID": 45,
            "Title": 160,
            "Category": 120,
            "Type": 100,
            "Amount": 130,
            "Date": 110
        }

        for column in columns:

            table.heading(
                column,
                text=column
            )

            table.column(
                column,
                width=widths[column],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=table.yview
        )

        table.configure(
            yscrollcommand=scrollbar.set
        )

        table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        return table

    def fill_table(self, table, transactions):

        for item in table.get_children():

            table.delete(item)

        for transaction in transactions:

            transaction_id = transaction[0]
            title = transaction[1]
            amount = transaction[2]
            category = transaction[3]
            transaction_type = transaction[4]
            transaction_date = transaction[5]

            table.insert(
                "",
                "end",
                values=(
                    transaction_id,
                    title,
                    category,
                    transaction_type,
                    f"{amount:,.0f}",
                    transaction_date
                )
            )

    def show_dashboard(self):

        self.clear_page()

        self.create_header(
            "Dashboard",
            "Welcome to your personal finance overview."
        )

        income, expense, balance = self.db.get_summary()

        stats = tk.Frame(
            self.page,
            bg=self.colors["background"]
        )

        stats.pack(fill="x", pady=(0, 25))

        self.create_stat_card(
            stats,
            "TOTAL INCOME",
            f"{income:,.0f}",
            self.colors["green"]
        )

        self.create_stat_card(
            stats,
            "TOTAL EXPENSES",
            f"{expense:,.0f}",
            self.colors["red"]
        )

        self.create_stat_card(
            stats,
            "AVAILABLE BALANCE",
            f"{balance:,.0f}",
            self.colors["primary_dark"]
        )

        month_income, month_expense = (
            self.db.get_monthly_summary()
        )

        monthly = tk.Frame(
            self.page,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        monthly.pack(fill="x", pady=(0, 25))

        tk.Label(
            monthly,
            text="THIS MONTH",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors["muted"],
            bg=self.colors["white"]
        ).pack(anchor="w", padx=18, pady=(15, 8))

        monthly_text = (
            f"Income: {month_income:,.0f}     "
            f"Expenses: {month_expense:,.0f}"
        )

        tk.Label(
            monthly,
            text=monthly_text,
            font=("Segoe UI", 12, "bold"),
            fg=self.colors["text"],
            bg=self.colors["white"]
        ).pack(anchor="w", padx=18, pady=(0, 15))

        table_header = tk.Frame(
            self.page,
            bg=self.colors["background"]
        )

        table_header.pack(fill="x", pady=(0, 12))

        tk.Label(
            table_header,
            text="Recent Transactions",
            font=("Segoe UI", 14, "bold"),
            fg=self.colors["text"],
            bg=self.colors["background"]
        ).pack(side="left")

        tk.Button(
            table_header,
            text="View All",
            command=self.show_transactions,
            bg=self.colors["background"],
            fg=self.colors["primary_dark"],
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(side="right")

        self.dashboard_table = self.create_table(
            self.page,
            height=7
        )

        recent = self.db.get_transactions()[:7]

        self.fill_table(
            self.dashboard_table,
            recent
        )

    def show_transactions(self):

        self.clear_page()

        self.create_header(
            "Transactions",
            "Manage and track all your financial activities."
        )

        toolbar = tk.Frame(
            self.page,
            bg=self.colors["background"]
        )

        toolbar.pack(fill="x", pady=(0, 20))

        self.search_var = tk.StringVar()

        search_entry = tk.Entry(
            toolbar,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            relief="flat",
            bg=self.colors["white"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"]
        )

        search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=11,
            padx=(0, 10)
        )

        self.search_var.trace_add(
            "write",
            self.search_transactions
        )

        self.filter_var = tk.StringVar(value="All")

        filter_box = ttk.Combobox(
            toolbar,
            textvariable=self.filter_var,
            values=["All", "Income", "Expense"],
            state="readonly",
            width=12
        )

        filter_box.pack(
            side="left",
            padx=5,
            ipady=5
        )

        filter_box.bind(
            "<<ComboboxSelected>>",
            self.search_transactions
        )

        tk.Button(
            toolbar,
            text="+ Add Transaction",
            command=self.add_transaction_dialog,
            bg=self.colors["primary"],
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=10
        ).pack(side="left", padx=5)

        # Delete Button Section

        bottom = tk.Frame(
            self.page,
            bg=self.colors["background"]
        )

        bottom.pack(
            side="bottom",
            fill="x",
            pady=10
        )

        tk.Button(
            bottom,
            text="Delete Selected",
            command=self.delete_transaction,
            bg=self.colors["red"],
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10
        ).pack(side="right")

        # Transaction Table

        table_frame = tk.Frame(
            self.page,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        self.transaction_table = self.create_table(
            table_frame,
            height=10
        )

        self.fill_table(
            self.transaction_table,
            self.db.get_transactions()
        )

    def search_transactions(self, *args):

        search_text = self.search_var.get()

        transaction_type = self.filter_var.get()

        results = self.db.get_transactions(
            search=search_text,
            transaction_type=transaction_type
        )

        self.fill_table(
            self.transaction_table,
            results
        )

    def add_transaction_dialog(self):

        dialog = tk.Toplevel(self.root)

        dialog.title("Add Transaction")

        dialog.geometry("430x820")

        dialog.resizable(False, False)

        dialog.configure(bg="#FFFFFF")

        dialog.transient(self.root)

        dialog.grab_set()

        tk.Label(
            dialog,
            text="New Transaction",
            font=("Segoe UI", 19, "bold"),
            fg=self.colors["text"],
            bg="#FFFFFF"
        ).pack(anchor="w", padx=30, pady=(25, 5))

        tk.Label(
            dialog,
            text="Enter your transaction details below.",
            font=("Segoe UI", 9),
            fg=self.colors["muted"],
            bg="#FFFFFF"
        ).pack(anchor="w", padx=30, pady=(0, 20))

        fields = {}

        def create_field(label, default=""):

            tk.Label(
                dialog,
                text=label,
                font=("Segoe UI", 10, "bold"),
                fg=self.colors["text"],
                bg="#FFFFFF"
            ).pack(anchor="w", padx=30, pady=(8, 5))

            entry = tk.Entry(
                dialog,
                font=("Segoe UI", 10),
                relief="solid",
                bd=1
            )

            entry.pack(
                fill="x",
                padx=30,
                ipady=8
            )

            if default:

                entry.insert(0, default)

            fields[label] = entry

        create_field("Title")

        create_field("Amount")

        tk.Label(
            dialog,
            text="Transaction Type",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors["text"],
            bg="#FFFFFF"
        ).pack(anchor="w", padx=30, pady=(12, 5))

        type_var = tk.StringVar(value="Expense")

        type_box = ttk.Combobox(
            dialog,
            textvariable=type_var,
            values=["Income", "Expense"],
            state="readonly"
        )

        type_box.pack(
            fill="x",
            padx=30,
            ipady=5
        )

        tk.Label(
            dialog,
            text="Category",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors["text"],
            bg="#FFFFFF"
        ).pack(anchor="w", padx=30, pady=(12, 5))

        category_var = tk.StringVar(value="Other")

        category_box = ttk.Combobox(
            dialog,
            textvariable=category_var,
            values=[
                "Food",
                "Shopping",
                "Transport",
                "Education",
                "Health",
                "Entertainment",
                "Salary",
                "Business",
                "Other"
            ],
            state="readonly"
        )

        category_box.pack(
            fill="x",
            padx=30,
            ipady=5
        )

        create_field(
            "Date",
            date.today().strftime("%Y-%m-%d")
        )

        create_field("Note")

        def save():

            title = fields["Title"].get().strip()

            amount_text = fields["Amount"].get().strip()

            transaction_date = fields["Date"].get().strip()

            note = fields["Note"].get().strip()

            if not title or not amount_text:

                messagebox.showwarning(
                    "Missing Information",
                    "Please enter title and amount.",
                    parent=dialog
                )

                return

            try:

                amount = float(amount_text)

                if amount <= 0:

                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    "Invalid Amount",
                    "Please enter a valid positive number.",
                    parent=dialog
                )

                return

            try:

                datetime.strptime(
                    transaction_date,
                    "%Y-%m-%d"
                )

            except ValueError:
                messagebox.showerror(
                    "Invalid Date",
                    "Date format must be YYYY-MM-DD.",
                    parent=dialog
                )

                return

            self.db.add_transaction(
                title,
                amount,
                category_var.get(),
                type_var.get(),
                transaction_date,
                note
            )

            dialog.destroy()

            self.refresh_data()

            messagebox.showinfo(
                "Success",
                "Transaction added successfully!"
            )

        tk.Button(
            dialog,
            text="Save Transaction",
            command=save,
            bg=self.colors["primary"],
            fg="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(
            fill="x",
            padx=30,
            pady=22,
            ipady=10
        )
    def delete_transaction(self):

        selected = self.transaction_table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a transaction first."
            )

            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this transaction?"
        )

        if not confirm:

            return

        for item in selected:

            values = self.transaction_table.item(
                item,
                "values"
            )

            transaction_id = values[0]

            self.db.delete_transaction(
                transaction_id
            )

        self.refresh_data()

        messagebox.showinfo(
            "Deleted",
            "Transaction deleted successfully."
        )

    def refresh_data(self):

        if self.transaction_table_exists():

            self.fill_table(
                self.transaction_table,
                self.db.get_transactions(
                    search=self.search_var.get(),
                    transaction_type=self.filter_var.get()
                )
            )

        elif hasattr(self, "dashboard_table"):

            if self.dashboard_table.winfo_exists():

                self.show_dashboard()


    def transaction_table_exists(self):

        return (
            hasattr(self, "transaction_table")
            and self.transaction_table.winfo_exists()
        )


    def on_close(self):

        self.db.close()

        self.root.destroy()
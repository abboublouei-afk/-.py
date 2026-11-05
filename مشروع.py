from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import tkinter as tk
from tkinter import messagebox, ttk


class PharmacyApp:

  def __init__(self, root):
    self.root = root
    self.root.title("النظام الذكي لإدارة الصيدلية")
    self.root.geometry("820x720")
    self.root.configure(bg="#f4f9f4")

    # لوحة الألوان الرسمية للصيدليات الرقمية
    self.PRIMARY = "#1b5e20"
    self.ACCENT = "#2e7d32"
    self.LIGHT_BG = "#e8f5e9"
    self.DANGER = "#c62828"
    self.WHITE = "#ffffff"

    # تنسيق عام للـ Widgets
    self.style = ttk.Style()
    self.style.theme_use("clam")
    self.style.configure(
        "Treeview.Heading",
        background=self.PRIMARY,
        foreground=self.WHITE,
        font=("Helvetica", 10, "bold"),
    )
    self.style.configure(
        "Treeview", font=("Helvetica", 10), rowheight=25, fieldbackground=self.WHITE
    )

    self.admin_email = "loueiabbob@gmail.com"
    self.admin_pass = "12345"
    self.current_user = None

    # إعدادات البريد الإلكتروني
    self.TARGET_EMAIL = "loueiabboub@gmail.com"
    self.SENDER_EMAIL = "loueiabbob@gmail.com"
    self.SENDER_PASSWORD = "YOUR_APP_PASSWORD_HERE"  # ضع كلمة مرور التطبيق هنا

    self.medicines = [
        {"id": 1, "name": "باراسيتامول 500مغ", "price": 150, "stock": 50},
        {"id": 2, "name": "فيتامين سي 1000مغ", "price": 300, "stock": 30},
        {"id": 3, "name": "أوميبرازول 20مغ", "price": 450, "stock": 20},
    ]
    self.orders = []
    self.completed_notifications = {}
    self.cart = []

    self.show_login_screen()

  def show_login_screen(self):
    self.clear_screen()

    login_container = tk.Frame(self.root, bg=self.LIGHT_BG)
    login_container.pack(fill="both", expand=True)

    card = tk.Frame(
        login_container, bg=self.WHITE, bd=0, relief="flat", padx=40, pady=40
    )
    card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=450)
    card.configure(highlightbackground="#c8e6c9", highlightthickness=2)

    tk.Label(
        card,
        text="🏥 صيدليتي الرقمية",
        font=("Helvetica", 20, "bold"),
        fg=self.PRIMARY,
        bg=self.WHITE,
    ).pack(pady=(0, 20))

    tk.Label(
        card,
        text="البريد الإلكتروني:",
        font=("Helvetica", 10, "bold"),
        fg="#333",
        bg=self.WHITE,
        anchor="e",
    ).pack(fill="x", pady=2)
    self.email_entry = tk.Entry(
        card, font=("Helvetica", 11), width=30, justify="right", bd=1, relief="solid"
    )
    self.email_entry.pack(fill="x", pady=(0, 15), ipady=5)
    self.email_entry.focus()

    tk.Label(
        card,
        text="الكود السري (كلمة المرور):",
        font=("Helvetica", 10, "bold"),
        fg="#333",
        bg=self.WHITE,
        anchor="e",
    ).pack(fill="x", pady=2)
    self.pass_entry = tk.Entry(
        card,
        font=("Helvetica", 11),
        width=30,
        show="*",
        justify="right",
        bd=1,
        relief="solid",
    )
    self.pass_entry.pack(fill="x", pady=(0, 25), ipady=5)

    login_btn = tk.Button(
        card,
        text="تسجيل الدخول",
        font=("Helvetica", 11, "bold"),
        bg=self.PRIMARY,
        fg=self.WHITE,
        relief="flat",
        cursor="hand2",
        command=self.handle_login,
    )
    login_btn.pack(fill="x", ipady=8)

  def handle_login(self):
    email = self.email_entry.get().strip().lower()
    password = self.pass_entry.get().strip()

    if not email or "@" not in email:
      messagebox.showerror("خطأ", "يرجى إدخال بريد إلكتروني صحيح!")
      return

    if not password:
      messagebox.showerror("خطأ", "يرجى إدخال الكود السري!")
      return

    if email == self.admin_email:
      if password == self.admin_pass:
        self.current_user = email
        messagebox.showinfo("مرحباً", "تم تسجيل الدخول بنجاح (مدير الصيدلية)")
        self.show_admin_dashboard()
      else:
        messagebox.showerror("خطأ", "الكود السري غير صحيح للمدير!")
        return
    else:
      self.current_user = email
      messagebox.showinfo("مرحباً", f"أهلاً بك: {email}")

      if (
          self.current_user in self.completed_notifications
          and self.completed_notifications[self.current_user]
      ):
        notif_msg = self.completed_notifications[self.current_user].pop(0)
        messagebox.showinfo("تحديث الطلب", notif_msg)

      self.show_customer_dashboard()

  def show_admin_dashboard(self):
    self.clear_screen()

    top_bar = tk.Frame(self.root, bg=self.PRIMARY, height=55)
    top_bar.pack(fill="x")
    top_bar.pack_propagate(False)

    tk.Label(
        top_bar,
        text=f"لوحة تحكم المدير ({self.current_user})",
        font=("Helvetica", 12, "bold"),
        fg=self.WHITE,
        bg=self.PRIMARY,
    ).pack(side="right", padx=20)

    tk.Button(
        top_bar,
        text="تسجيل خروج",
        bg=self.DANGER,
        fg=self.WHITE,
        font=("Helvetica", 9, "bold"),
        relief="flat",
        cursor="hand2",
        command=self.show_login_screen,
    ).pack(side="left", padx=20, ipadx=10, ipady=3)

    main_frame = tk.Frame(self.root, bg="#f4f9f4", padx=15, pady=10)
    main_frame.pack(fill="both", expand=True)

    add_frame = tk.LabelFrame(
        main_frame,
        text=" إضافة دواء جديد للمخزن ",
        font=("Helvetica", 10, "bold"),
        fg=self.PRIMARY,
        bg=self.WHITE,
        padx=10,
        pady=8,
    )
    add_frame.pack(fill="x", pady=(0, 10))

    tk.Label(add_frame, text="اسم الدواء:", bg=self.WHITE).grid(
        row=0, column=5, padx=5, pady=3
    )
    self.med_name_entry = tk.Entry(
        add_frame, width=18, justify="right", relief="solid", bd=1
    )
    self.med_name_entry.grid(row=0, column=4, padx=5, pady=3, ipady=3)

    tk.Label(add_frame, text="السعر (د.ج):", bg=self.WHITE).grid(
        row=0, column=3, padx=5, pady=3
    )
    self.med_price_entry = tk.Entry(
        add_frame, width=8, justify="right", relief="solid", bd=1
    )
    self.med_price_entry.grid(row=0, column=2, padx=5, pady=3, ipady=3)

    tk.Label(add_frame, text="الكمية:", bg=self.WHITE).grid(
        row=0, column=1, padx=5, pady=3
    )
    self.med_stock_entry = tk.Entry(
        add_frame, width=8, justify="right", relief="solid", bd=1
    )
    self.med_stock_entry.grid(row=0, column=0, padx=5, pady=3, ipady=3)

    tk.Button(
        add_frame,
        text="إضافة للمخزن",
        bg=self.ACCENT,
        fg=self.WHITE,
        font=("Helvetica", 9, "bold"),
        relief="flat",
        cursor="hand2",
        command=self.add_medicine,
    ).grid(row=1, column=0, columnspan=6, pady=(8, 0), ipadx=15, ipady=3)

    med_list_frame = tk.LabelFrame(
        main_frame,
        text=" إدارة المخزون (الأدوية المتاحة) ",
        font=("Helvetica", 10, "bold"),
        fg=self.PRIMARY,
        bg=self.WHITE,
        padx=10,
        pady=8,
    )
    med_list_frame.pack(fill="both", expand=True, pady=(0, 10))

    columns_med = ("stock", "price", "name", "id")
    self.admin_tree = ttk.Treeview(
        med_list_frame, columns=columns_med, show="headings", height=4
    )
    self.admin_tree.heading("id", text="المعرف")
    self.admin_tree.heading("name", text="اسم الدواء")
    self.admin_tree.heading("price", text="السعر (د.ج)")
    self.admin_tree.heading("stock", text="المتوفر")

    self.admin_tree.column("id", width=50, anchor="center")
    self.admin_tree.column("name", width=250, anchor="center")
    self.admin_tree.column("price", width=100, anchor="center")
    self.admin_tree.column("stock", width=100, anchor="center")
    self.admin_tree.pack(fill="both", expand=True, pady=(0, 5))
    self.refresh_admin_tree()

    tk.Button(
        med_list_frame,
        text="حذف الدواء المحدد من المخزن 🗑️",
        bg=self.DANGER,
        fg=self.WHITE,
        font=("Helvetica", 9, "bold"),
        relief="flat",
        cursor="hand2",
        command=self.delete_medicine_from_stock,
    ).pack(anchor="e", pady=2)

    orders_frame = tk.LabelFrame(
        main_frame,
        text=" طلبات الزبائن الواردة ",
        font=("Helvetica", 10, "bold"),
        fg=self.PRIMARY,
        bg=self.WHITE,
        padx=10,
        pady=8,
    )
    orders_frame.pack(fill="both", expand=True, pady=(0, 5))

    columns_ord = ("total", "time", "user", "id")
    self.orders_tree = ttk.Treeview(
        orders_frame, columns=columns_ord, show="headings", height=4
    )
    self.orders_tree.heading("id", text="رقم الطلب")
    self.orders_tree.heading("user", text="بريد الزبون")
    self.orders_tree.heading("time", text="وقت الطلب")
    self.orders_tree.heading("total", text="المبلغ الإجمالي")

    self.orders_tree.column("id", width=50, anchor="center")
    self.orders_tree.column("user", width=160, anchor="center")
    self.orders_tree.column("time", width=140, anchor="center")
    self.orders_tree.column("total", width=100, anchor="center")
    self.orders_tree.pack(fill="both", expand=True, pady=(0, 5))
    self.refresh_orders_tree()

    btn_ord_frame = tk.Frame(orders_frame, bg=self.WHITE)
    btn_ord_frame.pack(fill="x", pady=2)

    tk.Button(
        btn_ord_frame,
        text="عرض تفاصيل الطلب",
        bg=self.PRIMARY,
        fg=self.WHITE,
        font=("Helvetica", 9, "bold"),
        relief="flat",
        cursor="hand2",
        command=self.show_order_details_window,
    ).pack(side="right", padx=5)

    tk.Button(
        btn_ord_frame,
        text="قبول وتجهيز الطلب",
        bg="#388e3c",
        fg=self.WHITE,
        font=("Helvetica", 9, "bold"),
        relief="flat",
        cursor="hand2",
        command=self.complete_and_delete_order,
    ).pack(side="right", padx=5)

    tk.Button(
        btn_ord_frame,
        text="رفض الطلبية",
        bg=self.DANGER,
        fg=self.WHITE,
        font=("Helvetica", 9, "bold"),
        relief="flat",
        cursor="hand2",
        command=self.reject_order,
    ).pack(side="left", padx=5)

  def add_medicine(self):
    name = self.med_name_entry.get().strip()
    price = self.med_price_entry.get().strip()
    stock = self.med_stock_entry.get().strip()

    if not name or not price or not stock:
      messagebox.showerror("خطأ", "يرجى ملء جميع الحقول!")
      return

    try:
      price = float(price)
      stock = int(stock)
    except ValueError:
      messagebox.showerror("خطأ", "السعر والكمية يجب أن تكون أرقاماً صحيحة!")
      return

    new_id = max([m["id"] for m in self.medicines], default=0) + 1
    self.medicines.append(
        {"id": new_id, "name": name, "price": price, "stock": stock}
    )
    messagebox.showinfo("نجاح", f"تمت إضافة دواء ({name}) للمخزن بنجاح!")

    self.med_name_entry.delete(0, tk.END)
    self.med_price_entry.delete(0, tk.END)
    self.med_stock_entry.delete(0, tk.END)
    self.refresh_admin_tree()

  def delete_medicine_from_stock(self):
    selected_item = self.admin_tree.selection()
    if not selected_item:
      messagebox.showerror(
          "خطأ", "يرجى تحديد الدواء المراد حذفه من المخزن أولاً!"
      )
      return

    item_values = self.admin_tree.item(selected_item)["values"]
    med_id = item_values[3]
    med_name = item_values[2]

    confirm = messagebox.askyesno(
        "تأكيد الحذف", f"هل أنت متأكد من حذف دواء ({med_name}) نهائياً؟"
    )
    if confirm:
      self.medicines = [m for m in self.medicines if m["id"] != med_id]
      self.refresh_admin_tree()
      messagebox.showinfo("تم الحذف", f"تمت إزالة ({med_name}) من المخزن بنجاح.")

  def refresh_admin_tree(self):
    if hasattr(self, "admin_tree"):
      for row in self.admin_tree.get_children():
        self.admin_tree.delete(row)
      for med in self.medicines:
        self.admin_tree.insert(
            "",
            tk.END,
            values=(med["stock"], med["price"], med["name"], med["id"]),
        )

  def refresh_orders_tree(self):
    if hasattr(self, "orders_tree"):
      for row in self.orders_tree.get_children():
        self.orders_tree.delete(row)
      for order in self.orders:
        self.orders_tree.insert(
            "",
            tk.END,
            values=(
                f"{order['total']} د.ج",
                order["time"],
                order["user"],
                order["id"],
            ),
        )

  def show_order_details_window(self):
    selected_item = self.orders_tree.selection()
    if not selected_item:
      messagebox.showerror("خطأ", "يرجى تحديد طلب من القائمة أولاً!")
      return

    item_values = self.orders_tree.item(selected_item)["values"]
    order_id = item_values[3]

    selected_order = next(
        (ord for ord in self.orders if ord["id"] == order_id), None
    )
    if not selected_order:
      return

    det_win = tk.Toplevel(self.root)
    det_win.title(f"تفاصيل الطلب رقم #{order_id}")
    det_win.geometry("460x500")
    det_win.configure(bg="#f4f9f4")

    tk.Label(
        det_win,
        text=f"📋 تفاصيل الطلب رقم #{selected_order['id']}",
        font=("Helvetica", 14, "bold"),
        fg=self.PRIMARY,
        bg="#f4f9f4",
    ).pack(pady=10)

    info_frame = tk.Frame(det_win, bg=self.WHITE, padx=15, pady=15, bd=1, relief="solid")
    info_frame.pack(fill="both", expand=True, padx=15, pady=10)

    tk.Label(
        info_frame,
        text=f"👤 بريد الزبون: {selected_order['user']}",
        font=("Helvetica", 11),
        bg=self.WHITE,
        anchor="e",
    ).pack(fill="x", pady=2)
    tk.Label(
        info_frame,
        text=f"📞 رقم الهاتف: {selected_order['phone']}",
        font=("Helvetica", 11, "bold"),
        fg="#1565c0",
        bg=self.WHITE,
        anchor="e",
    ).pack(fill="x", pady=2)
    tk.Label(
        info_frame,
        text=f"⏰ وقت الطلب: {selected_order['time']}",
        font=("Helvetica", 11),
        bg=self.WHITE,
        anchor="e",
    ).pack(fill="x", pady=2)
    tk.Label(
        info_frame,
        text=f"🏠 عنوان المنزل:\n{selected_order['address']}",
        font=("Helvetica", 11),
        bg=self.WHITE,
        justify="right",
        anchor="e",
    ).pack(fill="x", pady=5)

    tk.Label(
        info_frame,
        text="💊 الأدوية المطلوبة:",
        font=("Helvetica", 11, "bold"),
        fg=self.PRIMARY,
        bg=self.WHITE,
        anchor="e",
    ).pack(fill="x", pady=3)

    items_text = ""
    for item in selected_order["items"]:
      items_text += f"• {item['name']} - السعر: {item['price']} د.ج\n"

    tk.Label(
        info_frame,
        text=items_text,
        font=("Helvetica", 10),
        bg=self.WHITE,
        justify="right",
        anchor="e",
    ).pack(fill="x", pady=2)

    tk.Label(
        info_frame,
        text=f"💰 المبلغ الإجمالي: {selected_order['total']} د.ج",
        font=("Helvetica", 12, "bold"),
        fg=self.DANGER,
        bg=self.WHITE,
        anchor="e",
    ).pack(fill="x", pady=8)

  def complete_and_delete_order(self):
    selected_item = self.orders_tree.selection()
    if not selected_item:
      messagebox.showerror("خطأ", "يرجى تحديد الطلب المراد قبوله أولاً!")
      return

    item_values = self.orders_tree.item(selected_item)["values"]
    order_id = item_values[3]

    selected_order = next(
        (ord for ord in self.orders if ord["id"] == order_id), None
    )
    if not selected_order:
      return

    items_list_str = ""
    for item in selected_order["items"]:
      items_list_str += f"- {item['name']} (السعر: {item['price']} د.ج)\n"

    customer_email = selected_order["user"]
    notification_message = (
        f"مرحباً بك!\n\nتم قبول وتجهيز طلبك رقم #{selected_order['id']}"
        f" وجاري التوصيل.\n\nالأدوية المطلوبة:\n{items_list_str}\nالمبلغ"
        f" الإجمالي: {selected_order['total']} د.ج\nشكراً لثقتك بصيدليتنا!"
    )

    if customer_email not in self.completed_notifications:
      self.completed_notifications[customer_email] = []
    self.completed_notifications[customer_email].append(notification_message)

    self.orders = [ord for ord in self.orders if ord["id"] != order_id]
    self.refresh_orders_tree()
    messagebox.showinfo(
        "تم بنجاح", "تم قبول الطلب وإشعار الزبون بنجاح عند فتحه للتطبيق."
    )

  def reject_order(self):
    selected_item = self.orders_tree.selection()
    if not selected_item:
      messagebox.showerror("خطأ", "يرجى تحديد الطلب المراد رفضه أولاً!")
      return

    item_values = self.orders_tree.item(selected_item)["values"]
    order_id = item_values[3]

    selected_order = next(
        (ord for ord in self.orders if ord["id"] == order_id), None
    )
    if not selected_order:
      return

    customer_email = selected_order["user"]
    reject_message = (
        f"عذراً،\n\nتم رفض طلبيتك رقم #{selected_order['id']} من قبل الإدارة لعدم"
        " توفر المتطلبات حالياً."
    )

    if customer_email not in self.completed_notifications:
      self.completed_notifications[customer_email] = []
    self.completed_notifications[customer_email].append(reject_message)

    self.orders = [ord for ord in self.orders if ord["id"] != order_id]
    self.refresh_orders_tree()
    messagebox.showinfo("رفض الطلب", "تم رفض الطلب وإعلام الزبون بذلك.")

  def show_customer_dashboard(self):
    self.clear_screen()

    top_bar = tk.Frame(self.root, bg=self.PRIMARY, height=55)
    top_bar.pack(fill="x")
    top_bar.pack_propagate(False)

    tk.Label(
        top_bar,
        text=f"بوابة الزبون - الحساب: {self.current_user}",
        font=("Helvetica", 12, "bold"),
        fg=self.WHITE,
        bg=self.PRIMARY,
    ).pack(side="right", padx=20)

    tk.Button(
        top_bar,
        text="تسجيل خروج",
        bg=self.DANGER,
        fg=self.WHITE,
        font=("Helvetica", 9, "bold"),
        relief="flat",
        cursor="hand2",
        command=self.show_login_screen,
    ).pack(side="left", padx=20, ipadx=10, ipady=3)

    main_frame = tk.Frame(self.root, bg="#f4f9f4", padx=15, pady=10)
    main_frame.pack(fill="both", expand=True)

    tk.Label(
        main_frame,
        text="قائمة الأدوية المتاحة للشراء:",
        font=("Helvetica", 11, "bold"),
        fg=self.PRIMARY,
        bg="#f4f9f4",
    ).pack(anchor="e", pady=(0, 3))

    columns = ("stock", "price", "name", "id")
    self.cust_tree = ttk.Treeview(
        main_frame, columns=columns, show="headings", height=5
    )
    self.cust_tree.heading("id", text="المعرف")
    self.cust_tree.heading("name", text="اسم الدواء")
    self.cust_tree.heading("price", text="السعر (د.ج)")
    self.cust_tree.heading("stock", text="المتوفر")

    self.cust_tree.column("id", width=50, anchor="center")
    self.cust_tree.column("name", width=250, anchor="center")
    self.cust_tree.column("price", width=100, anchor="center")
    self.cust_tree.column("stock", width=100, anchor="center")
    self.cust_tree.pack(fill="x", pady=(0, 5))

    for med in self.medicines:
      self.cust_tree.insert(
          "", tk.END, values=(med["stock"], med["price"], med["name"], med["id"])
      )

    tk.Button(
        main_frame,
        text="إضافة الدواء المحدد إلى السلة 🛒",
        bg=self.ACCENT,
        fg=self.WHITE,
        font=("Helvetica", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=self.add_to_cart,
    ).pack(anchor="center", pady=5, ipadx=15, ipady=3)

    cart_frame = tk.LabelFrame(
        main_frame,
        text=" تفاصيل التوصيل وعنوان المنزل ",
        font=("Helvetica", 11, "bold"),
        fg=self.PRIMARY,
        bg=self.WHITE,
        padx=15,
        pady=10,
    )
    cart_frame.pack(fill="both", expand=True, pady=5)

    tk.Label(cart_frame, text="رقم هاتف المشتري:", bg=self.WHITE).pack(anchor="e")
    self.phone_entry = tk.Entry(
        cart_frame, font=("Helvetica", 11), width=35, justify="right", bd=1, relief="solid"
    )
    self.phone_entry.pack(fill="x", pady=2, ipady=3)

    tk.Label(cart_frame, text="عنوان المنزل بالتفصيل:", bg=self.WHITE).pack(anchor="e")
    self.address_text = tk.Text(
        cart_frame, font=("Helvetica", 11), height=2, width=40, bd=1, relief="solid"
    )
    self.address_text.pack(fill="x", pady=2)

    self.total_label = tk.Label(
        cart_frame,
        text="المبلغ الإجمالي الكلي: 0 د.ج",
        font=("Helvetica", 12, "bold"),
        fg=self.DANGER,
        bg=self.WHITE,
    )
    self.total_label.pack(pady=5)

    tk.Button(
        cart_frame,
        text="تأكيد وسداد الطلب 📦",
        bg=self.PRIMARY,
        fg=self.WHITE,
        font=("Helvetica", 11, "bold"),
        relief="flat",
        cursor="hand2",
        command=self.place_order,
    ).pack(fill="x", ipady=5)

  def add_to_cart(self):
    selected_item = self.cust_tree.selection()
    if not selected_item:
      messagebox.showerror("خطأ", "يرجى تحديد دواء من القائمة أولاً!")
      return

    item_values = self.cust_tree.item(selected_item)["values"]
    med_id = item_values[3]
    med_name = item_values[2]
    med_price = item_values[1]

    self.cart.append({"id": med_id, "name": med_name, "price": med_price})
    self.update_total_price()
    messagebox.showinfo("السلة", f"تمت إضافة ({med_name}) إلى سلتك.")

  def update_total_price(self):
    total = sum(item["price"] for item in self.cart)
    self.total_label.config(text=f"المبلغ الإجمالي الكلي: {total} د.ج")

  def place_order(self):
    phone = self.phone_entry.get().strip()
    address = self.address_text.get("1.0", tk.END).strip()

    if not self.cart:
      messagebox.showerror("خطأ", "السلة فارغة! يجدر بك إضافة أدوية أولاً.")
      return
    if not phone:
      messagebox.showerror("خطأ", "يرجى إدخال رقم الهاتف للتواصل!")
      return
    if not address:
      messagebox.showerror("خطأ", "يرجى كتابة عنوان المنزل بالتفصيل!")
      return

    total = sum(item["price"] for item in self.cart)
    order_id = max([o["id"] for o in self.orders], default=0) + 1
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    order_details = {
        "id": order_id,
        "user": self.current_user,
        "phone": phone,
        "address": address,
        "items": list(self.cart),
        "total": total,
        "time": current_time,
    }

    self.orders.append(order_details)
    self.send_email_notification(order_details)

    messagebox.showinfo(
        "تم بنجاح",
        f"تم إرسال طلبك بنجاح للبريد الإلكتروني للصيدلية.\nالمبلغ الإجمالي:"
        f" {total} د.ج",
    )

    self.cart.clear()
    self.phone_entry.delete(0, tk.END)
    self.address_text.delete("1.0", tk.END)
    self.update_total_price()

  def send_email_notification(self, order):
    try:
      items_text = ""
      for item in order["items"]:
        items_text += f"- {item['name']} (السعر: {item['price']} د.ج)\n"

      subject = f"طلب دواء جديد رقم #{order['id']} من الزبون: {order['user']}"
      body = f"""
مرحباً مدير الصيدلية،

تفاصيل الطلب الوارد الجديد:
- رقم الطلب: #{order['id']}
- بريد الزبون: {order['user']}
- رقم الهاتف: {order['phone']}
- وقت الطلب: {order['time']}
- عنوان التوصيل:
{order['address']}

- الأدوية المطلوبة:
{items_text}
- المبلغ الإجمالي الكلي: {order['total']} د.ج
"""

      msg = MIMEMultipart()
      msg["From"] = self.SENDER_EMAIL
      msg["To"] = self.TARGET_EMAIL
      msg["Subject"] = subject
      msg.attach(MIMEText(body, "plain", "utf-8"))

      server = smtplib.SMTP("smtp.gmail.com", 587)
      server.starttls()
      server.login(self.SENDER_EMAIL, self.SENDER_PASSWORD)
      server.sendmail(self.SENDER_EMAIL, self.TARGET_EMAIL, msg.as_string())
      server.quit()
    except Exception as e:
      print(f"فشل إرسال البريد الإلكتروني: {e}")

  def clear_screen(self):
    for widget in self.root.winfo_children():
      widget.destroy()


if __name__ == "__main__":
  root = tk.Tk()
  app = PharmacyApp(root)
  root.mainloop()

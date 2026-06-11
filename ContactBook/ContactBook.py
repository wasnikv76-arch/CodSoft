import tkinter as tk
from tkinter import ttk, messagebox
import os, json
 
contacts = []
 
def getContacts():
    global contacts
    with open("contacts.json", "r") as f:
        contacts = json.load(f)
 
def saveContacts():
    with open("contacts.json", "w") as f:
        json.dump(contacts, f, indent=4)
 
if os.path.exists("contacts.json"):
    getContacts()
else:
    contacts = []
 
def verifyMob(mob, exclude_id=None):
    global contacts
    if not mob.isdigit():
        return False, "Mobile number must contain digits only."
    mobileNumbers = {c["mobNo"] for c in contacts if c["id"] != (exclude_id or -1)}
    if mob in mobileNumbers:
        return False, "Mobile number already exists."
    return True, ""
 
def addContact(name, mobNo, email, address):
    global contacts
    ok, msg = verifyMob(mobNo)
    if not ok:
        return False, msg
    name    = name.strip()
    mobNo   = mobNo.strip()
    if not name or not mobNo:
        return False, "Name and Mobile No. are mandatory."
    contactId = max([c["id"] for c in contacts], default=0) + 1
    contacts.append({
        "id":      contactId,
        "name":    name,
        "mobNo":   mobNo,
        "email":   email,
        "address": address
    })
    contacts.sort(key=lambda x: x["name"])
    saveContacts()
    return True, ""
 
def updateContact(contactId, field, value):
    global contacts
    for c in contacts:
        if c["id"] == contactId:
            if field == "mobNo":
                ok, msg = verifyMob(value, exclude_id=contactId)
                if not ok:
                    return False, msg
            c[field] = value
            saveContacts()
            return True, ""
    return False, "Contact not found."
 
def deleteContact(contactId):
    global contacts
    contacts = [c for c in contacts if c["id"] != contactId]
    saveContacts()
 
def searchByName(name):
    return [c for c in contacts if name.lower() in c["name"].lower()]
 
def searchByMob(mob):
    if not mob.isdigit():
        return None, "Invalid mobile number."
    return [c for c in contacts if mob in c["mobNo"]], ""
 
def searchByEmail(mail):
    return [c for c in contacts if mail.lower() in c.get("email","").lower()]
 
BG       = "#F8F8F8"
SIDEBAR  = "#1E1E2E"
SIDE_TXT = "#CDD6F4"
SIDE_MUT = "#6C7086"
ACCENT   = "#7C5CBF"
ACCENT_D = "#5E4A8C"
ACCENT_L = "#EDE9F7"
WHITE    = "#FFFFFF"
TEXT     = "#1E1E2E"
MUTED    = "#6C7086"
BORDER   = "#E0E0E0"
DANGER   = "#E53935"
DANGER_L = "#FFEBEE"
ROW_SEL  = "#EDE9F7"
ROW_HOV  = "#F3F0FA"
 
AVATAR_PALETTE = [
    ("#EDE9F7","#5E4A8C"), ("#E8F5E9","#2E7D32"),
    ("#FFF3E0","#E65100"), ("#FCE4EC","#880E4F"),
    ("#E3F2FD","#1565C0"), ("#F3E5F5","#6A1B9A"),
]
 
def avatar_col(name):
    return AVATAR_PALETTE[sum(ord(c) for c in name) % len(AVATAR_PALETTE)]
 
def initials(name):
    parts = name.strip().split()
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) >= 2 else name[:2].upper()

class ContactDialog(tk.Toplevel):
    def __init__(self, parent, contact=None, on_save=None):
        super().__init__(parent)
        self.contact = contact
        self.on_save = on_save
        self.configure(bg=WHITE)
        self.title("Edit contact" if contact else "Add contact")
        self.geometry("360x460")
        self.resizable(False, False)
        self.grab_set()
        self._build()
        self.after(50, lambda: self._center(parent))
 
    def _center(self, p):
        self.update_idletasks()
        x = p.winfo_rootx() + p.winfo_width()  // 2 - self.winfo_width()  // 2
        y = p.winfo_rooty() + p.winfo_height() // 2 - self.winfo_height() // 2
        self.geometry(f"+{x}+{y}")
 
    def _build(self):
        hdr = tk.Frame(self, bg=ACCENT, height=56)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="✎  Edit contact" if self.contact else "＋  New contact",bg=ACCENT, fg=WHITE,
                 font=("Segoe UI", 13, "bold")).pack(side="left", padx=20)

        body = tk.Frame(self, bg=WHITE)
        body.pack(fill="both", expand=True, padx=24, pady=8)
 
        c = self.contact or {}
        self.vars = {}
        for label, key in [("Name *","name"), ("Mobile No. *","mobNo"),("Email","email"), ("Address","address")]:
            tk.Label(body, text=label, bg=WHITE, fg=MUTED,font=("Segoe UI", 9)).pack(anchor="w", pady=(10,2))
            var = tk.StringVar(value=c.get(key, ""))
            tk.Entry(body, textvariable=var, font=("Segoe UI", 11),bg="#F5F5F5", fg=TEXT, relief="flat", bd=0,highlightthickness=1,
                      highlightbackground=BORDER,highlightcolor=ACCENT, insertbackground=TEXT).pack(fill="x", ipady=7)
            self.vars[key] = var
 
        self.err_lbl = tk.Label(body, text="", bg=WHITE, fg=DANGER,font=("Segoe UI", 9), wraplength=300, anchor="w")
        self.err_lbl.pack(anchor="w", pady=(8,0))
 
        bf = tk.Frame(self, bg=WHITE)
        bf.pack(fill="x", padx=24, pady=(0,20))
        tk.Button(bf, text="Cancel", command=self.destroy,bg=WHITE, fg=MUTED, relief="flat", cursor="hand2",font=("Segoe UI", 10), padx=16, pady=7,
                  highlightthickness=1, highlightbackground=BORDER,activebackground="#F0F0F0").pack(side="right", padx=(6,0))
        tk.Button(bf, text="Save contact", command=self._submit,bg=ACCENT, fg=WHITE, relief="flat", cursor="hand2",font=("Segoe UI", 10, "bold"),
                   padx=16, pady=7,activebackground=ACCENT_D, activeforeground=WHITE).pack(side="right")
 
        self.bind("<Return>", lambda e: self._submit())
        self.bind("<Escape>", lambda e: self.destroy())
 
    def _submit(self):
        name  = self.vars["name"].get().strip()
        mob   = self.vars["mobNo"].get().strip()
        email = self.vars["email"].get().strip()
        addr  = self.vars["address"].get().strip()
 
        if self.contact:
            ok, msg = updateContact(self.contact["id"], "name",    name)
            if ok: ok, msg = updateContact(self.contact["id"], "mobNo",   mob)
            if ok: ok, msg = updateContact(self.contact["id"], "email",   email)
            if ok: ok, msg = updateContact(self.contact["id"], "address", addr)
        else:
            ok, msg = addContact(name, mob, email, addr)
 
        if not ok:
            self.err_lbl.config(text=msg)
            return
        if self.on_save:
            self.on_save()
        self.destroy()
 
class ContactBook(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Contact Book")
        self.geometry("920x580")
        self.minsize(720, 460)
        self.configure(bg=BG)
        self.selected_id = None
        self.row_map = {}
        self._build()
        self._refresh()
   
    def _build(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self._build_main()
        self._build_detail()
 
    def _build_sidebar(self):
        sb = tk.Frame(self, bg=SIDEBAR, width=190)
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)
 
        tk.Label(sb, text="CONTACT BOOK", bg=SIDEBAR, fg=SIDE_MUT,font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=18, pady=(22,14))
 
        def nav(icon, label, cmd):
            f = tk.Frame(sb, bg=SIDEBAR, cursor="hand2")
            f.pack(fill="x", padx=10, pady=1)
            lbl = tk.Label(f, text=f"{icon}  {label}", bg=SIDEBAR, fg=SIDE_TXT,font=("Segoe UI", 11), anchor="w", padx=8, pady=8,cursor="hand2")
            lbl.pack(fill="x")
            for w in (f, lbl):
                w.bind("<Button-1>", lambda e, c=cmd: c())
                w.bind("<Enter>",    lambda e, w=f: [w.config(bg="#2A2A3E")] + [c.config(bg="#2A2A3E") for c in w.winfo_children()])
                w.bind("<Leave>",    lambda e, w=f: [w.config(bg=SIDEBAR)] + [c.config(bg=SIDEBAR)   for c in w.winfo_children()])
 
        nav("◉", "All contacts", self._show_all)
        nav("＋", "Add contact",  self._open_add)
 
        tk.Frame(sb, bg="#2A2A3E", height=1).pack(fill="x", padx=16, pady=12)
        self.count_lbl = tk.Label(sb, text="", bg=SIDEBAR, fg=SIDE_MUT,font=("Segoe UI", 10))
        self.count_lbl.pack(anchor="w", padx=18)
 
    def _build_main(self):
        main = tk.Frame(self, bg=BG)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)
 
        top = tk.Frame(main, bg=WHITE, height=54)
        top.grid(row=0, column=0, sticky="ew")
        top.grid_propagate(False)
        top.grid_columnconfigure(1, weight=1)
        self.title_lbl = tk.Label(top, text="All contacts", bg=WHITE, fg=TEXT, font=("Segoe UI", 14, "bold"))
        self.title_lbl.grid(row=0, column=0, sticky="w", padx=20)
 
        sf = tk.Frame(top, bg="#F0F0F0", highlightthickness=1,highlightbackground=BORDER)
        sf.grid(row=0, column=2, padx=16, pady=12, ipadx=6, ipady=4)
        tk.Label(sf, text="⌕", bg="#F0F0F0", fg=MUTED,font=("Segoe UI", 12)).pack(side="left", padx=(6,2))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._refresh())
        tk.Entry(sf, textvariable=self.search_var, bg="#F0F0F0", fg=TEXT,relief="flat", font=("Segoe UI", 11), width=18,
                 insertbackground=TEXT).pack(side="left", padx=4)
 
        tk.Frame(main, bg=BORDER, height=1).grid(row=0, column=0, sticky="sew")
 
        cont = tk.Frame(main, bg=BG)
        cont.grid(row=1, column=0, sticky="nsew", padx=16, pady=12)
        cont.grid_rowconfigure(0, weight=1)
        cont.grid_columnconfigure(0, weight=1)
 
        self.canvas = tk.Canvas(cont, bg=BG, highlightthickness=0, bd=0)
        vsb = ttk.Scrollbar(cont, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
 
        self.list_inner = tk.Frame(self.canvas, bg=BG)
        self._cw = self.canvas.create_window((0,0), window=self.list_inner, anchor="nw")
        self.list_inner.bind("<Configure>",lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",lambda e: self.canvas.itemconfig(self._cw, width=e.width))
        self.canvas.bind("<MouseWheel>",lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
 
    def _build_detail(self):
        self.detail_frame = tk.Frame(self, bg=WHITE, width=240)
        self.detail_frame.grid(row=0, column=2, sticky="nsew")
        self.detail_frame.grid_propagate(False)
        tk.Frame(self, bg=BORDER, width=1).grid(row=0, column=2, sticky="nsw")
        self._clear_detail()
 
   
    def _all_children(self, w):
        out = [w]
        for ch in w.winfo_children():
            out.extend(self._all_children(ch))
        return out
 
    def _set_bg(self, frame, color):
        for w in self._all_children(frame):
            try: w.configure(bg=color)
            except: pass
 
    def _make_row(self, parent, contact):
        f = tk.Frame(parent, bg=WHITE, cursor="hand2")
        f.pack(fill="x", pady=2)
 
        bg_col, fg_col = avatar_col(contact["name"])
        av = tk.Canvas(f, width=40, height=40, bg=WHITE,highlightthickness=0, bd=0)
        av.pack(side="left", padx=(12,10), pady=10)
        av.create_oval(2, 2, 38, 38, fill=bg_col, outline=bg_col)
        av.create_text(20, 20, text=initials(contact["name"]),fill=fg_col, font=("Segoe UI", 12, "bold"))
 
        txt = tk.Frame(f, bg=WHITE)
        txt.pack(side="left", fill="both", expand=True, pady=10)
        tk.Label(txt, text=contact["name"], bg=WHITE, fg=TEXT, anchor="w",font=("Segoe UI", 12, "bold")).pack(anchor="w")
        sub = contact.get("mobNo","")
        if contact.get("email"):
            sub += "   ·   " + contact["email"]
        tk.Label(txt, text=sub, bg=WHITE, fg=MUTED, anchor="w",
                 font=("Segoe UI", 10)).pack(anchor="w")
 
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=12)
 
        def on_click(e, c=contact): self._select(c)
        def on_enter(e, w=f):
            if contact["id"] != self.selected_id: self._set_bg(w, ROW_HOV)
        def on_leave(e, w=f):
            if contact["id"] != self.selected_id: self._set_bg(w, WHITE)
 
        for w in self._all_children(f):
            w.bind("<Button-1>", on_click)
            w.bind("<Enter>",    on_enter)
            w.bind("<Leave>",    on_leave)
        return f
  
    def _clear_detail(self):
        for w in self.detail_frame.winfo_children(): w.destroy()
        tk.Label(self.detail_frame, text="Select a contact\nto see details",bg=WHITE, fg=MUTED, font=("Segoe UI", 11),
                  justify="center").place(relx=.5, rely=.45, anchor="center")
 
    def _show_detail(self, contact):
        for w in self.detail_frame.winfo_children(): w.destroy()
        tk.Frame(self.detail_frame, height=24, bg=WHITE).pack()
 
        bg_col, fg_col = avatar_col(contact["name"])
        av = tk.Canvas(self.detail_frame, width=60, height=60,bg=WHITE, highlightthickness=0)
        av.pack()
        av.create_oval(2, 2, 58, 58, fill=bg_col, outline=bg_col)
        av.create_text(30, 30, text=initials(contact["name"]),fill=fg_col, font=("Segoe UI", 18, "bold"))
        tk.Label(self.detail_frame, text=contact["name"], bg=WHITE, fg=TEXT,font=("Segoe UI", 13, "bold"),wraplength=200).pack(pady=(10,0))
        tk.Frame(self.detail_frame, bg=BORDER, height=1).pack(fill="x", padx=20, pady=14)
 
        def field(icon, label, value):
            if not value: return
            row = tk.Frame(self.detail_frame, bg=WHITE)
            row.pack(fill="x", padx=16, pady=4)
            tk.Label(row, text=icon, bg=WHITE, fg=MUTED,font=("Segoe UI", 14), width=3).pack(side="left")
            inner = tk.Frame(row, bg=WHITE)
            inner.pack(side="left", fill="x", expand=True)
            tk.Label(inner, text=label, bg=WHITE, fg=MUTED, anchor="w",font=("Segoe UI", 8)).pack(anchor="w")
            tk.Label(inner, text=value, bg=WHITE, fg=TEXT, anchor="w",font=("Segoe UI", 11), wraplength=170).pack(anchor="w")
 
        field("📱", "MOBILE",  contact.get("mobNo",""))
        field("✉",  "EMAIL",   contact.get("email",""))
        field("📍", "ADDRESS", contact.get("address",""))
 
        bf = tk.Frame(self.detail_frame, bg=WHITE)
        bf.pack(side="bottom", fill="x", padx=16, pady=16)
        bf.columnconfigure((0,1), weight=1)
        tk.Button(bf, text="Edit",command=lambda: self._open_edit(contact),bg=ACCENT, fg=WHITE, relief="flat", cursor="hand2",font=("Segoe UI", 10, "bold"),
                   pady=7,activebackground=ACCENT_D, activeforeground=WHITE).grid(row=0, column=0, sticky="ew", padx=(0,4))
        tk.Button(bf, text="Delete",command=lambda: self._confirm_delete(contact),bg=DANGER_L, fg=DANGER, relief="flat", cursor="hand2",font=("Segoe UI", 10),
                   pady=7,activebackground="#FFCDD2", activeforeground=DANGER).grid(row=0, column=1, sticky="ew", padx=(4,0))
 
    def _filtered(self):
        q = self.search_var.get().strip().lower()
        pool = sorted(contacts, key=lambda c: c["name"].lower())
        if not q:
            return pool
        by_name  = set(c["id"] for c in searchByName(q))
        by_mob   = set(c["id"] for c in (searchByMob(q)[0] or []))
        by_email = set(c["id"] for c in searchByEmail(q))
        ids = by_name | by_mob | by_email
        return [c for c in pool if c["id"] in ids]
 
    def _refresh(self, reselect_id=None):
        for w in self.list_inner.winfo_children(): w.destroy()
        self.row_map.clear()
 
        n = len(contacts)
        self.count_lbl.config(text=f"{n} contact{'s' if n!=1 else ''}")
 
        rows = self._filtered()
        if not rows:
            msg = ("No contacts yet.\nClick 'Add contact' to get started."
                   if not self.search_var.get() else "No matches found.")
            tk.Label(self.list_inner, text=msg, bg=BG, fg=MUTED,
                     font=("Segoe UI", 12), justify="center").pack(pady=60)
            return
 
        target = reselect_id or self.selected_id
        for c in rows:
            rf = self._make_row(self.list_inner, c)
            self.row_map[c["id"]] = rf
            if c["id"] == target:
                self._set_bg(rf, ROW_SEL)
 
        if target not in self.row_map:
            self.selected_id = None
            self._clear_detail()
 
    def _select(self, contact):
        if self.selected_id and self.selected_id in self.row_map:
            self._set_bg(self.row_map[self.selected_id], WHITE)
        self.selected_id = contact["id"]
        if self.selected_id in self.row_map:
            self._set_bg(self.row_map[self.selected_id], ROW_SEL)
        self._show_detail(contact)
 
    def _show_all(self):
        self.search_var.set("")
 
    def _open_add(self):
        ContactDialog(self, on_save=self._refresh)
 
    def _open_edit(self, contact):
        ContactDialog(self, contact=contact,on_save=lambda: self._after_edit(contact))
 
    def _after_edit(self, contact):
        updated = next((c for c in contacts if c["id"] == contact["id"]), None)
        self._refresh(reselect_id=contact["id"])
        if updated:
            self._show_detail(updated)
 
    def _confirm_delete(self, contact):
        if messagebox.askyesno("Delete contact",f"Delete {contact['name']}? This can't be undone.",parent=self):
            deleteContact(contact["id"])
            self.selected_id = None
            self._refresh()
            self._clear_detail()
 
if __name__ == "__main__":
    app = ContactBook()
    app.mainloop()
 
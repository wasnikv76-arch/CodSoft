import tkinter as tk
from tkinter import messagebox
from backend import *

root = tk.Tk()
root.title("To-Do List")
root.geometry("1050x700")
root.minsize(900,600)
root.configure(bg="#ffffff")

left = tk.Frame(root,bg="#f0eeff", width=280)
right = tk.Frame(root,bg="#ffffff")
left.pack(side="left",fill="y")
left.pack_propagate(False)
right.pack(side="right", fill="both", expand=True)

lbl_logo = tk.Label(left,text="📋",font=("Segoe UI Emoji", 56),bg="#f0eeff")
lbl_title = tk.Label(left, text="To-Do List", font=("Georgia", 20, "bold"), bg="#f0eeff", fg="#3b2d8f")
lbl_sub = tk.Label(left, text="Consistency Compounds", font=("Georgia", 9), bg="#f0eeff", fg="#7070a0")
lbl_logo.pack(pady=(30, 4))
lbl_title.pack()
lbl_sub.pack(pady=(2, 20))

sep1 = tk.Frame(left, height=1, bg="#ddd8ff")
sep1.pack(fill="x", padx=20, pady=4)

btn_all = tk.Button(left, text="📋  All Tasks",font=("Georgia", 11),bg="#ede9ff",fg="#3b2d8f",bd=0,anchor="w",cursor="hand2")
btn_all.pack(fill="x",padx=16,pady=3,ipady=8,ipadx=10)

btn_pending = tk.Button(left, text="⏰  Pending",font=("Georgia", 11),bg="#f0eeff",fg="#5b4fcf",bd=0,anchor="w",cursor="hand2")
btn_pending.pack(fill="x",padx=16,pady=3,ipady=8,ipadx=10)

btn_completed = tk.Button(left, text="✅  Completed",font=("Georgia", 11),bg="#f0eeff",fg="#5b4fcf",bd=0, anchor="w", cursor="hand2")
btn_completed.pack(fill="x",padx=16,pady=3,ipady=8,ipadx=10)

sep2 = tk.Frame(left,height=1,bg="#ddd8ff")
sep2.pack(fill="x",padx=20,pady=10)

lbl_prog_title = tk.Label(left,text="PROGRESS",font=("Georgia",9,"bold"),bg="#f0eeff",fg="#9090b0")
lbl_prog_title.pack(pady=(8, 4))
canvas_prog = tk.Canvas(left, width=130, height=130, bg="#f0eeff", highlightthickness=0)
canvas_prog.pack()

lbl_percent = tk.Label(left, text="0%",font=("Georgia", 20, "bold"), bg="#f0eeff", fg="#3b2d8f")
lbl_count = tk.Label(left, text="0 of 0 tasks completed", font=("Georgia", 9),bg="#f0eeff",fg="#7070a0")
lbl_percent.pack()
lbl_count.pack(pady=(2, 0))

btn_clear = tk.Button(left, text="🗑   Clear Completed", font=("Georgia", 11),bg="#fff0f0",fg="#e05050",bd=0, cursor="hand2")
btn_clear.pack(side="bottom", fill="x", padx=16, pady=20, ipady=10)

lbl_header = tk.Label(right, text="My Tasks", font=("Georgia", 22, "bold"),bg="#ffffff",fg="#1a1a2e")
lbl_header.pack(anchor="w", padx=28, pady=(24, 10))

search_frame = tk.Frame(right, bg="#ffffff")
search_frame.pack(fill="x", padx=24, pady=(0, 10))

lbl_search = tk.Label(search_frame, text="🔍", font=("Segoe UI Emoji", 14), bg="#ffffff")
lbl_search.pack(side="left", padx=(0, 6))

entry_search = tk.Entry(search_frame, font=("Georgia", 11), bg="#f5f3ff", fg="#1a1a2e",insertbackground="#1a1a2e", relief="flat", bd=0)
entry_search.insert(0, "Search tasks...")
entry_search.pack(side="left", fill="x", expand=True, ipady=8, ipadx=8)

def on_search_focus_in(e):
    if entry_search.get() == "Search tasks...":
        entry_search.delete(0, "end")
        entry_search.config(fg="#1a1a2e")

def on_search_focus_out(e):
    if not entry_search.get():
        entry_search.insert(0, "Search tasks...")
        entry_search.config(fg="#9090b0")

entry_search.bind("<FocusIn>", on_search_focus_in)
entry_search.bind("<FocusOut>", on_search_focus_out)

entry_row = tk.Frame(right, bg="#ffffff")
entry_row.pack(fill="x", padx=24, pady=(0, 16))

entry_task = tk.Entry(entry_row,font=("Georgia",12), bg="#f5f3ff", fg="#9090b0",insertbackground="#1a1a2e",relief="flat", bd=0)
entry_task.insert(0, "Add a new task...")
entry_task.pack(side="left", fill="x", expand=True, ipady=12, ipadx=12)

def on_focus_in(e):
    if entry_task.get() == "Add a new task...":
        entry_task.delete(0, "end")
        entry_task.config(fg="#1a1a2e")

def on_focus_out(e):
    if not entry_task.get():
        entry_task.insert(0, "Add a new task...")
        entry_task.config(fg="#9090b0")

entry_task.bind("<FocusIn>", on_focus_in)
entry_task.bind("<FocusOut>", on_focus_out)

btn_add = tk.Button(entry_row, text="Add Task  +", font=("Georgia", 11, "bold"),bg="#5b4fcf", fg="white",bd=0, cursor="hand2")
btn_add.pack(side="right", ipady=12, ipadx=16, padx=(10, 0))

list_canvas = tk.Canvas(right, bg="#ffffff", highlightthickness=0)
scrollbar = tk.Scrollbar(right, orient="vertical", command=list_canvas.yview)
list_canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
list_canvas.pack(fill="both", expand=True, padx=(24, 0))

task_frame = tk.Frame(list_canvas, bg="#ffffff")
win_id = list_canvas.create_window((0, 0), window=task_frame, anchor="nw")

def on_canvas_resize(e):
    list_canvas.itemconfig(win_id, width=e.width)
list_canvas.bind("<Configure>", on_canvas_resize)

stats_frame = tk.Frame(right, bg="#ffffff")
stats_frame.pack(fill="x", padx=24, pady=12)

lbl_total = tk.Label(stats_frame,text="Total Tasks: 0",font=("Georgia",11),bg="#ffffff",fg="#7070a0")
lbl_total.pack(side="left")

lbl_pen_stat = tk.Label(stats_frame,text="Pending: 0",font=("Georgia",11),bg="#ffffff",fg="#e17055")
lbl_pen_stat.pack(side="right", padx=(10, 0))

lbl_comp_stat = tk.Label(stats_frame,text="Completed: 0",font=("Georgia",11),bg="#ffffff",fg="#2ecc71")
lbl_comp_stat.pack(side="right", padx=(10, 0))

current_filter = None 

def updateStats():
    total, rem = progress()
    done = total - rem
    pct  = int((done/total) * 100) if total else 0

    lbl_total.config(text=f"Total Tasks: {total}")
    lbl_pen_stat.config(text=f"Pending: {rem}")
    lbl_comp_stat.config(text=f"Completed: {done}")
    lbl_percent.config(text=f"{pct}%")
    lbl_count.config(text=f"{done} of {total} tasks completed")

    canvas_prog.delete("all")
    cx, cy, r = 65, 65, 50
    canvas_prog.create_oval(cx-r,cy-r,cx+r,cy+r, outline="#ddd8ff", width=10)
    if pct > 0:
        canvas_prog.create_arc(cx-r,cy-r,cx+r,cy+r,start=90, extent=-(360 * pct / 100),outline="#5b4fcf", width=10, style="arc")

def renderTasks(filter_fn=None):
    for widget in task_frame.winfo_children():
        widget.destroy()

    tasks = filter_fn() if filter_fn else getAllTask()

    for t in tasks:
        card = tk.Frame(task_frame, bg="#f5f3ff")
        card.pack(fill="x", pady=4, padx=4)

        chk_text = "✅" if t["done"] else "⬜"
        btn_chk = tk.Button(card, text=chk_text, font=("Segoe UI Emoji", 14),bg="#f5f3ff", bd=0, cursor="hand2",command=lambda tid=t["taskId"], done=t["done"]: undoRedo(tid, done))
        btn_chk.pack(side="left",padx=(10, 6),pady=8)

        font_style = ("Georgia", 12, "overstrike") if t["done"] else ("Georgia", 12)
        fg_color = "#aaaaaa" if t["done"] else "#1a1a2e"
        lbl_task = tk.Label(card, text=t["title"], font=font_style,bg="#f5f3ff", fg=fg_color, anchor="w")
        lbl_task.pack(side="left", fill="x", expand=True, pady=8)

        btn_del = tk.Button(card, text="🗑", font=("Segoe UI Emoji", 13),bg="#f5f3ff", bd=0, cursor="hand2", fg="#e05050",command=lambda tid=t["taskId"]: handleDelete(tid))
        btn_del.pack(side="right",padx=(6, 10),pady=8)
        btn_edit = tk.Button(card, text="✏️", font=("Segoe UI Emoji", 13),bg="#f5f3ff", bd=0, cursor="hand2",command=lambda tid=t["taskId"], lbl=lbl_task, card=card: enableEdit(tid, lbl, card))
        btn_edit.pack(side="right",padx=(6, 2),pady=8)

    task_frame.update_idletasks()
    list_canvas.configure(scrollregion=list_canvas.bbox("all"))

def enableEdit(tid, lbl, card):
    old_text = lbl.cget("text")
    lbl.pack_forget()

    edit_entry = tk.Entry(card, font=("Georgia", 12), bg="#f5f3ff",fg="#1a1a2e", insertbackground="#1a1a2e",relief="flat", bd=0)
    edit_entry.insert(0, old_text)
    edit_entry.pack(side="left", fill="x",expand=True,ipady=8)
    edit_entry.focus_set()
    edit_entry.select_range(0, tk.END)

    def saveEdit(e=None):
        new_text = edit_entry.get().strip()
        if new_text and new_text != old_text:
            replaceTask(tid, new_text)
        renderTasks(current_filter)
        updateStats()

    edit_entry.bind("<Return>", saveEdit)
    edit_entry.bind("<FocusOut>", saveEdit)

def handleAddTask():
    title = entry_task.get().strip()
    if not title or title == "Add a new task...":
        return
    addTask(title)
    entry_task.delete(0, tk.END)
    entry_task.insert(0, "Add a new task...")
    lbl_header.focus_set()
    entry_task.config(fg="#9090b0")
    renderTasks(current_filter)
    updateStats()

def undoRedo(tid, currently_done):
    if currently_done:
        undoneTask(tid)
    else:
        doneTask(tid)
    renderTasks(current_filter)
    updateStats()

def handleDelete(tid):
    deleteTask(tid)
    renderTasks(current_filter)
    updateStats()

def handleClear():
    count = len(getCompTask())
    if count == 0:
        messagebox.showinfo("Empty", "No completed tasks to clear")
        return
    
    if messagebox.askyesno("Confirm", f"Delete {count} completed task(s)?"):
        for t in getCompTask():
            deleteTask(t["taskId"])
        renderTasks(current_filter)
        updateStats()

def search(e=None):
    keyword = entry_search.get().strip()
    if keyword and keyword != "Search tasks...":
        tasks = searchTask(keyword)
        renderTasks(lambda: tasks)
    else:
        renderTasks(current_filter)
entry_search.bind("<KeyRelease>",search)

def setFilter(fn, btn_active):
    global current_filter
    current_filter = fn
    for b in [btn_all, btn_pending, btn_completed]:
        b.config(bg="#f0eeff")
    btn_active.config(bg="#ede9ff")
    renderTasks(current_filter)

btn_add.config(command=handleAddTask)
entry_task.bind("<Return>", lambda e: handleAddTask())
btn_clear.config(command=handleClear)
btn_all.config(command=lambda: setFilter(None, btn_all))
btn_pending.config(command=lambda: setFilter(getPenTask, btn_pending))
btn_completed.config(command=lambda: setFilter(getCompTask, btn_completed))

renderTasks()
updateStats()

root.mainloop()

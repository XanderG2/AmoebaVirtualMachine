import tkinter as Tk
import os
import sys

#setup
acc = 0
output = ""
finshed = False
opend = False
ram = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}

def resource_path(path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, path)

def run(code, i, conter):
    global acc, ram, output
    try:
        operation_code = i[0:4]
        number = int(i[4:8], 2)
    except ValueError:
        output = f"Error {i}"
        return False
        
        

    if len(i) < 8:
        output = f"Error {i} Instruction too short"
        return False

    if operation_code == "0000":
        try:
            acc= ram[number] # LDA
        except KeyError:
            output = f"Error {i} Ram Out of Range"
            return False

    elif operation_code == "0001":
        try:
            ram[number] = acc # STA
        except KeyError:
            output = f"Error {i} Ram Out of Range"
            return False

    elif operation_code == "0010":
        acc = number # LDAN

    elif operation_code == "0011":
        try:
            acc += ram[number] # ADD
        except KeyError:
            output = f"Error {i} Ram Out of Range"
            return False
    elif operation_code == "0100":
        try:
            acc -= ram[number] # SUB
        except KeyError:
            output = f"Error {i} Ram Out of Range"
            return False
    elif operation_code == "0101":
        try:
            acc *= ram[number] # MLT
        except KeyError:
            output = f"Error {i} Ram Out of Range"
            return False
    elif operation_code == "0110":
        try:
            acc //= ram[number] # DIV
        except KeyError or ZeroDivisionError:
            output = f"Error {i} Ram Out of range or division by zero"
            return False
    elif operation_code == "0111":
        if conter + ram[number]  >= len(code):
            output = f"Error {i} Code out of range"
            return False
        else:
            conter += ram[number] -1 # JF
    elif operation_code == "1000":
        if conter - ram[number] < 0:
            output = f"Error {i} Code out of range"
            return False
        else:
            conter -= ram[number] -1 # JB
    elif operation_code == "1001":
        if acc == 0:
            if conter + ram[number] >= len(code):
                output = f"Error {i} Code out of range"
                return False
            else:
                conter += ram[number] -1 # JFE
    elif operation_code == "1010":
        if acc == 0:
            if conter - ram[number] < 0:
                output = f"Error {i} Code out of range"
                return False
            else:
                conter -= ram[number] -1 # JBE
    elif operation_code == "1011":
        output = "" # CLO
    elif operation_code == "1100":
        output += str(acc) # DAN
    elif operation_code == "1101":
        output += str(acc) # DAC
    elif operation_code == "1110":
        return False # NOP
    elif operation_code == "1111":
        return True #END
    else:
        output = f"Error {i} Invalid operation code"
        return False

    return True

def getcode():
    global root
    root.destroy()
    root = Tk.Tk()
    root.title("Amoeba Virtual Machine V2")
    root.iconbitmap(resource_path("icon.ico"))
    root.geometry("400x400")
    root.resizable(False, False)
    root.configure(bg="white")
    entry_label = Tk.Label(root, text="Enter your code here:", font=("Arial", 12), bg="white")
    entry_label.pack(pady=10)
    back_button = Tk.Button(root, text="Back", font=("Arial", 12), bg="white", command=lambda: [root.destroy(), main()])
    back_button.pack()
    code_entry = Tk.Text(root, height=10, width=40, font=("Arial", 12))
    code_entry.pack(pady=10)
    submit_button = Tk.Button(root, text="Submit", font=("Arial", 12), bg="lightblue", command=lambda: submit_code(code_entry.get("1.0", "end-1c")))
    submit_button.pack(pady=10)
    root.mainloop()

def finshedfucn(conrole_frame, finshed):
    global acc, ram, output
    if finshed:
        acc = 0
        ram = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
        output = ""
        for widget in conrole_frame.winfo_children():
            widget.destroy()
        finished_label = Tk.Label(conrole_frame, text="Finished", font=("Arial", 12), bg="#c0ffec")
        finished_label.grid(row=0, column=0, padx=10, pady=10)
        restart = Tk.Button(conrole_frame, text="Restart", font=("Arial", 12), bg="#c0ffec", command=getcode)
        restart.grid(row=1, column=0, padx=10, pady=10)

def exicute(code, conrole_frame, prossesor_frame, memory_frame, auto):
    global acc, ram, output, finshed
    finshed = False
    if auto:
        conter = 0
        while True:
            i = code[conter]

            if not run(code, i, conter):
                finshed = True
                break
            else:
                if conter + 1 >= len(code):
                    output = "Error: Code out of range"
                    finshed = True
                    break
                else:
                    conter += 1

                update_memory(memory_frame, code)
                update_processor(prossesor_frame)
    else:
        for widget in conrole_frame.winfo_children():
            widget.destroy()
        conrole_frame.counter = 0
        def on_next():
            exicute_step(code, conrole_frame, prossesor_frame, memory_frame)
        
        conrole_label = Tk.Label(conrole_frame, text="Control", font=("Arial", 16), bg="#c0ffec")
        conrole_label.grid(row=0, column=0, padx=10, pady=2)

        next_button = Tk.Button(conrole_frame, text="Next", font=("Arial", 12), bg="#c0ffec", command=on_next)
        next_button.grid(row=1, column=0, padx=10, pady=10)

    finshedfucn(conrole_frame, finshed)
    

def exicute_step(code, conrole_frame, prossesor_frame, memory_frame):
    global acc, ram, output, finshed
    conter = getattr(conrole_frame, 'counter', 0)
    if conter < len(code):
        i = code[conter]

        if not run(code, i, conter):
            finshed = True
        else:
            conter += 1
            conrole_frame.counter = conter

        update_memory(memory_frame, code)
        update_processor(prossesor_frame)
    else:
        finshed = True
    finshedfucn(conrole_frame, finshed)


def update_memory(memory_frame, code):
    global ram
    for widget in memory_frame.winfo_children():
        widget.destroy()

    memory = Tk.Label(memory_frame, text="Memory", font=("Arial", 16), bg="#ffe0c0", padx=5, pady=5)
    memory.grid(row=0, column=0, columnspan=4)

    #Program

    program_frame = Tk.Frame(memory_frame, bg="#ffe0c0", padx=10, pady=10)
    program_frame.grid(row=1, column=0)

    program = Tk.Label(program_frame, text="Program", font=("Arial", 12), bg="#ffe0c0")
    program.grid(row=0, column=0, columnspan=2)

    canvas_program = Tk.Canvas(program_frame, bg = "#ffe0c0", width=200)
    scrollbar2 = Tk.Scrollbar(program_frame, orient="vertical", command=canvas_program.yview)
    canvas_program.configure(yscrollcommand=scrollbar2.set)

    canvas_program.grid(row=1, column=0, sticky="nsew")
    scrollbar2.grid(row=1, column=1, sticky="ns")

    program_scroll = Tk.Frame(canvas_program , bg="white")
    canvas_program.create_window((0, 0), window=program_scroll, anchor="nw")

    data = [["Op. Code", "Address"]]
    for i in code:
        if len(i) >= 4:
            opcode = i[0:4]
            address = i[4:].ljust(4, '0')[:4]
            data.append([opcode, address])
        else:
            data.append([i, "Invalid"])

        for row in range(len(data)):
            for col in range(len(data[row])):
                label = Tk.Label(program_scroll, text=data[row][col], font=("Arial", 12), borderwidth=1, bg = "white", relief="solid", width= 10 , padx=10, pady=5)
                label.grid(row=row + 1, column=col)
    program_scroll.bind("<Configure>", lambda e: canvas_program.configure(scrollregion=canvas_program.bbox("all")))
    #RAM

    ram_frame = Tk.Frame(memory_frame, bg="#ffe0c0")
    ram_frame.grid(row=1, column=2)

    ram_label = Tk.Label(ram_frame, text="RAM", font=("Arial", 12), bg="#ffe0c0")  
    ram_label.grid(row= 0, column=0)

    canvas_ram = Tk.Canvas(ram_frame, bg = "#ffe0c0", width=200)
    scrollbar = Tk.Scrollbar(ram_frame, orient="vertical", command=canvas_ram.yview)
    canvas_ram.configure(yscrollcommand=scrollbar.set)

    canvas_ram.grid(row=1, column=0, sticky="nsew")
    scrollbar.grid(row=1, column=1, sticky="ns")

    ram_scroll = Tk.Frame(canvas_ram , bg="white")
    canvas_ram.create_window((0, 0), window=ram_scroll, anchor="nw")

    

    data = [["Address", "Contents"]]
    for addr in range(16):
        data.append([str(addr), str(ram[addr])])

    for row in range(len(data)):
        for col in range(len(data[row])):
            label = Tk.Label(ram_scroll, text=data[row][col], font=("Arial", 12), borderwidth=1, bg = "white", relief="solid", width=10, padx=10, pady=5)
            label.grid(row=row +1, column=col)
    
    ram_scroll.bind("<Configure>", lambda e: canvas_ram.configure(scrollregion=canvas_ram.bbox("all")))

def update_processor(prossesor_frame):
    for widget in prossesor_frame.winfo_children():
        widget.destroy()

    processor = Tk.Label(prossesor_frame, text="Processor", font=("Arial", 16), bg="#c0ffc0")#, padx=10, pady=10)
    processor.grid(row=0, column=0, columnspan=2)

    acc_label = Tk.Label(prossesor_frame, text="Accumulator: " + str(acc), font=("Arial", 12), width= 25,bg="#c0ffc0")
    acc_label.grid(row=1, column=0)

    output_frame = Tk.Frame(prossesor_frame, bg="#c0ffc0")
    output_frame.grid(row=1, column=1)

    canvas_output = Tk.Canvas(output_frame, bg = "#c0ffc0", width=200, height= 50)
    scrollbar_output = Tk.Scrollbar(output_frame, orient="vertical", bg = "#c0ffc0", command=canvas_output.xview)
    canvas_output.configure(xscrollcommand=scrollbar_output.set)

    canvas_output.grid(row=1, column=0, sticky="nsew")
    scrollbar_output.grid(row=1, column=1, sticky="ns")

    output_scroll = Tk.Frame(canvas_output , bg="#c0ffc0")
    canvas_output.create_window((0, 0), window=output_scroll, anchor="nw")


    output_label = Tk.Label(output_scroll, text="Output: \n" + str(output), font=("Arial", 12), padx= 25, width= 25, bg="#c0ffc0")
    output_label.grid(row=1, column=1)

    output_scroll.bind("<Configure>", lambda e: canvas_output.configure(scrollregion=canvas_output.bbox("all")))

def theorangecow(cheese):
    global opend
    if not opend:
        window = Tk.Toplevel(root)
        window.title("Made by: TheOrangeCow")
        window.iconbitmap(resource_path("icon.ico"))
        label = Tk.Label(window, text="TheOrangeCow", font=("Arial", 12), wraplength=280)
        label.pack(pady=20)
        opend = True
    
def submit_code(code):
    global root
    if code != "":
        code = code.replace("\\n", "\n").split("\n")
        
        root.destroy()
        root = Tk.Tk()
        root.title("Amoeba Virtual Machine V2")
        root.geometry("680x600")
        root.resizable(False, False)
        root.configure(bg="white")
        root.iconbitmap(resource_path("icon.ico"))
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        title_label = Tk.Label(root, text="Amoeba Virtual Machine V2", font=("Arial", 20), bg="#dec0ff", padx=10, pady=10, borderwidth=5, relief="solid")
        title_label.grid(row=0, column=0, columnspan=2, sticky="ew")
        title_label.bind('<Button-1>', theorangecow)

        back_button = Tk.Button(title_label, text="Back", font=("Arial", 12), bg="#dec0ff", command=getcode)
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        raw_code_frame = Tk.Frame(root, bg="white", padx=10, pady=10,height=400, width=150, borderwidth=5, relief="solid")
        raw_code_frame.grid_propagate(False)
        raw_code_frame.grid(row=1, column=0, padx=10, pady=10)
        raw_code = Tk.Label(raw_code_frame, text="Raw Code", font=("Arial", 16), bg="white")
        raw_code.grid(row=0, column=0)

        raw_code_text = Tk.Label(raw_code_frame, font=("Arial", 12), bg="white")
        raw_code_text.grid(row=1, column=0, padx=10, pady=10)
        raw_code_text.configure(text="\n".join(code))

        memory_frame = Tk.Frame(root, bg="#ffe0c0", padx=10, pady=10, borderwidth=5, relief="solid", height=400, width=500)
        memory_frame.grid(row=1, column=1)
        memory_frame.grid_propagate(False)

        update_memory(memory_frame, code)

        

        prossesor_frame = Tk.Frame(root, bg="#c0ffc0", width=500, height= 110, borderwidth=5, relief="solid", padx=10, pady=10)
        prossesor_frame.grid(row=2, column=1)
        prossesor_frame.grid_propagate(False)

        update_processor(prossesor_frame)
        
        conrole_frame = Tk.Frame(root, bg="#c0ffec", width=150, height= 110, borderwidth=5, relief="solid", padx=5, pady=10)
        conrole_frame.grid(row=2, column=0)
        conrole_frame.grid_propagate(False)

        conrole_label = Tk.Label(conrole_frame, text="Control", font=("Arial", 16), bg="#c0ffec")
        conrole_label.grid(row=0, column=0, columnspan= 2, padx=10, pady=2)

        auto = Tk.Button(conrole_frame, text="Auto", font=("Arial", 10), bg="#c0ffec", command=lambda: exicute(code,conrole_frame, prossesor_frame, memory_frame,True))
        auto.grid(row=1, column=0, padx=1, pady=1)
        step = Tk.Button(conrole_frame, text="Step-by-Step", font=("Arial", 10), bg="#c0ffec", command=lambda: exicute(code,conrole_frame, prossesor_frame, memory_frame,False))
        step.grid(row=1, column=1, padx=1, pady=1)

        root.mainloop()
        
def main():
    global root
    root = Tk.Tk()
    root.title("Amoeba Virtual Machine V2")
    root.geometry("400x300")
    root.resizable(False, False)
    root.configure(bg="white")
    root.iconbitmap(resource_path("icon.ico"))

    title_label = Tk.Label(root, text="Amoeba Virtual Machine V2", font=("Arial", 16), bg="white")
    title_label.grid(row=0, column=0)

    text_label = Tk.Label(root, text= "This is a program that emulates a simple Von Neumann \narchitecture computer. The source code is available on", font=("Arial", 12), bg="white")
    text_label.grid(row=1, column=0)

    link_label = Tk.Label(root, text= "GitHub", font=("Arial", 12,"underline"), bg="white", cursor = "hand2", fg="blue")
    link_label.grid(row=2, column=0)
    link_label.bind("<Button-1>", lambda e: os.system("start https://github.com/TheOrangeCow/AmoebaVirtualMachineV2"))

    start_button = Tk.Button(root, text="Start", font=("Arial", 12), bg="lightblue", command= getcode)
    start_button.grid(row=3, column=0)


    root.mainloop()
main()
import json
import tkinter as tk
import networkx as nx
import customtkinter as ctk
import matplotlib.pyplot as plt
from tkinter import filedialog, messagebox
from networkx.algorithms import isomorphism
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LogColors:
    SUCCESS = "#28a745"
    WARNING = "#ffc107"
    ERROR = "#dc3545"
    TEXT = "#000000"
    
class GraphDisplay:
    def __init__(self, master):
        self.master = master
    
    def display_graph(self, graph, frame, max_nodes=100, max_edges=200):
        for widget in frame.winfo_children():
            widget.destroy()
        
        num_nodes = len(graph.nodes())
        num_edges = len(graph.edges())
        
        if num_nodes > max_nodes or num_edges > max_edges:
            label = tk.Label(frame, text="The graph is too big to open.")
            label.grid(row=1, column=0, sticky="nsew")
        else:
            fig, ax = plt.subplots(figsize=(5, 5))
            pos = nx.spring_layout(graph)
            nx.draw(graph, pos, with_labels=True, labels=nx.get_node_attributes(graph, 'label'), ax=ax)
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

class GraphIsomorphismCheckerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Graph Isomorphism Checker")
        self.geometry("1280x540")
        self.resizable(False, False)

        # Store references to after callbacks
        self.after_callbacks = []
        frame_width = 500
        frame_height = 500
        log_height = 360

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        # Frames for layout
        self.frame_controls = ctk.CTkFrame(self)
        self.frame_controls.grid(row=0, column=0, padx=(10,0), pady=(10,10), sticky="nsew")
        self.frame_graphs = ctk.CTkFrame(self)
        self.frame_graphs.grid(row=0, column=1, padx=(10,10), pady=(10,10), sticky="nsew")
        
        # Frames
        self.frame_graph1 = ctk.CTkFrame(self.frame_graphs, width=frame_width, height=frame_height)
        self.frame_graph1.grid(row=0, column=0, padx=(10,5), pady=(10,10), sticky="nsew")
        self.frame_graph1.grid_rowconfigure(0, weight=1)
        self.frame_graph1.grid_columnconfigure(0, weight=1)
        self.frame_graph1.grid_propagate(False)
        self.frame_graph2 = ctk.CTkFrame(self.frame_graphs, width=frame_width, height=frame_height)
        self.frame_graph2.grid(row=0, column=1, padx=(5,10), pady=(10,10), sticky="nsew")
        self.frame_graph2.grid_rowconfigure(0, weight=1)
        self.frame_graph2.grid_columnconfigure(0, weight=1)
        self.frame_graph2.grid_propagate(False)
        
        # Widgets in frames
        self.button_load1 = ctk.CTkButton(self.frame_controls, text="Загрузить 1 схему (JSON)", command=self.load_graph1)
        self.button_load1.grid(row=0, column=0, padx=(10,10), pady=(10,10), sticky="nsew")
        self.button_load2 = ctk.CTkButton(self.frame_controls, text="Загрузить 2 схему (JSON)", command=self.load_graph2)
        self.button_load2.grid(row=1, column=0, padx=(10,10), pady=(10,10), sticky="nsew")
        self.button_check = ctk.CTkButton(self.frame_controls, text="Проверить на изоморфизм", command=self.check_isomorphism)
        self.button_check.grid(row=2, column=0, padx=(10,10), pady=(10,10), sticky="nsew")
        self.log_widget = ctk.CTkTextbox(self.frame_controls, wrap="word", state='disabled', height=log_height)
        self.log_widget.grid(row=3, column=0, padx=(10,10), pady=(10,10), sticky="nsew")
        self.log_widget.grid_propagate(False)
        
        self.label_graph1 = ctk.CTkLabel(self.frame_graph1, text="Чтобы загрузить граф схемы 1\n" + 
                                                                 "для дальнейшей проверки на изоморфизм, \n" +
                                                                 "нажмите на кнопку «Загрузить схему 1 (JSON)».")
        self.label_graph1.grid(row=0, column=0, sticky="nsew")
        self.label_graph2 = ctk.CTkLabel(self.frame_graph2, text="Чтобы загрузить граф схемы 2\n" + 
                                                                 "для дальнейшей проверки на изоморфизм, \n" +
                                                                 "нажмите на кнопку «Загрузить схему 2 (JSON)».")
        self.label_graph2.grid(row=0, column=0, sticky="nsew")

        # Configure log text tags for colors
        self.log_widget.tag_config("SUCCESS", foreground=LogColors.SUCCESS)
        self.log_widget.tag_config("ERROR", foreground=LogColors.ERROR)
        self.log_widget.tag_config("TEXT", foreground=LogColors.TEXT)
        self.log_widget.tag_config("WARNING", foreground=LogColors.WARNING)
        # Examples
        # self.log("This is a success message.", "SUCCESS") 
        # self.log("This is an error message.", "ERROR")
        # self.log("This is a normal text message.", "TEXT")
        # self.log("This is a warning message.", "WARNING"

        self.graph1 = None
        self.graph2 = None

    def load_graph1(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as f:
                data = json.load(f)
                self.graph1 = self.create_graph(data)
                GraphDisplay.display_graph(self, self.graph1, self.frame_graph1)
            self.log(f"Graph 1 loaded from {file_path}", "SUCCESS")
        else:
            self.log("Graph 1 loading cancelled", "WARNING")

    def load_graph2(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as f:
                data = json.load(f)
                self.graph2 = self.create_graph(data)
                GraphDisplay.display_graph(self, self.graph2, self.frame_graph2)
            self.log(f"Graph 2 loaded from {file_path}", "SUCCESS")
        else:
            self.log("Graph 2 loading cancelled", "WARNING")

    def create_graph(self, data):
        graph = nx.Graph()
        for node in data["nodes"]:
            graph.add_node(node["id"], label=node["label"])
        for edge in data["edges"]:
            graph.add_edge(edge["source"], edge["target"])
        return graph

    def check_isomorphism(self):
        self.log("Checking isomorphism...", "TEXT")
        if self.graph1 is None or self.graph2 is None:
            self.log("Both graphs need to be loaded first.", "ERROR")
            return
        # GM = nx.isomorphism.GraphMatcher(self.graph1, self.graph2)
        GM = isomorphism.GraphMatcher(self.graph1, self.graph2)
        if GM.is_isomorphic():
            self.log("Graphs are isomorphic!", "SUCCESS")
        else:
            self.log("Graphs are not isomorphic.", "ERROR")

    def log(self, message, tag):
        self.log_widget.configure(state='normal')
        self.log_widget.insert("end", message + "\n", tag)
        self.log_widget.see("end")
        self.log_widget.configure(state='disabled')

    def cancel_after_callbacks(self):
        for callback in self.after_callbacks:
            self.after_cancel(callback)
        self.after_callbacks.clear()

    def destroy(self):
        self.cancel_after_callbacks()   # Cancel all scheduled tasks
        self.quit()                     # Stops the mainloop
        super().destroy()               # Destroys the window and its children

if __name__ == "__main__":
    app = GraphIsomorphismCheckerApp()
    app.protocol("WM_DELETE_WINDOW", app.destroy)
    app.mainloop()

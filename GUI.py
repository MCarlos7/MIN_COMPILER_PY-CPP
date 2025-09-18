import tkinter as tk
from Analisis_Lexico import SEPARADOR, imprimir_tokens, Automata
from Analisis_Sintactico import construir_arbol, imprimir_arbol
from tkinter import scrolledtext, PanedWindow, filedialog, messagebox
import sys
import io

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("IDLE CAHAFA")
        self.geometry("900x700")

        self.BG_COLOR = "#1E1E1E"  # Gris oscuro para el fondo
        self.FG_COLOR = "#D4D4D4"  # Gris claro para el texto

        # --- Creación de los componentes de la GUI ---
        self.create_menubar()
        self.create_widgets()
        self.create_key_bindings()

    def create_menubar(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # --- Menú Archivo ---
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="📂 Abrir", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="💾 Guardar", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="🧹 Limpiar pantalla", command=self.clear_screen, accelerator="Ctrl+L")
        file_menu.add_separator()
        file_menu.add_command(label="❌ Cerrar", command=self.close_app, accelerator="Ctrl+Q")

        # --- Menú Editar ---
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Editar", menu=edit_menu)
        edit_menu.add_command(label="↪️ Deshacer", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="↩️ Rehacer", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="✂️ Cortar", command=self.cut_text, accelerator="Ctrl+X")
        edit_menu.add_command(label="📋 Copiar", command=self.copy_text, accelerator="Ctrl+C")
        edit_menu.add_command(label="📝 Pegar", command=self.paste_text, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Seleccionar todo", command=self.select_all, accelerator="Ctrl+A")

        # --- Menú Ejecutar ---
        run_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ejecutar", menu=run_menu)
        run_menu.add_command(label="▶️ Ejecutar Código", command=self.run_code, accelerator="F5")
        run_menu.add_command(label=" depurar", command=self.placeholder_command)

        # --- Menú Compiladores ---
        self.selected_compiler = tk.StringVar(value="Python")
        
        compiler_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Compiladores", menu=compiler_menu)
        compiler_menu.add_radiobutton(label="Python", variable=self.selected_compiler, value="Python", command=self.compiler_selected)
        compiler_menu.add_radiobutton(label="C++", variable=self.selected_compiler, value="C++", command=self.compiler_selected)
        compiler_menu.add_separator()
        compiler_menu.add_command(label="🔬 Análisis Léxico", command=self.Analisis_Lexico)
        compiler_menu.add_command(label="🔍 Análisis Sintáctico", command=self.Analisis_Sintactico)
        compiler_menu.add_command(label="📊 Análisis Semántico", command=self.placeholder_command)

        # --- Menú Ayuda ---
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)

        # Submenú de "Librerias"
        libraries_menu = tk.Menu(help_menu, tearoff=0)
        help_menu.add_cascade(label="Librerías", menu=libraries_menu)
        
        libraries_menu.add_command(label="stdio.h", compound='left', command=self.placeholder_command)
        libraries_menu.add_command(label="conio.h", compound='left', command=self.placeholder_command)
        libraries_menu.add_command(label="math.h", compound='left', command=self.placeholder_command)
        libraries_menu.add_command(label="string.h", compound='left', command=self.placeholder_command)
        libraries_menu.add_command(label="stdlib.h", compound='left', command=self.placeholder_command)
        libraries_menu.add_command(label="ctype.h", compound='left', command=self.placeholder_command)

        help_menu.add_separator()
        help_menu.add_command(label="ℹ️ Acerca de", command=self.show_about)

        # --- Menú Variables ---
        variables_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Variables", menu=variables_menu)

        # Submenú de "Tipos"
        types_menu = tk.Menu(variables_menu, tearoff=0)
        variables_menu.add_cascade(label="Tipos", menu=types_menu)

        types_menu.add_command(label="int", compound='left', command=self.placeholder_command)
        types_menu.add_command(label="float", compound='left', command=self.placeholder_command)
        types_menu.add_command(label="str", compound='left', command=self.placeholder_command)
        types_menu.add_command(label="bool", compound='left', command=self.placeholder_command)
        types_menu.add_command(label="list", compound='left', command=self.placeholder_command)


    def create_widgets(self):
        """Crea las áreas de texto y el panel divisor."""
        paned_window = PanedWindow(self, orient=tk.VERTICAL, sashrelief=tk.RAISED, bg=self.BG_COLOR)
        paned_window.pack(fill=tk.BOTH, expand=True)

        # --- Editor de Código (panel superior) ---
        self.editor = scrolledtext.ScrolledText(
            paned_window,
            wrap=tk.WORD,
            font=("Consolas", 12),
            bg=self.BG_COLOR,
            fg=self.FG_COLOR,
            insertbackground="white", # Color del cursor
            undo=True # Habilitar la función de deshacer/rehacer
        )
        paned_window.add(self.editor, height=500)

        # --- Consola de Salida (panel inferior) ---
        self.console = scrolledtext.ScrolledText(
            paned_window,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg="#101010",
            fg="#FFFFFF",
            state="disabled"
        )
        paned_window.add(self.console)

    def create_key_bindings(self):
        """Asocia los atajos de teclado a las funciones."""
        self.bind("<Control-o>", self.open_file)
        self.bind("<Control-s>", self.save_file)
        self.bind("<Control-l>", self.clear_screen)
        self.bind("<Control-q>", self.close_app)
        self.bind("<F5>", self.run_code)
        #self.bind("<Control-a>", self.select_all)
        #self.bind("<Control-x>", self.cut_text)
        #self.bind("<Control-c>", self.copy_text)
        #self.bind("<Control-v>", self.paste_text)
        self.bind("<Control-z>", self.undo)
        self.bind("<Control-y>", self.redo)

    # --- Funciones de Archivo ---
    def open_file(self, event=None):
        filepath = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if not filepath:
            return
        self.editor.delete("1.0", tk.END)
        with open(filepath, "r", encoding="utf-8") as f:
            self.editor.insert("1.0", f.read())
        self.title(f"PYTHON IDE - {filepath}")

    def save_file(self, event=None):
        filepath = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if not filepath:
            return
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.editor.get("1.0", tk.END))
        self.title(f"PYTHON IDE - {filepath}")

    def clear_screen(self, event=None):
        self.editor.delete("1.0", tk.END)
        self.write_to_console("") # Limpia la consola

    def close_app(self, event=None):
        self.destroy()

    # --- Funciones de Edición ---
    def cut_text(self, event=None):
        self.editor.event_generate("<<Cut>>")
        return "break"
    
    def copy_text(self, event=None):
        self.editor.event_generate("<<Copy>>")
        return "break"

    def paste_text(self, event=None):
        self.editor.event_generate("<<Paste>>")
        return "break"

    def select_all(self, event=None):
        self.editor.tag_add("sel", "1.0", "end")
        return "break" # Evita que se propague el evento

    def undo(self, event=None):
        self.editor.edit_undo()
        return "break"

    def redo(self, event=None):
        self.editor.edit_redo()
        return "break"

    # --- Funciones de Ejecución ---
    def run_code(self, event=None):
        code = self.editor.get("1.0", tk.END)
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        try:
            exec(code)
            self.write_to_console(redirected_output.getvalue())
        except Exception as e:
            self.write_to_console(str(e))
        finally:
            sys.stdout = old_stdout

    def write_to_console(self, text):
        self.console.config(state="normal")
        self.console.delete("1.0", tk.END)
        self.console.insert("1.0", text)
        self.console.config(state="disabled")
    
    # --- MÉTODO DE ANÁLISIS LÉXICO ---
    def Analisis_Lexico(self, event=None):
        source_code = self.editor.get("1.0", tk.END)
        if not source_code.strip():
            self.write_to_console("No hay código para analizar.")
            return

        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()

        output = "--- ANÁLISIS LÉXICO ---\n"
        try:
            # 1. Obtiene los tokens usando la función importada.
            tokens = SEPARADOR(source_code)
            # 2. Imprime los tokens (la salida se captura).
            automata = Automata()
            imprimir_tokens(tokens, automata)
            output += redirected_output.getvalue()
        except Exception as e:
            output += f"Error durante el análisis: {e}"
        finally:
            sys.stdout = old_stdout 

        self.write_to_console(output)

    # --- MÉTODO DE ANÁLISIS SINTÁCTICO ---
    def Analisis_Sintactico(self, event=None):
        source_code = self.editor.get("1.0", tk.END)
        if not source_code.strip():
            self.write_to_console("No hay código para analizar.")
            return

        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()

        output = "--- ANÁLISIS SINTÁCTICO (ÁRBOL DE PARSEO) ---\n"
        try:
            # 1. El análisis sintáctico siempre necesita primero el léxico.
            tokens = SEPARADOR(source_code)
            # 2. Construye el árbol a partir de los tokens.
            arbol = construir_arbol(tokens)

            if arbol:
                # 3. Imprime el árbol si se construyó correctamente.
                imprimir_arbol(arbol)
                output += redirected_output.getvalue()
            else:
                output += "No se pudo construir el árbol. Verifique la expresión."
        except Exception as e:
            output += f"Error durante el análisis sintáctico: {e}"
        finally:
            sys.stdout = old_stdout

        self.write_to_console(output)


    # --- Funciones de Menús ---
    def compiler_selected(self):
        """Función que se llama al seleccionar un compilador. )"""
        messagebox.showinfo("Compilador", f"Has seleccionado: {self.selected_compiler.get()}")

    def show_about(self):
        messagebox.showinfo("Acerca de", "PYTHON IDE\n\nCreado con Tkinter en Python.")

    def placeholder_command(self, event=None):
        messagebox.showwarning("No implementado", "Esta función aún no está disponible.")

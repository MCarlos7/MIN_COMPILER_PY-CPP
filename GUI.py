import tkinter as tk
from Analisis_Lexico import SEPARADOR, imprimir_tokens, Automata
from Analisis_Sintactico import Sintactico
from Analisis_Semantico import AnalizadorSemantico
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
        self.LINE_NUM_BG = "#2A2A2A" # Fondo para los números de línea

        # --- Creación de los componentes de la GUI ---
        self.create_menubar()
        self.create_widgets()
        self.create_key_bindings()
        self._update_line_numbers() # Dibuja los números de línea iniciales

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
        compiler_menu.add_command(label="📊 Análisis Semántico", command=self.Analisis_Semantico)

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
        """Crea las áreas de texto, el panel divisor y el contador de líneas."""
        paned_window = PanedWindow(self, orient=tk.VERTICAL, sashrelief=tk.RAISED, bg=self.BG_COLOR)
        paned_window.pack(fill=tk.BOTH, expand=True)

        # --- Editor de Código y Contador de Líneas (panel superior) ---
        # Usamos un Frame para agrupar el contador y el editor
        editor_frame = tk.Frame(paned_window, bg=self.BG_COLOR)
        
        # Widget para los números de línea
        self.line_numbers = tk.Text(
            editor_frame,
            width=4,
            padx=4,
            font=("Consolas", 12),
            bg=self.LINE_NUM_BG,
            fg=self.FG_COLOR,
            state="disabled", # Para que el usuario no pueda escribir en él
            bd=0, # Sin borde
            highlightthickness=0 # Sin borde de resaltado
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Widget para el editor de código (usamos tk.Text en lugar de scrolledtext)
        self.editor = tk.Text(
            editor_frame,
            wrap=tk.WORD,
            font=("Consolas", 12),
            bg=self.BG_COLOR,
            fg=self.FG_COLOR,
            insertbackground="white",
            undo=True,
            bd=0,
            highlightthickness=0
        )
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar que controlará AMBOS widgets (editor y números de línea)
        scrollbar = tk.Scrollbar(editor_frame, command=self._on_scroll)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Vincular la scrollbar al editor
        self.editor.config(yscrollcommand=scrollbar.set)
        
        paned_window.add(editor_frame, height=500)

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

    def _on_scroll(self, *args):
        """Sincroniza el desplazamiento vertical del editor y el contador de líneas."""
        self.editor.yview(*args)
        self.line_numbers.yview(*args)
    
    def _update_line_numbers(self, event=None):
            """Actualiza los números en el widget de contador de líneas."""
            # Un pequeño retraso para asegurar que el widget del editor se actualice primero
            self.after(1, self._update_line_numbers_logic)

    def _update_line_numbers_logic(self):
        """Lógica real para actualizar los números de línea."""
        line_count = self.editor.index(tk.END).split('.')[0]
        
        # Creamos el texto de los números de línea (1\n2\n3\n...)
        # El rango ahora va hasta line_count para incluir la última línea si está vacía
        line_numbers_text = "\n".join(str(i) for i in range(1, int(line_count)))
        
        # Habilitamos, actualizamos y deshabilitamos el widget
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", tk.END)
        self.line_numbers.insert("1.0", line_numbers_text)
        self.line_numbers.config(state="disabled")

        # Aseguramos que la vista esté sincronizada
        self.line_numbers.yview_moveto(self.editor.yview()[0])

    def create_key_bindings(self):
        """Asocia los atajos de teclado a las funciones."""
        self.bind("<Control-o>", self.open_file)
        self.bind("<Control-s>", self.save_file)
        self.bind("<Control-l>", self.clear_screen)
        self.bind("<Control-q>", self.close_app)
        self.bind("<F5>", self.run_code)
        
        # Cada vez que se suelta una tecla o se hace clic, se actualiza el contador
        self.editor.bind("<KeyRelease>", self._update_line_numbers)
        self.editor.bind("<Button-1>", self._update_line_numbers)
        
        # Eventos para deshacer y rehacer también deben actualizar el contador
        self.editor.bind("<<Undo>>", self._update_line_numbers)
        self.editor.bind("<<Redo>>", self._update_line_numbers)
        self.editor.bind("<<Paste>>", self._update_line_numbers)

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
        self._update_line_numbers() # Actualiza los números al abrir archivo

    def save_file(self, event=None):
        filepath = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if not filepath:
            return
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.editor.get("1.0", tk.END))
        self.title(f"PYTHON IDE - {filepath}")

    def clear_screen(self, event=None):
        self.editor.delete("1.0", tk.END)
        self.write_to_console("") 
        self._update_line_numbers() # Actualiza los números al limpiar

    def close_app(self, event=None):
        self.destroy()

    # --- Funciones de Edición ---
    def cut_text(self, event=None):
        self.editor.event_generate("<<Cut>>")
        self._update_line_numbers()
        return "break"
    
    def copy_text(self, event=None):
        self.editor.event_generate("<<Copy>>")
        return "break"

    def paste_text(self, event=None):
        self.editor.event_generate("<<Paste>>")
        self._update_line_numbers()
        return "break"

    def select_all(self, event=None):
        self.editor.tag_add("sel", "1.0", "end")
        return "break"

    def undo(self, event=None):
        self.editor.event_generate("<<Undo>>")
        return "break"

    def redo(self, event=None):
        self.editor.event_generate("<<Redo>>")
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
            tokens = SEPARADOR(source_code)
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
            """
            Toma el código del editor, lo analiza con el nuevo compilador
            y muestra la salida en la consola de la GUI.
            """
            source_code = self.editor.get("1.0", tk.END)
            if not source_code.strip():
                self.write_to_console("No hay código para analizar.")
                return

            # 1. Preparar la redirección para capturar los 'print' del compilador
            old_stdout = sys.stdout
            redirected_output = io.StringIO()
            sys.stdout = redirected_output

            try:
                # 2. Llamar a la clase principal del compilador
                # La traza en True genera el resultado detallado que quieres
                Sintactico(fuente=source_code, traza=True)

            except Exception as e:
                # El error ya fue impreso en 'redirected_output' por el método 'errores'.
                # La excepción detiene el análisis y nos permite continuar aquí.
                # No es necesario hacer nada más con la excepción 'e'.
                pass

            finally:
                # 3. Restaurar la salida estándar original
                sys.stdout = old_stdout

            # 4. Obtener todo lo que se imprimió y mostrarlo en la consola
            output_final = redirected_output.getvalue()
            self.write_to_console(output_final)
        
    # --- MÉTODO DE ANÁLISIS SEMÁNTICO ---
    def Analisis_Semantico(self, event=None):
        source_code = self.editor.get("1.0", tk.END)
        if not source_code.strip():
            self.write_to_console("No hay código para analizar.")
            return

        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()

        output = ""
        try:
            tokens = SEPARADOR(source_code)
            automata = Automata()
            analizador = AnalizadorSemantico(tokens)
            output = analizador.analizar(automata)
        except Exception as e:
            output += f"Error durante el análisis semántico: {e}"
        finally:
            sys.stdout = old_stdout

        self.write_to_console(output)

    # --- Funciones de Menús ---
    def compiler_selected(self):
        messagebox.showinfo("Compilador", f"Has seleccionado: {self.selected_compiler.get()}")

    def show_about(self):
        messagebox.showinfo("Acerca de", "PYTHON IDE\n\nCreado con Tkinter en Python.")

    def placeholder_command(self, event=None):
        messagebox.showwarning("No implementado", "Esta función aún no está disponible.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
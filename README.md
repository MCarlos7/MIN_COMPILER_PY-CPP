# 🖥️ MIN_COMPILER_PY-CPP

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

A **didactic compiler for a C++ subset** built in **Python**. This project features a graphical Integrated Development Environment (IDE) named **IDLE CAHAFA**, which allows you to write code, manage files, and visualize the different stages of the compilation process: lexical, syntactic, and semantic analysis, as well as intermediate code generation.

## 🚀 Key Features

### 🛠️ Graphical IDE (IDLE CAHAFA)
- **Code Editor:** Text area with automatic line numbering and scrollbars.
- **File Management:** Open, save, and edit files (`.txt`, `.cpp`).
- **Integrated Console:** View analysis output, compilation errors, and debug traces.
- **Editing Tools:** Undo, redo, cut, copy, and paste functionalities.
- **Analysis Menus:** Run individual phases (Lexical, Syntactic, Semantic) or the full process.

### 🧠 Compiler Phases
The core analyzes code with C++ style syntax, now supporting **Object-Oriented Programming (OOP)** features:

1.  **🔬 Lexical Analysis:**
    - **Tokens:** Keywords (`int`, `float`, `class`, `public`, `if`, etc.), operators, and identifiers.
    - **Literals:** Integers, Strings (`"text"`), and Characters (`'c'`).
    - **Comments:** Support for single-line (`//`) and multi-line (`/* ... */`) comments.

2.  **🔍 Syntactic Analysis:**
    - **Recursive Descent Parser:** Handles complex hierarchies.
    - **OOP Support:** Definition of `class`, `public`/`private` access modifiers, and object instantiation.
    - **Structures:**
        - **Functions:** Definitions with parameters and return types (`void`, `int`, etc.).
        - **Arrays:** Declaration and index access (e.g., `arr[i]`).
        - **Control Flow:** `if-else`, `switch-case`, `while`, `do-while`, `for`.

3.  **📊 Semantic Analysis:**
    - **Symbol Table:** Advanced management of **Scopes** (Global, Local, Class-level).
    - **Type Checking:** strict validation for assignments and operations.
    - **Member Validation:** Checks for attribute existence and method calls within objects (e.g., `obj.method()`).
    - **Function Signatures:** Verification of argument count and types.

4.  **⚙️ Intermediate Code Generation:**
    - Translation to a **Stack-Based Three-Address Code**.
    - Instructions for arithmetic (`ADD`, `MUL`), logic (`EQ`, `GT`), control flow (`JMP`, `JMPF`), and memory (`STORE`, `LOAD`, `PUSHA`).
    - specific instructions for array indexing (`IDX_ADDR`) and function calls (`CALL`, `RET`).

## 📝 Supported Syntax (Examples)

### 1. Classes and Objects
The compiler now supports defining classes and accessing members.

```cpp
class Room {
   public:
    int length;
    int breadth;
    int height;

    int calculate_area() {
        return length * breadth;
    }

    int calculate_volume() {
        return length * breadth * height;
    }
};

int main() {
    Room room1;
    
    // Member access
    room1.length = 42;
    room1.breadth = 30;
    room1.height = 19;

    cout << "Area = " << room1.calculate_area();
    return 0;
}
```

### 2. Algorithms (Bubble Sort)
Complex logic with nested loops and arrays.

```cpp
int main() {
    int n;
    cin >> n;
    int arr[n]; // Array declaration

    for (int i = 0; i < n; ++i) {
        cin >> arr[i];
    }
    
    // Bubble Sort
    for (int i = 0; i < n - 1; ++i) {
        for (int j = 0; j < n - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) {   
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
    return 0;
}
```
## 📂 Project Structure

The project is organized into modular folders to separate the interface, compiler logic, and test files.

### 📁 Root Directory
| File | Description |
| :--- | :--- |
| `MAIN.py` | Main entry point of the application. |
| `GUI.py` | The **IDLE CAHAFA** graphical interface code. |
| `README.md` | Project documentation. |

### 📁 ANALISIS/
Contains the core logic for the compilation phases.
| File | Description |
| :--- | :--- |
| `Analisis_Lexico.py` | Token generation, finite automata, and comment filtering. |
| `Analisis_Sintactico.py` | Main parser logic, grammar rules (including classes and functions). |
| `Analisis_Semantico.py` | Symbol table logic, scope management, and type validation. |
| `GeneraCodigo.py` | Generates the Stack-Based Intermediate Code (Pseudo-assembly). |

### 📁 TEST/
Example source code files for testing the compiler's features.
| File | Description |
| :--- | :--- |
| `BUBLE.txt` | Implementation of the Bubble Sort algorithm with arrays. |
| `CLASS.txt` | OOP example with class definition, attributes, and methods. |
| `FUNCIONES.txt` | Example demonstrating function declaration, parameters, and calls. |

## 🛠️ Installation and Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/mcarlos7/MIN_COMPILER_PY-CPP.git](https://github.com/mcarlos7/MIN_COMPILER_PY-CPP.git)
    ```
2.  **Navigate to the directory:**
    ```bash
    cd MIN_COMPILER_PY-CPP
    ```
3.  **Run the application:**
    Requires Python 3.x (Tkinter is usually included).
    ```bash
    python MAIN.py
    ```

## ✅ To-Do

- [ ] Implement panic mode error recovery (Error resync).
- [ ] Add syntax highlighting to the editor text area.
- [ ] Develop a Virtual Machine (VM) to execute the generated intermediate code.
- [ ] Optimize intermediate code (dead code elimination).

## 🤝 Contributing

Contributions are welcome! If you find a bug or have an idea for a new feature, feel free to open an [issue](https://github.com/mcarlos7/MIN_COMPILER_PY-CPP/issues) or submit a pull request.

---
Made with 💻 and ☕ by [MCarlos7](https://github.com/MCarlos7).
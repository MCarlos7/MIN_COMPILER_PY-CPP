# 🖥️ MIN_COMPILER_PY-CPP

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Educational-orange?style=for-the-badge)

A **didactic compiler for a C++ subset** built in **Python**. This project features a graphical Integrated Development Environment (IDE) that allows you to write code, manage files, and visualize the different stages of the compilation process: lexical, syntactic, and semantic analysis, as well as intermediate code generation.

## 🚀 Key Features

### 🛠️ Graphical IDE (GUI)
- **Code Editor:** Text area with line numbering and scrollbars.
- **File Management:** Easily open, save, and edit files (`.txt`, `.cpp`, etc.).
- **Integrated Console:** View analysis output and errors directly within the application.
- **Editing Tools:** Undo, redo, cut, copy, and paste functionalities.

### 🧠 Compiler Phases
The core analyzes code with C++ style syntax:

1.  **🔬 Lexical Analysis:**
    - Complete source code tokenization.
    - Identification of keywords (`int`, `if`, `while`, `class`, etc.), operators, and literals.
    - Lexical error detection (invalid characters).

2.  **🔍 Syntactic Analysis:**
    - Recursive descent parser.
    - Validation of complex grammatical structures:
        - Functions and function calls.
        - Loops: `for`, `while`, `do-while`.
        - Flow control: `if`, `else`, `switch`, `case`.
        - Array and variable declarations.

3.  **📊 Semantic Analysis:**
    - **Symbol Table:** Management of global and local scopes.
    - **Type Checking:** Compatibility checks for assignments and operations (e.g., preventing addition of `int` with `void`).
    - **Function Validation:** Verification of argument count and types in function calls.

4.  **⚙️ Intermediate Code Generation:**
    - Translation of source code into three-address code instructions (pseudo-assembly).
    - Generation of labels for jumps (`JUMP`, `LABEL`) and stack operations (`PUSH`, `STORE`, `LOAD`).

## 📝 Supported Syntax (Example)

The compiler is capable of processing complex algorithms such as sorting or mathematical functions.

```cpp
int main() {
    int n;
    cin >> n;
    int arr[n];

    // Data input
    for (int i = 0; i < n; ++i) {
        cin >> arr[i];
    }
    
    // Bubble Sort Algorithm
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

| File | Description |
| :--- | :--- |
| `MAIN.py` | Main entry point of the application. |
| `GUI.py` | Graphical user interface built with Tkinter. |
| `Analisis_Lexico.py` | Logic for token generation and finite automaton. |
| `Analisis_Sintactico.py` | Grammar rules and the main parser. |
| `Analisis_Semantico.py` | Symbol tables and logic validations. |
| `GeneraCodigo.py` | Intermediate code generator (stack instructions). |

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
    Requires Python 3.x installed.
    ```bash
    python MAIN.py
    ```

## ✅ To-Do

- [ ] Implement panic mode error recovery.
- [ ] Add syntax highlighting to the editor.
- [ ] Generate real assembly code or executables.
- [ ] Support for classes and objects.

## 🤝 Contributing

Contributions are welcome! If you find a bug or have an idea for a new feature, feel free to open an [issue](https://github.com/mcarlos7/MIN_COMPILER_PY-CPP/issues) or submit a pull request.

---
Made with 💻 and ☕ by [MCarlos7](https://github.com/MCarlos7).
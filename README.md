# PhysiXC
Interactive TUI application that helps solve physics equations easily

<img width="1498" height="752" alt="image" src="https://github.com/user-attachments/assets/77dd80f0-e3a3-411a-98c6-694f0d04ded1" />
<hr>


## Usage
1. Install dependencies
```
pip install textual textual-dev
```
2. Compile .c files into `.dll` for Windows or `.so` for Linux/Mac (Using GCC)

Windows:
```
gcc -shared -o kinematics.dll kinematics.c
```

Linux/Mac:
```
gcc -shared -fPIC -o kinematics.so kinematics.c -lm
```

3. Run the application
```
python main.py
```

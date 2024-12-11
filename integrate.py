import time
from interpreter import Interpreter
from compiler import Compiler

class Integrate:
    def __init__(self):
        pass

    # プログラムを読み取る
    def read_file(self, path):
        try:
            with open(path, 'r') as file:
                code = file.read()
        except FileNotFoundError as e:
            print(f'File has not been found')
            return e
        return code

    # コンパイル
    def compile(self, code):
        compiler = Compiler(code, False)
        return compiler.compile()

    def execute(self, bytecodes, enable_inline_caching=False, debug_mode=False):
        interpreter = Interpreter(bytecodes, enable_inline_caching, debug_mode)
        interpreter.interpret()

    def measure_execution_time(self, bytecodes, enable_inline_caching=False, debug_mode=False):
        interpreter = Interpreter(bytecodes, enable_inline_caching, debug_mode)
        s = time.perf_counter()
        interpreter.interpret()
        e = time.perf_counter()
        return e - s

    def run_fullpath(self, path, enable_inline_caching=False, debug_mode=False):
        print(f"Evaluating file: {path}")
        code = self.read_file(path)
        print(f"--------")
        print(f"[Program]:\n{code}")
    
        bytecodes = self.compile(code)
        print(f"--------")
        print(f"[ByteCode]:\n{bytecodes}")

        print(f"--------")
        print(f"[Execution]:")
        self.execute(bytecodes, enable_inline_caching, debug_mode)

        print(f"--------")
        print("Execution Finished!!")

    def measure_execution_time_full_path(self, path, iteration, enable_inline_caching=False):
        code = self.read_file(path)
        bytecodes = self.compile(code)
        total_execution_time = 0
        for i in range(iteration):
            execution_time = self.measure_execution_time(bytecodes, enable_inline_caching, False)
            total_execution_time += execution_time
        avg_exectuion_time = total_execution_time / iteration
        return avg_exectuion_time
    
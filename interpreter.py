class Stack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        try:
            return self.stack.pop(-1)
        except IndexError as e:
            print(e)
    
    def __repr__(self):
        return str(self.stack)

class Register:
    def __init__(self):
        # 0,1 -> メソッドを検索するために使用
        # 　0 -> レシーバーのクラス
        # 　1 -> メソッド名
        # 
        # 9,10 -> 自由
        self.register = [0 for i in range(16)]

    def save(self, index, value):
        if 0 <= index <= 15:
            self.register[index] = value
            return 
        else:
            print("An invalid index was specified for the register.")
            print("required integer from 0 to 15")
            print(f"but given {index}")
            return
    
    def load(self, index):
        if 0 <= index <= 15:
            return self.register[index]
        else:
            print("An invalid index was specified for the register.")
            print("required integer from 0 to 15")
            print(f"but given {index}")
            return

class ClassTable:
    def __init__(self):
        self.table = dict()

    def set_method(self, m_name, pointer):
        self.table[m_name] = pointer
    
    def search_method(self, m_name):
        return self.table[m_name]

class ClassTables:
    def __init__(self):
        self.tables = dict()
    
    def def_cls(self, c_name):
        self.tables[c_name] = ClassTable()
    
    def set_method(self, c_name, m_name, pointer):
        self.tables[c_name].set_method(m_name, pointer)
    
    def search_method(self, c_name, m_name):
        return self.tables[c_name].search_method(m_name)

class Interpreter:
    def __init__(self, codes, debug_mode=False):
        self.stack = Stack()
        self.register = Register()
        self.codes = codes
        self.class_table = ClassTables()
        self.pc = 0
        self.ret_point = Stack()
        self.debug_mode = debug_mode

    def interpret(self):
        halt_called = False
        while (not halt_called) and (0 <= self.pc < len(self.codes)):
            code = self.codes[self.pc]
            self.pc += 1
            match code[0]:
                case 'PUSH': self.stack.push(code[1])
                case 'POP': self.stack.pop()
                case 'ADD': self.stack.push(self.stack.pop() + self.stack.pop())
                case 'SUB': self.stack.push(self.stack.pop() - self.stack.pop())
                case 'MUL': self.stack.push(self.stack.pop() * self.stack.pop())
                case 'DIV': self.stack.push(self.stack.pop() / self.stack.pop())
                case 'MOD': self.stack.push(self.stack.pop() % self.stack.pop())
                case 'EQ': self.stack.push(self.stack.pop() == self.stack.pop())
                case 'NEQ': self.stack.push(self.stack.pop() != self.stack.pop())
                case 'LT': self.stack.push(self.stack.pop() < self.stack.pop())
                case 'GT': self.stack.push(self.stack.pop() > self.stack.pop())
                case 'JMP': self.pc = code[1]
                case 'JMP_IF': 
                    if self.stack.pop(): 
                        self.pc = code[1]
                case 'JMP_NIF': 
                    if not self.stack.pop(): 
                        self.pc = code[1]
                case 'NOP': pass
                case 'HALT': halt_called = True
                case 'LOAD': self.stack.push(self.register.load(code[1]))
                case 'SAVE': self.register.save(code[1], self.stack.pop())
                case 'PRINT': print(self.stack.pop())
                # SuperInstructionの最適化を行ったときに追加されるはずのInstruction
                # LOAD i > LOAD j > SAVE i > SAVE jがこれに当たる
                case 'SWAP':
                    tmp = self.register.load(code[1])
                    self.register.save(code[1], self.register.load(code[2]))
                    self.register.save(code[2], tmp)
                # インスタンス作成やメソッド呼び出しのために必要なInstruction
                # クラスおよびそのメソッドは定義済みとする。
                case 'RET': 
                    self.pc = self.ret_point.pop()
                case 'CALL':
                    self.register.save(0, self.stack.pop()["__cls__"])
                    self.register.save(1, code[1])
                    self.ret_point.push(self.pc)
                    self.pc = self.class_table.search_method(self.register.load(0), self.register.load(1))
                case 'NEW_INSTANCE': self.stack.push({"__cls__": code[1]})
                case 'SET_ATTR':
                    attr = self.stack.pop()
                    receiver = self.stack.pop()
                    receiver[code[1]] = attr
                    self.stack.push(receiver)
                case 'GET_ATTR':
                    self.stack.push(self.stack.pop()[code[1]])
                case 'DEFINE_CLS': 
                    self.class_table.def_cls(code[1])
                case 'SET_METHOD':
                    self.class_table.set_method(code[1], code[2], code[3])
                case _:
                    print("Undefined Instruction is Called!!!")
            if self.debug_mode:
                print(f"pc {self.pc}: stack {self.stack}")
        return
  
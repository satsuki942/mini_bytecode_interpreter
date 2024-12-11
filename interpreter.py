import sys

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
    
    def __str__(self):
        return str(self.register)

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
    def __init__(self, codes, enable_inline_caching=False, debug_mode=False):
        self.stack = Stack()
        self.register = Register()
        self.codes = codes
        self.class_table = ClassTables()
        self.pc = 0
        self.ret_point = Stack()
        self.enable_inline_caching = enable_inline_caching
        self.debug_mode = debug_mode

    def inline_caching(self, m_old_address):
        # codes[pointer] = CALL
        # ->
        # LOAD 0
        # PUSH NUM
        # EQ
        # JMP_NIF <>
        # SET_RET <>
        # JMP <sumのアドレス>
        # CALL
        # 
        pointer = self.pc - 1
        # 前処理(メソッドの呼び出しの深さが2以上だと壊れるかも)
        for code in self.codes:
            if (code[0] == 'JMP') or (code[0] == 'JMP_IF') or (code[0] == 'JMP_NIF'):
                if code[1] >= pointer:
                    code[1] += 6
            if code[0] == 'SET_METHOD':
                if code[3] >= pointer:
                    code[3] += 6
        # inline cachingによるコード挿入
        self.codes.insert(pointer, ['JMP', m_old_address+6])
        self.codes.insert(pointer, ['SET_RET', pointer+7])
        self.codes.insert(pointer, ['JMP_NIF', pointer+6])
        self.codes.insert(pointer, ['EQ'])
        self.codes.insert(pointer, ['LOAD', 0])
        self.codes.insert(pointer, ['PUSH', 'NUM'])
        # sys.exit(0)

    def interpret(self):
        halt_called = False
        while (not halt_called) and (0 <= self.pc < len(self.codes)):
            current_pc = self.pc + 1
            code = self.codes[self.pc]
            self.pc += 1
            match code[0]:
                case 'PUSH': self.stack.push(code[1])
                case 'POP': self.stack.pop()
                case 'ADD': self.stack.push(self.stack.pop() + self.stack.pop())
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
                case 'LOAD': self.stack.push(self.register.load(code[1]))
                case 'SAVE': self.register.save(code[1], self.stack.pop())
                case 'NOP': pass
                case 'HALT': halt_called = True
                # SuperInstructionの最適化を行ったときに追加されるはずのInstruction
                # LOAD i > LOAD j > SAVE i > SAVE jがこれに当たる
                case 'SWAP':
                    tmp = self.register.load(code[1])
                    self.register.save(code[1], self.register.load(code[2]))
                    self.register.save(code[2], tmp)
                # インスタンス作成やメソッド呼び出しのために必要なInstruction
                # クラスおよびそのメソッドは定義済みとする。
                case 'SET_RET':
                    self.ret_point.push(code[1])
                case 'RET': 
                    self.pc = self.ret_point.pop()
                case 'CALL':
                    if self.enable_inline_caching:
                        self.ret_point.push(self.pc + 6)
                        method_pointer = self.class_table.search_method(self.register.load(0), self.register.load(1))

                        self.inline_caching(method_pointer)
                        self.pc = method_pointer + 6
                    else:
                        self.ret_point.push(self.pc)
                        # メモリアクセスにかかる時間を表現
                        for i in range(10):
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
                # 基本命令セットであるが、あまり使わないもの
                case 'SUB': self.stack.push(self.stack.pop() - self.stack.pop())
                case 'MUL': self.stack.push(self.stack.pop() * self.stack.pop())
                case 'DIV': self.stack.push(self.stack.pop() / self.stack.pop())
                case 'MOD': self.stack.push(self.stack.pop() % self.stack.pop())
                case 'PRINT': print(self.stack.pop())
                case _:
                    print("Undefined Instruction is Called!!!")
            if self.debug_mode:
                print(f"pc {current_pc}: {code}\n   stack   :{self.stack}\n   register:{self.register}")
        return
  
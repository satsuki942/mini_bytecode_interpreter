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

class Interpreter:
    def __init__(self, codes, debug_mode=False):
        self.stack = Stack()
        self.register = Register()
        self.codes = codes
        self.pc = 0
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
                case _: 
                    print("Undefined Instruction is Called!!!")
            if self.debug_mode:
                print(f"pc {self.pc}: stack {self.stack}")
        return
  
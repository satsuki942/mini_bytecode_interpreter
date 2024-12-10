def is_comment(word):
    if word[0] == "#":
        return True

def is_float(word):
    try:
        float(word)
    except ValueError:
        return False
    else:
        return True
    
def is_int(word):
    try:
        int(word)
    except ValueError:
        return False
    else:
        return True
    
def can_convert_swap(list):
    if len(list) != 4:
        return False
    if (list[0][0] == "LOAD") and (list[1][0] == "LOAD") and (list[2][0] == "SAVE") and (list[3][0] == "SAVE"):
        if (list[0][1] == list[2][1]) and (list[1][1] == list[3][1]):
            return True
    return False

class Compiler:
    def __init__(self, code, opt_mode=False):
        self.code = code
        self.opt_mode = opt_mode

    def compile(self):
        # コンパイル後のバイトコード列が入る配列
        compiled_code = []
        # 行毎に分割後、単語ごとに分割
        lines = [line.split() for line in self.code.splitlines()]

        # [共通処理]
        # コメントの削除や数値のPythonオブジェクトへのキャストなど
        for line in lines:
            compiled_line = []
            for word in line:
                if is_comment(word):
                    break
                if is_int(word):
                    compiled_line.append(int(word))
                elif is_float(word):
                    compiled_line.append(float(word))
                else:
                    compiled_line.append(word)
            compiled_code.append(compiled_line)

        if not self.opt_mode:
            return compiled_code
        
        # super instructionを含むバイトコードへ変更
        # !!!bug!!!
        # jump先のpcのずれを補正する必要があるがまだしていない。
        swap_indexes = []
        for i , line in enumerate(compiled_code):
            if i < 3:
                continue
            # swapにconvert可能かを確認する
            if can_convert_swap(compiled_code[i-3:i+1]):
                swap_indexes.append(i)
        swap_indexes.reverse()
        pre_index = None
        for index in swap_indexes:
            if pre_index is None:
                swap_indexes = index
            elif index - pre_index > 3:
                swap_indexes = index
            else:
                continue
                
            register_i1 = compiled_code[index-3][1]
            register_i2 = compiled_code[index-2][1]
            compiled_code[index-3:index+1] = [['SWAP', register_i1, register_i2]]   

        return compiled_code     

# transelate python byte code to wat
# this is dev branch
# test

from dis import dis,Bytecode

class Examples:
    def __init__(self):
        pass
    
    @property
    def ex1(self):
        return "a = 500\n"\
                "b = 600\n"\
                "c = a + b"
    @property
    def ex2(self):
        return "25 - 20"

    @property
    def ex3(self):
        return "a = 100\n"\
                "b = a - 5\n"\
                "print(b)"
    @property
    def ex4(self):
        return "a = 500\n"\
                "b = 600\n"\
                "c = 700\n"\
                "d = a + b * c\n"\
                "print(d)"
    @property
    def ex5(self):
        return "print(100)\n"\
                "print(200)\n"\
                "print(300)\n"\
                "print(400)"
    @property
    def ex6(self):
        #FIXME
        return "i = 0\n"\
                "while i < 100:\n"\
                "\tprint(i)"

    @property
    def ex7(self):
        #FIXME
        return "a = 1\n"\
                "b = 2\n"\
                "a < b\n"\
                "print(a)\n"
class Eval:
    def __init__(self):
        self.rettype = ""
        self.stack = []
        self.env = {}

    def eval(self,op):
        if op.opname == 'LOAD_CONST':
            self.stack.append(op.argval)
        
        elif op.opname == 'STORE_NAME':
            if len(self.stack) > 0:
                self.env.update({
                    op.argrepr:self.stack[-1]
                    })
                self.stack.pop()
            else:
                self.env.update({
                    op.argrepr:None
                    })
        elif op.opname == 'LOAD_NAME':
            if op.argval == 'print':
                self.stack.append('PRINT')
            else:
                self.stack.append(self.env[op.argval])
        
        elif op.opname == 'BINARY_ADD':
            #r = self.stack[-1]+ self.stack[-2]
            self.stack.pop()
            self.stack.pop()
            self.stack.append(None)
        
        elif op.opname == 'BINARY_MULTIPLY':
            #r = self.stack[-1]+ self.stack[-2]
            self.stack.pop()
            self.stack.pop()
            self.stack.append(None)
        
        elif op.opname == 'BINARY_SUBTRACT':
            #r = self.stack[-1]+ self.stack[-2]
            self.stack.pop()
            self.stack.pop()
            self.stack.append(None)
        
        elif op.opname == 'POP_TOP':
            self.stack.pop()
        
        elif op.opname == 'COMPARE_OP':
            if self.stack[-2] < self.stack[-1]:
                t = self.stack[-2]
                self.stack.pop()
                self.stack.pop()
                self.stack.append(t)
            else:
                self.stack.pop()
                self.stack.pop()
                self.stack.append(0)

        elif op.opname == 'RETURN_VALUE':
            self.rettype = type(self.stack[-1])


class Templates:
    def __init__(self):
        self.ret = None
        self.__vars = []
        self.ADD_PRINT = False
        self.modules = ";;Here built in modules\n"
        self.init_vars = ";;to init vars\n"
        self.program_body = ";;Here start programm boy\n"
        self.ret_type = ";;Here but return of main func\n"
        self.ret = ";;Here but the return\n"

    @property
    def Entry(self):
        return "(module\n"\
                f"\t{self.modules}\n"\
                f"\t(func (export \"__start\")\n"\
                f"\t(result {self.ret_type})\n"\
                f"\t\t{self.init_vars}\n"\
                f"\t\t{self.program_body}\n"\
                f"\t\t{self.ret}\n"\
                f"\t)\n)"
    
    @property
    def PRINT(self):
        if not self.ADD_PRINT:
            self.ADD_PRINT = True
            return "\t(import \"console\" \"log\" (func $PRINT (param i32)))"
        return ""

    def LOAD_CONST(self,x,name):
        if not name:
            return f"\t\t(i32.const {x})\n" 
        elif x:
            return f"\t\t(local.set ${name}(i32.const {x}))\n"
        return f"\t\t(local.set ${name})\n"

    def LOAD_NAME(self,x):
        return f"\t\t(local.get ${x})\n"

    def STORE_NAME(self,name,vtype):
        return f"\t\t(local ${name} {vtype})\n"

    @property
    def BINARY_ADD(self):
        return "\t\ti32.add\n"

    @property
    def BINARY_MULTIPLY(self):
        return "\t\ti32.mul\n"

    @property
    def BINARY_SUBTRACT(self):
        return "\t\ti32.sub\n"
    
    def CALL_FUNCTION(self,fn):
        if fn == 'PRINT':
            return f"\t\t(call $PRINT)\n"

    @property
    def COMPARE_OP(self):
        return f"\t\ti32.lt_u\n"

    def RETURN_TYPE(self,vtype):
        return f"\t\t{vtype}"


class Translate:
    def __init__(self,pycode):
        self.templates = Templates()
        self.Eval = Eval()
        self.pycode = pycode
        self.wat_code = ""
        self.start()
        print(self.templates.Entry)
        self.write(self.templates.Entry)

    def start(self):
        byte_code = list(Bytecode(self.pycode))
        for op_count in range(len(byte_code)):
            
            eval_op = self.Eval.eval(byte_code[op_count])
            if byte_code[op_count].opname == 'LOAD_CONST':
                if not byte_code[op_count].argval == None:
                    if byte_code[op_count + 1].opname != 'STORE_NAME':
                        self.templates.program_body += self.templates.LOAD_CONST(byte_code[op_count].argval,0)
            
            elif byte_code[op_count].opname == 'STORE_NAME':
                self.templates.init_vars += self.templates.STORE_NAME(byte_code[op_count].argval,'i32')
                self.templates.program_body += self.templates.LOAD_CONST(self.Eval.env[byte_code[op_count].argval],byte_code[op_count].argval)
            elif byte_code[op_count].opname == 'LOAD_NAME':
                if byte_code[op_count].argval == 'print':
                    self.templates.modules += self.templates.PRINT
                else:
                    self.templates.program_body += self.templates.LOAD_NAME(byte_code[op_count].argval)

            elif byte_code[op_count].opname == 'BINARY_ADD':
                self.templates.program_body += self.templates.BINARY_ADD
            
            elif byte_code[op_count].opname == 'BINARY_MULTIPLY':
                self.templates.program_body += self.templates.BINARY_MULTIPLY 

            elif byte_code[op_count].opname == 'BINARY_SUBTRACT':
                self.templates.program_body += self.templates.BINARY_SUBTRACT 
            
            elif byte_code[op_count].opname == 'CALL_FUNCTION':
                call = self.templates.CALL_FUNCTION(self.Eval.stack[byte_code[op_count].argval - 1])
                self.templates.program_body += call
            
            elif byte_code[op_count].opname == 'COMPARE_OP':
                if byte_code[op_count].argval == '<':
                    self.templates.program_body += self.templates.COMPARE_OP

            elif byte_code[op_count].opname == 'RETURN_VALUE':
                if self.Eval.stack[-1] != None:
                    #if type(self.Eval.stack[0]) == int:
                    self.templates.ret_type += self.templates.RETURN_TYPE('i32')
            print(self.Eval.stack)
    
    def write(self,g):
        with open('wat/out.wat','w') as out:
            out.write(g)

if __name__ == '__main__':
    print('\n-------python code------------------\n')
    code = Examples().ex7
    print(code)

    print('\n-------python byte code--------------\n')
    dis(code)
    
    print('\n-------- wat gen code-----------------\n') 
    t = Translate(code)

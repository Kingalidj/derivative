import re
class equation:

    operations = ["+", "-", "*", "/"]
    functions = []
    eqType = {
            "[a]*x^[b]": "[a*b]*x^([b-1])", 
            "x^[a]": "[a]*x^([a-1])", 
            "[a]*x":"[a]", 
            "x":"0", 
            "[a]":"0",
            "sin(x)": "cos(x)",
            "cos(x)": "-sin(x)"
            }

    def __init__(self, eq):
        self.eq = eq.lower().replace(" ", "").strip()

    def show(self):
        print(self.eq)

    def breakdown(self, eq):
        res = [""]
        for i in range(len(eq)):
            if eq[i] in ["+", "*", "/", "^"]:
                res.append("")
            #if eq[i] == "+":
            #    res.append("")
            elif eq[i] == "-" and eq[i - 1] != "^" and eq[i - 1] != "(" and i != 0:
                res.append("")
            #elif eq[i] in ["+", "*", "/", "^"]:
            #    res.append("")
            #elif eq[i] == "/":
            #    res.append("")
            #elif eq[i] == "^":
            #    res.append("")
            else:
                res[-1] += eq[i]
        return res

    def operate(self, a, b = "nan", o = "nan"):
        def isfloat(val):
            try:
                float(val)
                return True
            except ValueError:
                return False

        if b == "nan" and o == "nan":

            foundOp = False
            for op in ["+", "-", "*", "/"]:
                if op in a:
                    foundOp = True
            if not foundOp:
                return a


            parts = re.split('[+\-\*/]+', a)
            for op in self.operations:
                if op in a:
                    o = op
            a = parts[0]
            b = parts[1]

        if o not in ["+", "-", "*", "/"]:
            print("operation is not possible")
            return ""

        if isfloat(a) and isfloat(b):
            if o == "+":
                return str(float(a) + float(b))
            if o == "-":
                return str(float(a) - float(b))
            if o == "*":
                return str(float(a) * float(b))
            if o == "/":
                return str(float(a) / float(b))

        elif a[-1] == b[-1]:
            x = 1 if len(a) == 1 else a[:len(a) - 1]
            y = 1 if len(b) == 1 else b[:len(b) - 1]

            if o == "+":
                return str(float(x) + float(y)) + "*" + a[-1]
            if o == "-":
                return str(float(x) - float(y)) + "*" + a[-1]
            if o == "*":
                return str(float(x) * float(y)) + "*" + a[-1]
            if o == "/":
                return str(float(x) / float(y)) + "*" + a[-1]
        else:
            return a + o + b

    def dMatch(self, d = "x"):
        eq = self.breakdown(self.eq)

        for  eqType in self.eqType:
            eqT = self.breakdown(eqType)

            # TODO what about x^2 != ax^b
            # I think i solved it...

            found = False
            if len(eq) == len(eqT):
                found = True
                for i in range(len(eq)):
                    if "x" in eqT[i] and eq[i].replace(d, "x") != eqT[i]:
                        found = False
                        break
                    if "[" in eqT[i] and eq[i] == d:
                        found = False
                        break
            if found:
                return eqType

        return None

    def deriveFunc(self, d = "x"):
        match = self.dMatch(d)
        if (match == None): 
            return None
        
        eqParts = self.breakdown(match)
        eq = self.breakdown(self.eq)
        res = self.eqType[match]
        variables = []
        if "a" in match:
            variables.append("")
        if "b" in match:
            variables.append("")

        for i, p in enumerate(eqParts):
            if "a" in p:
                variables[0] = eq[i]
            if "b" in p:
                variables[1] = eq[i]

        if len(variables) >= 1:
            res = res.replace("a", variables[0])
        if len(variables) >= 2:
            res = res.replace("b", variables[1])
        
        additions = re.split(r"(?![^[]*])", res)
        res = ""
        for a in additions:
            if "[" in a:
                add = self.operate(a[1:-1])
                res += add
            else:
                res += a


        res = res.replace("x", d)
        return res

    def mapFunc(self, d = "x"):
        eq = ""
        numb = False
        numbers = [""]
        for i,s in enumerate(self.eq):
            if s.isnumeric() or s == "." and numb:
                numbers[-1] += s
                numb = True
            elif numb and not s.isnumeric():
                numb = False
                eq += f"[n{len(numbers) - 1}]"
                eq += s
                numbers.append("")
            else:
                eq += s
        if numb:
            eq += F"[n{len(numbers) - 1}]"


        numbers = list(map(int, filter(None, numbers)))

        additions = [""]
        bracket = 0
        print(eq)
        for e in eq:
            if e == "(":
                additions.append(e)
                bracket += 1
            elif e == ")":
                additions[-1] += e
                additions.append("")
                bracket -= 1
            elif bracket != 0:
                additions[-1] += e
            elif e in ["+", "-", "*", "/", "^"]:
                additions.append(e)
                additions.append("")
            else:
                additions[-1] += e

        additions = list(filter(None, additions))
        funcMap = [""]
        functions = {}

        fcount = 0
        for a in additions:
            if "(" in a or "x" in a:
                funcMap.append(f"[f{fcount}]")
                functions[f"[f{fcount}]"] = a
                fcount += 1
                funcMap.append("")
            else:
                funcMap[-1] += a


        

    def derive(self, d = "x"):
        eq = self.eq
        eq = eq.split("+")
        if len(eq) == 1:
            return self.deriveFunc(d)

        res = ""
        for i, func in enumerate(eq):
            f = equation(func)
            res += f.derive(d)
            res += "+" if i < len(eq) - 1 else ""

        return res


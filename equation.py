import re
class equation:

    operations = ["+", "-", "*", "/"]
    eqType = {
            "[a]*x^[b]": "[a*b]*x^([b-1])", 
            "x^[a]": "[a]*x^([a-1])", 
            "[b]*x":"[b]", 
            "x":"0", 
            "[a]":"0",
            "sin(x)": "cos(x)",
            "cos(x)": "-sin(x)"
            }

    def __init__(self, eq):
        self.eq = eq.lower()

    def show(self):
        print(self.eq)

    def breakdown(self, eq):
        res = [""]
        for i in range(len(eq)):
            if eq[i] == "+":
                res.append("")
            elif eq[i] == "-" and eq[i - 1] != "^" and eq[i - 1] != "(" and i != 0:
                res.append("")
            elif eq[i] == "*":
                res.append("")
            elif eq[i] == "/":
                res.append("")
            elif eq[i] == "^":
                res.append("")
            else:
                res[-1] += eq[i]

        return re.split('[+-/*/^]+', eq)

    def operate(self, a, b = "nan", o = "nan"):
        def isfloat(val):
            try:
                float(val)
                return True
            except ValueError:
                return False

        if b == "nan" and o == "nan":
            parts = re.split('[+-/*/]+', a)
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
        variables = [""] * (match.count('a') + match.count('b'))

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
        print(additions)
        res = ""
        for a in additions:
            if "[" in a:
                add = self.operate(a[1:-1])
                res += add
            else:
                res += a


        res = res.replace("x", d)
        return res




    def derive(self, d = "x"):
        eq = self.eq
        if self.dMatch(d) != "":
            return self.eqType[self.dMatch(d)]
        return "no derivative found"


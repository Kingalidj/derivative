import re
class equation:

    eqType = {"[a]*x^[b]": "[a*b]*x^[b-1]", 
            "x^[a]": "[a]*x^[a-1]", 
            "[b]*x":"[b]", 
            "x":"0", 
            "sin(x)": "cos(x)",
            "cos(x)": "-sin(x)"
            }

    def __init__(self, eq):
        self.eq = eq.lower()

    def show(self):
        print(self.eq)

    def breakdown(self, eq):
        return re.split('[+-/*/^]+', eq)

    def match(self, d = "x"):
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

        return ""


    def operate(a, b, o):
        def isfloat(val):
            try:
                float(val)
                return True
            except ValueError:
                return False

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


    def derive(self, d = "x"):
        eq = self.eq
        if self.match(d) != "":
            return self.eqType[self.match(d)]
        return "no derivative found"


"""
PVD Design Calculator
Author : ChatGPT
Reference : PVD Lecture
"""

import math


class PVDDesign:

    def __init__(self,
                 spacing,
                 pattern,
                 width=100,
                 thickness=5):

        self.spacing = spacing          # m
        self.pattern = pattern.lower()

        # PVD Dimension (mm)
        self.width = width
        self.thickness = thickness


    #################################################
    # Effective Diameter
    #################################################

    def effective_diameter(self):

        if self.pattern == "square":
            return 1.13 * self.spacing

        elif self.pattern == "triangle":
            return 1.05 * self.spacing

        else:
            raise ValueError("Pattern must be square or triangle")


    #################################################
    # Equivalent Diameter (Hansbo)
    #################################################

    def equivalent_diameter(self):

        a = self.thickness
        b = self.width

        dw = 2 * (a + b) / math.pi

        return dw


    #################################################
    # Drain Spacing Factor
    #################################################

    def n_factor(self):

        de = self.effective_diameter() * 100

        dw = self.equivalent_diameter()

        return de / dw


    #################################################
    # Barron Fn
    #################################################

    def Fn(self):

        n = self.n_factor()

        return math.log(n) - 0.75


    #################################################
    # Time Factor
    #################################################

    def time_factor(self,
                    Ch,
                    t):

        de = self.effective_diameter()

        Tr = Ch * t / (de ** 2)

        return Tr


    #################################################
    # Radial Consolidation
    #################################################

    def radial_consolidation(self,
                             Ch,
                             t):

        Tr = self.time_factor(Ch, t)

        F = self.Fn()

        Ur = 1 - math.exp((-8 * Tr) / F)

        return Ur


##########################################################
# Main
##########################################################

if __name__ == "__main__":

    print("-------------------------------------")
    print("PVD DESIGN")
    print("-------------------------------------")

    S = float(input("Spacing (m) : "))

    pattern = input("Pattern (square / triangle) : ")

    Ch = float(input("Horizontal Cv (m2/day): "))

    t = float(input("Time (day): "))

    pvd = PVDDesign(S,
                    pattern)

    print()

    print("========== RESULT ==========")

    print(f"Effective Diameter : {pvd.effective_diameter():.3f} m")

    print(f"Equivalent Diameter : {pvd.equivalent_diameter():.2f} mm")

    print(f"n = {pvd.n_factor():.2f}")

    print(f"Fn = {pvd.Fn():.3f}")

    print(f"Time Factor = {pvd.time_factor(Ch,t):.4f}")

    print(f"Ur = {pvd.radial_consolidation(Ch,t)*100:.2f} %")

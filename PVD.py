import math

def effective_diameter(spacing, pattern="square"):
    """
    Calculate effective drainage diameter (de)
    """
    if pattern.lower() == "square":
        return 1.13 * spacing
    elif pattern.lower() == "triangle":
        return 1.05 * spacing
    else:
        raise ValueError("Pattern must be square or triangle")

S = 1.0
de = effective_diameter(S, "square")

print(f"Drain spacing = {S:.2f} m")
print(f"Effective diameter = {de:.3f} m")

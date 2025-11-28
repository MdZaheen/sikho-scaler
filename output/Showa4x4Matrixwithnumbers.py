from manim import *

class MatrixCreation(Scene):
    def construct(self):
        # Step 1: Create a 4x4 matrix with numbers from 1 to 16
        # Numbers will be arranged in a grid format within a square bracket structure
        
        # Generate a list of numbers for the matrix (1-16)
        numbers = [i+1 for i in range(16)]
        
        # Create a 4x4 matrix using MathTex objects
        # Each cell is represented by a single MathTex element with numbers from 1 to 16
        matrix = VGroup(*[MathTex(f"{n}") for n in numbers])
        
        # Position the matrix elements in a 4x4 grid format within brackets
        # The positions are calculated based on the size of each number and its alignment
        bracket_size = 2 * (len(numbers) ** 0.5)
        offset = (bracket_size - len(numbers)) / 2
        
        # Position the matrix elements in a 4x4 grid format within brackets
        for i, tex in enumerate(matrix):
            row = i // 4
            col = i % 4
            
            # Position each number within its respective cell
            pos_x = (col - 1.5) * 0.8 + offset
            pos_y = (row - 1.5) * 0.8 + offset
            
            tex.move_to([pos_x, pos_y, 0])
        
        # Create the outer bracket with size adjusted to fit all elements
        bracket = Square(side_length=bracket_size)
        
        # Combine the matrix and brackets into a single VGroup
        matrix_mobject = VGroup(bracket, *matrix)
        
        # Animate the creation of the matrix (using the Create animation)
        self.play(Create(matrix_mobject), run_time=1.5)
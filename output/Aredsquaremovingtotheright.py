from manim import *

class RedSquareMovingRight(Scene):
    def construct(self):
        # Create a square object (red solid block) at the origin
        red_square = Square(side_length=1.5, color=RED, fill_opacity=1, stroke_width=0)
        
        # Position the square at the ORIGIN
        square_group = VGroup(red_square).move_to(ORIGIN)
        
        # Create a title with color change to show movement direction
        title = Text("Red Square Moving Right", color=RED_C)
        
        # Animate the creation of the title and square simultaneously
        self.play(Create(title), FadeIn(square_group))
        
        # Add a brief pause before starting the animation
        self.wait(0.5)
        
        # Move the square to the right by shifting it 3 units horizontally
        move_left = Square(side_length=1.5, color=RED_C, fill_opacity=1, stroke_width=0).move_to(LEFT*3 + UP)
        
        self.play(Transform(square_group, move_left), run_time=2)  # Animation time of 2 seconds
        
        # Create a fade-in effect for the title to make it more dynamic
        self.play(FadeIn(title))
        
        # Add a final pause before ending the animation
        self.wait(1)
        
        # Clean up by fading out the square and title after completing the sequence
        self.play(FadeOut(square_group), FadeOut(title))
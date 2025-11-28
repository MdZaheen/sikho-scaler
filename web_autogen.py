from manim import *

class ThreeJSAnimation(Scene):
    def construct(self):
        # Title
        title = Text("What is 3.js?", font_size=40)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        
        # Introduction to 3.js
        intro_text = Text("3.js: JavaScript for the Web", font_size=36)
        self.play(Write(intro_text))
        self.wait(2)
        self.play(FadeOut(intro_text))
        
        # Create a simple 3D cube using Manim's built-in functions
        # This is a simplified representation of what 3.js can do
        cube = Cube(side_length=1.5, color=BLUE)
        self.play(Create(cube))
        self.wait(2)
        
        # Add some text to explain the concept
        explanation = Text("3D graphics in your browser", font_size=30)
        explanation.next_to(cube, DOWN)
        self.play(Write(explanation))
        self.wait(1)
        
        # Clear screen for next section
        self.play(FadeOut(cube), FadeOut(explanation))
        
        # Show the 3.js logo
        js_logo = Text("3.js", font_size=40, color=YELLOW)
        self.play(Write(js_logo))
        self.wait(1)
        
        # Add a simple equation to explain how it works
        eq = MathTex(r"\text{3D} \rightarrow \text{Web}")
        eq.next_to(js_logo, DOWN)
        self.play(Write(eq))
        self.wait(2)
        
        # Clear screen for conclusion
        self.play(FadeOut(js_logo), FadeOut(eq))
        
        # Final message
        final_text = Text("3.js: The Future of Web Graphics", font_size=40)
        self.play(Write(final_text))
        self.wait(2)
        
        # Clean up and exit
        self.play(FadeOut(final_text))
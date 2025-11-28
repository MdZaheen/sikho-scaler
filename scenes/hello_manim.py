from manim import *


class HelloManim(Scene):
    """A simple test animation to verify Manim is working."""
    
    def construct(self):
        # Create text
        title = Text("Hello, Manim!", font_size=72)
        subtitle = Text("Foundation verified ✓", font_size=36, color=GREEN)
        subtitle.next_to(title, DOWN, buff=0.5)
        
        # Animations
        self.play(Write(title), run_time=2)
        self.wait(0.5)
        self.play(FadeIn(subtitle), run_time=1)
        self.wait(1)
        
        # Transform
        self.play(
            title.animate.scale(0.5).to_edge(UP),
            subtitle.animate.scale(0.8).next_to(title, DOWN, buff=0.3),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Circle animation
        circle = Circle(radius=2, color=BLUE)
        self.play(Create(circle), run_time=2)
        self.wait(0.5)
        
        # Rotate and fade out
        self.play(
            Rotate(circle, angle=2*PI, run_time=2),
            FadeOut(title),
            FadeOut(subtitle)
        )
        self.wait(0.5)

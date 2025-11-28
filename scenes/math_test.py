from manim import *


class MathTest(Scene):
    """Test animation with LaTeX formulas to verify full Manim functionality."""
    
    def construct(self):
        # Refresh PATH to access ffmpeg and latex
        import os
        user_path = os.environ.get('PATH', '')
        
        # Title
        title = Text("Manim + LaTeX Test", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        
        # Famous formulas
        einstein = MathTex(r"E = mc^2", font_size=72)
        self.play(Write(einstein), run_time=2)
        self.wait(1)
        
        # Transform to another formula
        euler = MathTex(r"e^{i\pi} + 1 = 0", font_size=72, color=YELLOW)
        self.play(Transform(einstein, euler), run_time=2)
        self.wait(1)
        
        # Quadratic formula
        quadratic = MathTex(
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            font_size=60,
            color=GREEN
        )
        self.play(
            einstein.animate.scale(0.5).to_edge(UP).shift(DOWN * 0.5),
            FadeIn(quadratic),
            run_time=2
        )
        self.wait(1)
        
        # Integral
        integral = MathTex(
            r"\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}",
            font_size=55,
            color=RED
        )
        integral.next_to(quadratic, DOWN, buff=0.7)
        self.play(Write(integral), run_time=2)
        self.wait(1)
        
        # Final message
        success = Text("✓ LaTeX Working!", font_size=40, color=GREEN)
        success.to_edge(DOWN)
        self.play(FadeIn(success), run_time=1)
        self.wait(2)
        
        # Fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.5)
        self.wait(0.5)

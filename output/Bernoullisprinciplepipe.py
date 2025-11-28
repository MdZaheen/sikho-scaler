from manim import *

class BernoulliPrincipleScene(Scene):
    def construct(self):
        # Create the horizontal pipe at bottom (6x4)
        pipe = Rectangle(width=8, height=3, color=WHITE).shift(DOWN*1.5)
        
        # Position P label above wide part
        p_label = Text("P", color=YELLOW).scale(0.7).move_to(pipe.get_center())
        self.play(Write(p_label))
        
        # Position V label below narrow part
        v_label = Text("V", color=YELLOW).scale(0.7).move_to(pipe.get_center() + UP*1)
        self.play(Write(v_label))
        
        # Show pipe to reveal all elements before animation starts
        self.play(Create(pipe))
        
        # Create 5 water dots - 3 at wide part, 2 at narrow part
        dots = VGroup()
        for i in range(3):  # 3 dots per side
            dot1 = Dot(point=pipe.get_left() + RIGHT * (i+0.5), color=BLUE)
            dot2 = Dot(point=pipe.get_right() + LEFT * (4-i*2-0.5), color=BLUE)
            dots.add(dot1, dot2)
        
        # Move dots to the left side of pipe
        self.play(Create(dots))
        
        # Animate the dots moving from the right to the left
        for i in range(3):
            self.play(
                dots.animate.shift(RIGHT*0.5),
                run_time=0.4  # Increase speed for wider pipes
            )
            
            # Speed up the dots as they enter the narrow section
            if i < 2:
                self.play(
                    dots.animate.scale(1.2),  # Pulsate effect
                    run_time=0.3
                )
        
        # Show final state with all dots in place and labels faded out
        self.play(FadeOut(p_label), FadeOut(v_label))
        self.wait()
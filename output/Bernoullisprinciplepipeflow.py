from manim import *

class BernoulliPrinciplePipeFlow(Scene):
    def construct(self):
        # Create the pipe object (horizontal tube)
        pipe = Rectangle(height=2, width=4, fill_opacity=0.3, stroke_width=0)
        pipe.set_stroke(color=GREY_B)  # Set the color of the pipe
        
        # Position the pipe in the center
        pipe.shift(LEFT * 2 + DOWN * 1)
        
        # Create water as a filled curve inside the pipe
        # Representing flow velocity with a gradient effect
        water_gradient_points = [
            [pipe.get_left() + UP * 0.5 + RIGHT * 0, pipe.get_right() + DOWN * 0.5 + LEFT * 1],
            [pipe.get_left() + DOWN * 0.5 + LEFT * 1, pipe.get_right() + UP * 0.5 + RIGHT * 0]
        ]
        
        # Create the gradient effect
        water_gradient = FilledCurve(
            points=water_gradient_points,
            color=BLUE_C
        )
        water_gradient.shift(LEFT * 2)
        
        # Add some transparency to the water for flow effect
        water_gradient.set_fill_opacity(0.7)  # Set fill opacity to 70%
        
        # Create velocity arrows at different points in the pipe
        # V1 arrow at left constriction
        V1 = Arrow(
            start=pipe.get_center() + LEFT * 0.8,
            end=pipe.get_center() + UP * 0.3 + RIGHT * 0.5,
            color=RED, 
            stroke_width=4
        )
        
        # V2 arrow at narrowest point
        V2 = Arrow(
            start=pipe.get_center() + RIGHT * 0.8,
            end=pipe.get_top(),
            color=RED,
            stroke_width=4
        )
        
        # Position the arrows slightly above the water surface
        V1.shift(UP * 0.5)
        V2.shift(UP * 0.5)
        
        # Create pressure gauge rectangles (simple bar gauges)
        P1_rect = Rectangle(height=1.8, width=0.6, color=GREEN_B, stroke_width=0)
        P2_rect = Rectangle(height=0.8, width=0.6, color=GREEN_B, stroke_width=0)
        
        # Position the pressure gauges at their respective points
        P1_rect.shift(LEFT * 2 + DOWN * 1)  # At left constriction
        P2_rect.shift(RIGHT * 2 + UP * 0.5)  # At narrowest point
        
        # Create labels next to velocity arrows and pressure gauges
        v1_label = Text("V1", color=WHITE).scale(0.4)
        p1_label = Text("P1", color=WHITE).scale(0.3)
        
        v2_label = Text("V2", color=WHITE).scale(0.4)
        p2_label = Text("P2", color=WHITE).scale(0.3)
        
        # Position the labels adjacent to their respective arrows/gauges
        v1_label.next_to(V1, UP)
        p1_label.next_to(P1_rect, DOWN)
        
        v2_label.next_to(V2, UP)
        p2_label.next_to(P2_rect, DOWN)
        
        # Add an equation for Bernoulli's principle
        bernoulli_equation = MathTex(
            "P + \\frac{1}{2}\\rho v^2 + \\rho gh = \\text{constant}"
        )
        # Center the equation horizontally
        equat_pos = UP * 3.5  # Position the equation slightly above the center of the screen
        bernoulli_equation.next_to(pipe, equat_pos)
        
        # Add all objects to a group for easier manipulation
        pipe_group = VGroup(
            pipe,
            water_gradient,
            V1,
            V2,
            P1_rect,
            P2_rect,
            v1_label,
            p1_label,
            v2_label,
            p2_label,
            bernoulli_equation
        )
        
        # Display all objects together as the scene begins
        self.play(Create(pipe_group))
        
        # Simulate fluid flow by moving water across the pipe
        # This creates an illusion of velocity and pressure changes
        def water_gradient_shift_effect():
            for point in water_gradient.get_points():
                x = point[0]
                y = point[1] + 0.2 if (x < -1 or x > 1) else point[1]
                yield Point(x, y)
        
        self.play(
            ShowCreation(water_gradient),
            run_time=3,
            rate_func=water_gradient_shift_effect
        )
        
        # Fade out the water gradient to show flow vectors
        self.play(FadeOut(water_gradient))
        
        # Animate the creation of velocity arrows and pressure gauges
        self.play(Create(V1), Write(v1_label))
        self.play(Write(p1_label))
        self.wait(0.5)
        
        self.play(Create(P2_rect), Write(p2_label))
        self.play(Create(V2), Write(v2_label))
        
        # Display the final equation at the end
        self.play(
            FadeOut(pipe_group),
            FadeIn(bernoulli_equation),
            run_time=1
        )
        
        # Final animation: show the pressure decrease and velocity increase
        self.play(
            V2.animate.set_length(V1.get_length() * 0.8),  # Decrease arrow length for pressure decrease
            p2_label.animate.scale(0.7).shift(DOWN * 0.5)   # Reduce size and shift vertically
        )
        
        self.wait(1)
        
        # Add a final message about the principle
        conclusion = Text("Bernoulli's Principle: Pressure decreases faster than velocity increases", color=WHITE).scale(0.6)
        conclusion.next_to(pipe, UP)
        self.play(FadeIn(conclusion), run_time=1)
        
        # Show pressure decrease arrow for emphasis
        pressure_arrow = Arrow(
            start=P2_rect.get_center() + DOWN * 0.2,
            end=P2_rect.get_center(),
            color=RED,
            stroke_width=4
        )
        self.play(Create(pressure_arrow), run_time=1)
        
        self.wait(3)
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.pyttsx3 import PyTTSX3Service

class AutogenScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(PyTTSX3Service())
        
        # Visual 1: Circle with radius 'r'
        circle = Circle(radius=2)
        label_r = Text("r", font_size=24).next_to(circle, RIGHT)
        circle_label = VGroup(circle, label_r)
        
        with self.voiceover(text="Consider a circle with radius 'r'.") as tracker:
            self.play(Create(circle), Write(label_r), run_time=tracker.duration)
        
        # Visual 2: Dividing the circle into sectors
        sectors = VGroup()
        for i in range(8):
            sector = Polygon(
                [0, 0, 0], 
                [-1.5, -1, 0],
                [-1, -1.5, 0]
            )
            sector.rotate(i * PI / 4)
            sectors.add(sector)
        self.play(FadeIn(sectors), run_time=2)
        
        # Visual 3: Rearranging the sectors
        for i in range(8):
            if i % 2 == 0:
                sectors[i].rotate(-PI/2)
            else:
                sectors[i].rotate(PI/2)
        
        self.play(FadeIn(circle_label), run_time=1.5)
        
        # Visual 4: Transforming the sectors into a rectangle
        rect = Rectangle(width=2*PI, height=2).move_to(np.array([0, 0, 0]))
        
        with self.voiceover(text="Arrange slices alternating up and down.") as tracker:
            self.play(
                ReplacementTransform(sectors, rect),
                run_time=tracker.duration
            )
        
        # Display the area equation
        area_eq = MathTex("Area = \\pi r^2")
        
        with self.voiceover(text="This forms a rectangle. Height 'r', length 'πr'. Area is πr².") as tracker:
            self.play(
                FadeIn(area_eq),
                run_time=tracker.duration
            )
        
        # Final fade out
        final = VGroup(rect, area_eq)
        self.play(FadeOut(final), FadeOut(circle_label), FadeOut(label_r), run_time=1)
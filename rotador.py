from manim import *

class PlanoCartesiano(MovingCameraScene):
    def construct(self):
        self.camera.frame.shift(UP)

        # Crear ejes
        axes = Axes(
            x_range=[-7, 7, 1],  # [min, max, step]
            y_range=[-10, 10, 1],
            x_length=14,  # largo visual en pantalla
            y_length=20,
            axis_config={
                "color": WHITE,
                "include_numbers": False
            }
        )
        grid = NumberPlane(
            y_range=[-12, 12, 1]
        )
        grid.set_opacity(.8)
        grid.set_z_index(0)
        p1 = Dot(grid.c2p(1, 1), color=YELLOW).set_z_index(1)
        p2 = Dot(grid.c2p(3, 1), color=GREEN).set_z_index(1)
        p3 = Dot(grid.c2p(2, 4), color=ORANGE).set_z_index(1)
        p4 = Dot(grid.c2p(2, 2), color=RED).set_z_index(1)
        p5 = Dot(grid.c2p(0.353553, 0), color=RED).set_z_index(1)
        p6 = Dot(grid.c2p(0.707106, 0.707106), color=BLUE).set_z_index(1)
        
        A = p1.get_center()
        B = p2.get_center()
        C = p3.get_center()

        # Animaciones
        self.play(FadeIn(p1, run_time=2))
        self.play(FadeIn(p2, run_time=2))
        self.play(FadeIn(p3, run_time=2))
        self.play(Create(grid, run_time=3, lag_ratio=0.1))
        self.remove(VGroup(p1, p2, p3))
        self.add(VGroup(p1, p2, p3))
        self.play(Create(axes))
        tri = Polygon(A, B, C, color=BLUE)
        self.play(Create(tri))
        self.play(tri.animate.set_fill(BLUE, opacity=0.5))
        self.wait()
        self.play(FadeIn(p4, run_time=2))
        self.play(FadeIn(p5, run_time=2))
        two = Polygon(p4.get_center(), p6.get_center(),p5.get_center(), color=BLUE)
        self.play(Create(two))

        self.play(FadeIn(p6, run_time=2))
        p7 = grid.c2p(0, 0)
        p8 = grid.c2p(0.707106, 0)
        one = Polygon(p7, p8,p6.get_center(), color=RED)
        self.play(FadeOut(VGroup(two, p4, p5)))
        self.play(Create(one))
        self.play(one.animate.set_fill(RED, opacity=0.5))
        
        self.wait()


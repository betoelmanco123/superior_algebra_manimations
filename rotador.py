from manim import *

import sympy as sp


def pythagorean_theorem(a, b):
    return sp.sqrt(a**2 + b**2)


AZUL_ELECTRICO = "#0800FF"
MORADO_ELECTRICO = "#9B00FF"
ROJO_ELECTRICO = "#FF0000"


class PlanoCartesiano(MovingCameraScene):

    def multiply_imaginary(self, dot_one, dot_two, grid):
        a_1, b_1 = dot_one
        a_2, b_2 = dot_two
        r_1 = pythagorean_theorem(b_1, a_1)
        r_2 = pythagorean_theorem(b_2, a_2)
        r_3 = r_1 * r_2
        theta_1 = sp.atan2(b_1, a_1)
        theta_2 = sp.atan2(b_2, a_2)
        c_1 = theta_1 + theta_2
        sin_1_ = sp.sin(c_1)
        cos_1 = sp.cos(c_1)
        b_r = sp.simplify(sin_1_ * r_3)
        a_r = sp.simplify(cos_1 * r_3)
        # get to an empty scene
        self.play(self.camera.frame.animate.shift(RIGHT * 15))

        # create the formula and adjust it
        d_moivre = MathTex(
            r"(a_1 + ib_1)",
            "(a_2 + ib_2)",
            "=",
            "r_1r_2",
            "(",
            r"cos(\theta_1 + \theta_2)",
            "+",
            r"isen(\theta_1 + \theta_2)",
            ")",
        ).move_to(RIGHT * 15)
        d_moivre.shift(UP * 3)

        original = MathTex(
            f"({sp.latex(a_1)} + i{sp.latex(b_1)})",
            f"({sp.latex(a_2)} + i{sp.latex(b_2)})",
            "=",
        ).move_to(RIGHT * 15)

        original.shift(UP * 3)
        original[0].set_color(YELLOW)
        original[1].set_color(BLUE)
        d_moivre_1 = MathTex(
            f"({sp.latex(r_1)})({sp.latex(r_2)})",
            "(",
            f"cos({sp.latex(theta_1)} + {sp.latex(theta_2)})",
            "+",
            f"isen({sp.latex(theta_1)} + {sp.latex(theta_2)})",
            ")",
        ).move_to(RIGHT * 15)
        d_moivre_1.shift(UP)
        d_moivre_2 = MathTex(
            f"{sp.latex(r_3)}",
            "(",
            f"cos({sp.latex(c_1)})",
            "+",
            f"isen({sp.latex(c_1)})",
            ")",
        ).move_to(RIGHT * 15)
        d_moivre_2.shift(UP)

        d_moivre_3 = MathTex(
            f"{sp.latex(r_3)}",
            "(",
            f"{sp.latex(cos_1)}",
            "+",
            f"{sp.latex(sin_1_)}",
            "i",
            ")",
        ).move_to(RIGHT * 15)
        d_moivre_3.shift(UP)
        d_moivre_4 = MathTex(f"{sp.latex(a_r)}", "+", f"{sp.latex(b_r)}", "i").move_to(
            RIGHT * 15
        )
        d_moivre_4.shift(UP)

        d_moivre_4.set_color(MORADO_ELECTRICO)

        self.play(Create(d_moivre))
        self.play(
            Transform(
                d_moivre, VGroup(original, d_moivre_1), run_time=2, rate_func=smooth
            )
        )
        self.wait(2)
        self.play(
            Transform(
                d_moivre, VGroup(original, d_moivre_2), run_time=2, rate_func=smooth
            )
        )
        self.wait()
        self.play(
            Transform(
                d_moivre, VGroup(original, d_moivre_3), run_time=2, rate_func=smooth
            )
        )
        self.wait()
        self.play(
            Transform(
                d_moivre, VGroup(original, d_moivre_4), run_time=2, rate_func=smooth
            )
        )
        self.wait()
        self.play(self.camera.frame.animate.shift(LEFT * 15))

        p1 = grid.c2p(float(a_1), float(b_1))
        p2 = grid.c2p(float(a_2), float(b_2))
        p3 = grid.c2p(float(a_r), float(b_r))

        result_dot = Dot(p3, color=MORADO_ELECTRICO).set_z_index(1)
        triang = Polygon(p1, p2, p3, color=AZUL_ELECTRICO)
        self.play(Create(triang))
        self.play(Create(result_dot))
        self.wait()
        self.play(FadeOut(triang))
        self.remove(d_moivre)

        self.wait()
        return ((float(a_r), float(b_r)), (result_dot.get_center()))

    def construct(self):
        self.camera.frame.shift(UP)

        # Crear ejes
        axes = Axes(
            x_range=[-7, 7, 1],  # [min, max, step]
            y_range=[-10, 10, 1],
            x_length=14,  # largo visual en pantalla
            y_length=20,
            axis_config={"color": WHITE, "include_numbers": False},
        )
        grid = NumberPlane(y_range=[-12, 12, 1])
        grid.set_opacity(0.8)
        grid.set_z_index(0)
        yellow_dot = Dot(grid.c2p(1, 1), color=YELLOW).set_z_index(1)
        green_dot = Dot(grid.c2p(3, 1), color=YELLOW).set_z_index(1)
        orange_dot = Dot(grid.c2p(2, 4), color=YELLOW).set_z_index(1)
        R_dot = Dot(grid.c2p(0.707106, 0.707106), color=AZUL_ELECTRICO).set_z_index(1)
        degrees = MathTex("45^\circ", font_size=36)

        # Animaciones
        self.play(FadeIn(yellow_dot, run_time=1))
        self.play(FadeIn(green_dot, run_time=1))
        self.play(FadeIn(orange_dot, run_time=1))
        self.play(Create(grid, run_time=3, lag_ratio=0.1))
        self.remove(VGroup(yellow_dot, green_dot, orange_dot))
        self.add(VGroup(yellow_dot, green_dot, orange_dot))
        self.play(Create(axes))
        tri = Polygon(
            yellow_dot.get_center(),
            green_dot.get_center(),
            orange_dot.get_center(),
            color=YELLOW,
        )
        self.play(Create(tri))
        self.play(tri.animate.set_fill(YELLOW, opacity=0.5))
        self.wait()
        self.play(FadeIn(R_dot, run_time=2))
        self.wait()
        a_value, x = self.multiply_imaginary(
            (1, 1), (1 / sp.sqrt(2), 1 / sp.sqrt(2)), grid=grid
        )
        b_value, y = self.multiply_imaginary(
            (3, 1), (1 / sp.sqrt(2), 1 / sp.sqrt(2)), grid=grid
        )
        c_value, z = self.multiply_imaginary(
            (2, 4), (1 / sp.sqrt(2), 1 / sp.sqrt(2)), grid=grid
        )
        last = Polygon(x, y, z, color=MORADO_ELECTRICO)
        self.play(Create(last))
        self.wait()
        self.play(last.animate.set_fill(MORADO_ELECTRICO, opacity=0.5))
        self.wait()
        aux = Polygon(R_dot.get_center(), tri.get_center(), last.get_center())
        line = Polygon(R_dot.get_center(), last.get_center(), color=ROJO_ELECTRICO)
        line_2 = Polygon(R_dot.get_center(), tri.get_center(), color=ROJO_ELECTRICO)
        self.play(Create(line))
        self.play(Create(line_2))
        degrees.move_to(aux.get_center())
        degrees.set_color(ROJO_ELECTRICO).set_opacity(0.8)
        self.play(Write(degrees))
        self.wait()

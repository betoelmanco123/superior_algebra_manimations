from manim import *
from fractions import Fraction


def text_to_fraction(tex_string):

    if isinstance(tex_string, (int, float)):
        return Fraction(tex_string).limit_denominator()

    if isinstance(tex_string, Fraction):
        return tex_string

    tex_string = str(tex_string).strip()

    tex_string = tex_string.replace(r"\cdot", "").replace("(", "").replace(")", "")

    if r"\frac" in tex_string:

        parts = tex_string.replace(r"\frac{", "").replace("}", "").split("{")
        if len(parts) >= 2:
            try:
                numerator = float(parts[0])
                denominator = float(parts[1])
                return Fraction(numerator / denominator).limit_denominator()
            except:
                pass

    if "/" in tex_string:
        a, b = tex_string.split("/")
        return Fraction(int(a), int(b))
    try:
        return Fraction(float(tex_string)).limit_denominator()
    except:
        print("The error is", type(tex_string))
        return Fraction(0)


def fraction_to_tex(val):

    val = Fraction(val).limit_denominator()
    if val.denominator == 1:
        return str(val.numerator)

    if val < 0:
        return r"-\frac{" + str(abs(val.numerator)) + "}{" + str(val.denominator) + "}"
    return r"\frac{" + str(val.numerator) + "}{" + str(val.denominator) + "}"


class Inversa(Scene):

    def Adder_row(self, donor, recipient, factor, A, I):

        """
        Docstring for Adder_row
        this method animates the sum of one row to another one icluding a factor
        
        :param self: self xd
        :param donor: the row that gets multiplied and sumed to another row
        :param recipient: the row that gets sumed with the donor row
        :param factor: the factor that multiplies the donor
        :param A: the left matrix
        :param I: the right matrix
        """
        for i in range(3):
            A.get_rows()[recipient][i].set_color("blue")
            I.get_rows()[recipient][i].set_color("blue")
            A.get_rows()[donor][i].set_color("red")
            I.get_rows()[donor][i].set_color("red")

        # convert the factor to a Fraction
        factor = text_to_fraction(factor)

        # Create a list with the multiplyed row donor of A
        donor_values = []
        donor_row = A.get_rows()[donor]
        for element in donor_row:
            donor_values.append(element.tex_string)

        new_values = [factor * text_to_fraction(x) for x in donor_values]

        # Create a list with the values of row recipient of I
        getter_values = []
        getter_row = I.get_rows()[recipient]
        for element in getter_row:
            getter_values.append(element.tex_string)

        # create a list with the multiplied of Row donor of I
        sender_values = []
        sender_row = I.get_rows()[donor]
        for element in sender_row:
            sender_values.append(element.tex_string)
        obtained_values = [factor * text_to_fraction(x) for x in sender_values]

        # create e list with the sum that correspond to the I operations
        resultant_values = [
            text_to_fraction(obtained_values[i]) + text_to_fraction(getter_values[i])
            for i in range(3)
        ]

        # result of A
        recipient_values = []
        recipient_row = A.get_rows()[recipient]
        for element in recipient_row:
            recipient_values.append(element.tex_string)

        worked_values = [
            text_to_fraction(new_values[i]) + text_to_fraction(recipient_values[i])
            for i in range(len(new_values))
        ]
        values = MathTex("(", str(factor), ") ", "=")

        # A matrix
        matrix_donor = Matrix([donor_values])
        matrix_new_values = Matrix([new_values])
        for i in range(3):
            matrix_donor.get_entries()[i].set_color("red")
            matrix_new_values.get_entries()[i].set_color("blue")

        # R matrix
        as_list = [
            [text_to_fraction(elem.tex_string) for elem in row] for row in A.get_rows()
        ]
        for i in range(3):
            as_list[recipient][i] = worked_values[i]
        resultant_A = Matrix(as_list).move_to(A.get_center())

        # RI matri
        the_list = [
            [text_to_fraction(elem.tex_string) for elem in row] for row in I.get_rows()
        ]
        for i in range(3):
            the_list[recipient][i] = resultant_values[i]
        correct_identity = Matrix(the_list).move_to(I.get_center())

        matrix_donor.next_to(A, UP, buff=1)
        matrix_donor.shift(LEFT)
        values.next_to(matrix_donor, RIGHT, buff=0.3)
        matrix_new_values.next_to(values, RIGHT, buff=0.3)

        initial_position = matrix_donor.get_center()

        matrix_donor.move_to(A.get_rows()[donor])

        self.play(matrix_donor.animate.move_to(initial_position))

        self.play(Write(values))
        self.play(Write(matrix_new_values))
        for b in A.get_brackets():
            self.remove(b)
            self.remove(b)
        for b in resultant_A.get_brackets():
            self.add(b)
        for b in I.get_brackets():
            self.remove(b)
            self.remove(b)
        for b in correct_identity.get_brackets():
            self.add(b)
        # identity Matrix
        sender = Matrix([sender_values])
        obtanined = Matrix([obtained_values])
        sender.move_to(I.get_rows()[donor])
        for i in range(3):
            for j in range(3):
                if j == i and resultant_A.get_rows()[i][j].tex_string == "1":
                    resultant_A.get_rows()[i][j].set_color("yellow")
                elif resultant_A.get_rows()[i][j].tex_string == "0":
                    resultant_A.get_rows()[i][j].set_color("yellow")

        
        for i in range(3):

            # The place selected to write
            destino = A.get_rows()[recipient][i]

            # positoin of the destiny
            pos_destino = destino.get_center()
            new_pos = resultant_A.get_rows()[recipient][i].get_center()

            # create the copy that is going to move
            fantasma = matrix_new_values[0][i].copy()
            fantasma.move_to(matrix_new_values[0][i])
            # draw the copy without animations
            self.add(fantasma)

            # move the copy to the destiny with animation
            self.play(fantasma.animate.move_to(pos_destino))

            # change the content of the selected positon
            destino.become(MathTex(fraction_to_tex(worked_values[i])))

            # change the position and the color

            destino.move_to(new_pos)
            destino.set_color(GREEN)

            # delete the copy
            self.remove(fantasma)
        # colorate the values that correspond with the identity
        for i in range(3):
            for j in range(3):
                if j == i and resultant_A.get_rows()[i][j].tex_string == "1":
                    resultant_A.get_rows()[i][j].set_color("yellow")
                elif resultant_A.get_rows()[i][j].tex_string == "0":
                    resultant_A.get_rows()[i][j].set_color("yellow")

        self.wait()
        # delete the aux matrices
        self.play(FadeOut(VGroup(matrix_new_values, values[-1], matrix_donor)))

        # colorate the values we want to work on
        for i in range(3):
            I.get_rows()[recipient][i].set_color("blue")
            I.get_rows()[donor][i].set_color("red")

        for i in range(3):
            sender.get_entries()[i].set_color("red")
            obtanined.get_entries()[i].set_color("blue")

        # config our work material and draw it
        self.play(sender.animate.move_to(initial_position))
        self.play(Write(values[-1]))
        obtanined.next_to(values, RIGHT)
        self.play(Write(obtanined))
        for i in range(3):  # columnas 0,1,2

            # the target
            destino = I.get_rows()[recipient][i]

            # the target position
            pos_destino = destino.get_center()

            # the future position
            new_pos = correct_identity.get_rows()[recipient][i].get_center()

            # create a copy of the value
            fantasma = obtanined[0][i - 3].copy()

            # move the copy to where it belongs
            fantasma.move_to(obtanined[0][i - 3])  # empieza donde está arriba
            self.add(fantasma)

            # move the copy to the destiny with animation
            self.play(fantasma.animate.move_to(pos_destino))

            # change the content of the matrix with animation
            destino.become(MathTex(fraction_to_tex(resultant_values[i])))

            # move the value to the new postion and change the color
            destino.move_to(new_pos)
            destino.set_color(GREEN)
            # delete the copy
            self.remove(fantasma)
        # delete the work
        self.play(FadeOut(VGroup(obtanined, values, sender)))
        self.wait()

        # create the new data and delete the older one
        self.add(resultant_A)
        for e in A.get_entries():
            self.remove(e)
        for b in A.get_brackets():
            self.remove(b)

        self.add(correct_identity)
        for e in I.get_entries():
            self.remove(e)
        for b in I.get_brackets():
            self.remove(b)
        self.wait()
        return resultant_A, correct_identity

    def scalar_timer(self, target, factor, A, I):
        """
        Docstring for scalar_timer
        this method animates the multiplication of a row with an scalar
        :param self: self xd
        :param target: the row to multiply by an scalar
        :param factor: the factor to multiply the row
        :param A: the original left matrix
        :param I: the original rigth matrix
        """
        factor = text_to_fraction(factor)
        values = MathTex("(", str(factor), ")=")

        target_values = A.get_rows()[target]
        results = []
        donor = []
        for element in target_values:
            results.append(text_to_fraction(element.tex_string) * factor)
            donor.append(text_to_fraction(element.tex_string))

        target_identity = I.get_rows()[target]
        results_identity = []
        donor_identity = []
        for element in target_identity:
            results_identity.append(text_to_fraction(element.tex_string) * factor)
            donor_identity.append(text_to_fraction(element.tex_string))

        resultados = Matrix([results])
        donante = Matrix([donor]).next_to(A, UP, buff=1)
        values.next_to(donante, RIGHT, buff=0.3)
        resultados.next_to(values, RIGHT, buff=0.3)

        resultados_identity = Matrix([results_identity])
        donante_identity = Matrix([donor_identity])
        resultados_identity.next_to(values, RIGHT, buff=0.3)

        initial_position = donante.get_center()

        donante.move_to(VGroup(A.get_rows()[target]))

        the_list = [
            [text_to_fraction(elem.tex_string) for elem in row] for row in A.get_rows()
        ]
        for i in range(3):
            the_list[target][i] = results[i]
        correct_A = Matrix(the_list).move_to(A.get_center())
        for i in range(3):

            A.get_rows()[target][i].set_color("blue")
            I.get_rows()[target][i].set_color("blue")
            donante.get_entries()[i].set_color("blue")
            donante_identity.get_entries()[i].set_color("blue")
            resultados.get_entries()[i].set_color("green")
            resultados_identity.get_entries()[i].set_color("green")

        self.play(donante.animate.move_to(initial_position))
        self.play(Write(VGroup(values, resultados)))

        for i in range(3):  # columnas 0,1,2

            # the destiny
            destino = A.get_rows()[target][i]

            # current position
            pos_destino = destino.get_center()

            # future positon
            new_pos = correct_A.get_rows()[target][i].get_center()

            # create a copy
            fantasma = resultados[0][i].copy()
            fantasma.move_to(resultados[0][i])

            # draw the copy without animation
            self.add(fantasma)

            # move the copy the the new postion with animation
            self.play(fantasma.animate.move_to(pos_destino))

            # modify the content of the value
            destino.become(MathTex(fraction_to_tex(results[i])))

            # move to the new postion and set the color to green
            destino.move_to(new_pos)
            destino.set_color("green")

            # stop drawing the copy
            self.remove(fantasma)
        # delete the work values
        self.play(FadeOut(VGroup(resultados, values, donante)))

        donante_identity.move_to(I.get_rows()[target])
        the_list_identity = [
            [text_to_fraction(elem.tex_string) for elem in row] for row in I.get_rows()
        ]
        for i in range(3):
            the_list_identity[target][i] = results_identity[i]
        correct_I = Matrix(the_list_identity).move_to(I.get_center())

        self.play(donante_identity.animate.move_to(initial_position))
        self.play(Write(VGroup(values, resultados_identity)))

        for i in range(3):  # columnas 0,1,2

            # destiny
            destino = I.get_rows()[target][i]

            # current position
            pos_destino = destino.get_center()
            new_pos = correct_I.get_rows()[target][i].get_center()

            # create a copy
            fantasma = resultados_identity[0][i].copy()
            fantasma.move_to(resultados_identity[0][i])  # empieza donde está arriba
            self.add(fantasma)

            # animate the copy to the new postion
            self.play(fantasma.animate.move_to(pos_destino))

            # trasnform the content to the objective
            destino.become(MathTex(fraction_to_tex(results_identity[i])))
            destino.set_color(GREEN)
            
            destino.move_to(new_pos)  

            # delete the copy
            self.remove(fantasma)
        
        # delete the workplace
        self.play(FadeOut(VGroup(resultados_identity, values, donante_identity)))

        # delete the old values and draw the new ones
        self.add(correct_A)
        for e in A.get_entries():
            self.remove(e)
        for b in A.get_brackets():
            self.remove(b)
        self.wait()
        self.add(correct_I)
        for e in I.get_entries():
            self.remove(e)
        for b in I.get_brackets():
            self.remove(b)
        self.wait()
        return correct_A, correct_I

    def multiply_matrices(self, A, B):
        """
        This method animates the multilication of two 
        valid matrices
        """
        #TODO
        ...
    def construct(self):
 
        # def the initial matrix A and identity
        A = Matrix(
            [
                [1, 2, 3],
                [4, 5, 7],
                [8, 9, 12],
            ]
        )
        I = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]).move_to(RIGHT * 2)

        # def the label for
        label = MathTex("A", "=")
        group = VGroup(label, A).arrange(RIGHT, buff=0.1)

        group.move_to(LEFT * 3)

        # create a workplace of matrices operatios}
        temp = Matrix(
            [
                [1, 2, 3],
            ]
        )

        temp_result = Matrix([[-4, -8, -12]])
        values = MathTex("*(", "-4", ")=")
        temp.next_to(A, UP, buff=1)
        values.next_to(temp, RIGHT, buff=0.3)
        temp_result.next_to(values, RIGHT, buff=0.3)
        A.next_to(I, LEFT, buff=0.5)
        self.play(Write(group))
        self.play(Write(I))

        A, I = self.Adder_row(0, 1, -4, A, I)

        A, I = self.Adder_row(donor=0, recipient=2, factor=-8, A=A, I=I)

        A, I = self.Adder_row(donor=1, recipient=2, factor=Fraction(-7, 3), A=A, I=I)

        A, I = self.scalar_timer(target=2, factor=-3, A=A, I=I)

        A, I = self.Adder_row(donor=2, recipient=0, factor=-3, A=A, I=I)

        A, I = self.Adder_row(donor=2, recipient=1, factor=5, A=A, I=I)

        A, I = self.scalar_timer(target=1, factor=Fraction(-1, 3), A=A, I=I)

        A, I = self.Adder_row(donor=1, recipient=0, factor=-2, A=A, I=I)

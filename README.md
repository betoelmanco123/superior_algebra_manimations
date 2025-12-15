# Superior Algebra Manimations

This project contains mathematical animations created with **Manim (Community Edition)**.

You can install Manim by following the official documentation:
[https://www.manim.community](https://www.manim.community)

---

## Requirements

* Python 3.9+
* Manim Community Edition
* A working LaTeX installation

Make sure Manim is correctly installed and available in your terminal before proceeding.

---

## Rendering the Matrix Inverse Animation

1. Clone this repository into a directory where Manim is installed.
2. Open a terminal inside the project folder.
3. Run the following command:

```bash
manim -pqh inversa.py Inversa
```

This command renders the **Inversa** scene defined in `inversa.py` using high quality settings.

You can also watch the result on this youtube video [https://youtu.be/qcmfL3yRyh4](https://youtu.be/qcmfL3yRyh4)

---

## Rendering the Rotation (Rotador) Animation

From the project directory, run:

```bash
manim -pqh rotador.py PlanoCartesiano
```

This renders the **PlanoCartesiano** scene from `rotador.py`.

You can also watch the result on this youtube video [https://youtu.be/FmPjUM-k8BU](https://youtu.be/FmPjUM-k8BU)


---

## Notes

* You can replace `-pqh` with other quality flags (`-pql`, `-pqm`) depending on your needs.
* Scene names are case-sensitive.
* If rendering fails, verify that LaTeX is properly installed and that Manim runs correctly with a simple test scene.

---

Feel free to modify the scenes or reuse the code for your own algebra animations.

from manim import *
import numpy as np


class Fourier3DDecomposition(ThreeDScene):

    def construct(self):
        # ==========================================
        # Configurações Globais e Títulos
        # ==========================================
        title = Text(
            "Decomposição de Fourier em 3D", font_size=40, color=WHITE
        ).to_edge(UP)
        self.play(FadeIn(title))
        self.wait(0.5)

        # ==========================================
        # 1. GRÁFICO 2D DO SINAL COMPLEXO NO DOMÍNIO DO TEMPO
        # ==========================================
        time_axes_2d = Axes(
            x_range=[0, 3, 0.5],
            y_range=[-4, 4, 2],
            x_length=10,
            y_length=4,
            axis_config={"color": BLUE_C},
            x_axis_config={"numbers_to_include": np.arange(0, 3.1, 0.5)},
            y_axis_config={"numbers_to_include": np.arange(-4, 4.1, 2)},
        ).to_edge(UP, buff=1.2)
        time_axes_2d.add_coordinates()

        time_label_2d = Text("Sinal Complexo (2D)", font_size=32, color=BLUE_B).next_to(
            time_axes_2d, UP, buff=0.2
        )
        time_axis_labels_2d = time_axes_2d.get_axis_labels(
            x_label=Text("Tempo (s)", font_size=24),
            y_label=Text("Amplitude", font_size=24),
        )

        freqs_amps = [
            (1, 1.0),
            (2, 0.7),
            (3, 0.5),
            (4, 0.9),
            (5, 0.4),
            (6, 0.3),
            (7, 0.6),
            (8, 0.2),
            (9, 0.5),
            (10, 0.3),
        ]

        def complex_wave_func(t):
            return sum(amp * np.sin(2 * PI * freq * t) for freq, amp in freqs_amps)

        complex_wave_2d = time_axes_2d.plot(complex_wave_func, color=YELLOW_C)

        self.play(
            FadeIn(time_label_2d),
            Create(time_axes_2d),
            Create(time_axis_labels_2d),
            run_time=1.5,
        )
        self.play(Create(complex_wave_2d), run_time=2.5, rate_func=smooth)
        self.wait(1)

        # ==========================================
        # 2. TRANSIÇÃO PARA 3D E DECOMPOSIÇÃO
        # ==========================================
        self.play(
            FadeOut(time_label_2d),
            FadeOut(time_axis_labels_2d),
            FadeOut(complex_wave_2d),
            FadeOut(time_axes_2d),
            run_time=1.5,
        )

        # Configurar a cena 3D
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # Eixos 3D: X=Tempo, Y=Frequência, Z=Amplitude
        axes_3d = ThreeDAxes(
            x_range=[0, 3, 0.5],
            y_range=[
                0,
                len(freqs_amps) + 1,
                1,
            ],  # Y-axis para as frequências individuais
            z_range=[-2, 2, 1],  # Amplitude
            x_length=8,
            y_length=5,
            z_length=4,
            axis_config={
                "stroke_width": 2,
                "include_numbers": True,
                "include_ticks": True,
            },
        )
        axes_3d.set_color(WHITE)

        # Rótulos dos eixos 3D
        x_label_3d = Text("Tempo (s)", font_size=20, color=RED).next_to(
            axes_3d.x_axis, DOWN
        )
        y_label_3d = Text("Frequência (índice)", font_size=20, color=GREEN).next_to(
            axes_3d.y_axis, LEFT
        )
        z_label_3d = Text("Amplitude", font_size=20, color=BLUE).next_to(
            axes_3d.z_axis, OUT
        )

        self.play(
            Create(axes_3d), FadeIn(x_label_3d), FadeIn(y_label_3d), FadeIn(z_label_3d)
        )
        self.wait(0.5)

        # Plotar cada sinal simples ao longo do eixo Y
        simple_waves_3d = VGroup()
        for i, (freq, amp) in enumerate(freqs_amps):
            # Função para o sinal simples (seno) no domínio do tempo
            def simple_wave_func(t):
                return amp * np.sin(2 * PI * freq * t)

            # Criar o gráfico 3D para cada onda simples
            # O eixo Y (frequência) será o índice `i`
            simple_wave_3d = ParametricFunction(
                lambda t: axes_3d.c2p(
                    t, i + 0.5, simple_wave_func(t)
                ),  # +0.5 para centralizar no tick
                t_range=[0, 3],
                color=self.get_color_for_frequency(freq),
                stroke_width=3,
            )
            simple_waves_3d.add(simple_wave_3d)

        self.play(Create(simple_waves_3d), run_time=5, lag_ratio=0.1)
        self.wait(2)

        # Opcional: Mostrar a soma dos sinais simples formando o sinal complexo original
        # Isso pode ser feito projetando a soma de volta para o plano XZ (Y=0)
        # ou mostrando uma linha que conecta os picos de cada onda simples.
        # Por simplicidade, vamos apenas mostrar o sinal complexo original como uma projeção.

        # Criar o sinal complexo no plano XZ (y=0) do sistema 3D
        complex_wave_3d_projection = ParametricFunction(
            lambda t: axes_3d.c2p(t, 0, complex_wave_func(t)),
            t_range=[0, 3],
            color=YELLOW_C,
            stroke_width=5,
        )

        self.play(Create(complex_wave_3d_projection), run_time=2)
        self.wait(2)

        self.play(
            FadeOut(title),
            FadeOut(axes_3d),
            FadeOut(x_label_3d),
            FadeOut(y_label_3d),
            FadeOut(z_label_3d),
            FadeOut(simple_waves_3d),
            FadeOut(complex_wave_3d_projection),
            run_time=1.5,
        )
        self.wait(1)

    def get_color_for_frequency(self, freq):
        # Mapeia a frequência para uma cor, para visualização
        # Usaremos um gradiente de cores para as diferentes frequências
        # Exemplo: de azul para verde, depois para vermelho
        if freq <= 3:
            return interpolate_color(BLUE_D, GREEN_D, freq / 3)
        elif freq <= 7:
            return interpolate_color(GREEN_D, ORANGE, (freq - 3) / 4)
        else:
            return interpolate_color(ORANGE, RED_D, (freq - 7) / 3)

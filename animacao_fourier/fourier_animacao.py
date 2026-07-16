from manim import *
import numpy as np


class FourierTransformDemo(Scene):
    def construct(self):
        # ==========================================
        # 1. GRÁFICO DO DOMÍNIO DO TEMPO
        # ==========================================
        # Gráfico movido mais para cima (buff ajustado para 0.8)
        time_axes = Axes(
            x_range=[0, 3, 0.5],
            y_range=[-4, 4, 2],
            x_length=9,
            y_length=2.2,
            axis_config={"color": BLUE_C},
        ).to_edge(UP, buff=0.8)

        time_label = Text("Domínio do Tempo", font_size=28, color=BLUE_B).next_to(
            time_axes, UP, buff=0.15
        )
        time_axis_labels = time_axes.get_axis_labels(
            x_label=Text("Tempo (s)", font_size=20),
            y_label=Text("Amplitude", font_size=20),
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

        complex_wave = time_axes.plot(complex_wave_func, color=YELLOW_C)

        # ==========================================
        # 2. INFORMATIVO DE TRANSIÇÃO (MEIO DA TELA)
        # ==========================================
        transition_text = Text("Transformada de Fourier", font_size=28, color=WHITE)
        arrow = Arrow(start=UP, end=DOWN, color=WHITE, buff=0.1).scale(0.5)

        transition_group = (
            VGroup(transition_text, arrow).arrange(DOWN, buff=0.1).move_to(ORIGIN)
        )

        # ==========================================
        # 3. GRÁFICO DO DOMÍNIO DA FREQUÊNCIA
        # ==========================================
        freq_axes = Axes(
            x_range=[0, 11, 1],
            y_range=[0, 1.5, 0.5],
            x_length=9,
            y_length=2.2,
            axis_config={"color": RED_C},
        ).to_edge(DOWN, buff=0.3)

        freq_label = Text("Domínio da Frequência", font_size=28, color=RED_B).next_to(
            freq_axes, UP, buff=0.15
        )
        freq_axis_labels = freq_axes.get_axis_labels(
            x_label=Text("Frequência (Hz)", font_size=20),
            y_label=Text("Amplitude", font_size=20),
        )

        # ==========================================
        # 4. OS PICOS DA TRANSFORMADA
        # ==========================================
        spikes_group = VGroup()

        for freq, amp in freqs_amps:
            spike = Line(
                start=freq_axes.c2p(freq, 0),
                end=freq_axes.c2p(freq, amp),
                color=YELLOW_E,
                stroke_width=6,
            )
            dot = Dot(freq_axes.c2p(freq, amp), color=YELLOW_E, radius=0.08)
            spikes_group.add(spike, dot)

        # ==========================================
        # 5. ROTEIRO DA ANIMAÇÃO
        # ==========================================
        # 5.1 Aparece o tempo
        self.play(
            FadeIn(time_label),
            Create(time_axes),
            Create(time_axis_labels),
            run_time=1.5,
        )
        self.play(Create(complex_wave), run_time=2, rate_func=smooth)
        self.wait(1)

        # 5.2 Aparece a transição no centro
        self.play(
            FadeIn(transition_group),
            run_time=0.5,
        )
        self.wait(0.5)

        # 5.3 Aparece a frequência
        self.play(
            FadeIn(freq_label),
            Create(freq_axes),
            Create(freq_axis_labels),
            run_time=1.5,
        )
        self.wait(0.5)

        # 5.4 A Mágica: Transforma a CÓPIA da onda nos picos, deixando a original no topo
        self.play(
            TransformFromCopy(complex_wave, spikes_group),
            run_time=2,
            rate_func=smooth,
        )
        self.wait(3)

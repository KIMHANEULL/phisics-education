"""소음 제거 기술 (교과서 119쪽, 그림 III-22, III-23).

소음 제거 이어폰: ① 외부 마이크가 소음 감지 ② 진폭·파장 같고 위상 반대인 소리 ③ 상쇄 간섭 →
음악만 들린다 → 비행기 객실 → 자동차 배기관·실내 → 상쇄는 줄이고 보강은 키운다 → 한 줄 정리.
"""
from ikit import *

A_N = 0.42
LN = 1.6
KN = 2 * np.pi / LN


def noise_shape(ph):
    return (np.sin(ph) + 0.5 * np.sin(2 * ph + 0.6) + 0.3 * np.sin(3 * ph + 1.1)) / 1.45


def ear_shape(h=2.6, color="#E8C9A8"):
    outer = VMobject(stroke_color=color, stroke_width=6)
    pts = [[0.0, -0.25, 0], [-0.12, -0.05, 0], [-0.14, 0.18, 0], [0.0, 0.32, 0], [0.16, 0.25, 0],
           [0.2, 0.05, 0], [0.1, -0.08, 0], [0.08, -0.22, 0], [0.0, -0.25, 0]]
    outer.set_points_smoothly([np.array(p) for p in pts])
    outer.set_fill(color, 0.22)
    inner = Arc(radius=0.08, start_angle=PI * 0.9, angle=-PI * 1.2, arc_center=[0.02, 0.12, 0],
                stroke_color=color, stroke_width=4)
    canal = Dot([0.04, 0.06, 0], radius=0.025, color="#5A4636")
    g = VGroup(outer, inner, canal)
    s = h / g.height
    g.scale(s, about_point=ORIGIN)
    g.canal = canal
    return g


def car(w=3.2):
    body = Polygon([-1.6, 0.2, 0], [-1.6, 0.62, 0], [-0.9, 0.66, 0], [-0.5, 1.05, 0], [0.55, 1.05, 0],
                   [1.0, 0.66, 0], [1.6, 0.58, 0], [1.6, 0.2, 0], stroke_color="#D7DEE6", stroke_width=2,
                   fill_color="#3B5878", fill_opacity=1)
    win = Polygon([-0.4, 0.68, 0], [-0.4, 0.98, 0], [0.5, 0.98, 0], [0.85, 0.68, 0], stroke_width=0,
                  fill_color="#7FB8E0", fill_opacity=0.9)
    wh = VGroup(*[Circle(radius=0.22, stroke_color="#9AA5B1", stroke_width=3, fill_color="#20262E",
                         fill_opacity=1).move_to([x, 0.2, 0]) for x in (-0.95, 0.95)])
    pipe = Rectangle(width=0.3, height=0.09, stroke_width=0, fill_color="#9AA5B1",
                     fill_opacity=1).move_to([-1.72, 0.27, 0])
    g = VGroup(body, win, wh, pipe)
    g.scale(w / 3.2, about_point=ORIGIN)
    g.pipe = pipe
    return g


class E3NoiseCancel(CaseScene):
    def construct(self):
        self.intro()
        self.earphone()
        self.airplane()
        self.car_beat()
        self.contrast()
        self.wrap()

    def intro(self):
        card = title_card("소음 제거 기술")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(card), run_time=0.6)

    # ------------------------------------------------------------ 1. 소음 제거 이어폰
    def earphone(self):
        tt = time_driver(self)
        sa = ValueTracker(1.0)      # 합성파에 남는 비율
        X0, X1 = -1.2, 5.8
        Y1, Y2, YS = 1.9, 0.45, -1.05

        ear = ear_shape(2.8).move_to([-4.8, 0.5, 0])
        cp = ear.canal.get_center()
        bud = VGroup(
            RoundedRectangle(corner_radius=0.12, width=0.32, height=0.9, stroke_width=0,
                             fill_color="#F2F5F8", fill_opacity=1).move_to(cp + RIGHT * 0.12 + DOWN * 0.55),
            Circle(radius=0.3, stroke_color=WHITE_T, stroke_width=2, fill_color="#F2F5F8",
                   fill_opacity=1).move_to(cp),
        )
        mic = Dot(cp + RIGHT * 0.3 + UP * 0.05, radius=0.07, color=ORANGE)
        micl = callout(mic.get_center(), "외부 마이크", None, direction=UR, length=0.9)

        def nf(x):
            return A_N * noise_shape(KN * (x + V * tt.get_value()))

        wn = always_redraw(lambda: wave_line(nf, X0, X1, Y1, C_NOISE))
        wo = ValueTracker(1.0)      # 반대 위상 소리를 켜고 끄는 비율
        wa = always_redraw(lambda: wave_line(lambda x: -nf(x) * wo.get_value(), X0, X1, Y2, C_ANTI))
        ws = always_redraw(lambda: wave_line(lambda x: nf(x) * sa.get_value(), X0, X1, YS, C_SUM, 5))
        ax = VGroup(*[Line([X0, y, 0], [X1, y, 0], color=GRAY_T, stroke_width=1.2, stroke_opacity=0.45)
                      for y in (Y1, Y2, YS)])
        ln = T("소음", 22, C_NOISE, bold=True).next_to([X0, Y1, 0], UP, buff=0.5).align_to([X0, 0, 0], LEFT)
        la = T("반대 위상 소리", 22, C_ANTI, bold=True).next_to([X0, Y2, 0], UP, buff=0.5).align_to([X0, 0, 0], LEFT)
        ls = T("합성파 (귀에 들어가는 소리)", 22, C_SUM, bold=True).next_to([X0, YS, 0], UP, buff=0.5).align_to(
            [X0, 0, 0], LEFT)
        arrow = Arrow([X0 + 1.6, Y1 + 0.75, 0], [X0 + 0.6, Y1 + 0.75, 0], buff=0, color=C_NOISE,
                      stroke_width=3, max_tip_length_to_length_ratio=0.25).next_to(ln, RIGHT, buff=0.3)

        self.play(FadeIn(ear), FadeIn(bud), run_time=0.6)
        self.add(ax[0], wn)
        self.play(FadeIn(ln), FadeIn(arrow), run_time=0.4)
        self.say("소음 제거 이어폰: 밖에서 소음이 들어온다", wait=1.2)
        b = badge("소음", C_NOISE).move_to([5.3, 3.35, 0])
        self.add(b)
        self.add_sound(hum(2.0))
        self.play(wiggle_icon(b, 2.0))
        self.remove(b)

        step = tag("① 외부 마이크가 소음을 감지", ORANGE, 24).to_edge(UP, buff=0.3)
        self.play(FadeIn(step), FadeIn(mic), FadeIn(micl), run_time=0.5)
        self.play(Flash(mic, color=ORANGE, line_length=0.18, num_lines=10), run_time=0.8)
        self.say("① 외부 마이크가 소음(파동)을 감지")

        step2 = tag("② 진폭·파장은 같고, 위상은 반대인 소리", C_ANTI, 24).to_edge(UP, buff=0.3)
        self.play(FadeOut(step), FadeIn(step2), FadeIn(ax[1]), FadeIn(wa), FadeIn(la), run_time=0.7)
        self.say("② 소음과 진폭·파장은 같고\n위상은 반대인 음파를 만든다")
        guide = DashedLine([1.0, Y1 + 0.7, 0], [1.0, Y2 - 0.7, 0], color=WHITE_T, stroke_width=2,
                           dash_length=0.08)
        self.say("소음의 마루 ↔ 반대 소리의 골", wait=0)
        tt.rate = 0.0       # 잠깐 멈춰서 마루·골 비교
        x_c = 1.0
        self.play(Create(guide), run_time=0.5)
        self.wait(2.4)
        self.play(FadeOut(guide), run_time=0.3)
        tt.rate = 1.0

        step3 = tag("③ 상쇄 간섭 → 소음이 사라진다", C_SUM, 24).to_edge(UP, buff=0.3)
        self.play(FadeOut(step2), FadeIn(step3), FadeIn(ax[2]), FadeIn(ws), FadeIn(ls), run_time=0.6)
        self.say("③ 둘이 만나면 상쇄 간섭", wait=1.6)
        b = badge("반대 위상 소리를 더하면", C_SUM).move_to([4.2, 3.35, 0])
        b.move_to([0, 0, 0]).to_corner(UR, buff=0.25)
        self.play(FadeOut(step3), FadeIn(b), run_time=0.3)
        self.add_sound(hum(2.0, quiet=0.1))
        self.play(sa.animate.set_value(0.0), wiggle_icon(b, 0.7), run_time=0.7)
        self.play(wiggle_icon(b, 1.3))
        self.remove(b)
        self.say("소음이 거의 사라진다!")

        # 다시 비교: 소음만 ↔ 반대 위상을 더하면
        self.say("한 번 더 비교해 보자", wait=1.2)
        b1 = badge("소음", C_NOISE).to_corner(UR, buff=0.25)
        b2 = badge("반대 위상 소리를 더하면", C_SUM).to_corner(UR, buff=0.25)
        self.add(b1)
        self.add_sound(hum(1.8))
        self.play(sa.animate.set_value(1.0), wo.animate.set_value(0.0), wiggle_icon(b1, 0.5), run_time=0.5)
        self.play(wiggle_icon(b1, 1.3))
        self.remove(b1)
        self.add(b2)
        self.add_sound(hum(1.8, quiet=0.1))
        self.play(sa.animate.set_value(0.0), wo.animate.set_value(1.0), wiggle_icon(b2, 0.5), run_time=0.5)
        self.play(wiggle_icon(b2, 1.3))
        self.remove(b2)
        self.wait(0.6)

        notes = VGroup(*[T(c, 34, GREEN, bold=True) for c in ("♪", "♫", "♪")])
        for i, n in enumerate(notes):
            n.move_to(cp + LEFT * (0.9 + 0.5 * i) + UP * (0.9 + 0.35 * (i % 2)))
        bm = badge("음악", GREEN).to_corner(UR, buff=0.25)
        self.add(bm)
        mel = [(523, 0.0), (659, 0.4), (784, 0.8), (1047, 1.2)]
        for f, off in mel:
            self.add_sound(tone(f, 0.38, vol=0.3), time_offset=off)
        self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.3) for n in notes], lag_ratio=0.3),
                  wiggle_icon(bm, 1.7), run_time=1.7)
        self.remove(bm)
        self.say("그래서 음악만 깨끗하게 들린다")
        tt.clear_updaters()
        self.clear_all()

    # ------------------------------------------------------------ 2. 비행기 객실
    def airplane(self):
        tt = time_driver(self)
        q = ValueTracker(1.0)        # 객실 안 소음 남는 비율
        ra = ValueTracker(0.0)       # 반대 위상 소리 세기
        C = np.array([-1.6, 0.45, 0])
        R = 2.0
        hull = Circle(radius=R, arc_center=C, stroke_color="#D7DEE6", stroke_width=5, fill_color="#1A2738",
                      fill_opacity=1)
        floor = Line(C + np.array([-1.75, -0.95, 0]), C + np.array([1.75, -0.95, 0]), color=GRAY_T,
                     stroke_width=3)
        pax = VGroup(*[person(1.0).move_to(C + np.array([x, -0.95, 0]), aligned_edge=DOWN) for x in (-0.8, 0.4)])
        wing = Polygon(C + np.array([1.7, -0.75, 0]), C + np.array([5.6, -0.4, 0]), C + np.array([5.6, -0.6, 0]),
                       C + np.array([1.8, -1.05, 0]), stroke_color="#D7DEE6", stroke_width=2,
                       fill_color="#2E425A", fill_opacity=1)
        E = C + np.array([4.2, -1.25, 0])
        eng = Ellipse(width=1.3, height=0.62, stroke_color="#D7DEE6", stroke_width=2, fill_color="#3B5878",
                      fill_opacity=1).move_to(E)
        engl = label_bg(T("엔진", 22, WHITE_T, bold=True)).next_to(eng, DOWN, buff=0.12)
        wall = C + np.array([R * np.cos(-0.2), R * np.sin(-0.2), 0])
        mic = Dot(wall + LEFT * 0.12, radius=0.08, color=ORANGE)
        SP = C + np.array([1.2, 0.85, 0])
        spk = speaker_icon(C_ANTI, 0.4).rotate(PI).move_to(SP)
        view = tag("비행기 객실 단면", GRAY_T, 20).to_corner(UL, buff=0.3)

        def waves():
            g = VGroup()
            t = tt.get_value()
            for k in range(int(t / 0.6) + 1):
                r = 0.35 + V * 1.3 * (t - k * 0.6)
                if 0.35 < r < 5.5:
                    p = E + LEFT * r
                    inside = np.linalg.norm(p - C) < R
                    past = p[0] < C[0] - R
                    if past:
                        continue
                    op = (1 - 0.5 * r / 5.5) * (q.get_value() if inside else 1.0)
                    if op > 0.02:
                        g.add(ring_arc(E, r, LEFT, 0.55, C_NOISE, 3.5, op))
            a = ra.get_value()
            if a > 0.01:
                for k in range(int(t / 0.6) + 1):
                    r = 0.2 + V * 1.3 * (t - k * 0.6)
                    if 0.2 < r < 2.4:
                        g.add(ring_arc(SP, r, LEFT + DOWN * 0.5, 1.0, C_ANTI, 3, a * (1 - r / 2.4)))
            return g

        wv = always_redraw(waves)
        self.add(hull, floor, pax, wing, eng, engl, view)
        self.add(wv)
        self.say("비행기: 엔진 소음이 객실로 들어온다", wait=0)
        b = badge("소음", C_NOISE).to_corner(UR, buff=0.25)
        self.add(b)
        self.add_sound(hum(2.2, base=90))
        self.play(wiggle_icon(b, 2.2))
        self.remove(b)
        self.wait(0.6)
        ml = label_bg(T("마이크", 22, ORANGE, bold=True)).next_to(mic, LEFT, buff=0.15)
        sl = label_bg(T("스피커", 22, C_ANTI, bold=True)).next_to(spk, UP, buff=0.12)
        self.play(FadeIn(mic), FadeIn(ml), run_time=0.4)
        self.play(Flash(mic, color=ORANGE, line_length=0.18), FadeIn(spk), FadeIn(sl), run_time=0.7)
        self.say("마이크로 감지 → 스피커가 반대 위상 소리", wait=0)
        self.play(ra.animate.set_value(1.0), run_time=1.0)
        b = badge("반대 위상 소리를 더하면", C_SUM).to_corner(UR, buff=0.25)
        self.add(b)
        self.add_sound(hum(2.2, base=90, quiet=0.1))
        self.play(q.animate.set_value(0.08), wiggle_icon(b, 2.2), run_time=2.2)
        self.remove(b)
        quiet = tag("조용~", GREEN, 24).move_to(C + UP * 1.05 + LEFT * 0.5)
        self.play(FadeIn(quiet, scale=0.9), run_time=0.4)
        self.say("객실 안이 조용해진다")
        tt.clear_updaters()
        self.clear_all()

    # ------------------------------------------------------------ 3. 자동차
    def car_beat(self):
        tt = time_driver(self)
        cr = car(4.0).move_to([0.8, 0.2, 0])
        P = cr.pipe.get_left()
        ground = Line([-7, cr.get_bottom()[1], 0], [7, cr.get_bottom()[1], 0], color=GRAY_T, stroke_width=2)

        def waves():
            g = VGroup()
            t = tt.get_value()
            for k in range(int(t / 0.5) + 1):
                r = 0.1 + V * 1.3 * (t - k * 0.5)
                if 0.1 < r < 3.2:
                    op = 1 - r / 3.2
                    g.add(ring_arc(P, r, LEFT, 0.8, C_NOISE, 3.5, op * (1 if r < 1.0 else 0.15)))
                    if r > 0.5:
                        g.add(ring_arc(P + LEFT * 0.5, r - 0.5, LEFT, 0.8, C_ANTI, 3, op * 0.9))
            return g

        wv = always_redraw(waves)
        t1 = tag("배기관", C_NOISE, 22).next_to(P, UP, buff=0.9).shift(LEFT * 0.3)
        t2 = tag("실내", GREEN, 22).next_to(cr, UP, buff=0.25)
        self.add(ground, cr, wv)
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.5)
        self.say("자동차 배기관·실내 소음에도 쓰인다")
        self.wait(2.0)
        tt.clear_updaters()
        self.clear_all()

    # ------------------------------------------------------------ 4. 상쇄 vs 보강
    def contrast(self):
        tt = time_driver(self)
        A, LL = 0.32, 1.4
        K = 2 * np.pi / LL

        def block(cx, sign, title, sub, col):
            x0, x1 = cx - 2.4, cx + 2.4

            def f(x):
                return A * np.sin(K * (x - V * tt.get_value()))

            w1 = always_redraw(lambda: wave_line(f, x0, x1, 1.6, CYAN, 3))
            w2 = always_redraw(lambda: wave_line(lambda x: sign * f(x), x0, x1, 0.75, ORANGE, 3))
            ws = always_redraw(lambda: wave_line(lambda x: (1 + sign) * f(x), x0, x1, -0.55, GREEN, 5))
            line = Line([x0, 0.2, 0], [x1, 0.2, 0], color=WHITE_T, stroke_width=1.5, stroke_opacity=0.5)
            head = T(title, 28, col, bold=True).move_to([cx, 2.7, 0])
            res = T(sub, 24, WHITE_T, bold=True).move_to([cx, -1.6, 0])
            return VGroup(w1, w2, ws), VGroup(line, head, res)

        (wa, sa_), (wb, sb) = block(-3.3, -1, "상쇄 간섭", "→ 소리를 줄인다", C_SOFT), \
            block(3.3, 1, "보강 간섭", "→ 소리를 크게", C_LOUD)
        div = Line([0, 3.0, 0], [0, -1.9, 0], color=PANEL_STROKE, stroke_width=2)
        self.add(wa, div)
        self.play(FadeIn(sa_), run_time=0.5)
        self.say("상쇄 간섭 → 소리를 줄이고,", wait=1.5)
        self.add(wb)
        self.play(FadeIn(sb), run_time=0.5)
        self.say("상쇄 간섭 → 소리를 줄이고,\n보강 간섭 → 소리를 크게 할 수도 있다")
        self.wait(1.5)
        tt.clear_updaters()
        self.clear_all()

    def wrap(self):
        l1 = colored([("소음 제거", WHITE_T), ("=", GRAY_T), ("반대 위상 소리", C_ANTI)], 34)
        l2 = colored([("→", GRAY_T), ("상쇄 간섭", C_SOFT), ("으로 소음을 지운다", WHITE_T)], 34)
        grp = VGroup(l1, l2).arrange(DOWN, buff=0.25)
        p = panel(grp, buff=0.5, pos=UP * 0.3)
        self.play(FadeIn(p, scale=0.96), run_time=0.8)
        self.wait(4.5)
        self.play(FadeOut(p), run_time=0.6)

"""소리의 간섭 (교과서 116~118쪽, 그림 III-20, III-21).

스피커 1개 앞을 걸으면 크기 일정 → 스피커 2개(2 m, 같은 소리)면 크게–작게–크게 →
위에서 본 두 파원의 파면(마루 실선, 골 점선), 보강점·상쇄점 → 1차원 확대(가)(나) →
경로차 규칙(P2: λ → 보강, P1: λ/2 → 상쇄) → 한 줄 정리.
"""
from ikit import *

# ---- 걷기 장면의 실제 배치 (m): 스피커 간격 2 m, 걷는 줄까지 3 m, 500 Hz → λ = 0.68 m
LAM_REAL = 340 / 500
D_REAL = 2.0
L_REAL = 3.0
SC = 1.6                 # 화면 단위 / m
SPK_Y = 2.25
FLOOR_Y = -1.25
WALK = (-4.2, 4.2)       # 학생이 걷는 화면 x 범위
A0 = 2 / np.hypot(1.0, L_REAL)   # 가운데에서 두 소리를 합친 크기(정규화용)


def amp_two(sx):
    x = sx / SC
    r1, r2 = np.hypot(x + D_REAL / 2, L_REAL), np.hypot(x - D_REAL / 2, L_REAL)
    k = 2 * np.pi / LAM_REAL
    return abs(np.exp(1j * k * r1) / r1 + np.exp(1j * k * r2) / r2) / A0


def amp_one(sx):
    return (1 / np.hypot(sx / SC, L_REAL)) / A0


# ---- 위에서 본 그림
LAM = 0.8                # 화면 속 파장
D = 2.0                  # 화면 속 파원 간격 (= 2.5 λ)
Y0 = 0.55
S1 = np.array([-D / 2, Y0, 0])
S2 = np.array([D / 2, Y0, 0])
RMAX = 4.6


def circle_hits(c1, r1, c2, r2):
    d = np.linalg.norm(c2 - c1)
    if r1 + r2 < d or abs(r1 - r2) > d:
        return []
    a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
    h2 = r1 ** 2 - a ** 2
    if h2 < 0:
        return []
    u = (c2 - c1) / d
    nrm = np.array([-u[1], u[0], 0])
    base = c1 + u * a
    h = np.sqrt(h2)
    return [base + nrm * h, base - nrm * h]


def in_view(p):
    """점은 파원 아래쪽(학생이 걷는 쪽)에만 찍어 화면을 덜 복잡하게."""
    return abs(p[0]) < 6.9 and -3.0 < p[1] < Y0 - 0.25


def hyperbola(delta, c, color, dashed=False, width=5, opacity=0.5):
    """r1 - r2 = delta 인 선 (S1 왼쪽, S2 오른쪽, 가운데 c)."""
    a = delta / 2
    b2 = (D / 2) ** 2 - a ** 2
    ys = np.linspace(-4.2 - Y0, -0.25, 80)
    if abs(a) < 1e-6:
        pts = [c + np.array([0, y, 0]) for y in ys]
    else:
        pts = [c + np.array([np.sign(a) * abs(a) * np.sqrt(1 + y ** 2 / b2), y, 0]) for y in ys]
    m = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity)
    m.set_points_smoothly(pts)
    if dashed:
        m = DashedVMobject(m, num_dashes=40, dashed_ratio=0.55)
    return m


class E2Interference(CaseScene):
    def construct(self):
        self.intro()
        self.walk()
        self.top_view()
        self.close_up()
        self.path_rule()
        self.wrap()

    # ------------------------------------------------------------ 제목
    def intro(self):
        card = title_card("소리의 간섭")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(card), run_time=0.6)

    # ------------------------------------------------------------ 1. 걸어 보기
    def walk(self):
        floor = Line([-6.2, FLOOR_Y, 0], [4.9, FLOOR_Y, 0], color=GRAY_T, stroke_width=2)
        wall = Line([-6.2, SPK_Y + 0.6, 0], [4.9, SPK_Y + 0.6, 0], color=GRAY_T, stroke_width=2,
                    stroke_opacity=0.4)
        self.add(floor, wall)

        sx = ValueTracker(WALK[0])
        stu = always_redraw(lambda: person(1.0).move_to([sx.get_value(), FLOOR_Y, 0], aligned_edge=DOWN))
        tt = time_driver(self)

        spk_c = front_speaker(0.9).move_to([0, SPK_Y, 0])
        spk_l = front_speaker(0.9).move_to([-D_REAL / 2 * SC, SPK_Y, 0])
        spk_r = front_speaker(0.9).move_to([D_REAL / 2 * SC, SPK_Y, 0])
        self.n_spk = 1

        def arcs():
            g = VGroup()
            t = tt.get_value()
            xs = [0.0] if self.n_spk == 1 else [-D_REAL / 2 * SC, D_REAL / 2 * SC]
            for x in xs:
                c = np.array([x, SPK_Y - 0.5, 0])
                for k in range(int(t / 0.7) + 1):
                    r = V * (t - k * 0.7)
                    if 0.05 < r < 2.6:
                        g.add(ring_arc(c, r, DOWN, 1.5, CYAN, 3, 0.8 * (1 - r / 2.6)))
            return g

        waves = always_redraw(arcs)

        # 소리 크기 막대
        MX, MB, MH = 5.9, -1.25, 2.7
        frame = Rectangle(width=0.5, height=MH, stroke_color=GRAY_T, stroke_width=2).move_to(
            [MX, MB + MH / 2, 0])
        mlab = T("소리 크기", 20, GRAY_T, bold=True).next_to(frame, UP, buff=0.15)
        self.amp_fn = amp_one

        def bar():
            a = min(self.amp_fn(sx.get_value()), 1.0)
            h = max(a * MH, 0.02)
            col = interpolate_color(ManimColor(C_SOFT), ManimColor(C_LOUD), a)
            return Rectangle(width=0.44, height=h, stroke_width=0, fill_color=col,
                             fill_opacity=1).move_to([MX, MB + h / 2, 0])

        meter = always_redraw(bar)

        self.trail_on = False
        self.trail_pts = []

        def trail():
            g = VGroup()
            if not self.trail_on:
                return g
            cur = sx.get_value()
            for x in np.arange(WALK[0], cur + 1e-6, 0.09):
                a = min(self.amp_fn(x), 1.0)
                col = interpolate_color(ManimColor(C_SOFT), ManimColor(C_LOUD), a)
                g.add(Dot([x, FLOOR_Y - 0.25, 0], radius=0.035 + 0.085 * a, color=col))
            return g

        tr = always_redraw(trail)

        self.add(spk_c, waves)
        self.play(FadeIn(stu), FadeIn(frame), FadeIn(mlab), FadeIn(meter), run_time=0.6)
        self.say("스피커 1개 앞을 걸어가면?")

        b = badge("500 Hz", CYAN, "같은 소리").move_to([4.7, 3.3, 0])
        self.add(b)
        dur = 3.0
        amps = [amp_one(WALK[0] + (WALK[1] - WALK[0]) * s) for s in np.linspace(0, 1, 120)]
        self.add_sound(tone_amp(500, dur, amps, vol=0.35))
        self.play(sx.animate.set_value(WALK[1]), wiggle_icon(b, dur), run_time=dur, rate_func=linear)
        self.remove(b)
        self.say("소리 크기가 크게 달라지지 않는다")

        # 스피커 2개
        dl = dim_line([-D_REAL / 2 * SC, SPK_Y + 0.85, 0], [D_REAL / 2 * SC, SPK_Y + 0.85, 0], "2 m",
                      side=RIGHT * 0.0 + UP * 0.0, size=24)
        dl[3].become(label_bg(T("2 m", 22, GREEN, bold=True)).move_to(dl[0]))
        self.n_spk = 2
        self.remove(spk_c)
        self.add(spk_l, spk_r)
        self.amp_fn = amp_two
        self.play(sx.animate.set_value(WALK[0]), FadeIn(dl), run_time=1.0)
        self.say("이번엔 같은 소리를 내는 스피커 2개")

        self.trail_on = True
        self.add(tr)
        self.unsay()
        b = badge("500 Hz", CYAN, "두 스피커 · 같은 소리").move_to([4.5, 3.3, 0])
        self.add(b)
        dur = 7.5
        amps = [amp_two(WALK[0] + (WALK[1] - WALK[0]) * s) for s in np.linspace(0, 1, 300)]
        self.add_sound(tone_amp(500, dur, amps, vol=0.4))
        self.play(sx.animate.set_value(WALK[1]), wiggle_icon(b, dur), run_time=dur, rate_func=linear)
        self.remove(b)
        self.say("크게 → 작게 → 크게 …\n자리마다 소리 크기가 다르다!")
        self.say("왜 그럴까? 위에서 내려다보자", wait=2.2)
        tt.clear_updaters()
        self.clear_all()

    # ------------------------------------------------------------ 2. 위에서 본 두 파원
    def top_view(self):
        tt = time_driver(self)

        def fronts():
            g = VGroup()
            t = tt.get_value()
            for c in (S1, S2):
                for k in range(int(V * t / LAM) + 2):
                    for half, dashed in ((0.0, False), (0.5, True)):
                        r = V * t - (k + half) * LAM
                        if 0.04 < r < RMAX:
                            op = 0.95 - 0.55 * r / RMAX
                            col = CYAN if c is S1 else ORANGE
                            circ = Circle(radius=r, arc_center=c, stroke_color=col, stroke_width=2.6,
                                          stroke_opacity=op)
                            if dashed:
                                circ = DashedVMobject(circ, num_dashes=int(10 * r) + 8, dashed_ratio=0.5)
                            g.add(circ)
            return g

        fr = always_redraw(fronts)

        def src(c, name, col):
            d = Dot(c, radius=0.1, color=col)
            lab = label_bg(sym("S", name, col, 28)).next_to(d, UP, buff=0.12)
            return VGroup(d, lab)

        srcs = VGroup(src(S1, "1", CYAN), src(S2, "2", ORANGE))
        view = tag("위에서 본 모습", GRAY_T, 20).to_corner(UL, buff=0.3)
        l1 = VGroup(Line(ORIGIN, RIGHT * 0.6, color=WHITE_T, stroke_width=3), T("마루", 22, bold=True)).arrange(RIGHT, buff=0.15)
        l2 = VGroup(DashedLine(ORIGIN, RIGHT * 0.6, color=WHITE_T, stroke_width=3, dash_length=0.08),
                    T("골", 22, bold=True)).arrange(RIGHT, buff=0.15)
        leg = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legp = panel(leg, buff=0.18).to_corner(UR, buff=0.3)

        self.add(fr)
        self.play(FadeIn(srcs), FadeIn(view), FadeIn(legp), run_time=0.6)
        self.add_foreground_mobjects(srcs)
        self.say("두 스피커에서 같은 파동이 퍼져 나간다\n(실선 = 마루, 점선 = 골)")

        self.show_red = False
        self.show_blue = False

        def hits():
            g = VGroup()
            t = tt.get_value()
            n = int(V * t / LAM) + 2
            crest = [V * t - k * LAM for k in range(n)]
            trough = [V * t - (k + 0.5) * LAM for k in range(n)]
            crest = [r for r in crest if 0.04 < r < RMAX]
            trough = [r for r in trough if 0.04 < r < RMAX]
            if self.show_red:
                for a in crest:
                    for b_ in crest:
                        for p in circle_hits(S1, a, S2, b_):
                            if in_view(p):
                                g.add(Dot(p, radius=0.1, color=C_LOUD))
            if self.show_blue:
                for a, bl in [(x, y) for x in crest for y in trough] + [(x, y) for x in trough for y in crest]:
                    for p in circle_hits(S1, a, S2, bl):
                        if in_view(p):
                            g.add(Dot(p, radius=0.075, color=C_SOFT))
            return g

        hd = always_redraw(hits)
        self.add(hd)
        self.show_red = True
        k1 = tag("마루 + 마루 → 보강 (크게)", C_LOUD, 22)
        k2 = tag("마루 + 골 → 상쇄 (작게)", C_SOFT, 22)
        keys = VGroup(k1, k2).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UL, buff=0.3).shift(DOWN * 0.6)
        self.play(FadeIn(k1), run_time=0.4)
        self.say("마루와 마루가 만나는 곳 → 보강 (빨간 점)\n(골과 골이 만나는 곳도 보강)")
        self.show_blue = True
        self.play(FadeIn(k2), run_time=0.4)
        self.say("마루와 골이 만나는 곳 → 상쇄 (파란 점)")

        anti = VGroup(*[hyperbola(m * LAM, (S1 + S2) / 2, C_LOUD, width=7, opacity=0.45) for m in (-2, -1, 0, 1, 2)])
        nodal = VGroup(*[hyperbola(m * LAM, (S1 + S2) / 2, C_SOFT, dashed=True, width=5, opacity=0.8)
                         for m in (-1.5, -0.5, 0.5, 1.5)])
        self.play(Create(anti), Create(nodal), run_time=1.5)
        self.say("점들은 줄을 지어 움직인다\n빨간 선 = 늘 크게, 파란 선 = 늘 작게")

        walker = person(0.6)
        path = DashedLine([-5.6, -1.75, 0], [5.6, -1.75, 0], color=WHITE_T, stroke_width=2, dash_length=0.12)
        walker.move_to([-5.6, -1.75, 0], aligned_edge=DOWN)
        self.play(Create(path), FadeIn(walker), run_time=0.6)
        self.say("걸어가는 학생은 이 선들을 번갈아 지난다\n→ 크게·작게", wait=0)
        self.play(walker.animate.move_to([5.6, -1.75, 0], aligned_edge=DOWN), run_time=4.0, rate_func=linear)
        self.wait(0.5)
        tt.clear_updaters()
        self.clear_all()

    # ------------------------------------------------------------ 3. 1차원 확대 (가)(나)
    def close_up(self):
        tt = time_driver(self)
        ph = ValueTracker(0.0)
        A, LL = 0.45, 1.6
        K = 2 * np.pi / LL
        X0, X1 = -4.0, 4.3
        Y1, Y2, YS = 2.05, 0.8, -1.05

        def f1(x):
            return A * np.sin(K * (x - V * tt.get_value()))

        def f2(x):
            return A * np.sin(K * (x - V * tt.get_value()) + ph.get_value())

        w1 = always_redraw(lambda: wave_line(f1, X0, X1, Y1, CYAN))
        w2 = always_redraw(lambda: wave_line(f2, X0, X1, Y2, ORANGE))
        ws = always_redraw(lambda: wave_line(lambda x: f1(x) + f2(x), X0, X1, YS, GREEN, 5))
        axes = VGroup(*[Line([X0, y, 0], [X1, y, 0], color=GRAY_T, stroke_width=1.2, stroke_opacity=0.5)
                        for y in (Y1, Y2, YS)])
        labs = VGroup(T("파동 1", 22, CYAN, bold=True).move_to([-5.3, Y1, 0]),
                      T("파동 2", 22, ORANGE, bold=True).move_to([-5.3, Y2, 0]),
                      T("합성파", 22, GREEN, bold=True).move_to([-5.3, YS, 0]))
        sep = Line([X0, 0.03, 0], [X1, 0.03, 0], color=WHITE_T, stroke_width=1.5, stroke_opacity=0.5)
        plus = T("+", 30, WHITE_T, bold=True).move_to([-5.3, (Y1 + Y2) / 2 + 0.05, 0])
        eq = T("=", 30, WHITE_T, bold=True).move_to([-5.3, 0.03, 0])

        head1 = T("(가) 위상이 같을 때", 30, WHITE_T, bold=True).to_corner(UL, buff=0.35)
        head2 = T("(나) 위상이 반대일 때", 30, WHITE_T, bold=True).to_corner(UL, buff=0.35)

        self.add(axes, w1, w2, ws)
        self.play(FadeIn(labs), FadeIn(head1), FadeIn(sep), FadeIn(plus), FadeIn(eq), run_time=0.6)
        self.say("가까이서 본 두 파동: 마루끼리, 골끼리 만나면")
        r1 = VGroup(T("보강 간섭", 24, C_LOUD, bold=True), T("소리 크게", 20, WHITE_T)).arrange(DOWN, buff=0.08)
        r1 = panel(r1, buff=0.15).move_to([5.65, YS, 0])
        self.play(FadeIn(r1), run_time=0.4)
        b = badge("크게", C_LOUD).move_to([5.4, 3.35, 0])
        self.add(b)
        self.say("진폭이 2배 → 보강 간섭", wait=0)
        self.add_sound(tone(500, 2.0, vol=0.4))
        self.play(wiggle_icon(b, 2.0))
        self.remove(b)
        self.wait(0.5)

        self.play(FadeOut(r1), FadeOut(head1), FadeIn(head2), run_time=0.5)
        self.say("파동 2를 반 파장 밀면 (위상 반대)", wait=0)
        self.play(ph.animate.set_value(np.pi), run_time=2.5)
        self.wait(1.2)
        r2 = VGroup(T("상쇄 간섭", 24, C_SOFT, bold=True), T("소리 작게", 20, WHITE_T)).arrange(DOWN, buff=0.08)
        r2 = panel(r2, buff=0.15).move_to([5.65, YS, 0])
        self.play(FadeIn(r2), run_time=0.4)
        b = badge("작게", C_SOFT, "거의 안 들림").move_to([5.2, 3.3, 0])
        self.add(b)
        self.say("마루와 골이 만나 합이 거의 0\n→ 상쇄 간섭, 소리가 거의 사라진다", wait=0)
        self.add_sound(tone(500, 2.0, vol=0.03))
        self.play(wiggle_icon(b, 2.0))
        self.remove(b)
        self.wait(1.2)
        tt.clear_updaters()
        self.clear_all()

    # ------------------------------------------------------------ 4. 경로차 규칙
    def path_rule(self):
        s1 = np.array([-4.4, 2.3, 0])
        s2 = s1 + RIGHT * D
        bg = VGroup()
        for c, col in ((s1, CYAN), (s2, ORANGE)):
            for k in range(1, 5):
                bg.add(Circle(radius=k * LAM, arc_center=c, stroke_color=col, stroke_width=2, stroke_opacity=0.32))
                bg.add(DashedVMobject(Circle(radius=(k - 0.5) * LAM, arc_center=c, stroke_color=col,
                                             stroke_width=2, stroke_opacity=0.32), num_dashes=10 * k + 6))
        srcs = VGroup(Dot(s1, radius=0.1, color=CYAN), Dot(s2, radius=0.1, color=ORANGE),
                      label_bg(sym("S", "1", CYAN, 26)).next_to(s1, UP, buff=0.12),
                      label_bg(sym("S", "2", ORANGE, 26)).next_to(s2, UP, buff=0.12))
        P2 = circle_hits(s1, 4 * LAM, s2, 3 * LAM)[1]
        P1 = circle_hits(s1, 3.5 * LAM, s2, 4 * LAM)[1]

        # 오른쪽 패널
        rows = VGroup(
            T("경로차 = | S₁P − S₂P |", 28, WHITE_T, bold=True),
            colored([("P₂ :", C_LOUD), ("4λ − 3λ = λ", WHITE_T), ("→ 보강", C_LOUD)], 25),
            colored([("P₁ :", C_SOFT), ("|3.5λ − 4λ| = λ/2", WHITE_T), ("→ 상쇄", C_SOFT)], 25),
            Line(LEFT * 2.9, RIGHT * 2.9, color=PANEL_STROKE, stroke_width=2),
            T("0, λ, 2λ, …  (반파장의 짝수 배)", 23, WHITE_T, bold=True),
            T("→ 보강 간섭 · 크게", 23, C_LOUD, bold=True),
            T("λ/2, 3λ/2, …  (반파장의 홀수 배)", 23, WHITE_T, bold=True),
            T("→ 상쇄 간섭 · 작게", 23, C_SOFT, bold=True),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        rows[3].set_x(rows.get_x())
        for i in (5, 7):
            rows[i].shift(UP * 0.08 + RIGHT * 0.3)
        pnl = panel(rows, buff=0.32)
        pnl.to_edge(RIGHT, buff=0.3).set_y(0.55)

        self.play(FadeIn(bg), FadeIn(srcs), run_time=0.8)
        self.play(FadeIn(pnl[0]), FadeIn(rows[0]), run_time=0.6)
        self.say("두 스피커에서 온 거리의 차 = 경로차")

        def paths(P, name, col, l1, l2, prop):
            a = Line(s1, P, color=CYAN, stroke_width=4)
            b_ = Line(s2, P, color=ORANGE, stroke_width=4)
            dot = Dot(P, radius=0.12, color=col)
            pl = label_bg(sym("P", name, col, 26)).next_to(dot, DOWN, buff=0.12)

            def lab(line, txt, c, side):
                m = label_bg(T(txt, 22, c, bold=True))
                return m.next_to(line.point_from_proportion(prop), side, buff=0.1)

            return VGroup(a, b_, dot, pl, lab(a, l1, CYAN, LEFT), lab(b_, l2, ORANGE, RIGHT))

        g2 = paths(P2, "2", C_LOUD, "4λ", "3λ", 0.5)
        self.play(Create(g2[0]), Create(g2[1]), FadeIn(g2[2:]), run_time=1.2)
        self.play(FadeIn(rows[1]), run_time=0.5)
        self.say("P₂: 경로차 λ → 마루와 마루가 만난다 → 보강")
        g1 = paths(P1, "1", C_SOFT, "3.5λ", "4λ", 0.72)
        self.play(g2[:2].animate.set_stroke(opacity=0.3), FadeOut(g2[4:]), Create(g1[0]), Create(g1[1]), FadeIn(g1[2:]),
                  run_time=1.2)
        self.play(FadeIn(rows[2]), run_time=0.5)
        self.say("P₁: 경로차 λ/2 → 마루와 골이 만난다 → 상쇄")
        self.play(Create(rows[3]), FadeIn(rows[4]), FadeIn(rows[5]), run_time=0.6)
        self.play(FadeIn(rows[6]), FadeIn(rows[7]), run_time=0.6)
        self.say("경로차가 반파장의 짝수 배 → 보강\n홀수 배 → 상쇄", wait=4.0)
        self.clear_all()

    # ------------------------------------------------------------ 5. 정리
    def wrap(self):
        l1 = T("같은 소리 두 개 →", 34, WHITE_T, bold=True)
        l2 = colored([("자리마다", WHITE_T), ("크게(보강)", C_LOUD), ("/", GRAY_T), ("작게(상쇄)", C_SOFT)], 34)
        grp = VGroup(l1, l2).arrange(DOWN, buff=0.25)
        p = panel(grp, buff=0.5, pos=UP * 0.3)
        self.play(FadeIn(p, scale=0.96), run_time=0.8)
        self.wait(3.4)
        self.play(FadeOut(p), run_time=0.6)

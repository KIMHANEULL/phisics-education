"""도플러 효과 ② 음원이 움직일 때 (교과서 111~114쪽, 그림 III-14).

복습 → 움직이는 음원의 파면(중심 0, T, 2T, 3T) → 오개념: 소리 속력은 그대로 →
한 주기 확대(실제 비율): λ_A = λ − v_sT, λ_B = λ + v_sT → f_A ≈ 1333 Hz, f_B ≈ 1091 Hz →
구급차가 지나갈 때 → 자료실: 충격파 → 정리.
"""
from dkit import *

C = 0.75     # 화면 속 소리 속력 (1 T 동안 퍼지는 거리)
VS = 0.375   # 화면 속 음원 속력 = C/2 (그림만 과장)
TS = 1.2     # 화면 속 1 T = 1.2 초


class D2MovingSource(CaseScene):
    def construct(self):
        card = title_card("도플러 효과 ② 음원이 움직일 때")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.wait(2.4)
        self.play(FadeOut(card), run_time=0.6)
        self.recap()
        self.moving2d()
        self.same_speed()
        self.zoom1d()
        self.derive_a()
        self.derive_b()
        self.pass_by()
        self.shock()
        self.wrap()

    # ------------------------------------------------------------ 1. 복습
    def recap(self):
        S = np.array([0, 0.4, 0])
        tt = time_driver(self, 1 / TS)
        waves = always_redraw(lambda: fronts(tt.get_value(), lambda k: S, C, 3.0, CYAN, 3))
        sd = Dot(S, radius=0.1, color=ORANGE)
        self.add(waves, sd)
        self.say("①편 복습: 음원이 멈춰 있으면 어느 방향이든\n파면 간격(파장 λ)이 같아 1200 Hz로 들린다", wait=5.0)
        self.remove(tt)
        self.clear_all()

    # ------------------------------------------------------------ 2. 움직이는 음원 (그림 III-14)
    def moving2d(self):
        Y = 0.35
        X0 = -0.8
        A_ = np.array([4.5, Y, 0])
        B_ = np.array([-5.4, Y, 0])
        tw = ValueTracker(0)
        cen = lambda k: np.array([X0 + VS * k, Y, 0])
        waves = always_redraw(lambda: fronts(tw.get_value(), cen, C, 3.3, CYAN, 3, fade=0.45))

        show_ar = [True]

        def src():
            t = tw.get_value()
            p = np.array([X0 + VS * t, Y, 0])
            if not show_ar[0]:
                return VGroup(Dot(p, radius=0.11, color=ORANGE))
            ar = Arrow(p + RIGHT * 0.12, p + RIGHT * 0.95, buff=0, color=C_S, stroke_width=5,
                       tip_length=0.18)
            lab = label_bg(sym("v", "s", C_S, 26)).next_to(ar, UP, buff=0.06)
            return VGroup(ar, lab, Dot(p, radius=0.11, color=ORANGE))

        def marks():
            t = tw.get_value()
            g = VGroup()
            names = ["0", "T", "2T", "3T"]
            for k in range(0, min(int(np.floor(t + 1e-6)), 3) + 1):
                if t - k < 0.02:
                    continue
                g.add(Dot(cen(k), radius=0.05, color=WHITE_T))
                g.add(T(names[k], 19, WHITE_T, bold=True).move_to(cen(k) + DOWN * 0.3))
            return g

        sn = slow_note()
        ex = T("※ 차이가 잘 보이게 음원 속력을 과장 (그림은 vₛ = v/2, 계산은 vₛ = 34 m/s)", 18, GRAY_T)
        ex.next_to(sn, DOWN, buff=0.08, aligned_edge=LEFT)
        pa = person(0.9).move_to(A_ + DOWN * 0.45, aligned_edge=DOWN)
        pb = person(0.9).move_to(B_ + DOWN * 0.45, aligned_edge=DOWN)
        la = T("A", 28, WHITE_T, bold=True).next_to(pa, UP, buff=0.1)
        lb = T("B", 28, WHITE_T, bold=True).next_to(pb, UP, buff=0.1)
        sg = always_redraw(src)
        mk = always_redraw(marks)
        self.add(waves, mk, sg)
        self.play(FadeIn(sn), FadeIn(ex), FadeIn(pa), FadeIn(pb), FadeIn(la), FadeIn(lb), run_time=0.7)
        self.say("이제 음원(소리의 파원)이 오른쪽(A 쪽)으로\n속력 vₛ로 움직이며 소리를 낸다")
        self.say("0, T, 2T, 3T … 한 주기마다 파면을 하나씩 낸다", wait=0.1)
        self.play(tw.animate.set_value(4.0), run_time=4 * TS, rate_func=linear)
        self.wait(1.6)
        self.say("각 원의 중심은 음원이 그 파면을 '낸 자리'다.\n음원이 움직였으니 중심이 조금씩 오른쪽으로 옮겨 간다")

        # 앞·뒤 간격
        xr2, xr3 = X0 + VS * 2 + C * 2, X0 + VS * 3 + C * 1
        xl1, xl2 = X0 + VS * 1 - C * 3, X0 + VS * 2 - C * 2
        dA = dim_line([xr3, Y, 0], [xr2, Y, 0], "", color=GREEN)
        dB = dim_line([xl1, Y, 0], [xl2, Y, 0], "", color=GREEN)
        show_ar[0] = False
        tA = label_bg(sym("λ", "A", GREEN, 28)).move_to([3.0, Y + 0.75, 0])
        tB = label_bg(sym("λ", "B", GREEN, 28)).move_to([(xl1 + xl2) / 2, Y + 0.45, 0])
        pA = Line(tA.get_left() + LEFT * 0.05, [(xr2 + xr3) / 2, Y + 0.1, 0], color=GREEN, stroke_width=2)
        nA = label_bg(T("촘촘 (짧다)", 22, GREEN, bold=True)).next_to(pa, DOWN, buff=0.2)
        nB = label_bg(T("듬성 (길다)", 22, GREEN, bold=True)).next_to(pb, DOWN, buff=0.2)
        self.play(Create(dA), FadeIn(tA), Create(pA), FadeIn(nA), run_time=0.8)
        self.say("음원이 다가가는 앞쪽(A 쪽)은 파면이 촘촘하다\n→ 파장 λ_A가 짧다", wait=4.2)
        self.play(Create(dB), FadeIn(tB), FadeIn(nB), run_time=0.8)
        self.say("음원이 멀어지는 뒤쪽(B 쪽)은 파면이 듬성하다\n→ 파장 λ_B가 길다", wait=4.2)
        self.remove(waves, mk, sg)
        self.clear_all()

    # ------------------------------------------------------------ 3. 오개념: 소리 속력은 그대로
    def same_speed(self):
        Y = 0.35
        P0 = np.array([-0.9, Y, 0])
        tw = ValueTracker(0)

        def scene_():
            t = tw.get_value()
            r = C * t
            g = VGroup()
            if r > 0.01:
                g.add(circle_front(P0, r, ORANGE, 5))
                for d in (LEFT, RIGHT):
                    e = P0 + d * r
                    g.add(Arrow(e, e + d * 0.85, buff=0, color=ORANGE, stroke_width=5, tip_length=0.18))
                    g.add(label_bg(T("340 m/s", 22, ORANGE, bold=True)).move_to(e + d * 0.5 + UP * 0.32))
            p = P0 + RIGHT * VS * t
            g.add(Dot(P0, radius=0.06, color=WHITE_T))
            g.add(Dot(p, radius=0.11, color=ORANGE))
            g.add(Arrow(p + RIGHT * 0.12, p + RIGHT * 0.8, buff=0, color=C_S, stroke_width=5, tip_length=0.16))
            return g

        sc = always_redraw(scene_)
        warn = tag("주의!", RED_T, 26).to_corner(UR, buff=0.4)
        sn = slow_note()
        ex = T("※ 차이가 잘 보이게 음원 속력을 과장 (그림은 vₛ = v/2, 계산은 vₛ = 34 m/s)", 18, GRAY_T)
        ex.next_to(sn, DOWN, buff=0.08, aligned_edge=LEFT)
        self.add(sc)
        self.play(FadeIn(warn), FadeIn(sn), FadeIn(ex), run_time=0.5)
        self.say("자주 하는 착각: 음원이 다가오면 소리가 더 빨리 온다?", wait=3.6)
        self.say("파면 하나만 따라가 보자", wait=0.1)
        self.play(tw.animate.set_value(3.0), run_time=3 * TS, rate_func=linear)
        lb = label_bg(T("파면을 낸 자리 (원의 중심)", 21, WHITE_T, bold=True)).next_to(P0, DOWN, buff=0.25)
        self.play(FadeIn(lb), run_time=0.4)
        self.say("한 번 나온 파면은 음원을 따라가지 않는다.\n원의 중심은 낸 자리에 그대로 남는다", wait=4.2)
        self.say("앞으로도 뒤로도 똑같이 (바람이 없을 때) v = 340 m/s로 퍼진다.\n달라지는 것은 속력이 아니라 파면 사이 '간격'뿐이다", wait=5.0)
        self.remove(sc)
        self.clear_all()

    # ------------------------------------------------------------ 4. 한 주기 확대 (실제 비율)
    def zoom1d(self):
        U = 1.0 / 0.1          # 화면 1칸 = 0.1 m
        LAM = 0.2833 * U       # 2.833
        DS = 34 / 1200 * U     # 0.2833
        O = np.array([-0.2, 0, 0])
        CR_LO, CR_HI = -1.2, 1.25
        RY = -1.55
        tw = ValueTracker(0)

        ruler = VGroup(Line(O + LEFT * 4.3 + UP * RY, O + RIGHT * 4.3 + UP * RY, color=GRAY_T, stroke_width=2))
        for i in range(-4, 5):
            x = O[0] + i
            ruler.add(Line([x, RY - 0.08, 0], [x, RY + 0.08, 0], color=GRAY_T, stroke_width=2))
            ruler.add(T(f"{abs(i) * 10}", 18, GRAY_T).move_to([x, RY - 0.3, 0]))
        ruler.add(T("(cm)", 18, GRAY_T).move_to([O[0] + 4.75, RY - 0.3, 0]))

        def crest(x, col=CYAN, w=5):
            return Line([x, CR_LO, 0], [x, CR_HI, 0], color=col, stroke_width=w)

        def scene_():
            t = tw.get_value()
            g = VGroup()
            if t > 0.005:
                g.add(crest(O[0] + LAM * t), crest(O[0] - LAM * t))
            g.add(crest(O[0], CYAN, 2).set_stroke(opacity=0.0))
            p = O + RIGHT * DS * t
            if t >= 0.999:
                g.add(crest(p[0], ORANGE, 6))
            g.add(Dot(p, radius=0.12, color=ORANGE))
            return g

        sc = always_redraw(scene_)
        sn = slow_note()
        ex = T("※ 실제 비율 (눈금 1칸 = 10 cm)", 18, GRAY_T).next_to(sn, DOWN, buff=0.08, aligned_edge=LEFT)
        clock = Clock(tw, "ms", "{:.3f}", scale=1000 / 1200)
        sa = T("A 쪽 →", 24, WHITE_T, bold=True).move_to([5.6, 0.0, 0])
        sb = T("← B 쪽", 24, WHITE_T, bold=True).move_to([-5.9, 0.0, 0])
        vs_ar = Arrow(O + RIGHT * 0.15 + DOWN * 0.45, O + RIGHT * 1.0 + DOWN * 0.45, buff=0, color=C_S,
                      stroke_width=4, tip_length=0.16)
        vs_l = row(sym("v", "s", C_S, 24), ("= 34 m/s", C_S), size=24).next_to(vs_ar, RIGHT, buff=0.1)
        self.add(sc)
        self.play(FadeIn(ruler), FadeIn(sn), FadeIn(ex), FadeIn(clock), FadeIn(sa), FadeIn(sb),
                  GrowArrow(vs_ar), FadeIn(vs_l), run_time=0.8)
        self.say("한 주기 T(= 1/1200 s) 동안 무슨 일이 생기는지\n실제 비율로 확대해 보자", wait=4.0)
        self.say("t = 0: 음원이 파면 하나를 낸다", wait=2.0)
        self.play(FadeOut(vs_ar), FadeOut(vs_l), run_time=0.3)
        self.play(tw.animate.set_value(1.0), run_time=5.0, rate_func=linear)
        self.say("t = T: 음원이 다음 파면(주황)을 낸다", wait=2.6)

        # λ = vT
        d_l = dim_line(O + UP * 1.0, O + RIGHT * LAM + UP * 1.0, "", color=WHITE_T)
        t_l = label_bg(row(("λ = vT = 28.3 cm", WHITE_T), size=24)).next_to(d_l, UP, buff=0.08)
        self.play(Create(d_l), FadeIn(t_l), run_time=0.6)
        self.say("그동안 첫 파면은 vT = 340 × 1/1200 m\n= 28.3 cm(원래 파장 λ)만큼 퍼져 나갔다", wait=4.4)
        # v_s T
        d_s = dim_line(O + DOWN * 0.6, O + RIGHT * DS + DOWN * 0.6, "", color=C_S)
        t_s = label_bg(row(sym("v", "s", C_S, 24), ("T ≈ 2.8 cm", C_S), size=24))
        t_s.next_to(d_s, LEFT, buff=0.15)
        self.play(Create(d_s), FadeIn(t_s), run_time=0.6)
        self.say("음원도 vₛT = 34 × 1/1200 m ≈ 2.8 cm\n앞으로 따라왔다", wait=3.8)
        # λ_A, λ_B
        d_a = dim_line(O + RIGHT * DS + UP * 0.3, O + RIGHT * LAM + UP * 0.3, "", color=GREEN)
        t_a = label_bg(row(sym("λ", "A", GREEN, 24), ("= 25.5 cm", GREEN), size=24)).next_to(d_a, UP, buff=0.06)
        self.play(Create(d_a), FadeIn(t_a), run_time=0.6)
        self.say("다음 파면은 따라온 그 자리에서 출발하므로\n앞쪽 간격 λ_A = λ − vₛT = 25.5 cm (짧아짐)", wait=5.0)
        d_b = dim_line(O + LEFT * LAM + UP * 0.3, O + RIGHT * DS + UP * 0.3, "", color=GREEN)
        t_b = label_bg(row(sym("λ", "B", GREEN, 24), ("= 31.2 cm", GREEN), size=24)).next_to(d_b, UP, buff=0.06)
        self.play(Create(d_b), FadeIn(t_b), run_time=0.6)
        self.say("뒤쪽은 음원이 vₛT만큼 멀어진 자리에서 다음 파면을 내므로\n뒤쪽 간격 λ_B = λ + vₛT = 31.2 cm (길어짐)")
        self.remove(sc)
        self.clear_all()

    # ------------------------------------------------------------ 5. A 쪽 진동수 유도
    def derive_a(self):
        Z = 32
        lamA = lambda c=WHITE_T: sym("λ", "A", c, Z)
        vs = lambda c=C_S: sym("v", "s", c, Z)
        r1 = row(lamA(GREEN), "=", sym("λ", None, C_L, Z), "−", vs(), sym("T", None, WHITE_T, Z), size=Z)
        n1 = T("(T = 1/f)", 22, GRAY_T)
        r1 = VGroup(r1, n1.next_to(r1, RIGHT, buff=0.4))
        r2 = row(sym("f", "A", C_F, Z), "=", fr([sym("v", None, C_V, Z)], [lamA(GREEN)], Z), "=",
                 fr([sym("v", None, C_V, Z)], [sym("λ", None, C_L, Z), "−", fr([vs()], [sym("f", None, C_F, Z)], Z)], Z),
                 size=Z)
        r3 = row("=", fr([sym("v", None, C_V, Z)], [sym("v", None, C_V, Z), "−", vs()], Z), "×",
                 sym("f", None, C_F, Z), size=Z)
        n3 = T("← 분자·분모에 f를 곱함 (λf = v)", 21, GRAY_T)
        r3 = VGroup(r3, n3.next_to(r3, RIGHT, buff=0.35))
        r4 = row("=", fr([("(340)", C_V)], [("(340)", C_V), "−", ("(34)", C_S)], Z), "×", ("(1200)", C_F),
                 ("≈ 1333 Hz", C_F), size=Z)
        rows = VGroup(r1, r2, r3, r4).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        r3.shift(RIGHT * 0.95)
        r4.shift(RIGHT * 0.95)
        head = T("A 쪽 (음원이 다가온다)", 26, GREEN, bold=True)
        body = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        pnl = panel(body, buff=0.3).to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.4)
        self.play(FadeIn(pnl[0]), FadeIn(head), FadeIn(r1), run_time=0.8)
        self.say("A가 듣는 진동수를 구해 보자.\n앞쪽 파장 λ_A = λ − vₛT", wait=3.8)
        self.play(FadeIn(r2), run_time=0.8)
        self.say("A는 정지해 있으므로 들리는 진동수 = v / 파장.\nT = 1/f 이므로 vₛT = vₛ / f")
        self.play(FadeIn(r3), run_time=0.8)
        self.say("분자와 분모에 f를 곱하면 λf = v 이므로\nf_A = v / (v − vₛ) × f", wait=4.4)
        self.play(FadeIn(r4[0]), FadeIn(r4[1]), FadeIn(r4[2]), FadeIn(r4[3]), run_time=0.8)
        self.say("v에 (340), vₛ에 (34), f에 (1200)을 넣으면", wait=3.4)
        self.play(FadeIn(r4[4], shift=LEFT * 0.2), run_time=0.6)
        self.play(Create(hl_box(r4[4], GREEN)), run_time=0.5)
        self.say("약 1333 Hz. 340/306 ≈ 1.11배\n→ 원래보다 약 11 % 높은 소리로 들린다", wait=4.4)
        b1 = sound_badge(1333, GREEN, "A가 듣는 소리").move_to([5.0, 0.4, 0])
        self.unsay()
        self.play(FadeIn(b1), run_time=0.3)
        play_beep(self, 1333, 1.2, b1, extra=0.6)
        self.clear_all()

    # ------------------------------------------------------------ 6. B 쪽
    def derive_b(self):
        Z = 32
        vs = lambda: sym("v", "s", C_S, Z)
        r1 = row(sym("λ", "B", GREEN, Z), "=", sym("λ", None, C_L, Z), "+", vs(), sym("T", None, WHITE_T, Z), size=Z)
        r2 = row(sym("f", "B", C_F, Z), "=", fr([sym("v", None, C_V, Z)], [sym("λ", "B", GREEN, Z)], Z), "=",
                 fr([sym("v", None, C_V, Z)], [sym("v", None, C_V, Z), "+", vs()], Z), "×",
                 sym("f", None, C_F, Z), size=Z)
        r3 = row("=", fr([("(340)", C_V)], [("(340)", C_V), "+", ("(34)", C_S)], Z), "×", ("(1200)", C_F),
                 ("≈ 1091 Hz", C_F), size=Z)
        rows = VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        r3.shift(RIGHT * 0.95)
        head = T("B 쪽 (음원이 멀어진다)", 26, CYAN, bold=True)
        body = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        pnl = panel(body, buff=0.3).to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.4)
        self.play(FadeIn(pnl[0]), FadeIn(head), FadeIn(r1), run_time=0.8)
        self.say("B 쪽도 같은 방법이다. 뒤쪽 파장 λ_B = λ + vₛT", wait=3.6)
        self.play(FadeIn(r2), run_time=0.8)
        self.say("빼기가 더하기로 바뀔 뿐: f_B = v / (v + vₛ) × f", wait=3.8)
        self.play(FadeIn(r3), run_time=0.8)
        self.play(Create(hl_box(r3[4], CYAN)), run_time=0.5)
        self.say("약 1091 Hz. 파장이 길어진 만큼\n1초에 도착하는 파면이 줄어 낮은 소리가 된다", wait=4.6)
        bs = [sound_badge(1333, GREEN, "A (다가옴)"), sound_badge(1200, GRAY_T, "원래 소리"),
              sound_badge(1091, CYAN, "B (멀어짐)")]
        bg = VGroup(*bs).arrange(RIGHT, buff=0.4).move_to([0, -1.75, 0])
        self.say("세 소리를 차례로 들어 보자", wait=0.1)
        for b, hz in zip(bs, (1333, 1200, 1091)):
            self.play(FadeIn(b), run_time=0.3)
            play_beep(self, hz, 1.1, b, extra=0.35)
        self.wait(0.6)
        self.clear_all()

    # ------------------------------------------------------------ 7. 구급차가 지나갈 때
    def pass_by(self):
        ROAD = -1.45
        GX0, GX1 = -5.4, 5.4
        fy = lambda f: 2.15 + (f - 1200) / 133.3 * 0.7
        d = 0.45

        def fh(x):
            cos = -x / np.sqrt(x * x + d * d)   # 다가올 때 +
            return 1200 * 340 / (340 - 34 * cos)

        axis = VGroup(Line([GX0, fy(1050), 0], [GX1 + 0.2, fy(1050), 0], color=GRAY_T, stroke_width=2),
                      Line([GX0, fy(1050), 0], [GX0, fy(1390), 0], color=GRAY_T, stroke_width=2))
        ref = DashedLine([GX0, fy(1200), 0], [GX1, fy(1200), 0], color=GRAY_T, stroke_width=1.5, dash_length=0.1)
        ticks = VGroup(*[T(str(f), 19, c, bold=True).next_to([GX0, fy(f), 0], LEFT, buff=0.12)
                         for f, c in ((1333, ORANGE), (1200, GRAY_T), (1091, CYAN))])
        ylab = T("들리는 진동수 (Hz)", 19, GRAY_T).next_to(axis[1], UP, buff=0.1).align_to(axis[1], LEFT)
        xlab = T("시간 →", 19, GRAY_T).next_to(axis[0], RIGHT, buff=0.1)

        def curve(xe):
            xe = min(xe, GX1)
            if xe <= GX0 + 0.02:
                return VMobject()
            xs = np.linspace(GX0, xe, 160)
            m = VMobject(stroke_color=WHITE_T, stroke_width=4)
            m.set_points_as_corners([[x, fy(fh(x)), 0] for x in xs])
            return m

        ground = Rectangle(width=16, height=2.9, stroke_width=0, fill_color=GROUND,
                           fill_opacity=0.55).move_to([0, ROAD - 1.45, 0])
        road = Line([-8, ROAD, 0], [8, ROAD, 0], color=GRAY_T, stroke_width=2)
        man = person(1.0).move_to([0, ROAD + 0.4, 0], aligned_edge=DOWN)
        me = T("나", 22, GRAY_T, bold=True).next_to(man, RIGHT, buff=0.15)
        amb = ambulance(1.9).move_to([-9.2, ROAD, 0], aligned_edge=DOWN)
        ax = lambda: amb.get_center()[0]
        self.add(ground, road, man, me, amb)
        self.play(FadeIn(axis), FadeIn(ref), FadeIn(ticks), FadeIn(ylab), FadeIn(xlab), run_time=0.7)
        self.say("다시 구급차. 들리는 진동수를 그래프로 그리며 들어 보자", wait=3.6)

        def badge():
            x = ax()
            if x < -0.6:
                return M("1333 Hz", 28, ORANGE).next_to(man, UP, buff=0.2)
            if x > 0.6:
                return M("1091 Hz", 28, CYAN).next_to(man, UP, buff=0.2)
            return M("↓", 28, WHITE_T).next_to(man, UP, buff=0.2)

        cv = always_redraw(lambda: curve(ax()))
        bd = always_redraw(badge)
        self.add(cv, bd)
        self.unsay()

        def drive():
            amb.move_to([-9.2, ROAD, 0], aligned_edge=DOWN)
            # x: -9.2 → 9.2, 3.8 s. |x|<0.6 구간은 1.78~2.02 s
            self.add_sound(tone(1333, 1.5, vol=0.3), time_offset=0.25)
            self.add_sound(tone((1333, 1091), 0.3, vol=0.3), time_offset=1.75)
            self.add_sound(tone(1091, 1.5, vol=0.3), time_offset=2.05)
            self.play(amb.animate.move_to([9.2, ROAD, 0], aligned_edge=DOWN), run_time=3.8, rate_func=linear)
            self.wait(0.3)

        drive()
        self.remove(cv)
        full = curve(GX1)
        self.add(full)
        hi = Line([GX0, fy(1333), 0], [-1.7, fy(1333), 0], color=ORANGE, stroke_width=7, stroke_opacity=0.5)
        lo = Line([1.7, fy(1091), 0], [GX1, fy(1091), 0], color=CYAN, stroke_width=7, stroke_opacity=0.5)
        self.play(Create(hi), run_time=0.6)
        self.say("다가오는 동안은 거의 1333 Hz 그대로다.\n점점 높아지는 것이 아니다!", wait=4.2)
        self.play(Create(lo), run_time=0.6)
        self.say("바로 옆을 지날 때 짧은 시간에 빠르게 낮아지고,\n멀어지는 동안은 거의 1091 Hz")
        self.say("가까워질 때 높고 멀어질 때 낮게 들리는 현상\n= 도플러 효과", wait=3.6)
        self.remove(bd)
        self.clear_all()

    # ------------------------------------------------------------ 8. 자료실: 충격파
    def shock(self):
        tg = tag("자료실", ORANGE, 22).to_corner(UL, buff=0.35)
        hd = T("음원이 점점 빨라지면?", 32, WHITE_T, bold=True).to_edge(UP, buff=0.35)
        self.play(FadeIn(tg), FadeIn(hd), run_time=0.6)
        c = 0.32
        XS = [-4.45, 0.0, 4.45]
        BY = 0.0
        specs = [("음원 정지", "(vₛ = 0)", 0.0), ("음속보다 느림", "(vₛ < v)", 0.5), ("음속과 같음", "(vₛ = v)", 1.0)]
        boxes = VGroup()
        draws = []
        for (t1, t2, r), x in zip(specs, XS):
            box = RoundedRectangle(corner_radius=0.1, width=4.05, height=3.7, stroke_color=PANEL_STROKE,
                                   stroke_width=1.5, fill_color=PANEL_FILL, fill_opacity=0.9).move_to([x, BY, 0])
            ttl = VGroup(T(t1, 24, WHITE_T, bold=True), T(t2, 20, GRAY_T)).arrange(RIGHT, buff=0.12)
            ttl.next_to(box, UP, buff=0.12)
            vsd = r * c
            base = x - 2.5 * vsd  # 전체가 상자 가운데 오도록
            g = VGroup()
            for k in range(5):
                g.add(circle_front([base + vsd * k, BY, 0], c * (5 - k), CYAN, 2.5, 1 - 0.1 * (4 - k)))
            g.add(Dot([base + vsd * 5, BY, 0], radius=0.09, color=ORANGE))
            boxes.add(box, ttl)
            draws.append(g)
        # 그림 가운데 맞춤: 원 묶음의 가로 중심을 상자 중심으로
        for g, x in zip(draws, XS):
            g.shift(RIGHT * (x - VGroup(*g[:-1]).get_center()[0]))
        self.play(FadeIn(boxes), run_time=0.6)
        for g in draws:
            self.play(Create(g), run_time=1.0)
        wall_x = draws[2][-1].get_center()[0]
        wall = Line([wall_x, BY - 1.0, 0], [wall_x, BY + 1.0, 0], color=ORANGE, stroke_width=8)
        wl = label_bg(T("압력의 벽", 21, ORANGE, bold=True)).next_to(wall, UP, buff=0.08)
        self.say("음원이 빨라질수록 앞쪽 파면이 점점 더 촘촘해진다", wait=3.6)
        self.play(Create(wall), FadeIn(wl), run_time=0.6)
        self.say("음원 속력 = 음속이면 파면이 음원 앞에 겹겹이 쌓여\n아주 큰 압력의 벽이 된다", wait=4.6)
        self.play(FadeOut(boxes), *[FadeOut(g) for g in draws], FadeOut(wall), FadeOut(wl), FadeOut(hd), run_time=0.6)
        self.unsay()

        # 음속보다 빠를 때: 원뿔
        hd2 = T("음원이 음속보다 빠르면", 30, WHITE_T, bold=True).to_edge(UP, buff=0.35)
        cc, vv = 0.45, 0.72  # v_s = 1.6 v
        X0, Y = -3.7, 0.25
        N = 7
        tw = ValueTracker(0)
        cen = lambda k: np.array([X0 + vv * k, Y, 0])
        waves = always_redraw(lambda: fronts(tw.get_value(), cen, cc, 3.3, CYAN, 3, fade=0.4))
        sd = always_redraw(lambda: Dot([X0 + vv * tw.get_value(), Y, 0], radius=0.11, color=ORANGE))
        self.play(FadeIn(hd2), run_time=0.4)
        self.add(waves, sd)
        self.say("파면보다 음원이 먼저 앞으로 나가 버린다", wait=0.1)
        self.play(tw.animate.set_value(N), run_time=N * 0.75, rate_func=linear)
        S = np.array([X0 + vv * N, Y, 0])
        th = np.arcsin(cc / vv)
        D = vv * N
        L = np.sqrt(D ** 2 - (cc * N) ** 2)
        up = Line(S, S + L * np.array([-np.cos(th), np.sin(th), 0]), color=ORANGE, stroke_width=6)
        dn = Line(S, S + L * np.array([-np.cos(th), -np.sin(th), 0]), color=ORANGE, stroke_width=6)
        lab = label_bg(T("충격파", 28, ORANGE, bold=True)).next_to(S, RIGHT, buff=0.3).shift(UP * 0.35)
        self.play(Create(up), Create(dn), FadeIn(lab), run_time=0.9)
        self.say("파면들이 V자(원뿔) 모양으로 겹쳐 강한 충격파가 된다\n→ 전투기의 소닉 붐", wait=4.6)
        self.say("물 위를 빠르게 달리는 보트 뒤의 V자 물결도\n파면이 겹쳐 생기는 비슷한 모습이다")
        self.remove(waves, sd)
        self.clear_all()

    # ------------------------------------------------------------ 9. 정리
    def wrap(self):
        p = summary(self, "② 음원이 움직일 때 정리", [
            "· 소리의 속력은 앞뒤 모두 v = 340 m/s 그대로 — 바뀌는 것은 파장",
            "· 다가오는 쪽: λ_A = λ − vₛT,   f_A = v/(v − vₛ) × f ≈ 1333 Hz (높게)",
            "· 멀어지는 쪽: λ_B = λ + vₛT,   f_B = v/(v + vₛ) × f ≈ 1091 Hz (낮게)",
            "· 구급차: 다가오는 동안 거의 일정하게 높고, 옆을 지날 때 빠르게 낮아져 계속 낮다",
            "· 음원 속력 = 음속이면 압력의 벽, 음속보다 빠르면 원뿔 모양 충격파(소닉 붐)",
        ], hold=4.0)
        self.play(FadeOut(p), run_time=0.6)

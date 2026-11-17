"""도플러 효과 ① 파원과 진동수 (교과서 110~111쪽).

구급차 사이렌 → 파원이란? → 스피커 진동판과 공기 → 위에서 본 파면 →
'1초에 귀에 도착하는 파면 수 = 진동수' → f = v/λ (340/0.283 ≈ 1200 Hz) → 정지 파원은 어디서나 같다.
"""
from dkit import *

LAM = 1.0      # 화면 속 파장 (위에서 본 그림)
TP = 1.0       # 화면 속 주기 1 T = 1 초 (실제 1/1200 s)


class D1Source(CaseScene):
    def construct(self):
        self.hook()
        self.sources()
        self.speaker_air()
        self.top_view()
        self.formula()
        self.stationary()
        self.wrap()

    # ------------------------------------------------------------ 0~1. 제목 + 구급차
    def hook(self):
        card = title_card("도플러 효과 ① 파원과 진동수")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.wait(2.4)
        self.play(FadeOut(card), run_time=0.6)

        ROAD = -1.0
        ground = Rectangle(width=16, height=3.3, stroke_width=0, fill_color=GROUND,
                           fill_opacity=0.55).move_to([0, ROAD - 1.65, 0])
        road = Line([-8, ROAD, 0], [8, ROAD, 0], color=GRAY_T, stroke_width=2)
        dashes = VGroup(*[Line([x, ROAD - 0.45, 0], [x + 0.5, ROAD - 0.45, 0], color=GRAY_T,
                               stroke_width=3, stroke_opacity=0.5) for x in np.arange(-7.5, 8, 1.3)])
        man = person(1.25).move_to([0, ROAD + 0.08, 0], aligned_edge=DOWN).shift(UP * 0.35)
        me = T("나", 22, GRAY_T, bold=True).next_to(man, UP, buff=0.12)
        amb = ambulance(2.3).move_to([-8.6, ROAD, 0], aligned_edge=DOWN)
        self.add(ground, road, dashes, man, me)
        self.add(amb)
        self.say("구급차가 내 앞을 지나간다.\n사이렌 소리를 잘 들어 보자", wait=2.8)

        BADGE = [4.6, 2.6, 0]
        hi = sound_badge(1333, ORANGE, "다가올 때: 높은 소리").move_to(BADGE)
        lo = sound_badge(1091, CYAN, "멀어질 때: 낮은 소리").move_to(BADGE)

        def drive(times=1):
            for _ in range(times):
                amb.move_to([-8.6, ROAD, 0], aligned_edge=DOWN)
                self.add(hi)
                self.add_sound(tone(1333, 1.5, vol=0.3), time_offset=0.15)
                self.play(amb.animate.move_to([-1.15, ROAD, 0], aligned_edge=DOWN), run_time=1.9,
                          rate_func=linear)
                self.add_sound(tone((1333, 1091), 0.2, vol=0.3))
                self.play(amb.animate.move_to([1.15, ROAD, 0], aligned_edge=DOWN), run_time=0.45,
                          rate_func=linear)
                self.remove(hi)
                self.add(lo)
                self.add_sound(tone(1091, 1.5, vol=0.3), time_offset=0.0)
                self.play(amb.animate.move_to([8.6, ROAD, 0], aligned_edge=DOWN), run_time=1.9,
                          rate_func=linear)
                self.wait(0.4)
                self.remove(lo)

        self.unsay()
        drive()
        self.add(lo)
        self.say("다가올 때는 높게,\n지나간 뒤에는 낮게 들린다", wait=2.8)
        self.say("사이렌은 늘 같은 소리를 내는데, 왜 다르게 들릴까?", wait=3.3)
        self.say("이 비밀(도플러 효과)을 풀려면\n먼저 '파원'이 무엇인지 알아야 한다", wait=3.6)
        self.clear_all()

    # ------------------------------------------------------------ 2. 파원의 예
    def sources(self):
        h1 = T("파원", 44, CYAN, bold=True)
        h2 = T("= 파동을 만들어 내는 물체", 34, WHITE_T, bold=True)
        h3 = T("(진동하는 물체)", 26, GRAY_T)
        head = VGroup(h1, h2, h3).arrange(RIGHT, buff=0.25, aligned_edge=DOWN).to_edge(UP, buff=0.5)
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.8)

        tt = time_driver(self)
        Y = 0.35
        X = [-4.4, 0.0, 4.4]

        # (가) 스피커: 진동판이 앞뒤로
        sx = X[0] - 1.1

        def spk():
            t = tt.get_value()
            d = 0.07 * np.sin(2 * PI * t / 0.8)
            box = RoundedRectangle(corner_radius=0.06, width=0.55, height=1.5, stroke_color=GRAY_T,
                                   stroke_width=2, fill_color="#1B2A3D", fill_opacity=1).move_to([sx - 0.25, Y, 0])
            cone = Polygon([sx, Y + 0.25, 0], [sx + 0.3 + d, Y + 0.62, 0], [sx + 0.3 + d, Y - 0.62, 0],
                           [sx, Y - 0.25, 0], stroke_color=WHITE_T, stroke_width=2, fill_color="#5B6B7E",
                           fill_opacity=1)
            g = VGroup(box, cone)
            for k in range(6):
                r = 0.75 * (t / 0.8 - k % 100)
            n = int(t / 0.8)
            for k in range(max(0, n - 4), n + 1):
                r = 0.55 + 0.75 * (t - k * 0.8)
                if 0.55 < r < 2.3:
                    g.add(ring_arc([sx, Y, 0], r, RIGHT, 1.1, CYAN, 3.5, 1 - 0.6 * r / 2.3))
            return g

        # (나) 손가락으로 물 치기: 수면파(타원 = 비스듬히 본 원)
        fx, wy = X[1], Y - 0.55

        def finger():
            t = tt.get_value()
            ph = (t / 1.0) % 1.0
            lift = 0.35 * (1 - np.cos(2 * PI * ph)) / 2
            water = Ellipse(width=3.6, height=1.15, stroke_width=0, fill_color=WATER_TOP,
                            fill_opacity=0.9).move_to([fx, wy, 0])
            g = VGroup(water)
            n = int(t)
            for k in range(max(0, n - 4), n + 1):
                r = 0.6 * (t - k)
                if 0.02 < r < 1.75:
                    g.add(Ellipse(width=2 * r, height=2 * r * 0.3, stroke_color=CYAN, stroke_width=3,
                                  stroke_opacity=1 - 0.6 * r / 1.75).move_to([fx, wy, 0]))
            fing = RoundedRectangle(corner_radius=0.11, width=0.24, height=1.0, stroke_color="#C9A27E",
                                    stroke_width=2, fill_color="#E8C9A8", fill_opacity=1)
            fing.move_to([fx, wy + 0.5 + lift, 0])
            g.add(fing)
            return g

        # (다) 소리굽쇠: 두 가지가 떨림
        gx = X[2]

        def fork():
            t = tt.get_value()
            d = 0.05 * np.sin(2 * PI * t / 0.5)
            col = "#B9C4CF"
            pl = Rectangle(width=0.14, height=1.3, stroke_width=0, fill_color=col, fill_opacity=1).move_to(
                [gx - 0.22 - d, Y + 0.35, 0])
            pr = pl.copy().move_to([gx + 0.22 + d, Y + 0.35, 0])
            base = Arc(radius=0.22, start_angle=PI, angle=PI, arc_center=[gx, Y - 0.3, 0], stroke_color=col,
                       stroke_width=9)
            stem = Rectangle(width=0.12, height=0.75, stroke_width=0, fill_color=col, fill_opacity=1).move_to(
                [gx, Y - 0.85, 0])
            g = VGroup(pl, pr, base, stem)
            n = int(t / 0.5)
            for k in range(max(0, n - 6), n + 1):
                r = 0.35 + 0.6 * (t - k * 0.5)
                if 0.35 < r < 1.6:
                    op = 1 - 0.6 * r / 1.6
                    g.add(ring_arc([gx, Y + 0.35, 0], r, RIGHT, 1.0, CYAN, 3, op))
                    g.add(ring_arc([gx, Y + 0.35, 0], r, LEFT, 1.0, CYAN, 3, op))
            return g

        a = always_redraw(spk)
        b = always_redraw(finger)
        c = always_redraw(fork)
        la = VGroup(T("스피커 진동판", 25, WHITE_T, bold=True), T("→ 소리", 22, CYAN)).arrange(DOWN, buff=0.08)
        lb = VGroup(T("물을 톡톡 치는 손가락", 25, WHITE_T, bold=True), T("→ 수면파", 22, CYAN)).arrange(DOWN, buff=0.08)
        lc = VGroup(T("소리굽쇠", 25, WHITE_T, bold=True), T("→ 소리", 22, CYAN)).arrange(DOWN, buff=0.08)
        for l, x in zip((la, lb, lc), X):
            l.move_to([x, -1.55, 0])

        self.say("파원은 파동을 만들어 내는 물체다.\n파원은 모두 '떨고(진동하고)' 있다", wait=0.1)
        self.add(a)
        self.play(FadeIn(la), run_time=0.7)
        self.add(b)
        self.play(FadeIn(lb), run_time=0.7)
        self.add(c)
        self.play(FadeIn(lc), run_time=0.7)
        self.wait(2.6)
        box = SurroundingRectangle(VGroup(la), color=ORANGE, buff=0.12, corner_radius=0.08)
        self.play(Create(box), run_time=0.5)
        self.say("스피커 진동판은 앞뒤로 떨며 공기를 밀고 당긴다 → 소리")
        self.play(Transform(box, SurroundingRectangle(lb, color=ORANGE, buff=0.12, corner_radius=0.08)),
                  run_time=0.5)
        self.say("손가락으로 물을 톡톡 치면 둥근 물결(수면파)이 퍼진다")
        self.play(Transform(box, SurroundingRectangle(lc, color=ORANGE, buff=0.12, corner_radius=0.08)),
                  run_time=0.5)
        self.say("소리굽쇠를 치면 두 가지가 떨며 소리를 낸다")
        self.remove(tt)
        self.clear_all()

    # ------------------------------------------------------------ 3. 스피커와 공기 알갱이
    def speaker_air(self):
        tt = time_driver(self)
        X0, Y = -4.6, 0.25
        PER = 1.3            # 화면 속 주기(초)
        LAMS = 2.3           # 화면 속 파장
        C = LAMS / PER
        A = 0.24
        K = 2 * PI / LAMS
        W = 2 * PI / PER

        xs = np.arange(X0 + 0.35, 6.6, 0.2)
        ys = np.arange(Y - 1.3, Y + 1.31, 0.29)
        rng = np.random.default_rng(3)
        base = []
        dots = VGroup()
        for yy in ys:
            for xx in xs:
                jx, jy = rng.uniform(-0.04, 0.04, 2)
                base.append((xx + jx, yy + jy))
                dots.add(Dot([xx + jx, yy + jy, 0], radius=0.035, color="#8FB3CF"))
        red_i = min(range(len(base)), key=lambda i: (base[i][0] - 0.0) ** 2 + (base[i][1] - Y) ** 2)
        dots[red_i].set_color(RED_T).scale(1.8)

        def disp(x, t):
            if x - X0 > C * t:
                return 0.0
            return A * np.sin(W * t - K * (x - X0))

        LO, HI = ManimColor("#3E5C75"), ManimColor("#CFF4FF")

        def upd(m):
            t = tt.get_value()
            for i, d in enumerate(m):
                bx, by = base[i]
                d.move_to([bx + disp(bx, t), by, 0])
                if i == red_i:
                    continue
                if bx - X0 > C * t:
                    a = 0.45
                else:
                    a = 0.5 + 0.5 * np.cos(W * t - K * (bx - X0))  # 1: 빽빽, 0: 듬성
                d.set_color(interpolate_color(LO, HI, a))

        dots.add_updater(upd)

        def spk():
            t = tt.get_value()
            d = A * np.sin(W * t)
            box = RoundedRectangle(corner_radius=0.08, width=1.0, height=2.9, stroke_color=GRAY_T,
                                   stroke_width=2, fill_color="#1B2A3D", fill_opacity=1).move_to([X0 - 1.05, Y, 0])
            cone = Polygon([X0 - 0.55, Y + 0.45, 0], [X0 + d, Y + 1.2, 0], [X0 + d, Y - 1.2, 0],
                           [X0 - 0.55, Y - 0.45, 0], stroke_color=WHITE_T, stroke_width=2,
                           fill_color="#5B6B7E", fill_opacity=1)
            mem = Line([X0 + d, Y + 1.2, 0], [X0 + d, Y - 1.2, 0], color=ORANGE, stroke_width=6)
            return VGroup(box, cone, mem)

        sp = always_redraw(spk)
        lab = T("진동판", 22, ORANGE, bold=True).move_to([X0 - 0.3, Y + 1.65, 0])
        air = T("공기 알갱이", 22, "#8FB3CF", bold=True).move_to([1.2, Y + 1.75, 0])
        sn = slow_note()
        self.add(sp, dots)
        self.play(FadeIn(lab), FadeIn(air), FadeIn(sn), run_time=0.6)
        self.say("가까이서 보자. 진동판이 앞뒤로 떨면\n바로 앞 공기도 같이 밀리고 당겨진다", wait=3.6)
        self.say("앞으로 밀 때 공기가 빽빽해지고(밀),\n뒤로 당길 때 듬성해진다(소)", wait=3.6)
        # 정지해서 밀·소 표시
        self.wait(max(0.0, (np.ceil((tt.get_value() + 1.2) / PER) * PER + 0.25 * PER) - tt.get_value() - 0.0))
        tt.clear_updaters()
        t0 = tt.get_value()
        marks = VGroup()
        for n in range(0, 6):
            xc = X0 + (W * t0 - 2 * PI * n) / K      # 밀: 위상 0
            xr = xc - LAMS / 2                          # 소
            for xx, s, col in ((xc, "밀", ORANGE), (xr, "소", CYAN)):
                if X0 + 0.6 < xx < 6.4 and xx - X0 < C * t0:
                    t_ = T(s, 24, col, bold=True).move_to([xx, Y - 1.72, 0])
                    marks.add(t_)
        self.play(FadeIn(marks), run_time=0.5)
        self.say("이 빽빽한 부분(밀)과 듬성한 부분(소)이\n옆으로 전달되며 퍼지는 것이 소리다", wait=3.8)
        tt.add_updater(lambda m, dt: m.increment_value(dt))
        self.play(FadeOut(marks), run_time=0.4)
        self.say("빨간 알갱이를 보자. 제자리에서 앞뒤로 떨 뿐,\n소리를 따라 날아가지 않는다", wait=4.2)
        dots.clear_updaters()
        self.remove(tt)
        self.clear_all()

    # ------------------------------------------------------------ 4. 위에서 본 파면, 도착 개수
    def top_view(self):
        S = np.array([-3.3, 0.35, 0])
        E = np.array([3.5, 0.35, 0])
        D = np.linalg.norm(E - S)
        tw = ValueTracker(0)  # 단위: T (단조 증가만)
        hl = []

        waves = always_redraw(lambda: fronts(tw.get_value(), lambda k: S, LAM / TP, 7.6, CYAN, 3, hl=hl))

        def src():
            t = tw.get_value()
            s = 1 + 0.35 * np.sin(2 * PI * t)
            return VGroup(Circle(radius=0.17 * s, stroke_color=ORANGE, stroke_width=2.5).move_to(S),
                          Dot(S, radius=0.09, color=ORANGE))

        sdot = always_redraw(src)
        slab = label_bg(T("파원", 24, ORANGE, bold=True)).next_to(S, DOWN, buff=0.3)
        sn = slow_note()
        clock = Clock(tw, "ms", "{:.2f}", scale=1000 / 1200)
        self.play(FadeIn(sdot), FadeIn(slab), FadeIn(sn), FadeIn(clock), run_time=0.7)
        self.add(waves)
        self.say("이번엔 위에서 내려다보자.\n파원이 떨 때마다 동그란 물결이 퍼진다", wait=0.1)
        self.play(tw.animate.set_value(3.5), run_time=3.5, rate_func=linear)
        self.wait(0.9)

        # 파면 정의
        hl.append(1)
        lbl = label_bg(T("파면", 26, ORANGE, bold=True)).move_to(S + np.array([1.35, 1.95, 0]))
        self.add(lbl)
        self.say("파면: 같은 순간에 출발한 마루를 이은 선.\n동그라미 하나하나가 파면이다")
        hl.clear()
        self.remove(lbl)

        # 진동 1번 = 파면 1개
        cnt = always_redraw(lambda: panel(VGroup(
            T("진동 횟수", 21, GRAY_T), M(f"{int(np.floor(tw.get_value() + 1e-6))}", 34, ORANGE)
        ).arrange(RIGHT, buff=0.25), buff=0.15).move_to([-5.2, 2.6, 0]))
        self.add(cnt)
        self.say("한 번 진동할 때(주기 T)마다 파면이 하나씩 생긴다", wait=0.1)
        self.play(tw.animate.set_value(5.0), run_time=1.5, rate_func=linear)
        self.wait(1.8)
        self.remove(cnt)

        # 파장, 속력 (tw = 5.0: 반지름 5,4,3,2,1)
        yy = S[1] - 0.0
        dl = dim_line(S + RIGHT * 2.0 + DOWN * 0.0, S + RIGHT * 3.0, "", color=WHITE_T)
        lam_t = label_bg(T("λ (파장)", 24, CYAN, bold=True)).next_to(dl, DOWN, buff=0.14)
        self.play(Create(dl), FadeIn(lam_t), run_time=0.7)
        self.say("이웃한 파면 사이 간격 = 파장 λ\n(이 소리는 약 0.283 m ≈ 28 cm)")
        ang = 0.42
        p0 = S + 4.0 * np.array([np.cos(ang), np.sin(ang), 0])
        ar = Arrow(p0 - 0.05 * np.array([np.cos(ang), np.sin(ang), 0]), p0 + 0.95 * np.array([np.cos(ang), np.sin(ang), 0]),
                   buff=0, color=ORANGE, stroke_width=5, tip_length=0.2)
        vt = label_bg(T("v = 340 m/s", 24, ORANGE, bold=True)).next_to(ar.get_end(), RIGHT, buff=0.1)
        self.play(GrowArrow(ar), FadeIn(vt), run_time=0.7)
        self.say("파면은 모든 방향으로 같은 속력 v로 퍼진다\n(공기 속 소리: 340 m/s)")
        self.play(FadeOut(dl), FadeOut(lam_t), FadeOut(ar), FadeOut(vt), run_time=0.5)

        # 귀에 도착하는 파면 세기
        ear = ear_icon(h=0.7).move_to(E + RIGHT * 0.25)
        elab = label_bg(T("귀(관찰자)", 22, "#E8C9A8", bold=True)).next_to(ear, UP, buff=0.15)
        T_START = D - 0.5  # 측정 시작 시각 (첫 파면 도착 0.5T 전)

        def glow():
            t = tw.get_value()
            ph = (t - D) % 1.0
            on = t >= D - 1e-6 and ph < 0.22
            return Circle(radius=0.45, stroke_color=GREEN, stroke_width=5,
                          stroke_opacity=(1 - ph / 0.22) if on else 0).move_to(ear)

        g = always_redraw(glow)

        def counter():
            t = tw.get_value()
            el = min(max(t - T_START, 0), 6.0)
            n = 0 if t < D else int(np.floor(min(t, T_START + 6.0 - 1e-6) - D + 1e-6)) + 1
            n = max(0, min(n, 6))
            l1 = VGroup(T("도착한 파면", 21, GRAY_T), M(f"{n} 개", 32, GREEN)).arrange(RIGHT, buff=0.22)
            l2 = VGroup(T("세는 시간", 21, GRAY_T), M(f"{el:.1f} T", 32, WHITE_T)).arrange(RIGHT, buff=0.22)
            l2.align_to(l1, RIGHT)
            body = VGroup(l1, l2).arrange(DOWN, buff=0.14, aligned_edge=RIGHT)
            return panel(body, buff=0.18).move_to([4.6, -1.45, 0])

        cn = always_redraw(counter)
        self.play(FadeIn(ear), FadeIn(elab), run_time=0.6)
        self.add(g)
        self.say("귀에 와 닿는 파면을 세어 보자", wait=0.1)
        self.play(tw.animate.set_value(T_START), run_time=(T_START - 5.0), rate_func=linear)
        self.add(cn)
        self.say("파면 하나가 닿을 때마다 고막이 한 번 떤다", wait=0.1)
        self.play(tw.animate.set_value(T_START + 6.0), run_time=6.0, rate_func=linear)
        self.say("6T 동안 6개가 도착했다.\n1초는 1200T이므로 1초 동안 1200개가 도착한다")

        # 핵심 한 줄 (크게)
        self.play(FadeOut(sn), FadeOut(clock), run_time=0.4)
        k1 = T("들리는 진동수", 40, GREEN, bold=True)
        k2 = T("=  1초 동안 귀에 도착하는 파면의 개수", 34, WHITE_T, bold=True)
        key = VGroup(k1, k2).arrange(DOWN, buff=0.2)
        kp = panel(key, buff=0.4).to_edge(UP, buff=0.3)
        kp[0].set_stroke(GREEN, 2.5)
        self.play(FadeIn(kp, shift=DOWN * 0.2), run_time=0.8)
        self.say("이것이 오늘의 핵심이다.\n1초에 1200개 도착 → 1200 Hz로 들린다", wait=4.2)
        self.remove(waves, sdot, g, cn)
        self.clear_all()

    # ------------------------------------------------------------ 5. f = v / λ
    def formula(self):
        Y = 1.9
        x0, x1 = -5.6, 5.6
        bar = Line([x0, Y, 0], [x1, Y, 0], color=ORANGE, stroke_width=4)
        t1 = T("1초 동안 소리가 가는 거리 = 340 m", 26, ORANGE, bold=True).next_to(bar, UP, buff=0.25)
        self.play(Create(bar), FadeIn(t1), run_time=1.0)
        self.say("1초 동안 소리는 340 m를 간다.\n그 안에 파면이 λ 간격으로 줄지어 있다", wait=0.1)
        w = 0.42
        cells = VGroup()
        for i in range(12):
            x = x0 + i * w
            cells.add(Line([x, Y - 0.22, 0], [x, Y + 0.22, 0], color=CYAN, stroke_width=3))
        cells.add(*[Line([x, Y - 0.22, 0], [x, Y + 0.22, 0], color=CYAN, stroke_width=3)
                    for x in (x1 - 2 * w, x1 - w, x1)])
        dots = T("· · ·", 30, CYAN, bold=True).move_to([(x0 + 12 * w + x1 - 2 * w) / 2, Y - 0.55, 0])
        self.play(LaggedStart(*[Create(c) for c in cells], lag_ratio=0.08), FadeIn(dots), run_time=1.8)
        dl = dim_line([x0, Y - 0.5, 0], [x0 + w, Y - 0.5, 0], "", color=CYAN)
        lt = T("λ", 26, CYAN, bold=True).next_to(dl, DOWN, buff=0.08)
        self.play(FadeIn(dl), FadeIn(lt), run_time=0.5)
        self.wait(1.6)
        self.say("파면 개수 = 340 m 안에 λ가 몇 번 들어가나\n= 340 ÷ λ")

        r1 = row(sym("f", None, C_F), "=", fr([sym("v", None, C_V)], [sym("λ", None, C_L)]))
        r2 = row("=", fr([("340 m/s", C_V)], [("0.283 m", C_L)]), ("≈ 1200 Hz", C_F))
        r2.next_to(r1, RIGHT, buff=0.3)
        body = VGroup(r1, r2)
        note1 = T("(f: 진동수, v: 소리 속력, λ: 파장)", 21, GRAY_T).next_to(body, DOWN, buff=0.3)
        body.add(note1)
        pnl = panel(body, buff=0.35).move_to([0, -0.45, 0])
        self.play(FadeIn(pnl[0]), FadeIn(r1), FadeIn(note1), run_time=0.8)
        self.say("그래서 진동수 f = v / λ", wait=2.6)
        self.play(FadeIn(r2[0]), FadeIn(r2[1]), run_time=0.8)
        self.say("v에 (340 m/s), λ에 (0.283 m)를 넣으면", wait=2.8)
        self.play(FadeIn(r2[2], shift=LEFT * 0.2), run_time=0.6)
        self.say("약 1200 Hz. 교과서 탐구의 음원과 같은 소리다")
        bd = sound_badge(1200, GREEN, "f = 1200 Hz").move_to([4.8, -2.05, 0])
        bd.next_to(pnl, DOWN, buff=0.2).set_x(0)
        self.unsay()
        self.play(FadeIn(bd), run_time=0.3)
        play_beep(self, 1200, 1.3, bd, extra=0.4)
        self.play(FadeOut(bd), run_time=0.3)
        self.say("파장이 짧을수록(파면이 빽빽할수록)\n1초에 더 많이 도착 → 더 높은 소리", wait=4.0)
        self.clear_all()

    # ------------------------------------------------------------ 6. 정지한 파원: A, B 모두 같다
    def stationary(self):
        S = np.array([0, 0.45, 0])
        A = np.array([4.9, 0.45, 0])
        B = np.array([-4.9, 0.45, 0])
        tt = time_driver(self)
        waves = always_redraw(lambda: fronts(tt.get_value(), lambda k: S, LAM, 4.6, CYAN, 3))
        sd = VGroup(Dot(S, radius=0.1, color=ORANGE))
        sl = label_bg(T("파원 (정지)", 22, ORANGE, bold=True)).next_to(S, DOWN, buff=0.2)
        pa = person(0.95).move_to(A + DOWN * 0.45, aligned_edge=DOWN)
        pb = person(0.95).move_to(B + DOWN * 0.45, aligned_edge=DOWN)
        la = T("A", 30, WHITE_T, bold=True).next_to(pa, UP, buff=0.12)
        lb = T("B", 30, WHITE_T, bold=True).next_to(pb, UP, buff=0.12)
        self.add(waves)
        self.play(FadeIn(sd), FadeIn(sl), FadeIn(pa), FadeIn(pb), FadeIn(la), FadeIn(lb), run_time=0.8)
        self.say("파원이 가만히 있으면, 오른쪽 A와 왼쪽 B에서\n파면 간격은 어떨까?", wait=4.6)
        # tt 를 정수 + 0.0 에서 멈춰 치수선 표시
        nxt = np.ceil(tt.get_value() + 0.6)
        self.wait(nxt - tt.get_value())
        tt.clear_updaters()
        tt.set_value(nxt)
        r_ = 2.0
        dA = dim_line(S + RIGHT * 2.0 + DOWN * 1.15, S + RIGHT * 3.0 + DOWN * 1.15, "", color=WHITE_T)
        dB = dim_line(S + LEFT * 3.0 + DOWN * 1.15, S + LEFT * 2.0 + DOWN * 1.15, "", color=WHITE_T)
        tA = label_bg(T("λ", 26, CYAN, bold=True)).next_to(dA, DOWN, buff=0.1)
        tB = label_bg(T("λ", 26, CYAN, bold=True)).next_to(dB, DOWN, buff=0.1)
        self.play(Create(dA), Create(dB), FadeIn(tA), FadeIn(tB), run_time=0.8)
        self.say("모든 방향으로 간격이 똑같이 λ다", wait=2.8)
        tt.add_updater(lambda m, dt: m.increment_value(dt))
        self.play(FadeOut(dA), FadeOut(dB), FadeOut(tA), FadeOut(tB), run_time=0.4)
        bA = sound_badge(1200, GREEN, "A가 듣는 소리").next_to(pa, DOWN, buff=0.25).shift(LEFT * 0.4)
        bB = sound_badge(1200, GREEN, "B가 듣는 소리").next_to(pb, DOWN, buff=0.25).shift(RIGHT * 0.4)
        self.say("A도 B도 1초에 1200개씩 받는다 → 둘 다 1200 Hz", wait=0.1)
        self.play(FadeIn(bA), run_time=0.3)
        play_beep(self, 1200, 1.2, bA, extra=0.2)
        self.play(FadeIn(bB), run_time=0.3)
        play_beep(self, 1200, 1.2, bB, extra=0.6)
        self.say("그런데 파원이 움직이면 어떻게 될까? → ②편에서", wait=3.0)
        self.remove(tt)
        self.clear_all()

    # ------------------------------------------------------------ 7. 정리
    def wrap(self):
        p = summary(self, "① 파원과 진동수 정리", [
            "· 파원: 파동을 만들어 내는 물체 (진동하는 물체)",
            "· 파면: 같은 순간에 출발한 마루를 이은 선 — 한 번 진동에 하나",
            "· 파면 사이 간격 = 파장 λ, 파면이 퍼지는 속력 = v",
            "· 들리는 진동수 = 1초 동안 귀에 도착하는 파면의 개수",
            "· f = v / λ = 340 / 0.283 ≈ 1200 Hz",
            "· 파원이 정지해 있으면 어느 방향에서나 같은 진동수",
        ], hold=4.0)
        self.play(FadeOut(p), run_time=0.6)

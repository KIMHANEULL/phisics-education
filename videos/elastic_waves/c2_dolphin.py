"""사례 2. 돌고래의 반향정위(에코로케이션) — 물속 초음파로 물고기 떼까지의 거리 재기."""
from common import *

SEA_SURF = 4.25  # 수면을 화면 밖 위로 → 화면 전체가 물속


class Capped:
    """시계·시간축용: 파동 tracker 가 지나가도 cap 에서 멈추는 값."""

    def __init__(self, tr, cap):
        self.tr, self.cap = tr, cap

    def get_value(self):
        return min(self.tr.get_value(), self.cap)


# ---------------------------------------------------------------- 그림
def _smooth_closed(pts, **style):
    m = VMobject(**style)
    p = [np.array([x, y, 0]) for x, y in pts]
    m.set_points_smoothly(p + [p[0]])
    return m


def dolphin_shape():
    """오른쪽을 보는 돌고래 옆모습. 국소 좌표(원점 = 몸 가운데), 길이 약 3.5."""
    body_pts = [(-1.55, 0.03), (-1.2, 0.12), (-0.7, 0.31), (-0.1, 0.45), (0.45, 0.43),
                (0.78, 0.33), (0.98, 0.2), (1.1, 0.07), (1.3, 0.02), (1.5, -0.01),
                (1.53, -0.05), (1.45, -0.09), (1.15, -0.13), (0.7, -0.23), (0.2, -0.34),
                (-0.4, -0.33), (-0.95, -0.21), (-1.35, -0.08), (-1.56, -0.03)]
    st = dict(stroke_color="#DDE7F0", stroke_width=1.6)
    body = _smooth_closed(body_pts, **st)
    body.set_fill(color=["#C9D6E2", "#6F8BA4"], opacity=1)
    body.set_sheen_direction(UP)
    dorsal = _smooth_closed([(-0.05, 0.43), (-0.3, 0.68), (-0.62, 0.9), (-0.56, 0.66),
                             (-0.62, 0.36)], **st).set_fill("#6F8BA4", 1)
    pect = _smooth_closed([(0.38, -0.2), (0.2, -0.45), (-0.06, -0.62), (0.02, -0.4),
                           (0.12, -0.24)], **st).set_fill("#7D97AE", 1)
    fluke = _smooth_closed([(-1.5, 0.02), (-1.72, 0.2), (-2.02, 0.32), (-1.86, 0.06),
                            (-1.98, -0.17), (-1.7, -0.1), (-1.5, -0.03)], **st)
    fluke.set_fill("#6F8BA4", 1)
    eye = Dot([0.8, 0.04, 0], radius=0.035, color="#0B1626")
    mouth = VMobject(stroke_color="#3B5268", stroke_width=1.8)
    mouth.set_points_smoothly([np.array(p) for p in
                               [[1.47, -0.06, 0], [1.2, -0.07, 0], [0.98, -0.04, 0]]])
    blow = Line([0.42, 0.44, 0], [0.5, 0.43, 0], stroke_color="#2E445A", stroke_width=2.5)
    return VGroup(fluke, dorsal, pect, body, eye, mouth, blow)


def fish_shape(scale=1.0, color="#B9D7C4", face=LEFT):
    b = Ellipse(width=0.42, height=0.17, fill_color=color, fill_opacity=0.95,
                stroke_color=WHITE_T, stroke_width=1)
    t = Polygon([0.18, 0, 0], [0.33, 0.1, 0], [0.33, -0.1, 0], fill_color=color,
                fill_opacity=0.95, stroke_color=WHITE_T, stroke_width=1)
    e = Dot([-0.12, 0.02, 0], radius=0.018, color="#0B1626")
    g = VGroup(t, b, e).scale(scale)
    if face[0] > 0:
        g.flip(UP)
    return g


FISH_OFFS = [(-0.35, 0.3), (0.15, 0.45), (0.55, 0.2), (-0.1, 0.05), (0.4, -0.15),
             (-0.45, -0.2), (0.05, -0.38), (0.6, -0.48), (-0.3, -0.6), (0.85, 0.0)]


def fish_school(center):
    g = VGroup()
    cols = ["#B9D7C4", "#C9E0D0", "#A8C9B6"]
    for i, (dx, dy) in enumerate(FISH_OFFS):
        f = fish_shape(0.9 + 0.15 * ((i * 7) % 3) / 2, cols[i % 3])
        f.move_to(np.array(center) + np.array([dx, dy, 0]))
        g.add(f)
    return g


def sea_decor():
    """위에서 비치는 빛줄기 + 떠다니는 알갱이."""
    g = VGroup()
    for x, w in [(-5.0, 1.3), (-1.5, 0.9), (2.2, 1.5), (5.5, 1.0)]:
        p = Polygon([x - w / 2, 4.3, 0], [x + w / 2, 4.3, 0], [x + w * 1.4 - 1.2, -2.2, 0],
                    [x - w * 0.4 - 1.2, -2.2, 0], stroke_width=0)
        p.set_fill(color=["#3FD3FF", "#0F3550"], opacity=0.05).set_sheen_direction(DOWN)
        g.add(p)
    rng = np.random.default_rng(3)
    for _ in range(38):
        x, y = rng.uniform(-7, 7), rng.uniform(-2.0, 4.0)
        g.add(Dot([x, y, 0], radius=rng.uniform(0.01, 0.025), color="#8FB8D0",
                  fill_opacity=rng.uniform(0.15, 0.4)))
    return g


class C2Dolphin(CaseScene):
    def construct(self):
        bg = VGroup(sea_bg(SEA_SURF), sea_decor())
        self.add(bg)

        S0, P0 = 0.95, np.array([-4.75, 0.25, 0])      # 기본 크기·위치
        S1, P1 = 2.4, np.array([-1.65, 0.15, 0])       # 확대

        def W(local, S=S0, P=P0):
            return P + S * np.array([local[0], local[1], 0])

        dol = dolphin_shape().scale(S0, about_point=ORIGIN).shift(P0)
        FISH = np.array([3.6, 0.25, 0])
        school = fish_school(FISH)

        # 0. 제목
        card = title_card("돌고래의 반향정위(에코로케이션)", case_no=2)
        self.play(FadeIn(dol, shift=RIGHT * 0.4), FadeIn(school, shift=LEFT * 0.2), run_time=1)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.wait(2.4)
        self.play(FadeOut(card), run_time=0.6)

        # 1. 등장 요소
        cd = callout(W((0.3, 0.45)), "돌고래", "물속에서 초음파를 낸다", UP + RIGHT * 0.6, 1.0)
        cf = callout(FISH + np.array([0.2, 0.45, 0]), "물고기 떼", "먹이 (목표물)", UP + RIGHT * 0.3, 0.7)
        self.play(Create(cd), run_time=0.8)
        self.play(Create(cf), run_time=0.8)
        self.say("돌고래는 '딸깍딸깍' 짧은 초음파(클릭음)를\n아주 빠르게 이어서 낸다")
        self.say("탁하고 어두운 물속에서도 되돌아온 소리(메아리)로\n먹이를 찾는다 → 반향정위(에코로케이션)")
        self.play(FadeOut(cd), FadeOut(cf), run_time=0.5)

        # 2. 몸속 구조 확대: 콧속 → 멜론 → 앞으로 / 아래턱 → 속귀
        self.unsay()
        self.play(dol.animate.scale(S1 / S0, about_point=P0).shift(P1 - P0),
                  FadeOut(school), run_time=1.5)
        Wb = lambda p: W(p, S1, P1)
        LIPS = (0.5, 0.3)
        lips = Dot(Wb(LIPS), radius=0.08, color=CYAN)
        melon = Ellipse(width=0.5 * S1, height=0.3 * S1, stroke_color=ORANGE, stroke_width=2,
                        fill_color="#FFD27A", fill_opacity=0.35).move_to(Wb((0.9, 0.16)))
        melon.rotate(-0.35)
        c_lips = callout(Wb(LIPS), "콧속 (소리 입술)", "여기서 '딸깍' 소리를 만든다",
                         UP + RIGHT * 0.25, 1.0, color=CYAN)
        self.play(FadeIn(lips, scale=2), Create(c_lips), run_time=0.9)
        # 작은 딸깍 펄스
        for _ in range(2):
            r = Circle(radius=0.08, color=CYAN, stroke_width=3).move_to(lips)
            self.play(r.animate.scale(3.2).set_stroke(opacity=0), run_time=0.45)
            self.remove(r)
        self.say("① 숨구멍 아래 콧속(소리 입술)에서 '딸깍' 소리를 만든다", wait=2.4)

        self.play(FadeOut(c_lips), run_time=0.4)
        c_mel = callout(Wb((1.02, 0.25)), "멜론", "이마의 지방 덩어리 — 소리를 앞으로 모은다",
                        UP + RIGHT * 0.9, 0.9)
        self.play(FadeIn(melon), Create(c_mel), run_time=1)
        # 광선: 콧속에서 퍼져 → 멜론을 지나며 모여 → 앞으로 나란히
        rays = VGroup()
        tip = Wb((1.55, 0.0))
        for k, dy in enumerate([-0.12, -0.06, 0.0, 0.06, 0.12]):
            a = Wb(LIPS)
            b = Wb((0.74, 0.16 + dy * 1.6))
            c = Wb((1.12, 0.12 + dy * 0.35))
            d = c + RIGHT * (tip[0] + 3.0 - c[0])
            ray = VMobject(stroke_color=CYAN, stroke_width=2.5).set_points_as_corners([a, b, c, d])
            rays.add(ray)
        self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.12), run_time=2)
        self.say("② 이마의 '멜론'이 렌즈처럼 소리를 모아\n앞쪽으로 좁게 내보낸다")
        tw0 = ValueTracker(0)
        beam = always_redraw(lambda: VGroup(*[
            ring_arc(tip, r, RIGHT, 0.7, CYAN, 4, max(0.0, 1 - r / 3.4))
            for r in [tw0.get_value() - 0.45 * k for k in range(4)] if 0.05 < r < 3.4]))
        self.add(beam)
        self.play(tw0.animate.set_value(4.8), run_time=2.2, rate_func=linear)
        self.remove(beam)
        self.play(FadeOut(rays), FadeOut(c_mel), run_time=0.6)

        # 아래턱 → 속귀
        jaw_path = VMobject(stroke_color=ORANGE, stroke_width=6)
        jaw_path.set_points_smoothly([Wb((1.4, -0.09)), Wb((1.1, -0.12)), Wb((0.82, -0.12)),
                                      Wb((0.66, -0.04))])
        ear = Dot(Wb((0.66, -0.04)), radius=0.08, color=GREEN)
        twb = ValueTracker(0)
        jaw_pt = Wb((1.35, -0.1))
        incoming = always_redraw(lambda: VGroup(*[
            ring_arc(jaw_pt + RIGHT * 3.4, r, LEFT, 0.7, ORANGE, 4, 0.9)
            for r in [twb.get_value() - 0.45 * k for k in range(4)] if 0.05 < r < 3.3]))
        self.add(incoming)
        self.say("③ 물고기에서 되돌아온 메아리는…", wait=0.2)
        self.play(twb.animate.set_value(4.6), run_time=2.2, rate_func=linear)
        self.remove(incoming)
        c_jaw = callout(Wb((1.15, -0.12)), "아래턱", "지방이 찬 턱뼈가 소리를 받는다",
                        DOWN + RIGHT * 0.8, 0.9)
        self.play(Create(jaw_path), Create(c_jaw), run_time=1.2)
        c_ear = callout(Wb((0.66, -0.04)), "속귀", "소리를 느낀다", UP + RIGHT * 0.12, 1.75,
                        color=GREEN)
        self.play(FadeIn(ear, scale=2), Create(c_ear), run_time=0.8)
        self.say("③ 아래턱으로 받아서 속귀로 전한다\n(아래턱 → 속귀)")
        self.wait(0.6)

        # 다시 원래 크기
        self.play(FadeOut(VGroup(lips, melon, jaw_path, ear, c_jaw, c_ear)), run_time=0.5)
        self.unsay()
        self.play(dol.animate.shift(P0 - P1).scale(S0 / S1, about_point=P0),
                  FadeIn(school), run_time=1.4)

        # 3. 물속 음속 비교
        L_W = 6.0
        bar_air = Rectangle(width=L_W * 340 / 1500, height=0.32, stroke_width=0,
                            fill_color=GRAY_T, fill_opacity=0.9)
        bar_wat = Rectangle(width=L_W, height=0.32, stroke_width=0, fill_color=CYAN,
                            fill_opacity=0.9)
        la = T("공기", 24, GRAY_T, bold=True)
        lw = T("물", 24, CYAN, bold=True)
        rows = VGroup()
        for lab, bar, val, col in [(la, bar_air, "약 340 m/s", GRAY_T),
                                   (lw, bar_wat, "약 1500 m/s", CYAN)]:
            rows.add(VGroup(lab, bar, T(val, 24, col, bold=True)))
        for r in rows:
            r[0].move_to(ORIGIN)
        rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        for r in rows:
            r[0].move_to([rows.get_left()[0] + 0.3, r[0].get_center()[1], 0])
            r[1].next_to([rows.get_left()[0] + 0.75, r[0].get_center()[1], 0], RIGHT, buff=0)
            r[2].next_to(r[1], RIGHT, buff=0.2)
        head = T("음속 비교", 22, GRAY_T)
        times = T("1500 ÷ 340 ≈ 4.4배 빠르다", 24, GREEN, bold=True)
        sp_body = VGroup(head, rows, times).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        sp_pnl = panel(sp_body, buff=0.3, pos=[0.9, 2.45, 0])
        for r in rows:
            r[1].save_state()
            r[1].stretch(0.01, 0, about_edge=LEFT)
        self.play(FadeIn(sp_pnl[0]), FadeIn(head), FadeIn(VGroup(rows[0][0], rows[1][0])),
                  run_time=0.6)
        self.play(Restore(rows[0][1]), FadeIn(rows[0][2]), run_time=0.8)
        self.wait(1.2)
        self.play(Restore(rows[1][1]), FadeIn(rows[1][2]), run_time=1.2)
        self.wait(1.0)
        self.play(FadeIn(times, shift=UP * 0.1), run_time=0.6)
        self.say("물속에서는 소리가 공기보다 약 4.4배 빠르다\n(물은 공기보다 훨씬 압축되기 어려워 소리가 빨리 전해진다)")
        self.play(FadeOut(sp_pnl), FadeOut(head), FadeOut(rows), FadeOut(times), run_time=0.6)

        # 4. 송신 → 반사 → 수신 (시간 측정)
        TRIP = 20.0  # 한 방향 (ms) : 30 m / 1500 m/s
        tw = ValueTracker(0)          # 파동용 (지나가도 됨)
        tclk = Capped(tw, 2 * TRIP)   # 시계·시간축용 (40 ms 에서 멈춤)
        src = W((1.6, 0.0))
        tgt = FISH + np.array([-0.55, 0.0, 0])
        D = np.linalg.norm(tgt - src)
        waves = always_redraw(lambda: echo_group(tw.get_value() / TRIP * D, src, tgt,
                                                 0.3, 5, 0.8, 1.0))
        clock = Clock(tclk, "ms", "{:.1f}")
        tl = Timeline(50, 10, tclk, "ms")
        sn = slow_note("※ 실제보다 아주 느리게 보여 줌 · 거리는 줄여서 그림")
        self.play(FadeIn(sn), FadeIn(clock), FadeIn(tl), run_time=0.8)
        m0 = tl.marker(0, "신호 발신 시각", ORANGE)
        self.play(FadeIn(m0), run_time=0.4)
        self.say("클릭음을 내는 순간 시간을 0으로 놓는다", wait=0.4)
        self.add(waves)
        self.play(tw.animate.set_value(TRIP), run_time=4.2, rate_func=linear)
        refl = callout(FISH + np.array([-0.3, 0.45, 0]), "물고기 떼에서 반사", None, UP + LEFT * 0.4, 0.7)
        self.play(FadeIn(refl), run_time=0.4)
        self.say("물고기 떼에 부딪힌 초음파가 반사되어 되돌아온다", wait=0.2)
        self.play(tw.animate.set_value(2 * TRIP), run_time=4.2, rate_func=linear)
        # 남은 고리가 빠져나가는 동안 시계는 40.0 에서 멈춰 있다
        rcv = callout(W((1.2, -0.13)), "아래턱으로 수신", None, DOWN * 0.45 + RIGHT, 0.6)
        m1 = tl.marker(2 * TRIP, "신호 수신 시각", GREEN)
        self.play(tw.animate.set_value(2 * TRIP + 3.9), FadeIn(rcv), FadeIn(m1), FadeOut(refl),
                  run_time=0.82, rate_func=linear)
        self.remove(waves)
        sp = tl.span(0, 2 * TRIP, "시간 차 = 40 ms").shift(UP * 0.75)
        self.play(FadeIn(sp), run_time=0.6)
        self.say("보낸 시각과 받은 시각의 차이 = 시간 차 40 ms (= 0.040 s)")
        self.play(FadeOut(rcv), run_time=0.4)

        # 5. 갔다가 되돌아온 경로
        go = Arrow(src + UP * 0.38, tgt + UP * 0.38, buff=0, color=CYAN, stroke_width=4,
                   tip_length=0.2)
        back = Arrow(tgt + DOWN * 0.38, src + DOWN * 0.38, buff=0, color=ORANGE,
                     stroke_width=4, tip_length=0.2)
        lg = T("갈 때", 22, CYAN, bold=True).next_to(go, UP, buff=0.08)
        lb = T("올 때", 22, ORANGE, bold=True).next_to(back, UP, buff=0.06)
        self.play(GrowArrow(go), FadeIn(lg), run_time=1)
        self.play(GrowArrow(back), FadeIn(lb), run_time=1)
        self.say("이 40 ms 동안 초음파는 물고기까지 갔다가 다시 왔다\n→ 실제로 움직인 길이는 '거리의 2배'")

        # 6. 공식
        f1 = distance_formula()
        nt = T("← 갔다가 되돌아왔으니 2로 나눈다", 20, GRAY_T)
        r1 = VGroup(f1, nt).arrange(RIGHT, buff=0.35)
        f2n = colored([("(1500 m/s)", ORANGE), ("×", WHITE_T), ("(0.040 s)", GREEN)])
        f2 = frac(f2n, colored([("2", WHITE_T)]))
        mid = colored([("=", WHITE_T), ("60 m", WHITE_T), ("÷ 2", WHITE_T)])
        res = T("= 30 m", 34, GREEN, bold=True)
        r2 = eq_row("=", f2, mid, res)
        r2.next_to(r1, DOWN, buff=0.35, aligned_edge=LEFT).shift(RIGHT * 1.15)
        rt = T("왕복한 길이", 18, GRAY_T).next_to(mid[1], DOWN, buff=0.12)
        body = VGroup(r1, r2, rt)
        pnl = panel(body, buff=0.28, pos=[0.9, 2.55, 0]).to_edge(UP, buff=0.3)
        self.play(FadeOut(sn), FadeOut(clock), FadeOut(go), FadeOut(lg), FadeOut(back),
                  FadeOut(lb), FadeIn(pnl[0]), Write(r1), run_time=1.2)
        self.wait(1.4)
        self.play(FadeIn(r2[0]), FadeIn(f2), run_time=1)
        self.say("물속 음속(1500 m/s)과 시간 차(0.040 s)를 대입한다\n(단위: m/s × s = m)", wait=4.4)
        self.play(FadeIn(mid), FadeIn(rt), run_time=0.8)
        self.say("1500 × 0.040 = 60 m … 이것은 갔다 온 왕복 길이", wait=2.6)
        self.play(FadeIn(res, shift=LEFT * 0.2), run_time=0.7)
        dl = dim_line(src + DOWN * 0.55, tgt + DOWN * 0.55, "30 m", offset=UP * 0.3)
        self.play(Create(dl), run_time=1)
        self.say("2로 나누면 물고기 떼까지의 거리는 30 m")
        self.say("물고기가 2배 멀면(60 m) 메아리도 2배 늦게(80 ms) 온다\n→ 거리와 시간 차는 비례한다")
        self.wait(0.5)

        # 7. 같은 30 m, 공기였다면?
        self.clear_all(keep=(bg,))
        head = T("같은 30 m 를 공기 속에서 잰다면?", 30, WHITE_T, bold=True)
        fw = VGroup(T("물속", 24, CYAN, bold=True),
                    colored([("시간 차 =", WHITE_T), ("2 × 30 m", WHITE_T), ("÷", WHITE_T),
                             ("(1500 m/s)", ORANGE), ("= 0.040 s", GREEN)], 26))
        fa = VGroup(T("공기", 24, GRAY_T, bold=True),
                    colored([("시간 차 =", WHITE_T), ("2 × 30 m", WHITE_T), ("÷", WHITE_T),
                             ("(340 m/s)", ORANGE), ("≈ 0.176 s", GREEN)], 26))
        for r in (fw, fa):
            r.arrange(RIGHT, buff=0.3)
            r[0].set_width(r[0].width)
        fw[1].next_to(fw[0], RIGHT, buff=0.5)
        fa[1].next_to(fa[0], RIGHT, buff=0.5)
        fa[1].align_to(fw[1], LEFT)
        # 막대 시간축 0~200 ms (같은 화면 속도로 자라게)
        X0, X1 = -3.6, 4.4
        TMAX = 200.0
        xo = lambda t: X0 + (X1 - X0) * t / TMAX
        axis_y = -1.15
        ax = Line([X0, axis_y, 0], [X1 + 0.2, axis_y, 0], color=GRAY_T, stroke_width=2)
        tks = VGroup(*[VGroup(Line([xo(t), axis_y - 0.06, 0], [xo(t), axis_y + 0.06, 0],
                                   color=GRAY_T, stroke_width=2),
                              T(f"{t}", 21, GRAY_T).move_to([xo(t), axis_y - 0.3, 0]))
                       for t in range(0, 201, 40)])
        axl = T("시간 (ms)", 18, GRAY_T).next_to(ax, RIGHT, buff=0.12)
        yw, ya = 0.2, -0.45
        nw = T("물속", 22, CYAN, bold=True).next_to([X0, yw, 0], LEFT, buff=0.2)
        na = T("공기", 22, GRAY_T, bold=True).next_to([X0, ya, 0], LEFT, buff=0.2)
        tb = ValueTracker(0)
        bars = always_redraw(lambda: VGroup(
            Line([X0, yw, 0], [xo(max(min(tb.get_value(), 40), 0.01)), yw, 0], color=CYAN,
                 stroke_width=16),
            Line([X0, ya, 0], [xo(max(min(tb.get_value(), 176), 0.01)), ya, 0], color=GRAY_T,
                 stroke_width=16)))
        top = VGroup(head, fw, fa).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fw[1].align_to(fa[1], LEFT)
        top.move_to([0.2, 2.35, 0])
        cmp_pnl = panel(VGroup(top, ax, tks, axl, nw, na), buff=0.4)
        self.play(FadeIn(cmp_pnl[0]), FadeIn(head), run_time=0.8)
        self.wait(1.2)
        self.play(FadeIn(fw), run_time=0.8)
        self.say("시간 차 = 2 × 거리 ÷ 음속 → 물속: 0.040 s (40 ms)", wait=2.6)
        self.play(FadeIn(fa), run_time=0.8)
        self.say("공기: 2 × 30 ÷ 340 ≈ 0.176 s (176 ms)", wait=2.8)
        self.play(FadeIn(ax), FadeIn(tks), FadeIn(axl), FadeIn(nw), FadeIn(na), run_time=0.6)
        self.add(bars)
        self.say("두 메아리가 돌아오는 시각을 나란히 비교하면", wait=0.2)
        self.play(tb.animate.set_value(176), run_time=4.8, rate_func=linear)
        lw_ = T("40 ms", 22, CYAN, bold=True).next_to([xo(40), yw, 0], RIGHT, buff=0.15)
        la_ = T("176 ms", 22, WHITE_T, bold=True).next_to([xo(176), ya, 0], RIGHT, buff=0.15)
        self.play(FadeIn(lw_), FadeIn(la_), run_time=0.6)
        self.say("물속에서는 메아리가 약 4.4배 빨리 돌아온다\n→ 음속이 빠를수록 같은 거리의 시간 차가 짧다")
        self.wait(0.6)

        # 8. 정리
        self.clear_all(keep=(bg,))
        summ = VGroup(
            T("돌고래 정리", 30, CYAN, bold=True),
            T("· 콧속에서 클릭음 → 멜론이 앞으로 모음 → 메아리는 아래턱 → 속귀", 26),
            T("· 물속 음속: 약 1500 m/s (공기 340 m/s 의 약 4.4배)", 26),
            T("· 시간 차 40 ms → 거리 = 1500 × 0.040 ÷ 2 = 30 m", 26),
            T("· 같은 30 m 라도 공기 속이면 약 176 ms — 물속 메아리가 더 빨리 온다", 26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        sp_ = panel(summ, buff=0.5, pos=ORIGIN + UP * 0.3)
        self.play(FadeIn(sp_[0], shift=UP * 0.2), FadeIn(summ[0], shift=UP * 0.2), run_time=0.8)
        for line in summ[1:]:  # 한 줄씩 (줄마다 읽을 시간)
            self.play(FadeIn(line, shift=RIGHT * 0.15), run_time=0.5)
            self.wait(2.4)
        self.wait(3.5)
        self.play(FadeOut(sp_), run_time=0.6)

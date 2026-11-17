"""도플러 효과 ④ 일반식과 이용 (교과서 그림 III-16 ~ III-19)."""
from d34_kit import *

BLOOD_R = "#FF4D5E"
BLOOD_B = "#4D8BFF"


# ---------------------------------------------------------------- 그림 도우미
def stream(t, src, direction, c, gap, rmax, spread, color, width=4, rmin=0.04):
    """src 에서 direction 으로 계속 나가는 호들 (반지름 r = c t - k gap)."""
    g = VGroup()
    s = c * t
    k_lo = int(np.floor((s - rmax) / gap))
    k_hi = int(np.floor(s / gap))
    for k in range(max(k_lo, 0), k_hi + 1):
        r = s - k * gap
        if rmin < r < rmax:
            g.add(ring_arc(np.array(src, dtype=float), r, direction, spread, color, width,
                           1 - 0.5 * r / rmax))
    return g


def car(color="#E85D5D"):
    body = RoundedRectangle(corner_radius=0.12, width=1.6, height=0.45, fill_color=color,
                            fill_opacity=1, stroke_color=WHITE_T, stroke_width=1.5)
    top = RoundedRectangle(corner_radius=0.12, width=0.85, height=0.38, fill_color=color,
                           fill_opacity=1, stroke_color=WHITE_T, stroke_width=1.5)
    top.next_to(body, UP, buff=-0.05).shift(LEFT * 0.1)
    win = Rectangle(width=0.6, height=0.2, fill_color="#9FD8FF", fill_opacity=0.9,
                    stroke_width=0).move_to(top).shift(UP * 0.02)
    w1 = Circle(radius=0.16, fill_color="#222", fill_opacity=1, stroke_color=WHITE_T,
                stroke_width=1.5).move_to(body.get_bottom() + LEFT * 0.5)
    w2 = w1.copy().move_to(body.get_bottom() + RIGHT * 0.5)
    return VGroup(top, win, body, w1, w2)


def speed_gun():
    grip = Polygon([0, 0, 0], [0.18, 0, 0], [0.28, -0.45, 0], [0.08, -0.45, 0],
                   fill_color="#555E6A", fill_opacity=1, stroke_color=WHITE_T, stroke_width=1.5)
    barrel = RoundedRectangle(corner_radius=0.08, width=0.8, height=0.3, fill_color="#6B7583",
                              fill_opacity=1, stroke_color=WHITE_T, stroke_width=1.5)
    barrel.move_to([-0.15, 0.12, 0])
    return VGroup(grip, barrel)


def dish():
    base = Polygon([-0.3, -0.6, 0], [0.3, -0.6, 0], [0.08, 0, 0], [-0.08, 0, 0],
                   fill_color="#6B7583", fill_opacity=1, stroke_color=WHITE_T, stroke_width=1.5)
    bowl = Arc(radius=0.55, start_angle=PI * 0.75, angle=PI, stroke_color=WHITE_T,
               stroke_width=4).move_to([0.1, 0.25, 0])
    bowl_f = Sector(radius=0.55, start_angle=PI * 0.75, angle=PI, fill_color="#C7CFD8",
                    fill_opacity=0.9, stroke_width=0)
    bowl_f.move_to(bowl)
    return VGroup(base, bowl_f, bowl)


def cloud(scale=1.0):
    g = VGroup(*[Circle(radius=r, fill_color="#8C9BB0", fill_opacity=1, stroke_width=0)
                 .move_to([x, y, 0]) for x, y, r in
                 [(-0.5, 0, 0.35), (0, 0.15, 0.48), (0.5, 0, 0.36), (0.0, -0.1, 0.4)]])
    drops = VGroup(*[Line([x, -0.55, 0], [x - 0.06, -0.8, 0], stroke_color=CYAN, stroke_width=3)
                     for x in (-0.45, -0.15, 0.15, 0.45)])
    return VGroup(g, drops).scale(scale)


def probe():
    body = RoundedRectangle(corner_radius=0.15, width=0.5, height=1.2, fill_color="#C7CFD8",
                            fill_opacity=1, stroke_color=WHITE_T, stroke_width=1.5)
    tip = RoundedRectangle(corner_radius=0.06, width=0.62, height=0.18, fill_color="#5E6B7A",
                           fill_opacity=1, stroke_color=WHITE_T, stroke_width=1.5)
    tip.next_to(body, DOWN, buff=-0.05)
    return VGroup(body, tip)


def galaxy(scale=1.0):
    g = VGroup()
    for i in range(3):
        g.add(Ellipse(width=1.6 - i * 0.45, height=0.6 - i * 0.16, fill_color="#FFE9B8",
                      fill_opacity=0.25 + i * 0.25, stroke_width=0))
    g.add(Dot(radius=0.08, color=WHITE))
    return g.rotate(0.35).scale(scale)


def wl_color(u):
    """u: 0(파랑/보라) → 1(빨강)."""
    stops = ["#6A3DFF", "#2F7BFF", "#25D0FF", "#3BE36B", "#F2F23A", "#FFA531", "#FF3B30"]
    x = u * (len(stops) - 1)
    i = min(int(x), len(stops) - 2)
    return interpolate_color(ManimColor(stops[i]), ManimColor(stops[i + 1]), x - i)


def spectrum(width=8.0, height=0.6, n=80):
    g = VGroup()
    w = width / n
    for i in range(n):
        g.add(Rectangle(width=w * 1.02, height=height, stroke_width=0, fill_opacity=1,
                        fill_color=wl_color(i / (n - 1))).move_to([-width / 2 + (i + 0.5) * w, 0, 0]))
    return g


def gen_formula(size=40, sub_o=True):
    """f_o = (v ± v_o) / (v ∓ v_s) × f_s"""
    return mrow(sym("f", OBS_SUB, F_C, size), "=",
                mfrac([sym("v", None, CYAN, size), ("±", WHITE_T), vo(size=size)],
                      [sym("v", None, CYAN, size), ("∓", WHITE_T), vs_(size=size)], size=size),
                "×", sym("f", "s", F_C, size), size=size)


class D4General(CaseScene):
    def construct(self):
        bg = studio_bg(horizon=0.9)
        self.add(bg)

        # 0. 제목만 먼저
        card = title_card("도플러 효과 ④ 일반식과 이용")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.wait(2.4)
        self.play(FadeOut(card), run_time=0.6)

        # ---------------------------------------------------------- 1. 일반식
        F = gen_formula(44)
        pf = panel(F, buff=0.35).move_to(UP * 1.6)
        self.say("②(음원이 움직임)와 ③(관찰자가 움직임)을\n하나의 식으로 합치면", wait=0.3)
        self.play(FadeIn(pf[0]), Write(F), run_time=1.5)
        self.wait(2.2)

        def leg(m, text):
            return VGroup(m, T(text, 22, WHITE_T)).arrange(RIGHT, buff=0.18)

        legs = VGroup(
            leg(sym("f", OBS_SUB, F_C, 28), "관찰자가 듣는 진동수"),
            leg(sym("f", "s", F_C, 28), "음원의 진동수"),
            leg(sym("v", None, CYAN, 28), "음속 (340 m/s)"),
            leg(vo(size=28), "관찰자의 속력"),
            leg(vs_(size=28), "음원의 속력"),
        )
        colA = VGroup(legs[0], legs[1], legs[2]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        colB = VGroup(legs[3], legs[4]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        lg = VGroup(colA, colB).arrange(RIGHT, buff=1.0, aligned_edge=UP)
        lgn = T("※ 속력은 공기에 대한 값, 음원과 관찰자는 한 직선 위에서 움직인다 (vₒ, vₛ < v)", 18, GRAY_T)
        lg = VGroup(lg, lgn).arrange(DOWN, buff=0.22)
        pl = panel(lg, buff=0.3).next_to(pf, DOWN, buff=0.35)
        self.play(FadeIn(pl), run_time=0.7)
        self.say("분자에는 관찰자의 속력, 분모에는 음원의 속력\n(③에서 관찰자는 분자, ②에서 음원은 분모에 있었다)")
        self.play(FadeOut(pl), run_time=0.5)

        # ---------------------------------------------------------- 2. 부호
        self.play(pf.animate.move_to(UP * 2.4), run_time=0.6)
        cw, ch = [3.7, 1.5, 1.5], 0.62
        rows = [["", None, None], ["상대 쪽으로 움직일 때", "+", "−"], ["상대에게서 멀어질 때", "−", "+"]]
        heads = [None, mrow(vo(size=28), ("앞", WHITE_T), size=28),
                 mrow(vs_(size=28), ("앞", WHITE_T), size=28)]
        tbl = VGroup()
        cells = {}
        for i, row in enumerate(rows):
            x = 0
            for j, val in enumerate(row):
                box = Rectangle(width=cw[j], height=ch, stroke_color=PANEL_STROKE, stroke_width=1.5,
                                fill_color=PANEL_FILL, fill_opacity=0.97)
                box.move_to([x + cw[j] / 2, -i * ch, 0])
                x += cw[j]
                if i == 0 and j > 0:
                    m = heads[j]
                elif j == 0:
                    m = T(val, 24, GREEN if i == 1 else RED_T, bold=True)
                else:
                    m = T(val, 40, WHITE_T, bold=True)
                m.move_to(box)
                cells[(i, j)] = VGroup(box, m)
                tbl.add(cells[(i, j)])
        tbl.move_to([-3.4, -0.4, 0])
        self.play(FadeIn(VGroup(*[cells[(0, j)] for j in range(3)])), run_time=0.5)
        self.play(FadeIn(VGroup(*[cells[(1, j)] for j in range(3)])), run_time=0.6)
        self.say("관찰자가 음원 쪽으로 움직이면 vₒ 앞 +,\n음원이 관찰자 쪽으로 움직이면 vₛ 앞 −")
        self.play(FadeIn(VGroup(*[cells[(2, j)] for j in range(3)])), run_time=0.6)
        self.say("상대에게서 멀어지는 쪽으로 움직이면\nvₒ 앞 −, vₛ 앞 +")

        tip = VGroup(
            T("외우는 법", 24, CYAN, bold=True),
            T("가까워지면 진동수가 커지도록", 24, WHITE_T, bold=True),
            T("부호를 고른다", 24, WHITE_T, bold=True),
            mrow(("분자 ↑", GREEN), ("또는", GRAY_T), ("분모 ↓", GREEN), "→",
                 sym("f", OBS_SUB, F_C, 28), ("↑", GREEN), size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        pt = panel(tip, buff=0.3).move_to([3.4, -0.4, 0])
        self.play(FadeIn(pt), run_time=0.7)
        self.say("가까워지면 → 분자는 커지게(+), 분모는 작아지게(−)\n멀어지면 그 반대")
        self.unsay()
        self.play(FadeOut(tbl), FadeOut(pt), run_time=0.5)

        # ---------------------------------------------------------- 3. 네 경우
        small = gen_formula(30)
        sp_ = panel(small, buff=0.2).to_edge(UP, buff=0.25)
        self.play(ReplacementTransform(pf, sp_), run_time=0.7)

        def pict(src_moves, toward):
            spk = speaker(0.42)
            per = person(ORANGE, 0.5)
            grp = VGroup(spk, per).arrange(RIGHT, buff=1.4)
            mover = spk if src_moves else per
            col = SRC_C if src_moves else ORANGE
            if src_moves:
                d = RIGHT if toward else LEFT
            else:
                d = LEFT if toward else RIGHT
            top = mover.get_top() + UP * 0.15
            arr = Arrow(top - d * 0.35, top + d * 0.45, buff=0, color=col, stroke_width=5,
                        tip_length=0.16)
            return VGroup(grp, arr)

        def case_card(title, tcol, src_moves, toward, num, den, res, rcol):
            tt = T(title, 24, tcol, bold=True)
            pc = pict(src_moves, toward)
            fm = mrow(mfrac(num, den, size=28), "×", ("(1200)", F_C), "≈" if src_moves else "=",
                      (res, rcol), size=28)
            top = VGroup(tt, pc).arrange(RIGHT, buff=0.5)
            body = VGroup(top, fm).arrange(DOWN, buff=0.12)
            box = RoundedRectangle(corner_radius=0.12, width=6.3, height=1.9,
                                   stroke_color=PANEL_STROKE, stroke_width=1.5,
                                   fill_color=PANEL_FILL, fill_opacity=0.97)
            body.move_to(box)
            return VGroup(box, body)

        c340 = ("(340)", CYAN)
        s34 = ("(34)", SRC_C)
        o34 = ("(34)", ORANGE)
        cards = [
            case_card("② 음원이 다가올 때", SRC_C, True, True, [c340], [c340, "−", s34],
                      "1333 Hz", GREEN),
            case_card("② 음원이 멀어질 때", SRC_C, True, False, [c340], [c340, "+", s34],
                      "1091 Hz", RED_T),
            case_card("③ 관찰자가 다가갈 때", ORANGE, False, True, [c340, "+", o34], [c340],
                      "1320 Hz", GREEN),
            case_card("③ 관찰자가 멀어질 때", ORANGE, False, False, [c340, "−", o34], [c340],
                      "1080 Hz", RED_T),
        ]
        grid = VGroup(*cards).arrange_in_grid(2, 2, buff=(0.3, 0.18))
        grid.next_to(sp_, DOWN, buff=0.2)
        self.say("②, ③의 네 경우를 이 식에 넣어 보자\n(v = 340 m/s, 속력 34 m/s, f = 1200 Hz)", wait=1.0)
        for i, cd in enumerate(cards):
            self.play(FadeIn(cd, shift=UP * 0.1), run_time=0.6)
            self.wait(2.2)
        self.say("다가오면 1200 Hz보다 높게,\n멀어지면 낮게 — 네 경우 모두 맞는다", wait=2.6)
        hl1 = SurroundingRectangle(cards[0], color=F_C, buff=0.04, stroke_width=4)
        hl2 = SurroundingRectangle(cards[2], color=F_C, buff=0.04, stroke_width=4)
        self.play(Create(hl1), Create(hl2), run_time=0.7)
        self.say("같은 34 m/s로 가까워져도 1333 Hz ≠ 1320 Hz\n소리는 공기에 대해 누가 움직이느냐에 따라 다르다")
        self.play(FadeOut(grid), FadeOut(hl1), FadeOut(hl2), run_time=0.5)
        self.unsay()

        # ---------------------------------------------------------- 4. 같은 속도로 함께
        tw = ValueTracker(0)
        tw.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(tw)
        road = Line([-7.5, -1.75, 0], [7.5, -1.75, 0], stroke_color=GRAY_T, stroke_width=2)
        spk = speaker(0.8)
        per = person(ORANGE, 0.9)
        X0 = -4.0
        spk.add_updater(lambda m: m.move_to([X0 + 0.5 * min(tw.get_value(), 5.0), -1.0, 0]))
        per.add_updater(lambda m: m.move_to([X0 + 3.6 + 0.5 * min(tw.get_value(), 5.0), -1.0, 0]))
        arr_s = always_redraw(lambda: Arrow(spk.get_top() + UP * 0.25 + LEFT * 0.4,
                                            spk.get_top() + UP * 0.25 + RIGHT * 0.6, buff=0,
                                            color=SRC_C, stroke_width=5, tip_length=0.18))
        arr_o = always_redraw(lambda: Arrow(per.get_top() + UP * 0.25 + LEFT * 0.4,
                                            per.get_top() + UP * 0.25 + RIGHT * 0.6, buff=0,
                                            color=ORANGE, stroke_width=5, tip_length=0.18))
        lab_s = always_redraw(lambda: T("34 m/s", 22, SRC_C, bold=True).next_to(arr_s, UP, buff=0.06))
        lab_o = always_redraw(lambda: T("34 m/s", 22, ORANGE, bold=True).next_to(arr_o, UP, buff=0.06))
        tw.set_value(0)
        self.add(road, spk, per, arr_s, arr_o, lab_s, lab_o)
        self.play(FadeIn(VGroup(road)), run_time=0.3)
        self.say("음원과 관찰자가 같은 방향, 같은 속력으로\n함께 움직이면? (공기는 가만히 있다)")
        same = mrow(sym("f", OBS_SUB, F_C), "=",
                    mfrac([c340, "−", o34], [c340, "−", s34]), "×", ("(1200)", F_C), "=",
                    ("1200 Hz", GREEN))
        nt = T("관찰자: 음원에서 멀어짐(−)   음원: 관찰자에게 다가감(−)", 20, GRAY_T)
        qs = VGroup(same, nt).arrange(DOWN, buff=0.2)
        ps = panel(qs, buff=0.25).move_to([1.6, 0, 0]).next_to(sp_, DOWN, buff=0.25)
        self.play(FadeIn(ps), run_time=0.7)
        self.say("분자와 분모가 같아져서 1200 Hz 그대로\n→ 상대 속도가 0이면 진동수 변화 없음")
        self.play(*[FadeOut(m) for m in (road, spk, per, arr_s, arr_o, lab_s, lab_o, ps, sp_)],
                  run_time=0.6)
        for m in (spk, per):
            m.clear_updaters()
        self.unsay()

        # ---------------------------------------------------------- 5. 이용
        hdr = T("도플러 효과의 이용", 30, CYAN, bold=True).to_corner(UL, buff=0.35)
        self.play(FadeIn(hdr), run_time=0.5)
        self.use_heart(tw, hdr)
        self.use_speedgun(tw)
        self.use_radar(tw)
        self.use_galaxy()
        self.play(FadeOut(hdr), run_time=0.4)
        self.unsay()

        # ---------------------------------------------------------- 6. 정리
        lines = [
            mrow(("· 일반식", WHITE_T), gen_formula(26), size=26),
            mrow("· 상대 쪽으로 움직이면", vo(size=26), "앞 +,", vs_(size=26), "앞 −   (멀어지면 반대)",
                 size=26),
            T("· 음원이 움직이면 파장이, 관찰자가 움직이면 만나는 속력이 바뀐다", 26, bold=True),
            T("· 상대 속도가 0이면 진동수 변화 없음", 26, bold=True),
            T("· 이용: 혈류 초음파, 스피드건, 기상 레이더, 은하의 적색 편이", 26, bold=True),
            T("· 다가오면 높게(진동수↑), 멀어지면 낮게(진동수↓)", 28, F_C, bold=True),
        ]
        summary_reveal(self, lines, "도플러 효과 정리", pos=UP * 0.25, hold=4.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.wm and m is not bg],
                  run_time=0.6)

    # ================================================================== 이용 장면들
    def use_heart(self, tw, hdr):
        t0 = tw.get_value()
        sub = T("① 도플러 혈류 초음파", 26, WHITE_T, bold=True).next_to(hdr, DOWN, buff=0.15,
                                                                         aligned_edge=LEFT)
        y0 = -0.9
        wall_t = Line([-7.2, y0 + 0.55, 0], [7.2, y0 + 0.55, 0], stroke_color="#C98A8A",
                      stroke_width=4)
        wall_b = Line([-7.2, y0 - 0.55, 0], [7.2, y0 - 0.55, 0], stroke_color="#C98A8A",
                      stroke_width=4)
        flow = Rectangle(width=14.4, height=1.1, stroke_width=0, fill_color=BLOOD_R,
                         fill_opacity=0.0).move_to([0, y0, 0])
        vlab = T("혈관", 20, GRAY_T).next_to(wall_b, DOWN, buff=0.08).to_edge(LEFT, buff=0.5)
        st = {"v": -0.9, "x": 0.0, "t": t0}

        def cell_x():
            t = tw.get_value()
            st["x"] += st["v"] * (t - st["t"])
            st["t"] = t
            return st["x"]

        cells = VGroup(*[Ellipse(width=0.42, height=0.22, fill_color="#D63B4A", fill_opacity=1,
                                 stroke_color="#FF9AA5", stroke_width=1.2) for _ in range(12)])
        offs = [(-6.4, 0.18), (-5.2, -0.2), (-4.1, 0.1), (-2.9, -0.25), (-1.7, 0.22), (-0.6, -0.08),
                (0.6, 0.2), (1.7, -0.2), (2.9, 0.1), (4.0, -0.22), (5.2, 0.18), (6.4, -0.05)]

        def upd(g):
            x = cell_x()
            for c, (ox, oy) in zip(g, offs):
                xx = (ox + x + 7.2) % 14.4 - 7.2
                c.move_to([xx, y0 + oy, 0])

        cells.add_updater(upd)
        pr = probe().rotate(0.5).move_to([-2.4, 1.6, 0])
        ptip = np.array([-2.0, 0.95, 0])
        pdir = np.array([0.5, -0.87, 0])
        tgt = np.array([-1.3, y0 + 0.2, 0])
        D = np.linalg.norm(tgt - ptip)
        out = always_redraw(lambda: stream(tw.get_value() - t0, ptip, pdir, 2.0, 0.22, D, 0.7, CYAN, 3))
        back = always_redraw(lambda: stream(max(tw.get_value() - t0 - 0.9, 0), tgt, -pdir, 2.0,
                                            0.17 if st["v"] < 0 else 0.29, D * 0.9, 0.7, ORANGE, 3))
        cp = bcall(ptip + LEFT * 0.35 + UP * 0.6, "탐촉자", "초음파를 보내고 받는다", UL, 0.6)
        self.play(FadeIn(sub), FadeIn(wall_t), FadeIn(wall_b), FadeIn(flow), FadeIn(cells),
                  FadeIn(vlab), FadeIn(pr), run_time=0.8)
        self.add(out, back)
        self.play(FadeIn(cp), run_time=0.4)
        self.say("초음파를 혈관에 쏘면, 움직이는 적혈구에 반사되어\n진동수가 바뀐 채 돌아온다")
        self.play(FadeOut(cp), flow.animate.set_fill(BLOOD_R, 0.45), run_time=0.6)
        sc1 = tagbox("탐촉자 쪽으로 오는 피 → 빨강 (보통)", BLOOD_R).move_to([3.6, 1.6, 0])
        self.play(FadeIn(sc1), run_time=0.4)
        self.say("다가오는 피: 진동수가 커진다 → 화면에 (보통 빨강)", wait=3.0)
        st["v"] = 0.9
        sc2 = tagbox("탐촉자에서 멀어지는 피 → 파랑 (보통)", BLOOD_B).move_to(sc1)
        self.play(flow.animate.set_fill(BLOOD_B, 0.45), ReplacementTransform(sc1, sc2), run_time=0.8)
        self.say("멀어지는 피: 진동수가 작아진다 → 화면에 (보통 파랑)\n→ 피가 흐르는 속력과 방향을 알 수 있다")
        cells.clear_updaters()
        self.remove(out, back)
        self.play(*[FadeOut(m) for m in (sub, wall_t, wall_b, flow, cells, vlab, pr, sc2)],
                  run_time=0.5)

    def use_speedgun(self, tw):
        t0 = tw.get_value()
        sub = T("② 스피드건", 26, WHITE_T, bold=True).move_to([-7, 3.05, 0], aligned_edge=LEFT)
        sub.to_edge(LEFT, buff=0.35)
        road = Line([-7.5, -0.95, 0], [7.5, -0.95, 0], stroke_color=GRAY_T, stroke_width=2)
        cr = car()
        cr.add_updater(lambda m: m.move_to([-5.8 + 0.7 * (tw.get_value() - t0), -0.45, 0]))
        gun = speed_gun().scale(1.3).move_to([5.6, 0.0, 0])
        mouth = np.array([5.0, 0.15, 0])

        # 파면 앞 x = 5.0 - 2.2 t, 차 앞 x = -4.95 + 0.7 t → 만나는 순간 t = 9.95 / 2.9
        T_HIT = (mouth[0] - (-5.8 + 0.85)) / (2.2 + 0.7)

        def waves():
            t = tw.get_value() - t0
            cx = -5.8 + 0.7 * t + 0.85
            D = mouth[0] - cx
            g = stream(t, mouth, LEFT, 2.2, 0.32, max(D, 0.1), 0.35, CYAN, 3)
            g.add(stream(max(t - T_HIT, 0), [cx, 0.0, 0], RIGHT, 2.2, 0.24, max(D, 0.1) * 0.95,
                         0.35, ORANGE, 3))
            return g

        wv = always_redraw(waves)
        disp = panel(VGroup(T("측정 속력", 18, GRAY_T), M("98 km/h", 34, GREEN)).arrange(DOWN, buff=0.08),
                     buff=0.18).next_to(gun, UP, buff=0.35)
        self.play(FadeIn(sub), FadeIn(road), FadeIn(cr), FadeIn(gun), run_time=0.6)
        self.add(wv)
        self.say("스피드건은 전자기파를 쏘고,\n다가오는 차에 반사된 파동을 받는다")
        self.play(FadeIn(disp), run_time=0.5)
        self.say("반사파는 진동수가 커져서 돌아온다\n→ 진동수 차이로 속력을 잰다 (야구공 속력도)")
        self.remove(wv)
        cr.clear_updaters()
        self.play(*[FadeOut(m) for m in (sub, road, cr, gun, disp)], run_time=0.5)

    def use_radar(self, tw):
        t0 = tw.get_value()
        sub = T("③ 기상 레이더", 26, WHITE_T, bold=True).to_edge(LEFT, buff=0.35).set_y(3.05)
        ds = dish().scale(1.2).move_to([-5.2, -0.6, 0])
        mouth = np.array([-4.7, 0.0, 0])
        cl = cloud(1.2)
        cl.add_updater(lambda m: m.move_to([3.6 - 0.35 * (tw.get_value() - t0), 1.4, 0]))

        def waves():
            t = tw.get_value() - t0
            tg = np.array([3.6 - 0.35 * t - 0.6, 1.0, 0])
            d = tg - mouth
            D = np.linalg.norm(d)
            u = d / D
            g = stream(t, mouth, u, 2.2, 0.34, D, 0.55, CYAN, 3)
            g.add(stream(max(t - D / 2.2, 0), tg, -u, 2.2, 0.3, D * 0.95, 0.55, ORANGE, 3))
            return g

        wv = always_redraw(waves)
        self.play(FadeIn(sub), FadeIn(ds), FadeIn(cl), run_time=0.6)
        self.add(wv)
        self.say("기상 레이더는 전파를 쏘아\n빗방울·구름에 반사된 파동을 받는다")
        mv = tagbox("비구름이 다가오는 중", F_C).move_to([3.2, -0.6, 0])
        self.play(FadeIn(mv), run_time=0.4)
        self.say("진동수 변화로 비구름이 움직이는 방향과 속력을 알아내\n날씨를 예측한다")
        self.remove(wv)
        cl.clear_updaters()
        self.play(*[FadeOut(m) for m in (sub, ds, cl, mv)], run_time=0.5)

    def use_galaxy(self):
        sub = T("④ 별빛과 은하", 26, WHITE_T, bold=True).to_edge(LEFT, buff=0.35).set_y(3.05)
        gx = galaxy(1.2).move_to([-3.6, 1.4, 0])
        spec = spectrum(8.0, 0.8).move_to([1.4, -0.3, 0])
        sx0 = spec.get_left()[0]
        fr = [0.18, 0.42, 0.63]
        lines = VGroup(*[Line([sx0 + 8 * f, -0.7, 0], [sx0 + 8 * f, 0.1, 0], stroke_color=BLACK,
                              stroke_width=9) for f in fr])
        refs = VGroup(*[Line([sx0 + 8 * f, 0.15, 0], [sx0 + 8 * f, 0.4, 0], stroke_color=WHITE_T,
                             stroke_width=2) for f in fr])
        lb = T("파랑: 진동수 큼", 20, "#6FA8FF", bold=True).next_to(spec, DOWN, buff=0.15).align_to(spec, LEFT)
        lr = T("빨강: 진동수 작음", 20, "#FF7B6B", bold=True).next_to(spec, DOWN, buff=0.15).align_to(spec, RIGHT)
        rl = T("가만히 있을 때 위치", 18, GRAY_T).next_to(refs, UP, buff=0.08)
        earth = VGroup(Circle(radius=0.25, fill_color="#3A7BD5", fill_opacity=1, stroke_color=WHITE_T,
                              stroke_width=1.5), T("지구 (관측자)", 20, GRAY_T))
        earth[1].next_to(earth[0], DOWN, buff=0.1)
        earth.move_to([3.4, 1.4, 0])
        self.play(FadeIn(earth), FadeIn(sub), FadeIn(gx), FadeIn(spec), FadeIn(lines), FadeIn(lb), FadeIn(lr),
                  run_time=0.8)
        self.say("빛도 파동이다 → 빛에서도 도플러 효과가 생긴다\n(별빛을 무지개처럼 펼친 띠: 스펙트럼)")
        self.play(FadeIn(refs), FadeIn(rl), run_time=0.5)
        ga = Arrow(gx.get_center() + UP * 0.8 + LEFT * 0.3, gx.get_center() + UP * 0.8 + LEFT * 1.4,
                   buff=0, color=RED_T, stroke_width=5, tip_length=0.2)
        gl = T("멀어지는 은하", 22, RED_T, bold=True).next_to(ga, UP, buff=0.06)
        self.play(GrowArrow(ga), FadeIn(gl), gx.animate.shift(LEFT * 0.6),
                  lines.animate.shift(RIGHT * 0.8), run_time=1.5)
        self.say("멀어지는 은하의 빛: 진동수가 작아져 붉은 쪽으로\n밀린다 → 적색 편이")
        ga2 = Arrow(gx.get_center() + UP * 0.8 + LEFT * 0.4, gx.get_center() + UP * 0.8 + RIGHT * 0.7,
                    buff=0, color="#6FA8FF", stroke_width=5, tip_length=0.2)
        gl2 = T("다가오는 은하 (예: 안드로메다)", 22, "#6FA8FF", bold=True).next_to(ga2, UP, buff=0.06)
        self.play(ReplacementTransform(ga, ga2), ReplacementTransform(gl, gl2),
                  gx.animate.shift(RIGHT * 0.6), lines.animate.shift(LEFT * 1.6), run_time=1.5)
        self.say("다가오면 진동수가 커져 파란 쪽으로 → 청색 편이", wait=3.2)
        self.play(lines.animate.shift(RIGHT * 1.6 + RIGHT * 0.4), FadeOut(ga2), FadeOut(gl2),
                  run_time=1.0)
        self.say("허블은 멀리 있는 은하일수록 더 크게 적색 편이된 것을 보고\n은하들이 서로 멀어지고 있다(우주 팽창)는 것을 알아냈다")
        self.say("※ 빛의 도플러 식은 소리의 식과 다르다.\n'다가오면 진동수↑, 멀어지면 진동수↓'라는 생각만 같다",
                 color=GRAY_T)
        self.play(*[FadeOut(m) for m in (sub, gx, spec, lines, refs, rl, lb, lr, earth)], run_time=0.5)


def bcall(*a, **k):
    c = callout(*a, **k)
    bgr = BackgroundRectangle(c[2], color=config.background_color, fill_opacity=0.85, buff=0.08)
    return VGroup(c[0], c[1], bgr, c[2])


def tagbox(text, color):
    t = T(text, 24, color, bold=True)
    return panel(t, buff=0.18)

"""사례 4. 해저 지형 조사 (음향 측심) — 배에서 초음파를 쏘아 수심 재기."""
from common import *

SURF = 1.9          # 수면 높이 (화면 좌표)
K = 0.95            # 1000 m 당 화면 길이 (세로를 크게 늘려 그림)


def y_of(depth_m):
    return SURF - depth_m / 1000 * K


class Capped:
    """시계·시간축용: 파동 tracker 가 지나가도 cap 에서 멈추는 값."""

    def __init__(self, tr, cap):
        self.tr, self.cap = tr, cap

    def get_value(self):
        return min(self.tr.get_value(), self.cap)


# 측정 지점 (x 좌표, 수심 m)
SPOTS = [(-5, 3000), (-3, 2250), (-1, 1500), (1, 1875), (3, 2625), (5, 3000)]
# 실제 바닥 모양 (측정 지점 사이에도 굴곡이 있다)
FLOOR_PTS = [(-7.6, 2850), (-6.2, 3150), (-5, 3000), (-4, 2700), (-3, 2250), (-2, 1800),
             (-1, 1500), (0, 1600), (1, 1875), (2, 2350), (3, 2625), (4, 2950), (5, 3000),
             (6.2, 2800), (7.6, 2950)]


def seafloor():
    pts = [np.array([x, y_of(d), 0]) for x, d in FLOOR_PTS]
    edge = VMobject(stroke_color="#B08A63", stroke_width=3)
    edge.set_points_smoothly(pts)
    fill = edge.copy().set_stroke(width=0)
    fill.add_line_to(np.array([7.6, -4.4, 0]))
    fill.add_line_to(np.array([-7.6, -4.4, 0]))
    fill.add_line_to(pts[0])
    fill.set_fill(color=["#4A3A2E", "#1E1712"], opacity=1).set_sheen_direction(DOWN)
    return VGroup(fill, edge)


def ship_shape():
    """옆에서 본 조사선. 원점 = 배 밑바닥의 송수파기."""
    hull = Polygon([-0.95, 0.42, 0], [0.95, 0.42, 0], [0.75, 0.0, 0], [-0.8, 0.0, 0],
                   fill_color="#C94C4C", fill_opacity=1, stroke_color=WHITE_T, stroke_width=1.4)
    band = Polygon([-0.93, 0.42, 0], [0.95, 0.42, 0], [0.88, 0.28, 0], [-0.87, 0.28, 0],
                   fill_color="#E8EDF2", fill_opacity=1, stroke_width=0)
    cab = Rectangle(width=0.8, height=0.32, fill_color="#E8EDF2", fill_opacity=1,
                    stroke_color=WHITE_T, stroke_width=1.2).move_to([-0.15, 0.58, 0])
    brg = Rectangle(width=0.45, height=0.22, fill_color="#E8EDF2", fill_opacity=1,
                    stroke_color=WHITE_T, stroke_width=1.2).move_to([-0.1, 0.85, 0])
    wins = VGroup(*[Square(0.07, fill_color="#2A4A66", fill_opacity=1, stroke_width=0)
                    .move_to([-0.25 + 0.12 * i, 0.87, 0]) for i in range(4)])
    mast = Line([0.25, 0.74, 0], [0.25, 1.25, 0], stroke_color=WHITE_T, stroke_width=2)
    yard = Line([0.12, 1.12, 0], [0.38, 1.12, 0], stroke_color=WHITE_T, stroke_width=2)
    tr = Dot(ORIGIN, radius=0.07, color=CYAN)
    return VGroup(hull, band, cab, brg, wins, mast, yard, tr)


def depth_color(d, dmin=1300, dmax=3200):
    cols = [ManimColor("#FF6B6B"), ManimColor("#FFB547"), ManimColor("#5BE39B"),
            ManimColor("#3FD3FF"), ManimColor("#3A5BD9")]
    u = np.clip((d - dmin) / (dmax - dmin), 0, 0.999) * (len(cols) - 1)
    i = int(u)
    return interpolate_color(cols[i], cols[i + 1], u - i)


class C4Seafloor(CaseScene):
    def construct(self):
        bg = sea_bg(SURF)
        floor = seafloor()
        self.add(bg, floor)

        X0 = SPOTS[0][0]
        DRAFT = 0.15
        ship = ship_shape().shift([X0, SURF - DRAFT, 0])
        TR = lambda: ship[-1].get_center()

        # 0. 제목
        card = title_card("해저 지형 조사 (음향 측심)", case_no=4)
        self.play(FadeIn(ship, shift=RIGHT * 0.4), run_time=1)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.wait(2.4)
        self.play(FadeOut(card), run_time=0.6)

        # 1. 등장 요소
        c_ship = callout(TR() + np.array([0.25, 1.15, 0]), "조사선", "바다 위에서 수심을 잰다",
                         RIGHT + UP * 0.3, 0.7)
        c_tr = callout(TR(), "송수파기", "배 밑바닥 — 초음파를 보내고 받는 장치",
                       DOWN + RIGHT * 0.9, 0.9, color=CYAN)
        c_fl = callout([0.0, y_of(1600), 0], "해저 (바다 밑바닥)", None, DOWN + RIGHT * 0.5, 0.8)
        self.play(Create(c_ship), run_time=0.7)
        self.play(Create(c_tr), run_time=0.8)
        self.say("배 밑바닥의 '송수파기'가 초음파 펄스를\n바로 아래(바다 밑바닥)로 쏜다")
        self.play(Create(c_fl), run_time=0.7)
        self.say("바닥에서 반사된 펄스를 같은 송수파기가 다시 받는다")
        self.play(FadeOut(c_ship), FadeOut(c_tr), FadeOut(c_fl), run_time=0.5)

        # 2. 한 지점에서 측정: 시간 차 4.0 s
        d0 = SPOTS[0][1]
        TRIP = d0 / 1500  # 2.0 s (한 방향)
        tw = ValueTracker(0)
        tclk = Capped(tw, 2 * TRIP)
        src = TR()
        tgt = np.array([X0, y_of(d0), 0])
        D = np.linalg.norm(tgt - src)
        waves = always_redraw(lambda: echo_group(tw.get_value() / TRIP * D, src, tgt, 0.3, 5,
                                                 0.7, 0.8, back_dir=UP))
        clock = Clock(tclk, "s", "{:.2f}")
        tl = Timeline(5, 1, tclk, "s", y=-2.4, x0=-4.0, x1=4.4)
        sn = slow_note("※ 실제보다 느리게 보여 줌")
        self.play(FadeIn(sn), FadeIn(clock), FadeIn(tl), run_time=0.8)
        m0 = tl.marker(0, "신호 발신 시각", ORANGE)
        self.play(FadeIn(m0), run_time=0.4)
        self.say("이번에는 시간 단위가 '초(s)' — 바다가 아주 깊기 때문", wait=1.8)
        self.say("펄스를 쏘는 순간 시간을 0으로 놓는다", wait=0.3)
        self.add(waves)
        self.play(tw.animate.set_value(TRIP), run_time=4.4, rate_func=linear)
        refl = callout(tgt + UP * 0.02, "바닥에서 반사", None, UP + RIGHT * 0.8, 0.8)
        self.play(FadeIn(refl), run_time=0.4)
        self.say("바닥에 부딪힌 초음파가 반사되어 올라온다", wait=0.2)
        self.play(tw.animate.set_value(2 * TRIP), run_time=4.4, rate_func=linear)
        m1 = tl.marker(2 * TRIP, "신호 수신 시각", GREEN)
        self.play(tw.animate.set_value(2 * TRIP + 0.6), FadeIn(m1), FadeOut(refl),
                  run_time=1.32, rate_func=linear)
        self.remove(waves)
        sp = tl.span(0, 2 * TRIP, "시간 차 = 4.0 s").shift(UP * 0.55)
        self.play(FadeIn(sp), run_time=0.6)
        self.say("보낸 시각과 받은 시각의 차이 = 시간 차 4.0 s")

        go = Arrow(src + LEFT * 0.35 + DOWN * 0.1, tgt + LEFT * 0.35 + UP * 0.1, buff=0,
                   color=CYAN, stroke_width=4, tip_length=0.2)
        back = Arrow(tgt + RIGHT * 0.35 + UP * 0.1, src + RIGHT * 0.35 + DOWN * 0.1, buff=0,
                     color=ORANGE, stroke_width=4, tip_length=0.2)
        lg = T("갈 때", 22, CYAN, bold=True).next_to(go, LEFT, buff=0.1)
        lb = T("올 때", 22, ORANGE, bold=True).next_to(back, RIGHT, buff=0.1)
        self.play(GrowArrow(go), FadeIn(lg), run_time=0.9)
        self.play(GrowArrow(back), FadeIn(lb), run_time=0.9)
        self.say("4.0 s 동안 초음파는 바닥까지 내려갔다가 다시 올라왔다\n→ 실제로 움직인 길이는 '수심의 2배'")

        # 3. 공식
        f = frac([("음속", ORANGE), ("×", WHITE_T), ("시간 차", GREEN)], [("2", WHITE_T)])
        f1 = eq_row("수심", "=", f)
        nt = T("← 갔다가 되돌아왔으니 2로 나눈다", 20, GRAY_T)
        r1 = VGroup(f1, nt).arrange(RIGHT, buff=0.35)
        f2n = colored([("(1500 m/s)", ORANGE), ("×", WHITE_T), ("(4.0 s)", GREEN)])
        f2 = frac(f2n, colored([("2", WHITE_T)]))
        mid = colored([("=", WHITE_T), ("6000 m", WHITE_T), ("÷ 2", WHITE_T)])
        res = T("= 3000 m", 34, GREEN, bold=True)
        r2 = eq_row("=", f2, mid, res)
        r2.next_to(r1, DOWN, buff=0.35, aligned_edge=LEFT).shift(RIGHT * 1.15)
        rt = T("왕복한 길이", 18, GRAY_T).next_to(mid[1], DOWN, buff=0.12)
        pnl = panel(VGroup(r1, r2, rt).scale(0.86), buff=0.3, pos=[1.65, 2.8, 0])
        self.play(FadeOut(clock), FadeOut(sn), FadeIn(pnl[0]), Write(r1), run_time=1.2)
        self.say("수심(바닥까지의 거리) = 음속 × 시간 차 ÷ 2", wait=2.2)
        self.play(FadeIn(r2[0]), FadeIn(f2), run_time=1)
        self.say("바닷물 속 음속(1500 m/s)과 시간 차(4.0 s)를 대입한다\n(단위: m/s × s = m)", wait=3.4)
        self.play(FadeIn(mid), FadeIn(rt), run_time=0.8)
        self.say("1500 × 4.0 = 6000 m … 내려갔다 올라온 왕복 길이", wait=2.6)
        self.play(FadeIn(res, shift=LEFT * 0.2), run_time=0.7)
        self.play(FadeOut(go), FadeOut(lg), FadeOut(back), FadeOut(lb), run_time=0.4)
        dl = dim_line([X0 + 0.55, SURF, 0], [X0 + 0.55, y_of(d0), 0], "3000 m",
                      side=RIGHT * 0.8)
        self.play(Create(dl), run_time=1)
        self.say("2로 나누면 이 지점의 수심은 3000 m (= 3 km)")
        self.wait(0.4)

        # 4. 여러 지점에서 재기
        self.play(FadeOut(pnl), FadeOut(dl), FadeOut(tl), FadeOut(m0), FadeOut(m1),
                  FadeOut(sp), run_time=0.6)
        sn2 = slow_note("※ 실제보다 빠르게 보여 줌")
        vnote = T("※ 세로(깊이)를 실제보다 크게 늘려 그림", 18, GRAY_T).next_to(sn2, DOWN,
                                                                     aligned_edge=LEFT, buff=0.1)
        # 바닥을 물 색으로 덮어 '안 보이는' 상태로 (물 그라데이션과 같은 색)
        top_c = interpolate_color(ManimColor(WATER_TOP), ManimColor(WATER_DEEP),
                                  (SURF - floor[0].get_top()[1]) / (SURF + 4.3))
        fog = floor[0].copy().set_stroke(width=0)
        fog.set_fill(color=[top_c, WATER_DEEP], opacity=1).set_sheen_direction(DOWN)
        self.play(FadeIn(sn2), FadeIn(vnote), FadeIn(fog), FadeOut(floor[1]), run_time=1)
        self.say("실제로 배에서는 바닥이 보이지 않는다.\n배를 옮기며 여러 곳에서 재어 보자")

        # 수심 눈금
        AX = -6.25
        axis = Line([AX, SURF, 0], [AX, y_of(3300), 0], stroke_color=GRAY_T, stroke_width=2)
        ticks = VGroup()
        for d in (0, 1000, 2000, 3000):
            ticks.add(Line([AX - 0.06, y_of(d), 0], [AX + 0.06, y_of(d), 0], color=GRAY_T,
                           stroke_width=2))
            ticks.add(T(f"{d} m", 16, GRAY_T).next_to([AX - 0.08, y_of(d), 0], LEFT, buff=0.06))
        axl = T("수심", 18, GRAY_T, bold=True).next_to(axis, DOWN, buff=0.1)
        self.play(FadeIn(axis), FadeIn(ticks), FadeIn(axl), run_time=0.6)

        dots = VGroup()
        labs = VGroup()

        def place(x, d, run=0.5):
            t = 2 * d / 1500
            dot = Dot([x, y_of(d), 0], radius=0.09, color=GREEN)
            lab = VGroup(T(f"{t:.1f} s", 19, GREEN, bold=True), T("→", 19, WHITE_T),
                         T(f"{d} m", 19, WHITE_T, bold=True)).arrange(RIGHT, buff=0.08)
            lab.next_to(dot, UP, buff=0.18)
            bgk = BackgroundRectangle(lab, color="#06111D", fill_opacity=0.6, buff=0.05)
            lab = VGroup(bgk, lab)
            self.play(FadeIn(dot, scale=1.8), FadeIn(lab, shift=UP * 0.1), run_time=run)
            dots.add(dot)
            labs.add(lab)

        place(X0, d0)
        for i, (x, d) in enumerate(SPOTS[1:], start=1):
            self.play(ship.animate.move_to(ship.get_center() + RIGHT * (x - ship[-1].get_x())),
                      run_time=0.9)
            s_ = TR()
            g_ = np.array([x, y_of(d), 0])
            Dk = np.linalg.norm(g_ - s_)
            Tk = d / 1500
            tk = ValueTracker(0)
            wk = always_redraw(lambda tk=tk, s_=s_, g_=g_, Dk=Dk, Tk=Tk: echo_group(
                tk.get_value() / Tk * Dk, s_, g_, 0.25, 3, 0.6, 0.7, back_dir=UP))
            self.add(wk)
            # 화면 속 파동 속력은 모든 지점에서 같게 (깊을수록 오래 걸린다)
            self.play(tk.animate.set_value(2 * Tk + 0.5), run_time=(2 * Tk + 0.5) * 0.42,
                      rate_func=linear)
            self.remove(wk)
            place(x, d, run=0.45)
            if i == 1:
                self.say("3.0 s → 수심 = 1500 × 3.0 ÷ 2 = 2250 m", wait=2.2)
            elif i == 2:
                self.say("2.0 s → 수심 = 1500 × 2.0 ÷ 2 = 1500 m\n메아리가 빨리 왔다 = 바닥이 얕다", wait=3.0)
            elif i == 3:
                self.unsay()

        # 5. 점을 이어 지형 복원
        prof = VMobject(stroke_color=GREEN, stroke_width=4)
        prof.set_points_as_corners([d.get_center() for d in dots])
        self.say("측정한 점들을 이으면…", wait=0.2)
        self.play(Create(prof), run_time=1.6)
        self.play(FadeOut(fog), FadeIn(floor[1]), run_time=1.2)
        self.bring_to_front(prof, dots, labs)
        self.say("바다 밑바닥의 모양(해저 지형)이 드러난다", wait=2.2)
        key = T("시간 차가 클수록 수심이 깊다", 30, GREEN, bold=True)
        kp = panel(key, buff=0.25, pos=[1.2, 3.0, 0])
        self.play(FadeIn(kp, shift=DOWN * 0.1), run_time=0.7)
        self.play(Indicate(labs[2], color=ORANGE, scale_factor=1.15),
                  Indicate(labs[0], color=ORANGE, scale_factor=1.15), run_time=1.2)
        self.say("2.0 s 는 1500 m(얕다), 4.0 s 는 3000 m(깊다)\n→ 음속이 같으면 시간 차가 2배일 때 수심도 2배 (비례)")
        self.wait(0.4)

        # 6. 다중빔 (한 박자)
        self.clear_all(keep=(bg,))
        fs = VGroup()  # 앞에서 본 배
        fh = Polygon([-0.55, 0.3, 0], [0.55, 0.3, 0], [0.35, 0, 0], [-0.35, 0, 0],
                     fill_color="#C94C4C", fill_opacity=1, stroke_color=WHITE_T, stroke_width=1.2)
        fc = Rectangle(width=0.5, height=0.35, fill_color="#E8EDF2", fill_opacity=1,
                       stroke_color=WHITE_T, stroke_width=1.2).move_to([0, 0.47, 0])
        fs.add(fh, fc)
        SX = -3.4
        fs.shift([SX, SURF - DRAFT, 0])
        src2 = np.array([SX, SURF - DRAFT, 0])
        prof2 = lambda x: 2350 + 420 * np.sin(1.6 * (x - SX) + 0.6) + 160 * np.sin(4.1 * (x - SX))
        xs = np.linspace(SX - 3.2, SX + 3.2, 60)
        fl2 = VMobject(stroke_color="#B08A63", stroke_width=3)
        fl2.set_points_smoothly([np.array([x, y_of(prof2(x)), 0]) for x in xs])
        fill2 = fl2.copy().set_stroke(width=0)
        fill2.add_line_to(np.array([SX + 3.2, -1.9, 0]))
        fill2.add_line_to(np.array([SX - 3.2, -1.9, 0]))
        fill2.add_line_to(fl2.get_start())
        fill2.set_fill(color=["#4A3A2E", "#1E1712"], opacity=1).set_sheen_direction(DOWN)
        lab_front = T("배 앞에서 본 모습", 20, GRAY_T).move_to([SX, -2.25, 0])
        rays = VGroup()
        hits = VGroup()
        for a in np.linspace(-0.8, 0.8, 15):
            # 각 빔이 바닥에 닿는 점 찾기
            dirv = np.array([np.sin(a), -np.cos(a), 0])
            for s in np.linspace(0.2, 6, 600):
                p = src2 + dirv * s
                if p[1] <= y_of(prof2(p[0])):
                    break
            c = depth_color(prof2(p[0]))
            rays.add(Line(src2, p, stroke_color=CYAN, stroke_width=1.6, stroke_opacity=0.75))
            hits.add(Dot(p, radius=0.07, color=c))
        self.play(FadeIn(fill2), FadeIn(fl2), FadeIn(fs), FadeIn(lab_front), run_time=0.8)
        self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.05), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(h, scale=1.6) for h in hits], lag_ratio=0.05),
                  run_time=1.0)
        self.say("요즘 조사선은 부채꼴로 여러 빔을 한꺼번에 쏜다 (다중빔)", wait=2.2)

        # 위에서 본 지형도 띠
        cols, rows_ = 16, 6
        cw, chh = 0.34, 0.34
        MX, MY = 3.6, -0.15
        cells = VGroup()
        for i in range(cols):
            for j in range(rows_):
                xx = (i - cols / 2) * 0.55
                yy = (j - rows_ / 2) * 0.55
                d = 2300 + 520 * np.sin(0.9 * xx + 0.4 * yy) + 260 * np.cos(1.3 * yy - 0.6 * xx)
                cells.add(Square(cw, stroke_width=0, fill_color=depth_color(d), fill_opacity=1)
                          .move_to([MX + (i - (cols - 1) / 2) * cw, MY + (j - (rows_ - 1) / 2) * chh, 0]))
        frame = SurroundingRectangle(cells, buff=0.0, stroke_color=WHITE_T, stroke_width=1.5)
        mlab = T("위에서 본 해저 지형도", 20, GRAY_T).next_to(frame, UP, buff=0.15)
        cb = VGroup(*[Square(0.22, stroke_width=0, fill_color=depth_color(1300 + 1900 * k / 11),
                             fill_opacity=1) for k in range(12)]).arrange(RIGHT, buff=0)
        cb.next_to(frame, DOWN, buff=0.35)
        cbl = VGroup(T("얕다", 18, WHITE_T).next_to(cb, LEFT, buff=0.12),
                     T("깊다", 18, WHITE_T).next_to(cb, RIGHT, buff=0.12))
        arrow = Arrow([MX - 3.1, MY - 1.3, 0], [MX + 3.1, MY - 1.3, 0], buff=0, color=GRAY_T,
                      stroke_width=2, tip_length=0.15)
        alab = T("배가 지나간 길", 16, GRAY_T).next_to(arrow, DOWN, buff=0.06)
        self.play(FadeIn(frame), FadeIn(mlab), run_time=0.5)
        order = sorted(range(len(cells)), key=lambda k: k // rows_)
        self.play(LaggedStart(*[FadeIn(cells[k]) for k in order], lag_ratio=0.01),
                  GrowArrow(arrow), FadeIn(alab), run_time=2.2)
        self.play(FadeIn(cb), FadeIn(cbl), run_time=0.5)
        self.say("배가 지나가는 동안 넓은 띠 모양으로 수심을 재어\n수심에 따라 색을 칠한 지형도를 만든다")
        self.wait(0.3)

        # 7. 정리
        self.clear_all(keep=(bg,))
        summ = VGroup(
            T("해저 지형 조사 정리", 30, CYAN, bold=True),
            T("· 배 밑의 송수파기가 초음파를 아래로 쏘고, 바닥의 반사파를 받는다", 26),
            T("· 바닷물 속 음속: 약 1500 m/s", 26),
            T("· 시간 차 4.0 s → 수심 = 1500 × 4.0 ÷ 2 = 3000 m", 26),
            T("· 시간 차가 클수록 수심이 깊다 → 여러 곳을 재면 해저 지형이 보인다", 26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        sp_ = panel(summ, buff=0.5, pos=ORIGIN + UP * 0.3)
        self.play(FadeIn(sp_, shift=UP * 0.2), run_time=0.8)
        self.wait(5)
        self.play(FadeOut(sp_), run_time=0.6)

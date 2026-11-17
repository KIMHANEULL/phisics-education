"""사례 8. 비파괴 검사 (초음파 탐상) — 강철판 속 균열의 깊이 재기."""
from common import *

# ------------------------------------------------------------ 배치 (화면 단위)
TOP, BOT = 0.55, -2.25           # 강철판 윗면 / 바닥면  → 두께 3 cm
CM = (TOP - BOT) / 3.0           # 1 cm 의 화면 길이
PX0, PX1 = -7.6, 0.95            # 강철판 가로 범위 (왼쪽은 화면 밖으로 이어짐)
CRACK_X = (-2.25, -0.0)          # 균열 가로 범위 (2.25 단위 ≈ 2.4 cm)
CRACK_Y = TOP - 1.2 * CM         # 균열 깊이 1.2 cm
D_BACK = TOP - BOT
D_CRACK = TOP - CRACK_Y
US_ONEWAY = 5.0                  # 바닥면까지 한 방향 5.0 μs (왕복 10.0 μs)
UNIT_PER_US = D_BACK / US_ONEWAY  # 화면 속 파동 속도 (실제 거리에 비례)
BEAM_HALF = 0.28                 # 빔 반폭 (화면 단위)


def steel_plate():
    body = Rectangle(width=PX1 - PX0, height=D_BACK, stroke_color="#A9B8C6",
                     stroke_width=2)
    body.set_fill(color=["#5D6976", "#38414B"], opacity=1).set_sheen_direction(DOWN)
    body.move_to([(PX0 + PX1) / 2, (TOP + BOT) / 2, 0])
    tex = VGroup()
    for i in range(1, 6):
        y = BOT + D_BACK * i / 6
        tex.add(Line([PX0, y, 0], [PX1, y, 0], stroke_width=1, color="#7D8B99",
                     stroke_opacity=0.18))
    lab = T("강철판", 22, "#D5DDE5", bold=True).move_to([-6.25, TOP - 0.3, 0])
    return VGroup(body, tex, lab)


def crack_shape(opacity=1.0):
    xs = np.linspace(CRACK_X[0], CRACK_X[1], 11)
    rng = np.random.default_rng(3)
    pts = [[x, CRACK_Y + 0.05 * rng.standard_normal(), 0] for x in xs]
    pts[0][1] = pts[-1][1] = CRACK_Y
    ln = VMobject(stroke_color="#0B0F14", stroke_width=5, stroke_opacity=opacity)
    ln.set_points_as_corners(pts)
    edge = ln.copy().set_stroke(color=RED_T, width=1.5, opacity=0.8 * opacity)
    return VGroup(ln, edge)


def probe_shape(x):
    gel = Rectangle(width=0.8, height=0.07, stroke_width=0, fill_color=CYAN,
                    fill_opacity=0.45).move_to([x, TOP + 0.035, 0])
    crystal = Rectangle(width=0.62, height=0.07, stroke_width=0, fill_color=ORANGE,
                        fill_opacity=0.9).move_to([x, TOP + 0.105, 0])
    body = RoundedRectangle(corner_radius=0.08, width=0.7, height=0.55,
                            stroke_color=WHITE_T, stroke_width=1.5,
                            fill_color="#2B3D52", fill_opacity=1)
    body.move_to([x, TOP + 0.14 + 0.275, 0])
    cable = Line([x, TOP + 0.69, 0], [x, TOP + 0.85, 0], stroke_width=4, color="#8A98A8")
    return VGroup(cable, body, crystal, gel)


def crack_overlap(x):
    """빔(폭 2*BEAM_HALF)이 균열과 겹치는 비율 0~1."""
    a, b = x - BEAM_HALF, x + BEAM_HALF
    ov = max(0.0, min(b, CRACK_X[1]) - max(a, CRACK_X[0]))
    return ov / (2 * BEAM_HALF)


def plate_waves(t_us, x, gap=0.26, n=3):
    """t_us: 경과 시간(μs). 송신파(청록) + 균열 반사파 + 바닥면 반사파(주황)."""
    s = t_us * UNIT_PER_US
    f = crack_overlap(x)
    g = VGroup()
    for k in range(n):
        w = 1 - 0.25 * k
        r = s - k * gap
        if 0.03 < r < D_BACK:
            op = (1 - 0.35 * r / D_BACK) * w
            if r > D_CRACK:
                op *= (1 - 0.6 * f)
            g.add(ring_arc([x, TOP, 0], r, DOWN, 0.8, CYAN, 5, op))
        rb = s - D_BACK - k * gap
        if 0.03 < rb < D_BACK:
            op = (1 - 0.35 * rb / D_BACK) * w * (1 - 0.6 * f)
            g.add(ring_arc([x, BOT, 0], rb, UP, 0.7, ORANGE, 5, op))
        if f > 0:
            rc = s - D_CRACK - k * gap
            if 0.03 < rc < D_CRACK:
                op = (1 - 0.35 * rc / D_CRACK) * w * min(1, 0.4 + f)
                g.add(ring_arc([x, CRACK_Y, 0], rc, UP, 0.8, ORANGE, 5, op))
    return g


def echoes_at(x):
    """탐촉자 위치 x 에서 A-스캔에 나타나는 (시각 μs, 세기) 목록."""
    f = crack_overlap(x)
    out = [(0.0, 1.0), (2 * US_ONEWAY, 0.78 * (1 - 0.6 * f))]
    if f > 0:
        out.append((2 * US_ONEWAY * D_CRACK / D_BACK, 0.9 * min(1, 0.3 + f)))
    return out


class AScan(VGroup):
    """오실로스코프 모양 A-스캔 화면. 가로 = 시간(μs), 세로 = 되돌아온 신호 세기."""

    def __init__(self, t_tracker, x_tracker, x0=2.85, x1=6.35, yb=-1.8, h=2.0,
                 tmax=12, **kw):
        super().__init__(**kw)
        self.x0, self.x1, self.yb, self.h, self.tmax = x0, x1, yb, h, tmax
        box = RoundedRectangle(corner_radius=0.12, width=x1 - x0 + 0.85,
                               height=h + 1.25, stroke_color=PANEL_STROKE,
                               stroke_width=1.5, fill_color="#06120E", fill_opacity=0.95)
        box.move_to([(x0 + x1) / 2 - 0.05, yb + h / 2 + 0.05, 0])
        ttl = T("A-스캔 화면 (초음파 탐상기)", 20, GRAY_T, bold=True)
        ttl.move_to(box.get_top() + DOWN * 0.22)
        grid = VGroup()
        for i in range(0, tmax + 1, 2):
            x = self.x_of(i)
            grid.add(Line([x, yb, 0], [x, yb + h, 0], stroke_width=1, color=GREEN,
                          stroke_opacity=0.15))
        axis = Line([x0, yb, 0], [x1, yb, 0], stroke_width=2, color=GRAY_T)
        nums = VGroup(*[T(str(i), 18, GRAY_T).move_to([self.x_of(i), yb - 0.22, 0])
                        for i in range(0, tmax + 1, 2)])
        ul = T("시간 (μs)", 18, GRAY_T).next_to(nums, DOWN, buff=0.06).align_to(axis, RIGHT)
        self.box = box
        self.add(box, ttl, grid, axis, nums, ul)

        def trace():
            tm = min(max(t_tracker.get_value(), 0), tmax)
            ts = np.arange(0, tm + 1e-9, 0.02)
            if len(ts) < 2:
                ts = np.array([0, 0.001])
            ech = echoes_at(x_tracker.get_value())
            pts = []
            for t in ts:
                v = 0.03 + 0.025 * abs(np.sin(37 * t) * np.sin(11 * t + 1))
                for t0, a in ech:
                    if t >= t0 - 0.4:
                        v += a * np.exp(-((t - t0) / 0.13) ** 2) * (0.6 + 0.4 * np.cos(45 * (t - t0)))
                pts.append([self.x_of(t), yb + h * min(v, 1.0), 0])
            m = VMobject(stroke_color=GREEN, stroke_width=2.5)
            m.set_points_as_corners(pts)
            return m

        self.trace = always_redraw(trace)
        self.add(self.trace)

    def x_of(self, t):
        return self.x0 + (self.x1 - self.x0) * t / self.tmax

    def tag(self, t, amp, text, color):
        x = self.x_of(t)
        lab = T(text, 16, color, bold=True)
        lab.move_to([x, self.yb + self.h * amp + 0.22, 0])
        return lab


def frac_row(num_parts, size=27):
    return frac(colored(num_parts, size), colored([("2", WHITE_T)], size), size)


class C8NDT(CaseScene):
    def construct(self):
        bg = studio_bg(horizon=1.9)
        self.add(bg)

        plate = steel_plate()
        crack = crack_shape(0.55)
        px = ValueTracker(-4.3)
        probe = always_redraw(lambda: probe_shape(px.get_value()))

        # 0. 제목
        card = title_card("비파괴 검사 (초음파 탐상)", case_no=8)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(card), run_time=0.6)
        self.play(FadeIn(plate), FadeIn(crack), FadeIn(probe, shift=DOWN * 0.2), run_time=1)

        # 1. 등장 요소
        thick = dim_line([PX1 + 0.25, TOP, 0], [PX1 + 0.25, BOT, 0], "3 cm",
                         side=RIGHT * 0.5, size=24)
        c_probe = callout([-4.05, TOP + 0.55, 0], "탐촉자", "전기 신호 ↔ 초음파 진동", UR, 0.75)
        c_gel = callout([-3.9, TOP + 0.035, 0], "접촉 매질 (기름·젤)",
                        "틈의 공기층을 없애 초음파가 잘 들어가게", RIGHT + UP * 0.45, 1.1,
                        color=CYAN)
        self.play(Create(thick), Create(c_probe), run_time=0.8)
        self.say("두께 3 cm 강철판 단면. 탐촉자는 전기 신호를 초음파로 바꿔 보내고,\n되돌아온 초음파를 다시 전기 신호로 바꾼다", wait=5.2)
        self.play(FadeOut(c_probe), Create(c_gel), run_time=0.8)
        self.say("탐촉자와 강철 사이에 기름·젤을 발라 공기층을 없앤다\n(공기층이 있으면 초음파가 거의 다 반사되어 못 들어간다)",
                 wait=4.5)
        self.play(FadeOut(c_gel), run_time=0.5)
        c_crack = callout([(CRACK_X[0] + CRACK_X[1]) / 2, CRACK_Y, 0], "속에 숨은 균열",
                          "겉에서는 보이지 않는다", UP + RIGHT * 0.35, 1.75, color=RED_T)
        self.play(Create(c_crack), run_time=0.8)
        self.say("강철 속에 금(균열)이 숨어 있을 수 있다.\n자르지 않고 어떻게 찾을까?")
        self.play(FadeOut(c_crack), run_time=0.5)

        # 2. 균열 없는 곳: 바닥면 에코만
        tt = ValueTracker(0)  # μs
        clock = Clock(tt, "μs", "{:.1f}")
        sn = slow_note()
        scope = AScan(tt, px)
        self.play(FadeIn(sn), FadeIn(clock), FadeIn(scope), run_time=0.8)
        waves = always_redraw(lambda: plate_waves(tt.get_value(), px.get_value()))
        self.add(waves)
        self.say("탐촉자가 아주 짧은 초음파 펄스를 아래로 보낸다\n(강철 속 음속 약 5900 m/s)",
                 wait=0.5)
        self.play(tt.animate.set_value(US_ONEWAY), run_time=4.5, rate_func=linear)
        c_back = callout([px.get_value() + 0.15, BOT, 0], "바닥면에서 반사", None,
                         RIGHT + UP * 0.6, 0.6)
        self.play(FadeIn(c_back), run_time=0.4)
        self.say("균열이 없는 곳에서는 바닥면까지 가서 반사된다", wait=0.3)
        self.play(tt.animate.set_value(2 * US_ONEWAY), run_time=4.5, rate_func=linear)
        self.remove(waves)
        tg0 = scope.tag(0, 1.0, "송신 펄스", GRAY_T).shift(RIGHT * 0.5 + DOWN * 0.08)
        tgb = scope.tag(10, 0.78, "바닥면 에코", ORANGE)
        self.play(FadeOut(c_back), FadeIn(tg0), FadeIn(tgb), run_time=0.6)
        self.play(tt.animate.set_value(12), run_time=1.2, rate_func=linear)
        self.say("화면에서 10.0 μs 뒤에 바닥면 에코가 뾰족하게 나타난다\nμs(마이크로초) = 백만분의 1초 → 10.0 μs = 0.0000100 s", wait=5.4)

        # 3. 공식 → 두께
        f1 = distance_formula(27)
        nt = T("← 갔다가 되돌아왔으니 2로 나눈다", 19, GRAY_T)
        r1 = VGroup(f1, nt).arrange(RIGHT, buff=0.35)
        f2 = frac_row([("(5900 m/s)", ORANGE), ("×", WHITE_T), ("(0.0000100 s)", GREEN)])
        res = T("= 0.0295 m  ≈  3.0 cm", 27, GREEN, bold=True)
        r2 = eq_row("=", f2, res)
        r2[0].scale(27 / 34)
        r2.arrange(RIGHT, buff=0.22)
        r2.next_to(r1, DOWN, buff=0.3, aligned_edge=LEFT).shift(RIGHT * 1.0)
        body = VGroup(r1, r2)
        pnl = panel(body, buff=0.3).scale(0.9).move_to([-0.6, 2.8, 0]).to_edge(UP, buff=0.08)
        self.play(FadeOut(sn), FadeOut(clock), FadeIn(pnl[0]), Write(r1), run_time=1.2)
        self.play(FadeIn(r2[0]), FadeIn(f2), run_time=1)
        self.say("음속(5900 m/s)과 시간 차(0.0000100 s)를 대입\n(단위: m/s × s = m)", wait=3.7)
        self.play(FadeIn(res, shift=LEFT * 0.2), run_time=0.7)
        self.play(Indicate(thick[3], color=GREEN, scale_factor=1.3), run_time=1)
        self.say("계산한 약 3.0 cm ≈ 실제 판 두께 3 cm\n→ 바닥면까지의 거리를 맞게 잰 것", wait=3.5)
        self.play(FadeOut(pnl), FadeOut(tg0), FadeOut(tgb), FadeOut(scope.trace), run_time=0.6)

        # 4. 균열 위로 이동 → 균열 에코가 먼저 온다
        tt.set_value(0)
        self.add(scope.trace)
        self.say("탐촉자를 균열 위로 옮겨 다시 쏘아 보자", wait=0.3)
        self.play(px.animate.set_value(-1.1), run_time=1.8)
        clock2 = Clock(tt, "μs", "{:.1f}")
        sn2 = slow_note()
        self.play(FadeIn(sn2), FadeIn(clock2), run_time=0.5)
        waves = always_redraw(lambda: plate_waves(tt.get_value(), px.get_value()))
        self.add(waves)
        self.play(tt.animate.set_value(2.0), run_time=1.8, rate_func=linear)
        self.say("균열을 만나면 일부가 그곳에서 먼저 반사된다", wait=0.6)
        self.play(tt.animate.set_value(4.0), run_time=1.8, rate_func=linear)
        tgc = scope.tag(4, 0.9, "균열 에코", ORANGE)
        self.play(FadeIn(tgc), run_time=0.4)
        self.say("균열 에코: 4.0 μs 만에 돌아왔다 (바닥면보다 빨리)", wait=1.5)
        self.play(tt.animate.set_value(2 * US_ONEWAY), run_time=5.4, rate_func=linear)
        self.remove(waves)
        tgb2 = scope.tag(10, 0.78 * 0.4 + 0.05, "바닥면 에코 (약해짐)", ORANGE)
        self.play(FadeIn(tgb2), run_time=0.4)
        self.play(tt.animate.set_value(12), run_time=1.0, rate_func=linear)
        self.say("균열에 가려 바닥면 에코는 약해진다", wait=2.2)

        # 5. 균열 깊이 계산
        g1 = distance_formula(27)
        g2 = frac_row([("(5900 m/s)", ORANGE), ("×", WHITE_T), ("(0.0000040 s)", GREEN)])
        gres = T("= 0.0118 m  ≈  1.2 cm", 27, GREEN, bold=True)
        q2 = eq_row("=", g2, gres)
        q2[0].scale(27 / 34)
        q2.arrange(RIGHT, buff=0.22)
        q1 = VGroup(g1, T("4.0 μs = 0.0000040 s", 19, GRAY_T)).arrange(RIGHT, buff=0.35)
        q2.next_to(q1, DOWN, buff=0.3, aligned_edge=LEFT).shift(RIGHT * 1.0)
        pnl2 = panel(VGroup(q1, q2), buff=0.3).scale(0.9).move_to([-0.6, 2.8, 0]).to_edge(UP, buff=0.08)
        self.play(FadeOut(sn2), FadeOut(clock2), FadeIn(pnl2[0]), Write(q1), run_time=1)
        self.play(FadeIn(q2[0]), FadeIn(g2), run_time=1)
        self.say("같은 공식에 균열 에코의 시간 차(0.0000040 s)를 대입", wait=2.5)
        self.play(FadeIn(gres, shift=LEFT * 0.2), run_time=0.7)
        dd = dim_line([-0.45, TOP, 0], [-0.45, CRACK_Y, 0], "1.2 cm", side=RIGHT * 0.55,
                      size=22)
        self.play(crack.animate.set_stroke(opacity=1), Create(dd), run_time=1)
        self.say("균열은 겉면에서 1.2 cm 아래에 있다\n시간이 바닥면의 0.4배(4.0 ÷ 10.0) → 깊이도 두께의 0.4배", wait=5.4)
        self.play(FadeOut(pnl2), FadeOut(dd), FadeOut(tgc), FadeOut(tgb2), run_time=0.6)

        # 6. 탐촉자를 옮기며 훑기 → 균열 위치·크기
        self.say("탐촉자를 표면을 따라 옮기면서 화면을 계속 본다", wait=0.3)
        self.play(px.animate.set_value(-3.4), run_time=1.5)
        xs_on, xs_off = CRACK_X[0], CRACK_X[1]
        self.play(px.animate.set_value(xs_on + 0.05), run_time=1.6, rate_func=linear)
        mk1 = Line([xs_on, TOP + 0.02, 0], [xs_on, TOP + 1.15, 0], color=GREEN,
                   stroke_width=3)
        self.play(Create(mk1), run_time=0.4)
        self.bring_to_front(probe)
        self.say("균열 에코가 나타나기 시작 → 이 근처가 균열의 시작", wait=2.0)
        self.play(px.animate.set_value(xs_off - 0.05), run_time=2.6, rate_func=linear)
        self.play(px.animate.set_value(xs_off + 0.4), run_time=1.0, rate_func=linear)
        mk2 = Line([xs_off, TOP + 0.02, 0], [xs_off, TOP + 1.15, 0], color=GREEN,
                   stroke_width=3)
        self.play(Create(mk2), run_time=0.4)
        self.bring_to_front(probe)
        self.say("균열 에코가 사라짐 → 이 근처가 균열의 끝", wait=2.0)
        self.play(px.animate.set_value(0.4), run_time=0.8)
        ln = dim_line([xs_on, TOP + 0.95, 0], [xs_off, TOP + 0.95, 0], "균열 길이 약 2.4 cm",
                      offset=UP * 0.3, size=22)
        self.play(Create(ln), run_time=0.8)
        self.say("에코가 보인 구간 = 균열의 위치와 크기\n부품을 자르거나 부수지 않고 속을 알아낸다", wait=4)

        # 7. 어디에 쓰일까
        self.clear_all(keep=(bg,))
        uses = VGroup(
            T("왜 중요할까? — 안전 점검", 30, CYAN, bold=True),
            T("· 비행기 날개·동체,  기차 바퀴·레일", 26),
            T("· 다리(교량),  가스·석유 배관,  원자력 설비", 26),
            T("· 겉은 멀쩡해도 속의 균열이 커지면 큰 사고가 된다", 26),
            T("· 관련 직업: 비파괴검사 기술자", 26, GREEN),
            T("   (국가기술자격: 초음파비파괴검사 기능사·산업기사·기사)", 22, GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        up = panel(uses, buff=0.45, pos=UP * 0.45)
        self.play(FadeIn(up, shift=UP * 0.2), run_time=0.8)
        self.say("미리 찾아 고치면 사고를 막을 수 있다", wait=9)
        self.unsay()
        self.wait(1)
        self.play(FadeOut(up), run_time=0.6)

        # 8. 정리
        summ = VGroup(
            T("비파괴 검사 정리", 30, CYAN, bold=True),
            T("· 강철 속 음속(종파):  약 5900 m/s,   μs = 백만분의 1초", 26),
            T("· 바닥면 에코 10.0 μs → 5900 × 0.0000100 ÷ 2 ≈ 3.0 cm (두께)", 26),
            T("· 균열 에코 4.0 μs → 5900 × 0.0000040 ÷ 2 ≈ 1.2 cm (균열 깊이)", 26),
            T("· 탐촉자를 옮기며 훑으면 균열의 위치·크기를 안다", 26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        sp_ = panel(summ, buff=0.5, pos=UP * 0.3)
        self.play(FadeIn(sp_, shift=UP * 0.2), run_time=0.8)
        self.wait(11)
        self.play(FadeOut(sp_), run_time=0.6)

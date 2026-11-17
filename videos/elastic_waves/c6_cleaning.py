"""사례 6. 초음파 세척 — 밀·소가 번갈아 오는 종파와 공동 현상(캐비테이션)."""
from common import *

# ------------------------------------------------------------ 배치 (화면 단위)
TX0, TX1 = -6.0, -0.8             # 세척조 안쪽 가로 범위
WB, WS = -2.0, 1.0                # 물 바닥 / 물 표면 → 깊이 15 cm
CM = (WS - WB) / 15.0             # 1 cm = 0.2 단위
LAM = 3.75 * CM                   # 파장 3.75 cm (40 kHz, 1500 m/s)
K = 2 * PI / LAM
AMP = 0.07                        # 물 알갱이 변위 (보이게 과장)
G_C = np.array([-3.4, -0.55, 0])  # 안경 중심
INSET_C = np.array([3.6, -0.15, 0])
GS = 1.25                         # 안경 크기 배율


def gp(v):
    """안경 중심 기준 상대 위치 → 화면 위치."""
    return G_C + GS * np.array(v, dtype=float)

DIRT = "#8A6A3A"


def tank():
    water = Rectangle(width=TX1 - TX0, height=WS - WB, stroke_width=0)
    water.set_fill(color=[WATER_TOP, WATER_DEEP], opacity=1).set_sheen_direction(DOWN)
    water.move_to([(TX0 + TX1) / 2, (WS + WB) / 2, 0])
    surf = Line([TX0, WS, 0], [TX1, WS, 0], color=CYAN, stroke_width=2, stroke_opacity=0.6)
    wall = VMobject(stroke_color="#B9C7D4", stroke_width=5)
    wall.set_points_as_corners([[TX0 - 0.06, WS + 0.55, 0], [TX0 - 0.06, WB - 0.06, 0],
                                [TX1 + 0.06, WB - 0.06, 0], [TX1 + 0.06, WS + 0.55, 0]])
    return VGroup(water, surf, wall)


def transducers(ph=0.0):
    g = VGroup()
    dy = -0.035 * np.sin(ph)   # 바닥 물 알갱이와 같은 위상으로 민다
    for x in (-4.9, -3.4, -1.9):
        top = Rectangle(width=0.9, height=0.07, stroke_width=0, fill_color=ORANGE,
                        fill_opacity=0.95).move_to([x, WB - 0.13 + dy, 0])
        body = Rectangle(width=0.9, height=0.26, stroke_color=WHITE_T, stroke_width=1.2,
                         fill_color="#2B3D52", fill_opacity=1).move_to([x, WB - 0.3 + dy, 0])
        g.add(body, top)
    return g


def glasses(dirty=1.0):
    c = G_C
    frame = "#E3E8EE"
    lens_l = Circle(radius=0.48, stroke_color=frame, stroke_width=4, fill_color="#BFE6FF",
                    fill_opacity=0.18).move_to(c + LEFT * 0.62)
    lens_r = lens_l.copy().move_to(c + RIGHT * 0.62)
    bridge = ArcBetweenPoints(c + LEFT * 0.16 + UP * 0.2, c + RIGHT * 0.16 + UP * 0.2,
                              angle=-PI / 2, stroke_color=frame, stroke_width=4)
    arm_l = Line(c + LEFT * 1.08 + UP * 0.18, c + LEFT * 1.45 + UP * 0.28,
                 stroke_color=frame, stroke_width=4)
    arm_r = Line(c + RIGHT * 1.08 + UP * 0.18, c + RIGHT * 1.45 + UP * 0.28,
                 stroke_color=frame, stroke_width=4)
    hinge_l = Dot(c + LEFT * 1.1 + UP * 0.18, radius=0.06, color=frame)
    hinge_r = Dot(c + RIGHT * 1.1 + UP * 0.18, radius=0.06, color=frame)
    pad_l = Ellipse(width=0.1, height=0.18, stroke_color=frame, stroke_width=2,
                    fill_color=frame, fill_opacity=0.5).move_to(c + LEFT * 0.22 + DOWN * 0.15)
    pad_r = pad_l.copy().move_to(c + RIGHT * 0.22 + DOWN * 0.15)
    g = VGroup(lens_l, lens_r, bridge, arm_l, arm_r, hinge_l, hinge_r, pad_l, pad_r)
    dirt = VGroup()
    rng = np.random.default_rng(5)
    spots = [c + LEFT * 0.62 + [0.15, -0.2, 0], c + LEFT * 0.75 + [0, 0.18, 0],
             c + RIGHT * 0.5 + [0.1, -0.1, 0], c + RIGHT * 0.75 + [0, 0.25, 0],
             c + LEFT * 0.22 + DOWN * 0.08, c + RIGHT * 0.22 + DOWN * 0.22,
             c + LEFT * 1.1 + UP * 0.25, c + RIGHT * 1.12 + UP * 0.12]
    for p in spots:
        dirt.add(Dot(p, radius=rng.uniform(0.04, 0.065), color=DIRT).set_opacity(dirty))
    return VGroup(g, dirt).scale(GS, about_point=c)


def particles(ph):
    """물 알갱이: 바닥에서 위로 퍼지는 종파(위아래 변위)."""
    front = WB + max(ph, 0) / K
    g = VGroup()
    for i, x in enumerate(np.arange(TX0 + 0.18, TX1 - 0.1, 0.24)):
        for j, y0 in enumerate(np.arange(WB + 0.1, WS - 0.05, 0.18)):
            if y0 <= front:
                y = y0 + AMP * np.sin(K * (y0 - WB) - ph) * min(1, (front - y0) / 0.3)
            else:
                y = y0
            g.add(Dot([x + 0.06 * (j % 2), y, 0], radius=0.026, color="#9CD8F2"))
    g.set_opacity(0.7)
    return g


def comp_centers(ph):
    """압축(밀) 중심의 y 목록:  K(y-WB) - ph = π + 2πn."""
    front = WB + max(ph, 0) / K
    out = []
    for n in range(-12, 12):
        y = WB + (PI + 2 * PI * n + ph) / K
        if WB < y < min(front, WS):
            out.append(y)
    return out


def bands(ph):
    g = VGroup()
    for y in comp_centers(ph):
        for h, op in ((0.34, 0.10), (0.18, 0.14)):
            lo, hi = max(y - h / 2, WB), min(y + h / 2, WS)
            if hi - lo < 0.02:
                continue
            r = Rectangle(width=TX1 - TX0, height=hi - lo, stroke_width=0,
                          fill_color=CYAN, fill_opacity=op)
            g.add(r.move_to([(TX0 + TX1) / 2, (lo + hi) / 2, 0]))
    return g


def dirt_blob(center, s=1.0):
    pts = [[-0.32, 0], [-0.25, 0.13], [-0.08, 0.2], [0.1, 0.17], [0.27, 0.1], [0.33, 0]]
    return Polygon(*[np.array([x * s, y * s, 0]) + center for x, y in pts],
                   stroke_width=1.5, stroke_color="#C9A46A", fill_color=DIRT, fill_opacity=1)


class C6Cleaning(CaseScene):
    def construct(self):
        bg = studio_bg(horizon=1.9)
        self.add(bg)
        tk = tank()
        ph = ValueTracker(0)
        txd = always_redraw(lambda: transducers(ph.get_value()))
        gl = glasses()

        # 0. 제목
        card = title_card("초음파 세척 (안경·금속 장식품)", case_no=6)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(card), run_time=0.6)
        self.play(FadeIn(tk), FadeIn(txd), FadeIn(gl), run_time=1)

        # 1. 등장 요소
        c_tank = callout([TX1 - 0.3, WS - 0.3, 0], "세척조", "물이 담긴 통", UR, 0.9, color=CYAN)
        c_gl = callout(gp([1.3, 0.25, 0]), "안경", "물속에 담가 둔다", RIGHT, 1.0)
        c_tx = callout([TX1 - 0.5, WB - 0.3, 0], "초음파 진동자", "통 바닥에 붙어 떨린다",
                       RIGHT + DOWN * 0.1, 0.9)
        self.play(Create(c_tank), Create(c_gl), run_time=0.9)
        self.play(Create(c_tx), run_time=0.7)
        self.say("초음파 세척기: 물이 담긴 통 바닥에 초음파 진동자가 붙어 있다", wait=3)
        self.play(FadeOut(c_tank), FadeOut(c_gl), FadeOut(c_tx), run_time=0.5)

        # 2. 진동 → 밀·소가 위로 퍼지는 종파
        dots = always_redraw(lambda: particles(ph.get_value()))
        bnd = always_redraw(lambda: bands(ph.get_value()))
        sn = slow_note()
        clock = Clock(ph, "μs", "{:.0f}", scale=25 / (2 * PI))
        self.play(FadeIn(dots), FadeIn(sn), FadeIn(clock), run_time=0.6)
        self.add(bnd)
        self.bring_to_front(gl)
        self.say("진동자가 1초에 약 4만 번(40 kHz) 떨며\n물을 밀었다 당겼다 한다 (한 번 떨리는 데 25 μs)", wait=0.2)
        self.play(ph.animate.set_value(2 * PI * 3), run_time=7, rate_func=linear)
        self.say("물 알갱이가 파동이 나아가는 방향(위아래)으로 떨리며\n빽빽한 곳(압축)과 듬성한 곳(팽창)이 번갈아 위로 퍼진다 = 종파", wait=0.5)
        self.play(ph.animate.set_value(2 * PI * 5.5), run_time=5.5, rate_func=linear)
        # 멈춰서 이름 붙이기
        cs = comp_centers(ph.get_value())
        yc = [y for y in cs if 0.0 < y < 0.9][0]
        yr = yc - LAM / 2
        c_c = callout([TX1 - 0.15, yc, 0], "압축 (밀)", "압력이 높다", RIGHT + UP * 0.9, 0.6,
                      color=CYAN)
        c_r = callout([TX1 - 0.15, yr, 0], "팽창 (소)", "압력이 낮다", RIGHT + DOWN * 0.9, 0.6,
                      color=GRAY_T)
        self.play(FadeIn(c_c), FadeIn(c_r), run_time=0.6)
        self.say("밀(압축) = 압력이 높은 곳,  소(팽창) = 압력이 낮은 곳", wait=3)

        # 3. 파장 = 음속 / 진동수
        lx = TX0 + 0.35
        dl = dim_line([lx, yc, 0], [lx, yc - LAM, 0], "λ", side=LEFT * 0.6, size=26)
        self.play(FadeOut(c_c), FadeOut(c_r), Create(dl), run_time=0.8)
        f1 = eq_row(T("파장", 28, WHITE_T, bold=True), T("=", 28, WHITE_T, bold=True),
                    frac([("음속", ORANGE)], [("진동수", GREEN)], 28))
        f2 = eq_row(T("=", 28, WHITE_T, bold=True),
                    frac([("(1500 m/s)", ORANGE)], [("(40000 Hz)", GREEN)], 28),
                    T("= 0.0375 m", 28, GREEN, bold=True))
        f3 = T("≈ 3.8 cm", 30, GREEN, bold=True)
        nt = T("Hz = 1/s  →  (m/s) ÷ (1/s) = m", 19, GRAY_T)
        fb = VGroup(f1, f2, f3, nt).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        f3.shift(RIGHT * 0.4)
        pnl = panel(fb, buff=0.35, pos=[3.45, -0.05, 0])
        self.play(FadeIn(pnl[0]), Write(f1), run_time=1)
        self.say("밀과 밀 사이 거리 = 파장 λ\n한 번 떨리는 동안 파동이 나아가는 거리", wait=3.6)
        self.play(FadeIn(f2), run_time=0.8)
        self.say("물속 음속(약 1500 m/s)을 진동수(40000 Hz)로 나눈다\n40000 Hz = 1초에 40000번 진동", wait=5.0)
        self.play(FadeIn(f3), FadeIn(nt), run_time=0.7)
        lab38 = T("λ ≈ 3.8 cm", 22, GREEN, bold=True).next_to([lx - 0.12, yc, 0], UP, buff=0.12, aligned_edge=LEFT)
        self.play(FadeIn(lab38), run_time=0.5)
        self.say("그래서 밀·소 줄무늬가 약 3.8 cm 간격으로 생긴다", wait=3)
        self.play(FadeOut(pnl), FadeOut(dl), FadeOut(lab38), run_time=0.6)

        # 4. 확대: 팽창 → 거품 생성, 압축 → 거품이 터지며 물줄기
        lens_pt = gp([-0.47, -0.2, 0])
        box = RoundedRectangle(corner_radius=0.15, width=5.4, height=3.9,
                               stroke_color=PANEL_STROKE, stroke_width=2,
                               fill_color="#081C2E", fill_opacity=0.97).move_to(INSET_C)
        ring = Circle(radius=0.16, stroke_color=WHITE_T, stroke_width=2).move_to(lens_pt)
        z1 = DashedLine(ring.get_top(), box.get_corner(UL), stroke_width=1.5, color=GRAY_T)
        z2 = DashedLine(ring.get_bottom(), box.get_corner(DL), stroke_width=1.5, color=GRAY_T)
        it = T("확대: 렌즈 표면", 21, GRAY_T, bold=True).move_to(box.get_corner(UL) + [1.15, -0.28, 0])
        SY = INSET_C[1] - 1.2
        surf = Rectangle(width=5.0, height=0.45, stroke_width=0, fill_color="#A9C3D6",
                         fill_opacity=0.55).move_to([INSET_C[0], SY - 0.22, 0])
        sl = T("렌즈", 21, "#DDE8F0", bold=True).move_to([INSET_C[0] + 2.0, SY - 0.22, 0])
        DP = np.array([INSET_C[0] - 0.4, SY, 0])
        dirt = dirt_blob(DP, 1.1)
        dl_ = T("때", 22, "#E9CF9F", bold=True).next_to(dirt, LEFT, buff=0.12)
        self.play(Create(ring), Create(z1), Create(z2), run_time=0.6)
        self.play(FadeIn(box), FadeIn(it), FadeIn(surf), FadeIn(sl), FadeIn(dirt), FadeIn(dl_),
                  run_time=0.7)

        def plabel(text, color):
            m = T(text, 22, color, bold=True)
            return m.move_to(box.get_corner(UR) + [-1.25, -0.28, 0])

        BC = DP + UP * 0.95
        bub = Circle(radius=0.04, stroke_color=WHITE_T, stroke_width=2, fill_color=WHITE_T,
                     fill_opacity=0.08).move_to(BC)
        pl = plabel("압력 낮음 (팽창)", CYAN)
        self.play(FadeIn(pl), FadeIn(bub), run_time=0.5)
        self.say("팽창(압력이 낮은) 순간, 물이 당겨져\n아주 작은 거품(수증기·기체가 찬 작은 공간)이 생긴다", wait=0.2)
        big = Circle(radius=0.55, stroke_color=WHITE_T, stroke_width=2, fill_color=WHITE_T,
                     fill_opacity=0.08).move_to(BC)
        self.play(Transform(bub, big), run_time=3, rate_func=smooth)
        self.wait(1.6)
        pl2 = plabel("압력 높음 (압축)", ORANGE)
        self.play(FadeOut(pl), FadeIn(pl2), run_time=0.4)
        self.say("이어서 압축(압력이 높은) 순간, 거품이 순식간에 찌그러지며 터진다", wait=0.2)
        squash = Ellipse(width=0.8, height=0.32, stroke_color=WHITE_T, stroke_width=2,
                         fill_color=WHITE_T, fill_opacity=0.1).move_to(BC + DOWN * 0.25)
        dent = squash.copy().stretch(0.6, 0).stretch(0.7, 1).shift(DOWN * 0.1)
        self.play(Transform(bub, squash), run_time=1.2)
        self.play(Transform(bub, dent), run_time=0.5)
        jet = Arrow(BC + UP * 0.2, DP + UP * 0.22, buff=0, stroke_width=9, color=CYAN,
                    tip_length=0.25, max_stroke_width_to_length_ratio=20)
        shock = Circle(radius=0.1, stroke_color=WHITE_T, stroke_width=3).move_to(DP + UP * 0.15)
        self.play(FadeOut(bub, scale=0.2), GrowArrow(jet), run_time=0.35)
        self.play(shock.animate.scale(9).set_stroke(opacity=0), run_time=0.8)
        rng = np.random.default_rng(2)
        bits = VGroup(*[dirt_blob(DP + [rng.uniform(-0.25, 0.25), 0.05, 0], 0.25)
                        for _ in range(6)])
        self.remove(dirt)
        self.add(bits)
        self.play(*[b.animate.shift([rng.uniform(-1.4, 1.4), rng.uniform(0.6, 1.4), 0])
                    .rotate(rng.uniform(-2, 2)).set_opacity(0) for b in bits],
                  FadeOut(jet), FadeOut(dl_), run_time=1.4)
        jl = T("센 물줄기 + 충격파", 22, CYAN, bold=True).move_to(BC + UP * 0.2)
        self.play(FadeIn(jl), run_time=0.4)
        self.say("공동 현상(캐비테이션): 거품이 터질 때 생기는 센 물줄기와 충격파가\n표면의 때를 떼어 낸다", wait=5.0)
        self.say("이런 일이 1초에 수만 번, 물속 곳곳에서 일어난다", wait=2.8)
        self.play(FadeOut(VGroup(box, it, surf, sl, pl2, jl, ring, z1, z2)), run_time=0.6)

        # 좁은 틈
        cp = callout(gp([-0.22, -0.15, 0]), "코받침 틈", None, DOWN + RIGHT * 0.25,
                     0.85, color=CYAN)
        ch = callout(gp([1.1, 0.18, 0]), "경첩 틈", None, UR, 1.0, color=CYAN)
        self.play(Create(cp), Create(ch), run_time=0.7)
        self.say("솔이 닿지 않는 코받침·경첩의 좁은 틈도\n물이 들어가는 곳이면 깨끗해진다", wait=1.5)
        self.play(FadeOut(gl[1]), run_time=1.5)
        self.wait(1.2)
        self.play(FadeOut(cp), FadeOut(ch), run_time=0.5)

        # 5. 거리 공식으로 확인: 바닥 → 물 표면 → 바닥
        self.play(FadeOut(dots), FadeOut(bnd), FadeOut(clock), run_time=0.5)
        self.remove(dots, bnd)
        ph.set_value(0)
        tt = ValueTracker(0)  # ms
        clock2 = Clock(tt, "ms", "{:.2f}")
        src = np.array([-3.4, WB + 0.02, 0])
        tgt = np.array([-3.4, WS, 0])
        D = np.linalg.norm(tgt - src)
        TRIP = 0.1  # 한 방향 0.1 ms
        pw = always_redraw(lambda: echo_group(tt.get_value() / TRIP * D, src, tgt, 0.25, 3,
                                              1.0, 1.0, width=5))
        d15 = dim_line([TX1 - 0.35, WB, 0], [TX1 - 0.35, WS, 0], "15 cm", side=LEFT * 0.5 + DOWN * 1.1,
                       size=24)
        sn2 = slow_note("※ 실제보다 아주 느리게 보여 줌 (앞 장면보다는 빠르게)")
        self.play(FadeOut(gl[0], shift=UP * 1.5), FadeOut(sn), FadeIn(sn2), run_time=0.9)
        self.play(FadeIn(clock2), Create(d15), run_time=0.6)
        self.add(pw)
        self.say("거리 공식으로 확인해 보자: 안경을 꺼낸 통 바닥에서 짧은 펄스를 쏘면\n15 cm 위의 물 표면에서 반사되어 돌아온다", wait=0.2)
        self.play(tt.animate.set_value(2 * TRIP), run_time=8, rate_func=linear)
        self.remove(pw)

        r1 = colored([("시간 차", GREEN), ("=", WHITE_T), ("2 × 거리 ÷ 음속", WHITE_T)], 26)
        r2 = colored([("=", WHITE_T), ("2 ×", WHITE_T), ("(0.15 m)", WHITE_T), ("÷", WHITE_T),
                      ("(1500 m/s)", ORANGE)], 26)
        r3 = colored([("= 0.0002 s = 0.2 ms", GREEN)], 26)
        r4a = distance_formula(26)
        r4n = T("← 갔다가 되돌아왔으니 2로 나눈다", 20, GRAY_T)
        r4 = VGroup(r4a, r4n).arrange(RIGHT, buff=0.25)
        r5 = eq_row(T("=", 26, WHITE_T, bold=True),
                    frac(colored([("(1500 m/s)", ORANGE), ("×", WHITE_T), ("(0.0002 s)", GREEN)], 26),
                         colored([("2", WHITE_T)], 26), 26),
                    T("= 0.15 m", 26, GREEN, bold=True))
        fb2 = VGroup(r1, r2, r3, r4, r5).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        r2.shift(RIGHT * 0.9)
        r3.shift(RIGHT * 0.9)
        r5.shift(RIGHT * 0.4)
        pnl2 = panel(fb2, buff=0.3)
        if pnl2.width > 7.4:
            pnl2.scale_to_fit_width(7.4)
        pnl2.move_to([0, -0.05, 0]).to_edge(RIGHT, buff=0.15)
        self.play(FadeIn(pnl2[0]), FadeIn(r1), FadeIn(r2), run_time=0.9)
        self.say("왕복 길이(2 × 0.15 m)를 음속(1500 m/s)으로 나누면", wait=3.5)
        self.play(FadeIn(r3), run_time=0.6)
        self.say("시간 차 = 0.0002 s = 0.2 ms (시계와 같다)", wait=2.6)
        self.play(FadeIn(r4), FadeIn(r5), run_time=0.9)
        self.say("거꾸로 거리 공식에 넣으면 다시 0.15 m = 15 cm", wait=3.3)
        self.say("하지만 세척은 시간을 재지 않고\n초음파의 에너지(압력 변화)를 이용한다", color=GREEN,
                 wait=4)

        # 6. 환경에 좋은 점
        self.clear_all(keep=(bg,))
        adv = VGroup(
            T("환경에 좋은 점", 30, CYAN, bold=True),
            T("· 물(또는 순한 세제 조금)만으로 씻는다 → 독한 세제·화학 폐수가 줄어든다", 25),
            T("· 솔로 문지르지 않아 흠집 걱정이 적다 (단, 코팅이 약한 렌즈·진주 등은 주의)", 25),
            T("· 좁은 틈까지 한 번에 → 물과 시간을 아낀다", 25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        ap = panel(adv, buff=0.45, pos=UP * 0.45)
        self.play(FadeIn(ap, shift=UP * 0.2), run_time=0.8)
        self.wait(9.5)
        self.play(FadeOut(ap), run_time=0.6)

        # 7. 정리
        summ = VGroup(
            T("초음파 세척 정리", 30, CYAN, bold=True),
            T("· 진동자 약 40 kHz → 물속에 밀(압축)·소(팽창)가 번갈아 퍼지는 종파", 25),
            T("· 파장 = 1500 m/s ÷ 40000 Hz = 0.0375 m ≈ 3.8 cm", 25),
            T("· 팽창 때 거품 생성 → 압축 때 터짐(공동 현상) → 때가 떨어진다", 25),
            T("· 거리 재기가 아니라 압력 변화의 에너지를 쓴다", 25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        sp_ = panel(summ, buff=0.5, pos=UP * 0.3)
        self.play(FadeIn(sp_, shift=UP * 0.2), run_time=0.8)
        self.wait(10)
        self.play(FadeOut(sp_), run_time=0.6)

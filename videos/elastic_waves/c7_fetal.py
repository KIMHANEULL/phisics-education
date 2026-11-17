"""사례 7. 태아 초음파 검사 — 메아리 시간으로 깊이, 세기로 밝기, 한 줄씩 모아 영상."""
from common import *

# ------------------------------------------------------------ 배치 (화면 단위)
P = np.array([-3.3, 1.0, 0])       # 탐촉자 면(피부와 닿는 곳)
SC = 0.27                          # 1 cm 의 화면 길이
DMAX = 12.0                        # 화면에 보이는 최대 깊이 (cm)
R = DMAX * SC
HALF = 35 * DEGREES                # 부채꼴 반각
M0 = np.array([3.6, 1.05, 0])      # 모니터 속 부채꼴 꼭짓점
SHIFT = M0 - P
V_CM_PER_MS = 154.0                # 1540 m/s = 154 cm/ms

# 층 경계 깊이 (cm)
D_FAT, D_WALL, D_BACK = 1.5, 2.5, 11.5
HEAD_TOP = 7.7                     # 가운데 줄에서 태아 머리 윗면 깊이
HEAD_R = 0.42                      # 화면 단위
HEAD_C = P + DOWN * (HEAD_TOP * SC + HEAD_R)

FAT_C = "#7A5A48"
WALL_C = "#8A4343"
FLUID_C = "#0D1F33"
FETUS_C = "#E6C2A4"


def ypos(d_cm):
    return P[1] - d_cm * SC


def body_section():
    x0, x1 = -7.6, 0.15
    yb = -2.6
    def band(d0, d1, color, op=1):
        y0, y1 = ypos(d0), (ypos(d1) if d1 is not None else yb)
        r = Rectangle(width=x1 - x0, height=y0 - y1, stroke_width=0, fill_color=color,
                      fill_opacity=op)
        return r.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
    g = VGroup(
        band(0, D_FAT, FAT_C),
        band(D_FAT, D_WALL, WALL_C),
        band(D_WALL, D_BACK, FLUID_C),
        band(D_BACK, None, "#6E3434"),
    )
    skin = Line([x0, P[1], 0], [x1, P[1], 0], color="#E9B79A", stroke_width=4)
    edge = Line([x1, P[1], 0], [x1, yb, 0], color=GRAY_T, stroke_width=1.5,
                stroke_opacity=0.5)
    labs = VGroup(
        T("피부·지방", 19, "#F3D9C8", bold=True).move_to([-6.3, ypos(0.75), 0]),
        T("자궁벽 (근육)", 19, "#F6C9C9", bold=True).move_to([-6.1, ypos(2.0), 0]),
        T("양수", 21, "#9CC7E8", bold=True).move_to([-6.3, ypos(5.0), 0]),
    )
    return VGroup(g, skin, edge, labs)


def fetus_shape():
    head = Circle(radius=HEAD_R, stroke_color=WHITE_T, stroke_width=2,
                  fill_color=FETUS_C, fill_opacity=0.9).move_to(HEAD_C)
    body = Ellipse(width=1.35, height=0.72, stroke_color=WHITE_T, stroke_width=2,
                   fill_color=FETUS_C, fill_opacity=0.9)
    body.rotate(-0.12).move_to(HEAD_C + np.array([0.95, -0.12, 0]))
    arm = Ellipse(width=0.5, height=0.16, stroke_color=WHITE_T, stroke_width=1.5,
                  fill_color=FETUS_C, fill_opacity=1).rotate(0.5)
    arm.move_to(HEAD_C + np.array([0.55, -0.32, 0]))
    leg = Ellipse(width=0.6, height=0.2, stroke_color=WHITE_T, stroke_width=1.5,
                  fill_color=FETUS_C, fill_opacity=1).rotate(-0.4)
    leg.move_to(HEAD_C + np.array([1.35, -0.42, 0]))
    nose = Dot(HEAD_C + np.array([-0.4, -0.12, 0]), radius=0.05, color=FETUS_C)
    return VGroup(body, arm, leg, head, nose)


def probe_shape(lift=0.0, gel=True):
    base = P + UP * (0.06 + lift)
    face = Rectangle(width=0.9, height=0.08, stroke_width=0, fill_color=ORANGE,
                     fill_opacity=0.9).move_to(base + UP * 0.04)
    body = Polygon(base + LEFT * 0.48 + UP * 0.08, base + RIGHT * 0.48 + UP * 0.08,
                   base + RIGHT * 0.3 + UP * 0.85, base + LEFT * 0.3 + UP * 0.85,
                   stroke_color=WHITE_T, stroke_width=1.5, fill_color="#2B3D52",
                   fill_opacity=1)
    cable = Line(base + UP * 0.85, base + UP * 1.05 + RIGHT * 0.25, stroke_width=4,
                 color="#8A98A8")
    g = VGroup(cable, body, face)
    if gel:
        gl = Ellipse(width=1.3, height=0.16, stroke_width=0, fill_color=CYAN,
                     fill_opacity=0.45).move_to(P + UP * 0.03)
        g.add(gl)
    return g


def dirv(theta):
    return np.array([np.sin(theta), -np.cos(theta), 0])


# 가운데 줄(A-line)에서 만나는 경계: (깊이 cm, 반사 세기, 이름)
ECHOES = [(D_FAT, 0.45, "지방|근육"), (D_WALL, 0.6, "자궁벽|양수"),
          (HEAD_TOP, 1.0, "태아 머리 윗면"), (HEAD_TOP + 2 * HEAD_R / SC, 0.65, "머리 아랫면"),
          (D_BACK, 0.55, "자궁 뒷벽")]


def aline_waves(t_ms, gap=0.12, n=2):
    s = V_CM_PER_MS * t_ms * SC     # 진행한 경로 길이 (화면 단위)
    g = VGroup()
    for k in range(n):
        r = s - k * gap
        if 0.03 < r < R:
            g.add(ring_arc(P, r, DOWN, 0.45, CYAN, 5, (1 - 0.6 * r / R) * (1 - 0.4 * k)))
        for d, a, _ in ECHOES:
            D = d * SC
            rb = s - D - k * gap
            if 0.03 < rb < D:
                op = a * (1 - 0.4 * rb / D) * (1 - 0.4 * k)
                g.add(ring_arc(P + DOWN * D, rb, UP, 0.45, ORANGE, 4, op))
    return g


def bmode_points(seed=7):
    """단면에서 반사가 생기는 점들 (위치, 밝기). 부채꼴 안만."""
    rng = np.random.default_rng(seed)
    pts = []

    def inside(p):
        v = p - P
        r = np.linalg.norm(v)
        if r < 0.05 or r > R:
            return False
        th = np.arctan2(v[0], -v[1])
        return abs(th) <= HALF

    # 층 경계 (밝은 선)
    for d, b in [(D_FAT, 0.55), (D_WALL, 0.8), (D_BACK, 0.7)]:
        for x in np.arange(-5.5, -1.0, 0.045):
            p = np.array([x, ypos(d) + 0.025 * rng.standard_normal(), 0])
            if inside(p):
                pts.append((p, b * rng.uniform(0.75, 1.0)))
    # 조직 알갱이 (회색 점)
    for _ in range(900):
        d = rng.uniform(0, DMAX)
        if D_WALL + 0.15 < d < D_BACK - 0.1:
            continue
        p = np.array([rng.uniform(-5.5, -1.0), ypos(d), 0])
        if inside(p):
            pts.append((p, rng.uniform(0.15, 0.45)))
    # 태아: 머리(뼈) 윤곽은 아주 밝게, 몸 윤곽은 밝게, 속은 흐린 알갱이
    fet = fetus_shape()
    head, body, arm, leg = fet[3], fet[0], fet[1], fet[2]
    for mob, b, n in [(head, 1.0, 110), (body, 0.75, 110), (arm, 0.6, 30), (leg, 0.6, 34)]:
        for a in np.linspace(0, 1, n, endpoint=False):
            p = mob.point_from_proportion(a) + 0.015 * rng.standard_normal(3) * [1, 1, 0]
            if inside(p):
                pts.append((p, b * rng.uniform(0.8, 1.0)))
    for _ in range(260):
        p = HEAD_C + np.array([rng.uniform(-0.4, 1.7), rng.uniform(-0.55, 0.4), 0])
        inh = np.linalg.norm(p - HEAD_C) < HEAD_R * 0.9
        bc = body.get_center()
        inb = ((p[0] - bc[0]) / 0.62) ** 2 + ((p[1] - bc[1]) / 0.32) ** 2 < 1
        if (inh or inb) and inside(p):
            pts.append((p, rng.uniform(0.25, 0.5)))
    return pts


def build_slices(nslice=48):
    pts = bmode_points()
    edges = np.linspace(-HALF, HALF, nslice + 1)
    slices = [VGroup() for _ in range(nslice)]
    for p, b in pts:
        v = p - P
        th = np.arctan2(v[0], -v[1])
        i = min(int((th + HALF) / (2 * HALF) * nslice), nslice - 1)
        c = interpolate_color(ManimColor("#000000"), ManimColor("#FFFFFF"), b)
        slices[i].add(Dot(p + SHIFT, radius=0.028, color=c))
    centers = (edges[:-1] + edges[1:]) / 2
    return slices, centers


def frac_row(num_parts, size=27):
    return frac(colored(num_parts, size), colored([("2", WHITE_T)], size), size)


class C7Fetal(CaseScene):
    def construct(self):
        bg = studio_bg(horizon=1.9)
        self.add(bg)
        body = body_section()
        fetus = fetus_shape()
        lift = ValueTracker(0.0)
        gel_on = [False]
        probe = always_redraw(lambda: probe_shape(lift.get_value(), gel_on[0]))

        # 0. 제목
        card = title_card("태아 초음파 검사", case_no=7)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(card), run_time=0.6)
        self.play(FadeIn(body), FadeIn(fetus), FadeIn(probe, shift=DOWN * 0.2), run_time=1)

        # 1. 등장 요소
        cf = callout(HEAD_C + np.array([0.5, 0.45, 0]), "태아", "양수 속에 떠 있다",
                     RIGHT + UP * 0.25, 0.45)
        cp = callout(P + np.array([0.4, 0.5, 0]), "탐촉자", "압전 소자: 전기 ↔ 초음파",
                     UR, 0.7)
        self.play(Create(cf), Create(cp), run_time=0.9)
        self.say("엄마 배를 옆에서 자른 단면: 피부·지방 → 자궁벽 → 양수 → 태아")
        self.say("탐촉자 속 결정(압전 소자)이 전기 신호를 받아 떨리며\n약 2~10 MHz의 아주 짧은 초음파 펄스를 낸다", wait=4.5)
        self.play(FadeOut(cf), FadeOut(cp), run_time=0.5)

        # 2. 젤을 바르는 이유
        sn0 = slow_note("※ 실제보다 아주 느리게, 공기층은 크게 과장해 그림")
        self.play(lift.animate.set_value(0.55), FadeIn(sn0), run_time=0.8)
        air = callout(P + LEFT * 0.55 + UP * 0.3, "공기층", "초음파를 거의 다 반사",
                      UL, 0.6, color=RED_T)
        self.play(FadeIn(air), run_time=0.5)
        tw = ValueTracker(0)
        src = P + UP * 0.61
        bounce = always_redraw(lambda: echo_group(tw.get_value(), src, P + UP * 0.01, 0.15,
                                                  3, 1.5, 1.5, width=6, fade=False))
        self.add(bounce)
        self.say("탐촉자와 피부 사이에 공기층이 있으면\n초음파가 거의 다 튕겨 나와 몸속으로 못 들어간다", wait=0.2)
        for _ in range(2):
            tw.set_value(0)
            self.play(tw.animate.set_value(1.55), run_time=3, rate_func=linear)
        self.remove(bounce)
        self.wait(1.5)
        gel_on[0] = True
        self.play(FadeOut(air), FadeOut(sn0), lift.animate.set_value(0), run_time=0.8)
        cg = callout(P + RIGHT * 0.6 + UP * 0.03, "젤", "공기층을 없앤다", RIGHT + UP * 0.6,
                     0.7, color=CYAN)
        self.play(FadeIn(cg), run_time=0.5)
        self.say("그래서 배에 젤을 바른다 → 공기층이 없어져 초음파가 잘 들어간다")
        self.play(FadeOut(cg), run_time=0.4)

        # 3. 한 줄(A-line): 경계마다 일부 반사 → 시간 = 깊이, 세기 = 밝기
        mon = RoundedRectangle(corner_radius=0.14, width=6.0, height=3.95,
                               stroke_color=PANEL_STROKE, stroke_width=1.5,
                               fill_color="#05080C", fill_opacity=0.96)
        mon.move_to([3.6, -0.42, 0])
        mt = T("모니터", 18, GRAY_T, bold=True).move_to(mon.get_corner(UR) + [-0.5, -0.24, 0])
        fan = AnnularSector(inner_radius=0, outer_radius=R, angle=2 * HALF,
                            start_angle=-PI / 2 - HALF, arc_center=M0, fill_color="#0B0F14",
                            fill_opacity=1, stroke_color="#33414F", stroke_width=1.5)
        ruler = VGroup()
        rx = 1.15
        ruler.add(Line([rx, M0[1], 0], [rx, M0[1] - R, 0], stroke_width=1.5, color=GRAY_T))
        for d in range(0, 13, 2):
            y = M0[1] - d * SC
            ruler.add(Line([rx, y, 0], [rx + 0.1, y, 0], stroke_width=1.5, color=GRAY_T))
            ruler.add(T(str(d), 18, GRAY_T).next_to([rx, y, 0], LEFT, buff=0.1))
        ruler.add(T("깊이 (cm)", 18, GRAY_T).next_to([rx - 0.2, M0[1] + 0.18, 0], UP, buff=0.0)
                  .align_to([rx - 0.45, 0, 0], LEFT))
        aline = DashedLine(M0, M0 + DOWN * R, stroke_width=1.5, color=CYAN,
                           stroke_opacity=0.5)
        tt = ValueTracker(0)  # ms
        clock = Clock(tt, "ms", "{:.3f}")
        sn = slow_note()
        self.play(FadeIn(mon), FadeIn(mt), FadeIn(fan), FadeIn(ruler), FadeIn(aline),
                  FadeIn(sn), FadeIn(clock), run_time=0.8)
        beam = DashedLine(P, P + DOWN * R, stroke_width=1.5, color=CYAN, stroke_opacity=0.5)
        self.add(beam)

        def adots():
            g = VGroup()
            t = tt.get_value()
            for d, a, _ in ECHOES:
                if t >= d / V_CM_PER_MS * 2 - 1e-9:
                    c = interpolate_color(ManimColor("#000000"), ManimColor("#FFFFFF"), a)
                    g.add(Dot(M0 + DOWN * d * SC, radius=0.07, color=c))
                    g.add(Dot(M0 + DOWN * d * SC, radius=0.14, color=c).set_opacity(0.25))
            return g
        adot = always_redraw(adots)
        waves = always_redraw(lambda: aline_waves(tt.get_value()))
        self.add(waves, adot)
        self.say("한 방향으로 펄스를 쏘면, 조직의 경계를 만날 때마다\n일부가 반사되어 되돌아온다 (나머지는 더 들어간다)",
                 wait=1.5)
        t_head = 2 * HEAD_TOP / V_CM_PER_MS          # 0.100 ms
        self.play(tt.animate.set_value(0.05), run_time=4, rate_func=linear)
        self.say("되돌아온 시각이 늦을수록 → 더 깊은 곳 (모니터에서 아래쪽)", wait=0.2)
        self.play(tt.animate.set_value(t_head), run_time=4, rate_func=linear)
        hl = T("태아 머리: 0.100 ms", 18, ORANGE, bold=True)
        hl.next_to(M0 + DOWN * HEAD_TOP * SC, RIGHT, buff=0.3)
        self.play(FadeIn(hl), run_time=0.4)
        self.say("반사가 강할수록 → 밝은 점. 태아 머리뼈에서 강하게 반사된다", wait=2.8)
        t_end = 2 * D_BACK / V_CM_PER_MS
        self.play(tt.animate.set_value(t_end), run_time=3.6, rate_func=linear)
        self.remove(waves)
        self.say("양수는 반사가 거의 없어 검게 보인다", wait=2.2)

        # 4. 공식: 시간 → 깊이
        f1 = distance_formula(27)
        nt = T("← 갔다가 되돌아왔으니 2로 나눈다", 19, GRAY_T)
        r1 = VGroup(f1, nt).arrange(RIGHT, buff=0.35)
        f2 = frac_row([("(1540 m/s)", ORANGE), ("×", WHITE_T), ("(0.000100 s)", GREEN)])
        res = T("= 0.077 m = 7.7 cm", 27, GREEN, bold=True)
        r2 = eq_row("=", f2, res)
        r2[0].scale(27 / 34)
        r2.arrange(RIGHT, buff=0.22)
        r2.next_to(r1, DOWN, buff=0.25, aligned_edge=LEFT).shift(RIGHT * 0.6)
        pnl = panel(VGroup(r1, r2), buff=0.28).scale(0.88).to_corner(UR, buff=0.12)
        self.play(FadeOut(sn), FadeOut(clock), FadeIn(pnl[0]), Write(r1), run_time=1.2)
        self.say("몸속 연한 조직에서 음속은 약 1540 m/s\n0.100 ms = 0.000100 s", wait=3.7)
        self.play(FadeIn(r2[0]), FadeIn(f2), run_time=1)
        self.say("음속(1540 m/s)과 시간 차(0.000100 s)를 대입\n(단위: m/s × s = m)", wait=3.8)
        self.play(FadeIn(res, shift=LEFT * 0.2), run_time=0.7)
        dl = dim_line(P + RIGHT * 0.75, P + RIGHT * 0.75 + DOWN * HEAD_TOP * SC, "7.7 cm",
                      side=RIGHT * 0.5, size=22)
        self.play(Create(dl), run_time=0.8)
        self.say("태아 머리 윗면은 피부에서 7.7 cm 깊이에 있다\n→ 기계는 이 계산을 매 점마다 자동으로 한다", wait=3.8)
        self.play(FadeOut(pnl), FadeOut(dl), FadeOut(hl), run_time=0.6)

        # 5. 방향을 바꾸며 한 줄씩 → 부채꼴 영상(B-모드)
        slices, centers = build_slices()
        for s_ in slices:
            s_.set_opacity(0)
            self.add(s_)
        sw = ValueTracker(-HALF)

        def upd(m):
            th = sw.get_value()
            for s_, c in zip(slices, centers):
                s_.set_opacity(1 if c <= th else 0)
        ctrl = Mobject()
        ctrl.add_updater(upd)
        self.add(ctrl)
        sbeam = always_redraw(lambda: VGroup(
            Line(P, P + dirv(sw.get_value()) * R, stroke_width=8, color=CYAN,
                 stroke_opacity=0.25),
            Line(P, P + dirv(sw.get_value()) * R, stroke_width=2, color=CYAN),
            Line(M0, M0 + dirv(sw.get_value()) * R, stroke_width=1.5, color=CYAN,
                 stroke_opacity=0.7)))
        self.play(FadeOut(adot), FadeOut(beam), FadeOut(aline), FadeOut(ruler),
                  FadeIn(sbeam), run_time=0.6)
        self.say("이제 방향을 조금씩 바꾸며 한 줄씩 쏘고,\n점들을 모니터에 차례로 찍는다",
                 wait=0.3)
        self.play(sw.animate.set_value(HALF), run_time=9, rate_func=linear)
        self.play(FadeOut(sbeam), run_time=0.4)
        bm = T("B-모드 영상", 18, GREEN, bold=True).next_to(mt, DOWN, buff=0.1).align_to(mt, RIGHT)
        self.play(FadeIn(bm), run_time=0.4)
        self.say("줄들이 모여 태아의 모습이 나타난다.\n1초에 수십 장을 다시 그려서 움직이는 실시간 영상이 된다", wait=5.0)
        self.say("진동수가 높을수록 더 선명하지만, 깊이는 덜 들어간다\n(그래서 검사 부위 깊이에 맞춰 진동수를 고른다)",
                 wait=5.0)

        # 6. 장점
        ctrl.clear_updaters()
        self.clear_all(keep=(bg,))
        adv = VGroup(
            T("왜 초음파로 검사할까?", 30, CYAN, bold=True),
            T("· X선 같은 방사선을 쓰지 않아 태아와 엄마에게 비교적 안전하다", 26),
            T("· 움직이는 모습을 실시간으로 볼 수 있다 (심장 박동도)", 26),
            T("· 아프지 않고, 자르거나 주사할 필요가 없다", 26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        ap = panel(adv, buff=0.45, pos=UP * 0.45)
        self.play(FadeIn(ap, shift=UP * 0.2), run_time=0.8)
        self.wait(9.0)
        self.play(FadeOut(ap), run_time=0.6)

        # 7. 정리
        summ = VGroup(
            T("태아 초음파 검사 정리", 30, CYAN, bold=True),
            T("· 연한 조직 속 음속:  약 1540 m/s,  젤로 공기층을 없앤다", 26),
            T("· 시간 차 0.100 ms → 1540 × 0.000100 ÷ 2 = 0.077 m = 7.7 cm", 26),
            T("· 되돌아온 시각 → 깊이,  반사 세기 → 밝기", 26),
            T("· 방향을 바꾸며 한 줄씩 모으면 영상이 된다", 26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        sp_ = panel(summ, buff=0.5, pos=UP * 0.3)
        self.play(FadeIn(sp_, shift=UP * 0.2), run_time=0.8)
        self.wait(12.5)
        self.play(FadeOut(sp_), run_time=0.6)

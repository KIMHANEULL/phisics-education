"""사례 9. 지진파 — P파·S파, PS시, 편도 거리(거리 = 속력 × 시간).

메아리(왕복)와 달리 지진파는 진원 → 관측소로 한 번만 가므로 2로 나누지 않는다.
계산을 쉽게 하려고 P파 6 km/s, S파 3 km/s, 진원 거리 60 km 로 가정한다.
"""
from common import *

SURF = 1.1
HYP = np.array([-3.6, -1.9, 0])
EPI = np.array([HYP[0], SURF, 0])
STA = np.array([3.4, SURF, 0])
DIST = np.linalg.norm(STA - HYP)        # 화면 단위 = 60 km
UPK = DIST / 60                          # 화면 단위 / km
VP, VS = 6.0, 3.0                        # km/s
TP, TS = 60 / VP, 60 / VS                # 10 s, 20 s
CRUST = "#3A2E26"


def sky_bg():
    sky = Rectangle(width=16, height=4.4 - SURF, stroke_width=0)
    sky.set_fill(color=[BG_TOP, "#15263B"], opacity=1).set_sheen_direction(DOWN)
    sky.move_to([0, (4.4 + SURF) / 2, 0])
    return sky


def ground_bg():
    g = Rectangle(width=16, height=SURF + 4.4, stroke_width=0)
    g.set_fill(color=["#43352B", "#251C17"], opacity=1).set_sheen_direction(DOWN)
    g.move_to([0, (SURF - 4.4) / 2, 0])
    line = Line([-8, SURF, 0], [8, SURF, 0], color="#8E7A5E", stroke_width=2)
    return VGroup(g, line)


def station_icon(p):
    x, y = p[0], p[1]
    body = Rectangle(width=0.5, height=0.32, fill_color="#C9D2DC", fill_opacity=1,
                     stroke_color=WHITE_T, stroke_width=1).move_to([x, y + 0.16, 0])
    roof = Polygon([x - 0.32, y + 0.32, 0], [x + 0.32, y + 0.32, 0], [x, y + 0.55, 0],
                   fill_color="#7F8FA3", fill_opacity=1, stroke_color=WHITE_T, stroke_width=1)
    zz = VMobject(stroke_color="#1B6FA0", stroke_width=2).set_points_as_corners(
        [[x - 0.17 + 0.034 * k, y + 0.16 + (0.07 if k % 2 else -0.07) * (k not in (0, 10)), 0]
         for k in range(11)])
    return VGroup(body, roof, zz)


# ---------------------------------------------------------------- 파면
def _runs(pts, ok):
    out, cur = [], []
    for p, o in zip(pts, ok):
        if o:
            cur.append(p)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return [np.array(c) for c in out if len(c) > 1]


def ring(c, r, color, width, opacity, wig=0.0, wl=0.24, glow=True):
    g = VGroup()
    if r <= 0.02 or opacity <= 0.01:
        return g
    n = max(90, int(r * 70))
    th = np.linspace(0, TAU, n)
    rr = r + (wig * np.sin(TAU * r * th / wl) if wig else 0)
    pts = np.stack([c[0] + rr * np.cos(th), c[1] + rr * np.sin(th), np.zeros(n)], 1)
    ok = (pts[:, 1] < SURF - 0.01) & (np.abs(pts[:, 0]) < 7.4) & (pts[:, 1] > -4.4)
    for run in _runs(pts, ok):
        m = VMobject().set_points_as_corners(run).set_stroke(color, width, opacity)
        if glow:
            g.add(m.copy().set_stroke(color, width * 3.5, opacity * 0.18))
        g.add(m)
    return g


def quake_waves(t):
    """P파: 촘촘한 고리 묶음(압축) 두 개 — 종파. S파: 구불구불한 고리 — 횡파."""
    g = VGroup()
    rp = VP * UPK * t
    fade = lambda r: max(0.25, 1 - r / 14)
    for off, op in [(0, 1), (0.07, 0.7), (0.14, 0.45), (0.38, 0.6), (0.45, 0.42), (0.52, 0.25)]:
        r = rp - off
        g.add(ring(HYP, r, CYAN, 2.4, op * fade(r), glow=(off == 0)))
    rs = VS * UPK * t
    g.add(ring(HYP, rs, ORANGE, 3.4, fade(rs), wig=0.07))
    g.add(ring(HYP, rs - 0.3, ORANGE, 2.2, 0.4 * fade(rs), wig=0.06, glow=False))
    return g


# ---------------------------------------------------------------- 지진 기록
class Seismogram(VGroup):
    def __init__(self, tracker, x0=-2.85, x1=2.05, tmax=25.0, **kw):
        super().__init__(**kw)
        self.x0, self.x1, self.tmax = x0, x1, tmax
        self.base = 2.95
        self.ay = 2.12
        box = RoundedRectangle(corner_radius=0.1, width=x1 - x0 + 1.6, height=1.9,
                               stroke_color=PANEL_STROKE, stroke_width=1.5,
                               fill_color=PANEL_FILL, fill_opacity=0.92)
        box.move_to([(x0 + x1) / 2 + 0.35, 2.6, 0])
        self.box = box
        title = T("지진계 기록", 17, GRAY_T, bold=True)
        title.move_to(box.get_corner(UL) + np.array([title.width / 2 + 0.15, -0.2, 0]))
        ax = Line([x0, self.ay, 0], [x1, self.ay, 0], color=GRAY_T, stroke_width=1.5)
        self.add(box, title, ax)
        for k in range(6):
            tv = 5 * k
            x = self.x_of(tv)
            self.add(Line([x, self.ay - 0.05, 0], [x, self.ay + 0.05, 0], color=GRAY_T,
                          stroke_width=1.5))
            self.add(T(f"{tv}", 17, GRAY_T).move_to([x, self.ay - 0.21, 0]))
        self.add(T("시간 (s)", 17, GRAY_T).next_to([x1, self.ay, 0], RIGHT, buff=0.1))
        rng = np.random.default_rng(3)
        self.noise_t = np.linspace(0, tmax, 1200)
        nz = rng.normal(0, 1, 1200)
        nz = np.convolve(nz, np.ones(4) / 4, mode="same")
        self.noise = 0.018 * nz
        self.add(always_redraw(lambda: self._trace(tracker)))

    def x_of(self, t):
        return self.x0 + (self.x1 - self.x0) * t / self.tmax

    def amp(self, ts):
        a = np.interp(ts, self.noise_t, self.noise)
        u = ts - TP
        a += np.where(u > 0, 0.15 * np.exp(-u / 2.2) * np.sin(TAU * 1.8 * u)
                      * np.minimum(1, u / 0.15), 0)
        u = ts - TS
        a += np.where(u > 0, 0.32 * np.exp(-u / 2.6) * np.sin(TAU * 1.1 * u)
                      * np.minimum(1, u / 0.2), 0)
        return a

    def _trace(self, tracker):
        tn = min(max(tracker.get_value(), 0.0), self.tmax)
        n = max(int(900 * tn / self.tmax), 2)
        ts = np.linspace(0, max(tn, 1e-3), n)
        pts = np.stack([self.x0 + (self.x1 - self.x0) * ts / self.tmax, self.base + self.amp(ts),
                        np.zeros(n)], 1)
        return VMobject().set_points_as_corners(pts).set_stroke(WHITE_T, 1.8)

    def marker(self, t, text, color):
        x = self.x_of(t)
        ln = DashedLine([x, self.ay, 0], [x, 3.33, 0], color=color, stroke_width=2,
                        dash_length=0.06)
        lab = T(text, 16, color, bold=True).move_to([x, 3.42, 0])
        return VGroup(ln, lab)

    def span(self, t0, t1, text, color=GREEN):
        a, b = self.x_of(t0), self.x_of(t1)
        y = 2.33
        br = DoubleArrow([a, y, 0], [b, y, 0], buff=0, stroke_width=2.5, color=color,
                         tip_length=0.1, max_tip_length_to_length_ratio=0.15)
        lab = T(text, 16, color, bold=True).next_to(br, UP, buff=0.04)
        return VGroup(br, lab)


# ---------------------------------------------------------------- 장면
class C9Seismic(CaseScene):
    def construct(self):
        sky = sky_bg()
        self.add(sky)

        # 0. 제목
        card = title_card("지진파", case_no=9)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.wait(1.8)
        self.play(FadeOut(card), run_time=0.6)

        # 1. 단면: 진원 · 진앙 · 관측소
        gnd = ground_bg()
        u = np.array([0.48, 0.877, 0])
        fault = Line(HYP - u * 2.85, HYP + u * 3.42, color="#B04A4A", stroke_width=3)
        flab = T("단층", 16, "#E08A8A", bold=True).next_to(HYP - u * 2.2, LEFT, buff=0.12)
        star = Star(5, outer_radius=0.2, inner_radius=0.09, fill_color=RED_T, fill_opacity=1,
                    stroke_color=WHITE_T, stroke_width=1.2).move_to(HYP)
        self.play(FadeIn(gnd), run_time=0.8)
        self.play(Create(fault), FadeIn(flab), run_time=0.8)
        self.play(GrowFromCenter(star), run_time=0.5)
        vline = DashedLine(HYP + UP * 0.22, EPI, color=WHITE_T, stroke_width=2, dash_length=0.1)
        epi = Triangle(fill_color=RED_T, fill_opacity=1, stroke_width=0).scale(0.11)
        epi.rotate(PI).move_to(EPI + UP * 0.1)
        c_h = callout(HYP + RIGHT * 0.15, "진원", "땅속에서 지진이 처음 시작된 곳", RIGHT + DOWN * 0.3,
                      0.8, color=RED_T)
        self.play(Create(c_h), run_time=0.8)
        self.play(Create(vline), FadeIn(epi), run_time=0.8)
        c_e = callout(EPI + UP * 0.2, "진앙", "진원 바로 위의 땅 표면", UR, 0.6, color=RED_T)
        self.play(Create(c_e), run_time=0.8)
        self.say("지진이 처음 시작된 땅속 지점이 진원,\n진원 바로 위의 땅 표면이 진앙이다", wait=3.6)
        hl = T("진원", 18, RED_T, bold=True).next_to(star, LEFT, buff=0.12)
        el = T("진앙", 18, RED_T, bold=True).next_to(epi, LEFT, buff=0.12)
        self.play(FadeOut(c_h), FadeOut(c_e), FadeIn(hl), FadeIn(el), run_time=0.6)

        sta = station_icon(STA)
        self.play(FadeIn(sta, shift=DOWN * 0.2), run_time=0.6)
        c_s = callout(STA + np.array([0.15, 0.4, 0]), "관측소", "지진계가 땅의 흔들림을 기록", UL, 0.5,
                      color=GREEN)
        self.play(Create(c_s), run_time=0.7)
        dline = DashedLine(HYP, STA, color=GRAY_T, stroke_width=2, dash_length=0.12)
        ang = np.arctan2(*(STA - HYP)[[1, 0]])
        dlab = T("진원 거리 60 km", 20, WHITE_T, bold=True).rotate(ang)
        dlab.move_to((HYP + STA) / 2 + np.array([-np.sin(ang), np.cos(ang), 0]) * 0.25)
        self.play(Create(dline), FadeIn(dlab), run_time=0.8)
        self.say("계산을 쉽게 하려고 P파 6 km/s, S파 3 km/s,\n진원에서 관측소까지 60 km라고 가정한다", wait=4.0)
        self.play(FadeOut(c_s), run_time=0.4)

        # 2. P파 · S파 퍼짐 + 지진 기록
        tt = ValueTracker(0)
        waves = always_redraw(lambda: quake_waves(tt.get_value()))
        sg = Seismogram(tt)
        clock = Clock(tt, "s", "{:.1f}", label="경과 시간 (지진 발생 후)")
        sn = slow_note("※ 실제보다 빠르게 보여 줌")
        slab = T("관측소", 18, GREEN, bold=True).next_to(sta, RIGHT, buff=0.1)
        self.play(FadeIn(sg), FadeIn(clock), FadeIn(sn), FadeIn(slab), run_time=0.8)
        self.say("지진이 나면 P파와 S파가 동시에 출발해 사방으로 퍼진다", wait=0.3)
        self.add(waves)
        self.add_foreground_mobjects(star)
        self.play(tt.animate.set_value(5), run_time=2.5, rate_func=linear)
        th = np.deg2rad(40)
        pp = HYP + VP * UPK * 5 * np.array([np.cos(th), np.sin(th), 0])
        th2 = np.deg2rad(-8)
        ps = HYP + VS * UPK * 5 * np.array([np.cos(th2), np.sin(th2), 0])
        c_p = callout(pp, "P파", "빠르다 · 진행 방향으로 앞뒤 진동 (종파)", RIGHT + UP * 0.55, 0.55,
                      color=CYAN)
        c_q = callout(ps, "S파", "느리다 · 진행 방향에 수직으로 진동 (횡파)", RIGHT + DOWN * 0.15, 0.5,
                      color=ORANGE)
        for c_ in (c_p, c_q):
            c_.add_to_back(BackgroundRectangle(c_[2], color="#050B14", fill_opacity=0.7,
                                               buff=0.08))
        self.play(FadeIn(c_p), run_time=0.7)
        self.play(FadeIn(c_q), run_time=0.7)
        self.say("P파는 빠르고(앞뒤로 밀고 당기는 종파),\nS파는 느리다(옆으로 흔드는 횡파)", wait=3.6)
        self.play(FadeOut(c_p), FadeOut(c_q), run_time=0.4)
        self.unsay()
        self.play(tt.animate.set_value(TP), run_time=2.5, rate_func=linear)
        mp = sg.marker(TP, "P파 도착", CYAN)
        self.play(Flash(STA + UP * 0.25, color=CYAN, line_length=0.25), FadeIn(mp), run_time=0.7)
        self.say("P파가 먼저 도착한다 (10 s)", wait=1.8)
        self.play(tt.animate.set_value(TS), run_time=5.0, rate_func=linear)
        ms = sg.marker(TS, "S파 도착", ORANGE)
        self.play(Flash(STA + UP * 0.25, color=ORANGE, line_length=0.3), FadeIn(ms), run_time=0.7)
        self.say("S파는 나중에, 더 크게 흔들며 도착한다 (20 s)", wait=2.2)
        self.play(tt.animate.set_value(24), run_time=2.0, rate_func=linear)
        self.remove(waves)
        sp = sg.span(TP, TS, "PS시 = 10 s")
        self.play(FadeIn(sp), run_time=0.6)
        self.say("두 파동이 도착한 시각의 차이를 PS시(P-S 시간 차)라고 한다", wait=3.0)

        # 3. 편도! (반사 없음)
        one = Arrow(HYP, STA, buff=0.15, color=CYAN, stroke_width=6, tip_length=0.25)
        olab = T("한 번만 간다 (편도)", 22, CYAN, bold=True).rotate(ang)
        olab.move_to((HYP + STA) / 2 + np.array([np.sin(ang), -np.cos(ang), 0]) * 0.32)
        self.play(GrowArrow(one), FadeIn(olab), run_time=1.0)
        self.say("지진파는 진원에서 관측소까지 한 번만 간다\n되돌아오는 메아리가 아니므로 2로 나누지 않는다", wait=4.0)

        def icon_round():
            a = Arrow(LEFT * 0.45, RIGHT * 0.45, buff=0, color=CYAN, stroke_width=4,
                      tip_length=0.14).shift(UP * 0.09)
            b = Arrow(RIGHT * 0.45, LEFT * 0.45, buff=0, color=ORANGE, stroke_width=4,
                      tip_length=0.14).shift(DOWN * 0.09)
            return VGroup(a, b)

        def icon_one():
            return Arrow(LEFT * 0.45, RIGHT * 0.45, buff=0, color=CYAN, stroke_width=4,
                         tip_length=0.14)

        r1 = VGroup(T("메아리 (왕복)", 24, WHITE_T, bold=True), icon_round(),
                    colored([("거리 =", WHITE_T), ("음속", ORANGE), ("×", WHITE_T),
                             ("시간 차", GREEN), ("÷ 2", WHITE_T)], 26))
        r2 = VGroup(T("지진파 (편도)", 24, CYAN, bold=True), icon_one(),
                    colored([("거리 =", WHITE_T), ("속력", ORANGE), ("×", WHITE_T),
                             ("시간", GREEN)], 26))
        for r, y in ((r1, 0.35), (r2, -0.35)):
            r[0].move_to([-2.6, y, 0], aligned_edge=LEFT).shift(LEFT * 0)
            r[0].align_to([-3.2, 0, 0], LEFT)
            r[1].move_to([-0.6, y, 0])
            r[2].move_to([0, y, 0]).align_to([0.0, 0, 0], LEFT)
        x_ = T("÷ 2 없음", 20, RED_T, bold=True).next_to(r2[2], RIGHT, buff=0.3)
        cmp_body = VGroup(r1, r2, x_)
        cmp_ = panel(cmp_body, buff=0.3, pos=[-1.0, 2.65, 0])
        cmp_.shift(RIGHT * (-2.75 - cmp_.get_left()[0]))
        self.play(FadeOut(sg), FadeOut(mp), FadeOut(ms), FadeOut(sp), FadeOut(clock),
                  FadeOut(sn), run_time=0.5)
        self.play(FadeIn(cmp_[0]), FadeIn(r1), run_time=0.7)
        self.wait(1.2)
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.7)
        self.play(FadeIn(x_), run_time=0.5)
        self.say("왕복이면 ÷2, 편도면 그대로", wait=2.4)

        # 4. 대입
        self.play(FadeOut(cmp_), FadeOut(x_), run_time=0.5)
        e0 = colored([("거리 =", WHITE_T), ("속력", ORANGE), ("×", WHITE_T), ("시간", GREEN)], 26)
        e1 = colored([("P파:  60 km =", WHITE_T), ("(6 km/s)", CYAN), ("×", WHITE_T),
                      ("(10 s)", GREEN)], 26)
        e2 = colored([("S파:  60 km =", WHITE_T), ("(3 km/s)", ORANGE), ("×", WHITE_T),
                      ("(20 s)", GREEN)], 26)
        e3 = colored([("PS시 =", WHITE_T), ("20 s − 10 s", GREEN), ("=", WHITE_T),
                      ("10 s", GREEN)], 26)
        ex = VGroup(e0, e1, e2, e3).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        exp_ = panel(ex, buff=0.28, pos=[-1.0, 2.6, 0])
        exp_.shift(RIGHT * (-2.75 - exp_.get_left()[0]))
        self.play(FadeIn(exp_[0]), FadeIn(e0), run_time=0.6)
        self.play(FadeIn(e1), run_time=0.6)
        self.say("P파: 6 km/s로 10 s 동안 가면 60 km", wait=2.2)
        self.play(FadeIn(e2), run_time=0.6)
        self.say("S파는 속력이 P파의 절반이니 같은 60 km를 가는 데 2배(20 s) 걸린다", wait=3.6)
        self.play(FadeIn(e3), run_time=0.6)
        self.say("그래서 PS시 = 10 s", wait=1.6)

        # 5. 거꾸로: PS시 → 거리
        self.play(FadeOut(exp_), run_time=0.5)
        self.say("거꾸로, PS시만 재면 (지진이 언제 났는지 몰라도)\n진원까지의 거리를 알 수 있다", wait=2.4)
        ticks = VGroup()
        nrm = np.array([-np.sin(ang), np.cos(ang), 0])
        for k in range(1, 11):
            p = HYP + (STA - HYP) * k / 10
            ticks.add(Line(p - nrm * 0.11, p + nrm * 0.11, color=GREEN, stroke_width=3))
        t1 = T("6 km", 16, GREEN, bold=True).move_to(HYP + (STA - HYP) * 0.1 - nrm * 0.3)
        self.play(FadeOut(olab), FadeOut(dlab),
                  LaggedStart(*[Create(tk) for tk in ticks], lag_ratio=0.15), run_time=1.6)
        self.play(FadeIn(t1), run_time=0.4)
        q1 = colored([("6 km 가는 데:", WHITE_T), ("P파 1 s,", CYAN), ("S파 2 s", ORANGE),
                      ("→  PS시 1 s", GREEN)], 23)
        q2 = colored([("→ PS시가 1 s 늘 때마다 거리는", WHITE_T), ("6 km", GREEN), ("씩", WHITE_T)], 23)
        q3 = colored([("PS시", WHITE_T), ("(10 s)", GREEN), ("→ 거리 =", WHITE_T),
                      ("6 km × 10", GREEN), ("=", WHITE_T), ("60 km", GREEN)], 24)
        q4 = VGroup(T("(일반식) 거리 = vP × vS ÷ (vP − vS) × PS시", 20, GRAY_T),
                    T("= 6 × 3 ÷ 3 × 10 = 60 km", 20, GRAY_T)).arrange(DOWN, aligned_edge=LEFT,
                                                                       buff=0.08)
        q4[1].shift(RIGHT * 1.2)
        rv = VGroup(q1, q2, q3, q4).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        rvp = panel(rv, buff=0.24, pos=[-0.9, 2.6, 0])
        rvp.shift(RIGHT * (-2.75 - rvp.get_left()[0]) + UP * (3.92 - rvp.get_top()[1]))
        self.play(FadeIn(rvp[0]), FadeIn(q1), run_time=0.6)
        self.say("6 km마다 P파는 1 s, S파는 2 s 걸리니\nPS시가 1 s씩 벌어진다", wait=3.4)
        self.play(FadeIn(q2), run_time=0.6)
        self.wait(1.4)
        t10 = T("60 km · PS시 10 s", 18, GREEN, bold=True).rotate(ang)
        t10.move_to(HYP + (STA - HYP) * 0.86 - nrm * 0.4)
        self.play(FadeIn(q3), FadeIn(t10), Indicate(ticks, color=WHITE_T, scale_factor=1.0),
                  run_time=0.9)
        self.play(FadeIn(q4), run_time=0.5)
        self.say("PS시 10 s → 60 km. PS시가 길수록 진원이 멀다\n(PS시가 2배면 거리도 2배)", wait=5.0)

        # 6. 관측소 3곳 → 진앙
        self.clear_all(keep=(sky,))
        full = Rectangle(width=16, height=9, stroke_width=0)
        full.set_fill(color=[BG_TOP, "#0F1C2E"], opacity=1).set_sheen_direction(DOWN)
        self.play(FadeIn(full), run_time=0.4)
        self.remove(sky)
        sky = full
        mapbg = RoundedRectangle(corner_radius=0.15, width=8.6, height=5.7, stroke_color=PANEL_STROKE,
                                 stroke_width=1.5, fill_color="#14202E", fill_opacity=1)
        mapbg.move_to([0.25, 0.65, 0])
        grid = VGroup(*[Line([x, mapbg.get_bottom()[1], 0], [x, mapbg.get_top()[1], 0],
                             color=GRID, stroke_width=1, stroke_opacity=0.18)
                        for x in np.arange(-3.75, 4.3, 0.6)],
                      *[Line([mapbg.get_left()[0], y, 0], [mapbg.get_right()[0], y, 0],
                             color=GRID, stroke_width=1, stroke_opacity=0.18)
                        for y in np.arange(-2.15, 3.5, 0.6)])
        mtitle = T("위에서 내려다본 지도", 20, GRAY_T, bold=True).next_to(mapbg.get_corner(UL),
                                                                    DR, buff=0.15)
        self.play(FadeIn(mapbg), FadeIn(grid), FadeIn(mtitle), run_time=0.7)
        E = np.array([0.2, 0.6, 0])
        stations = [("A", np.array([-1.3, 1.4, 0])), ("B", np.array([1.8, 1.6, 0])),
                    ("C", np.array([0.6, -0.9, 0]))]
        cols = [CYAN, GREEN, ORANGE]
        icons, circs = VGroup(), VGroup()
        for (nm, p), col in zip(stations, cols):
            tri = Triangle(fill_color=WHITE_T, fill_opacity=1, stroke_width=0).scale(0.12).move_to(p)
            lb = T(nm, 20, WHITE_T, bold=True).next_to(tri, UR, buff=0.04)
            icons.add(VGroup(tri, lb))
            circs.add(Circle(radius=np.linalg.norm(E - p), color=col, stroke_width=3).move_to(p))
        self.play(FadeIn(icons, lag_ratio=0.3), run_time=0.8)
        self.say("관측소 세 곳에서 각각 PS시를 재서 진원까지의 거리를 구한다\n(진원이 얕으면 진앙까지의 거리와 거의 같다)", wait=3.6)
        for c in circs:
            self.play(GrowFromCenter(c), run_time=0.8)
        estar = Star(5, outer_radius=0.2, inner_radius=0.09, fill_color=RED_T, fill_opacity=1,
                     stroke_color=WHITE_T, stroke_width=1.2).move_to(E)
        elab = T("진앙", 22, RED_T, bold=True).next_to(estar, UP + RIGHT, buff=0.02)
        self.play(GrowFromCenter(estar), FadeIn(elab), Flash(E, color=RED_T), run_time=0.8)
        self.say("그 거리를 반지름으로 지도에 원을 그리면\n세 원이 만나는 곳이 진앙이다 (진원이 얕다고 볼 때)", wait=4.8)

        # 7. 지구 내부
        self.clear_all(keep=(sky,))
        C = np.array([-1.6, 0.45, 0])
        R = 2.45
        mantle = Circle(radius=R, fill_color="#6B4A35", fill_opacity=1, stroke_color="#B89B72",
                        stroke_width=3).move_to(C)
        outer = Circle(radius=0.55 * R, fill_color="#B07431", fill_opacity=1, stroke_width=0).move_to(C)
        inner = Circle(radius=0.19 * R, fill_color="#E3C57E", fill_opacity=1, stroke_width=0).move_to(C)
        self.play(FadeIn(mantle), FadeIn(outer), FadeIn(inner), run_time=0.8)
        c1 = callout(C + np.array([1.2, 1.75, 0]), "맨틀", "고체", RIGHT, 1.5, color=WHITE_T)
        c2 = callout(C + np.array([0.95, 0.8, 0]), "외핵", "액체", RIGHT, 1.75, color=WHITE_T)
        c3 = callout(C + np.array([0.2, -0.3, 0]), "내핵", "고체", RIGHT, 2.5,
                     color=WHITE_T)
        self.play(FadeIn(c1), FadeIn(c2), FadeIn(c3), run_time=0.8)
        S0 = C + UP * R
        qst = Star(5, outer_radius=0.17, inner_radius=0.08, fill_color=RED_T, fill_opacity=1,
                   stroke_color=WHITE_T, stroke_width=1).move_to(S0)
        self.play(GrowFromCenter(qst), run_time=0.4)

        def surf_pt(delta_deg, side):
            a = np.deg2rad(90 - side * delta_deg)
            return C + R * np.array([np.cos(a), np.sin(a), 0])

        s_ok = VGroup()
        for side in (1, -1):
            for dd in (45, 75, 100):
                s_ok.add(ArcBetweenPoints(S0, surf_pt(dd, side), angle=0.35 * side,
                                          color=ORANGE, stroke_width=3))
        s_stop, xs = VGroup(), VGroup()
        Rc = 0.55 * R
        for side in (1, -1):
            for dd in (130, 155):
                P_ = surf_pt(dd, side)
                d = (P_ - S0) / np.linalg.norm(P_ - S0)
                w = S0 - C
                b = np.dot(w, d)
                s = -b - np.sqrt(b * b - (np.dot(w, w) - Rc * Rc))
                hit = S0 + d * s
                s_stop.add(Line(S0, hit, color=ORANGE, stroke_width=3))
                xs.add(Cross(scale_factor=0.09, stroke_color=RED_T, stroke_width=4).move_to(hit))
        p_ray = Line(S0, C + DOWN * R, color=CYAN, stroke_width=3)
        self.play(LaggedStart(*[Create(a) for a in s_ok], lag_ratio=0.15), run_time=1.4)
        self.play(LaggedStart(*[Create(a) for a in s_stop], lag_ratio=0.15), run_time=1.0)
        plab = T("P파", 22, CYAN, bold=True).next_to(C + DOWN * R * 0.78, RIGHT, buff=0.1)
        slab2 = T("S파", 22, ORANGE, bold=True).move_to(C + np.array([-1.25, 1.35, 0]))
        self.play(FadeIn(slab2), run_time=0.3)
        self.play(FadeIn(xs), Create(p_ray), FadeIn(plab), run_time=0.7)
        shadow = Arc(radius=R + 0.08, start_angle=np.deg2rad(90 - 103),
                     angle=-np.deg2rad(360 - 206), arc_center=C, color=GRAY_T, stroke_width=6)
        c4 = callout(C + (R + 0.08) * np.array([np.cos(-0.87), np.sin(-0.87), 0]),
                     "S파가 오지 않는 지역", "외핵에 막혔기 때문 (약 103° 너머)", RIGHT + DOWN * 0.2, 0.9,
                     color=GRAY_T)
        self.play(Create(shadow), FadeIn(c4), run_time=0.8)
        self.say("S파는 고체만 지나고 액체는 지나지 못한다\n→ 103° 너머에 S파가 오지 않으므로 외핵은 액체임을 알았다", wait=5.5)

        # 8. 정리
        self.clear_all(keep=(sky,))
        summ = VGroup(
            T("지진파 정리", 30, CYAN, bold=True),
            T("· P파(빠름, 종파)가 먼저, S파(느림, 횡파)가 나중에 도착", 24),
            T("· 지진파는 편도: 거리 = 속력 × 시간  (60 km = 6 km/s × 10 s = 3 km/s × 20 s)", 24),
            T("· PS시가 길수록 멀다: PS시 10 s → 60 km", 24),
            T("· 관측소 세 곳의 원이 만나는 곳 = 진앙", 24),
            T("· S파가 외핵을 못 지나감 → 외핵은 액체", 24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        sp_ = panel(summ, buff=0.45, pos=UP * 0.75)
        fin = T("왕복이면 ÷2, 편도면 그대로", 38, GREEN, bold=True).next_to(sp_, DOWN, buff=0.4)
        self.play(FadeIn(sp_[0]), FadeIn(summ[0]), run_time=0.7)
        for ln in summ[1:]:                       # 한 줄씩 읽을 시간
            self.play(FadeIn(ln, shift=RIGHT * 0.15), run_time=0.5)
            self.wait(1.9)
        self.play(FadeIn(fin, shift=UP * 0.15), run_time=0.7)
        self.wait(3.5)
        self.play(FadeOut(sp_), FadeOut(fin), run_time=0.6)

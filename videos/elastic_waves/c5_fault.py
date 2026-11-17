"""사례 5. 단층 조사 — 반사법 탄성파 탐사.

진동 트럭이 만든 탄성파가 지층 경계면마다 일부 반사되어 수진기로 돌아온다.
깊이 = 속력 × 시간 차 / 2.  같은 지층의 깊이가 좌우에서 어긋나면 단층.
(교과서 그림의 '반사된 초음파' → 실제 탐사는 진동수가 낮은 탄성파. 영상에서는 '탄성파'로 부른다.)
"""
from common import *

SURF = 1.0                     # 지표면 y
UPM = 2.0 / 500                # 화면 단위 / m  (500 m = 2 단위)
V = 2000 * UPM                 # 탄성파 속력 2000 m/s → 화면 단위 / s (= 8)
DEPTHS = [250, 500, 750]
BYS = [SURF - d * UPM for d in DEPTHS]       # 경계면 y : 0, -1, -2
SLIP = 100 * UPM                              # 단층 어긋남 100 m
LAYER_COLS = ["#4A3A2B", "#62482F", "#3D4A3B", "#5A3A33"]
LINE_COL = "#CDAE7E"
BEIGE = "#EADFC9"
XL, XR, BOT = -7.5, 7.5, -4.4
XS_L = -4.4                    # 왼쪽 측정 위치(진동판)
XS_R = 3.1                     # 오른쪽 측정 위치
REC_OFF = 0.45                 # 진동판 ~ 가장 가까운 수진기 (약 110 m)


def FX(y):
    """단층면의 x (오른쪽으로 기울어진 정단층: 오른쪽 블록이 내려감)."""
    return -0.6 + (SURF - y) * 0.27


# ---------------------------------------------------------------- 그림 요소
def sky_bg():
    sky = Rectangle(width=16, height=4.4 - SURF, stroke_width=0)
    sky.set_fill(color=[BG_TOP, "#15263B"], opacity=1).set_sheen_direction(DOWN)
    sky.move_to([0, (4.4 + SURF) / 2, 0])
    return sky


def block(xl, xr, shift=0.0):
    """xl, xr: y → x 함수. 지층 다각형 + 경계선."""
    polys, lines = VGroup(), VGroup()
    tops = [SURF] + [b - shift for b in BYS]
    bots = [b - shift for b in BYS] + [BOT]
    for i, (yt, yb) in enumerate(zip(tops, bots)):
        p = Polygon([xl(yt), yt, 0], [xr(yt), yt, 0], [xr(yb), yb, 0], [xl(yb), yb, 0],
                    fill_color=LAYER_COLS[i], fill_opacity=1, stroke_color=LAYER_COLS[i],
                    stroke_width=1.2)
        polys.add(p)
    for b in BYS:
        y = b - shift
        lines.add(Line([xl(y), y, 0], [xr(y), y, 0], color=LINE_COL, stroke_width=2.2))
    return VGroup(polys, lines)


def ground(shift_right=0.0):
    left = block(lambda y: XL, FX)
    right = block(FX, lambda y: XR, shift_right)
    return VGroup(left, right)


def truck(xs):
    """진동판이 xs(트럭 뒤쪽)에 오는 진동 트럭."""
    y0 = SURF
    body_c = "#C9D2DC"
    bed = Rectangle(width=1.05, height=0.13, fill_color="#8C99A8", fill_opacity=1,
                    stroke_width=0).move_to([xs - 0.45, y0 + 0.27, 0])
    box = RoundedRectangle(corner_radius=0.04, width=0.55, height=0.3, fill_color=body_c,
                           fill_opacity=1, stroke_color=WHITE_T, stroke_width=1)
    box.move_to([xs - 0.35, y0 + 0.48, 0])
    cab = RoundedRectangle(corner_radius=0.06, width=0.38, height=0.46, fill_color=body_c,
                           fill_opacity=1, stroke_color=WHITE_T, stroke_width=1)
    cab.move_to([xs - 1.02, y0 + 0.47, 0])
    win = Rectangle(width=0.2, height=0.15, fill_color="#20364F", fill_opacity=1,
                    stroke_width=0).move_to([xs - 1.08, y0 + 0.57, 0])
    w1 = Circle(radius=0.1, fill_color="#1B232D", fill_opacity=1, stroke_color=GRAY_T,
                stroke_width=1.5).move_to([xs - 0.98, y0 + 0.1, 0])
    w2 = w1.copy().move_to([xs - 0.45, y0 + 0.1, 0])
    piston = Rectangle(width=0.08, height=0.16, fill_color="#8C99A8", fill_opacity=1,
                       stroke_width=0).move_to([xs, y0 + 0.14, 0])
    plate = Rectangle(width=0.34, height=0.06, fill_color="#E8C65A", fill_opacity=1,
                      stroke_width=0).move_to([xs, y0 + 0.03, 0])
    stripe = Rectangle(width=0.55, height=0.04, fill_color=CYAN, fill_opacity=1,
                       stroke_width=0).move_to([xs - 0.35, y0 + 0.44, 0])
    return VGroup(bed, box, stripe, cab, win, w1, w2, piston, plate)


def receivers():
    xs = [-6.2 + 0.75 * k for k in range(18)]
    g = VGroup()
    cable = Line([xs[0], SURF + 0.13, 0], [xs[-1], SURF + 0.13, 0], color=GRAY_T,
                 stroke_width=1.2, stroke_opacity=0.6)
    g.add(cable)
    for x in xs:
        spike = Polygon([x - 0.06, SURF + 0.06, 0], [x + 0.06, SURF + 0.06, 0],
                        [x, SURF - 0.1, 0], fill_color="#B9C4CF", fill_opacity=1,
                        stroke_width=0)
        head = Circle(radius=0.07, fill_color="#5BE39B", fill_opacity=1, stroke_color=WHITE_T,
                      stroke_width=1).move_to([x, SURF + 0.12, 0])
        g.add(VGroup(spike, head))
    return g


# ---------------------------------------------------------------- 파면
def _arc(c, r, a0, a1, n):
    th = np.linspace(a0, a1, n)
    return np.stack([c[0] + r * np.cos(th), c[1] + r * np.sin(th), np.zeros(n)], 1)


def _add_runs(g, pts, ok, key, op_fn, xs, xw, color, width, mult):
    """ok 인 연속 구간을 잘게 나눠, 가장자리로 갈수록 흐리게 그린다."""
    n = len(pts)
    i = 0
    while i < n:
        if not ok[i]:
            i += 1
            continue
        j = i
        while j + 1 < n and ok[j + 1] and key[j + 1] == key[i]:
            j += 1
        run = pts[i:j + 1]
        step = 8
        for s in range(0, max(len(run) - 1, 1), step):
            ch = run[s:s + step + 1]
            if len(ch) < 2:
                continue
            dx = abs(ch[len(ch) // 2][0] - xs) / xw
            op = op_fn(key[i]) * max(0.0, 1 - dx ** 3) * mult
            if op < 0.02:
                continue
            m = VMobject().set_points_as_corners(ch)
            m.set_stroke(color, width, op)
            gl = m.copy().set_stroke(color, width * 3.5, op * 0.18)
            g.add(gl, m)
        i = j + 1


def wave_field(t, xs, bys, xw=2.3, gaps=(0.0, 0.24)):
    """t 초 뒤의 파면. 내려가는 탄성파(청록, 경계면 지날 때마다 약해짐)와
    각 경계면에서 반사되어 올라오는 탄성파(주황, 거울상 원점에서 퍼지는 원)."""
    g = VGroup()
    src = np.array([xs, SURF, 0])
    for gi, gap in enumerate(gaps):
        r = V * t - gap
        if r <= 0.03:
            continue
        mult = 1.0 if gi == 0 else 0.4
        pts = _arc(src, r, -PI, 0, 140)
        lay = [sum(1 for b in bys if b > p[1]) for p in pts]
        ok = (pts[:, 1] < SURF - 0.01) & (np.abs(pts[:, 0] - xs) < xw)
        _add_runs(g, pts, ok, lay, lambda k: 0.62 ** k, xs, xw, CYAN, 4, mult)
        for k, b in enumerate(bys):
            if r < SURF - b:
                continue
            c = np.array([xs, 2 * b - SURF, 0])
            pts = _arc(c, r, 0, PI, 140)
            ok = (pts[:, 1] > b) & (pts[:, 1] < SURF - 0.01) & (np.abs(pts[:, 0] - xs) < xw)
            _add_runs(g, pts, ok, [0] * len(pts), lambda _k, k=k: 0.95 * 0.75 ** k, xs, xw,
                      ORANGE, 4, mult)
    return g


# ---------------------------------------------------------------- 기록계
class Recorder(VGroup):
    """수진기 기록(지진 기록과 같은 꼴). rows: [(이름, 도착 시각들, 색)]"""

    def __init__(self, tracker, rows, tmax=1.0, x0=-2.4, x1=1.6, top=3.55, row_h=0.55,
                 **kw):
        super().__init__(**kw)
        self.x0, self.x1, self.tmax = x0, x1, tmax
        n = len(rows)
        h = 0.42 + n * row_h + 0.42
        box = RoundedRectangle(corner_radius=0.1, width=(x1 - x0) + 1.35, height=h,
                               stroke_color=PANEL_STROKE, stroke_width=1.5,
                               fill_color=PANEL_FILL, fill_opacity=0.92)
        box.move_to([(x0 + x1) / 2 - 0.35, top - h / 2, 0])
        title = T("수진기 기록", 18, GRAY_T, bold=True).move_to(box.get_corner(UL) +
                                                         np.array([0.65, -0.2, 0]))
        self.add(box, title)
        self.base_y = []
        for i, (name, arr, col, trk) in enumerate(rows):
            y = top - 0.42 - row_h * (i + 0.5) + 0.06
            self.base_y.append(y)
            base = Line([x0, y, 0], [x1, y, 0], color=GRAY_T, stroke_width=1,
                        stroke_opacity=0.35)
            lab = T(name, 17, BEIGE, bold=True).next_to([x0, y, 0], LEFT, buff=0.12)
            self.add(base, lab)
            trk = tracker if trk is None else trk
            tr = always_redraw(lambda y=y, arr=arr, col=col, trk=trk: self._trace(trk, y, arr, col))
            self.add(tr)
        ay = top - h + 0.36
        self.axis_y = ay
        self.add(Line([x0, ay, 0], [x1, ay, 0], color=GRAY_T, stroke_width=1.5))
        for k in range(5):
            tv = k * 0.25
            x = self.x_of(tv)
            self.add(Line([x, ay - 0.05, 0], [x, ay + 0.05, 0], color=GRAY_T, stroke_width=1.5))
            self.add(T(f"{tv:g}", 14, GRAY_T).move_to([x, ay - 0.2, 0]))
        self.add(T("시간 (s)", 14, GRAY_T).next_to([x1, ay, 0], RIGHT, buff=0.1))

    def x_of(self, t):
        return self.x0 + (self.x1 - self.x0) * t / self.tmax

    def _trace(self, tracker, y, arr, col):
        tn = min(max(tracker.get_value(), 0.0), self.tmax)
        ts = np.linspace(0, max(tn, 1e-3), max(int(600 * tn / self.tmax), 2))
        amp = np.zeros_like(ts)
        for k, ta in enumerate(arr):
            u = (ts - ta) / 0.016
            amp += (0.32 * 0.82 ** k) * (1 - 2 * u ** 2) * np.exp(-u ** 2)
        pts = np.stack([self.x0 + (self.x1 - self.x0) * ts / self.tmax, y + amp,
                        np.zeros_like(ts)], 1)
        m = VMobject().set_points_as_corners(pts).set_stroke(col, 2.2)
        return m

    def tag(self, row, t, text, color=GREEN, up=True):
        x = self.x_of(t)
        y = self.base_y[row]
        lab = T(text, 15, color, bold=True)
        lab.next_to([x, y + 0.34, 0], UP, buff=0.04) if up else lab.next_to([x, y - 0.17, 0], DOWN, buff=0.03)
        return lab


# ---------------------------------------------------------------- 장면
class C5Fault(CaseScene):
    def construct(self):
        sky = sky_bg()
        self.add(sky)

        # 0. 제목
        card = title_card("단층 조사 (반사법 탄성파 탐사)", case_no=5)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.wait(1.8)
        self.play(FadeOut(card), run_time=0.6)

        # 1. 땅속 단면 + 장비
        gnd = ground(0.0)
        surf_line = Line([XL, SURF, 0], [XR, SURF, 0], color="#8E7A5E", stroke_width=2)
        blabs = VGroup(*[T(f"경계 {i + 1}", 16, BEIGE, bold=True).move_to([-6.75, b + 0.17, 0])
                         for i, b in enumerate(BYS)])
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in
                                [VGroup(gnd[0][0][i], gnd[1][0][i]) for i in range(4)]],
                              lag_ratio=0.25),
                  run_time=1.6)
        self.play(Create(VGroup(gnd[0][1], gnd[1][1])), FadeIn(surf_line), FadeIn(blabs),
                  run_time=1)
        self.say("땅속은 여러 겹의 지층(암석층)으로 되어 있다", wait=1.8)

        trk = truck(XS_L)
        recs = receivers()
        self.play(FadeIn(recs, lag_ratio=0.05), run_time=0.9)
        self.play(FadeIn(trk, shift=RIGHT * 0.6), run_time=0.9)
        ct = callout([XS_L - 0.35, SURF + 0.65, 0], "진동 트럭", "땅을 세게 흔들어 탄성파를 만든다",
                     UR, 0.95, color=CYAN)
        cr = callout([-1.7, SURF + 0.2, 0], "수진기 (지오폰)", "땅의 떨림을 기록한다",
                     UR, 0.55, color=GREEN)
        self.play(Create(ct), run_time=0.8)
        self.play(Create(cr), run_time=0.8)
        self.say("진동 트럭이 땅을 흔들어 탄성파를 만들고,\n땅 위에 늘어놓은 수진기가 되돌아온 떨림을 기록한다",
                 wait=3.6)
        self.play(FadeOut(ct), FadeOut(cr), run_time=0.5)

        # 2. 발신 → 경계면마다 반사/통과
        tt = ValueTracker(0)
        waves = always_redraw(lambda: wave_field(tt.get_value(), XS_L, BYS))
        clock = Clock(tt, "s", "{:.2f}")
        sn = slow_note()
        echoes = [2 * d / 2000 for d in DEPTHS]           # 0.25, 0.50, 0.75 s
        rec = Recorder(tt, [("", echoes, ORANGE, None)], row_h=0.9)
        self.play(FadeIn(sn), FadeIn(clock), FadeIn(rec), run_time=0.8)
        self.say("트럭이 땅을 흔드는 순간을 0 s로 놓는다", wait=1.4)
        self.add(waves)
        self.play(Wiggle(trk, scale_value=1.0, rotation_angle=0.02 * TAU, n_wiggles=5),
                  tt.animate.set_value(0.165), run_time=2.2, rate_func=linear)
        hit = np.array([XS_L + 0.9, BYS[0], 0])
        cb = callout(hit, "경계면", "일부는 반사(주황), 나머지는 통과(청록)", RIGHT + DOWN * 0.35,
                     0.9, color=WHITE_T)
        self.play(Create(cb), run_time=0.7)
        self.say("지층 경계면을 만나면 일부는 반사되어 올라오고,\n나머지는 통과해서 더 깊이 내려간다", wait=3.4)
        self.play(FadeOut(cb), run_time=0.4)
        self.say("경계면마다 메아리가 하나씩 생겨 차례로 수진기에 도착한다", wait=0.3)
        self.play(tt.animate.set_value(0.95), run_time=6.5, rate_func=linear)
        self.remove(waves)
        tags = VGroup(*[rec.tag(0, e, f"경계 {i + 1}\n{e:.2f} s") for i, e in enumerate(echoes)])
        self.play(LaggedStart(*[FadeIn(tg, shift=DOWN * 0.1) for tg in tags], lag_ratio=0.4),
                  run_time=1.4)
        self.say("깊은 경계면에서 반사된 탄성파일수록 늦게 돌아온다", wait=2.6)

        # 3. 거의 수직으로 갔다가 되돌아옴
        rx = XS_L + REC_OFF
        bot = np.array([XS_L + REC_OFF / 2, BYS[1], 0])
        go = Arrow([XS_L, SURF - 0.05, 0], bot, buff=0, color=CYAN, stroke_width=5,
                   tip_length=0.2)
        back = Arrow(bot, [rx, SURF - 0.12, 0], buff=0, color=ORANGE, stroke_width=5,
                     tip_length=0.2)
        lg = T("갈 때", 20, CYAN, bold=True).next_to(go, LEFT, buff=0.1)
        lb = T("올 때", 20, ORANGE, bold=True).next_to(back, RIGHT, buff=0.1)
        hl = SurroundingRectangle(tags[1], color=GREEN, buff=0.05, stroke_width=2)
        self.play(Create(hl), GrowArrow(go), FadeIn(lg), run_time=1)
        self.play(GrowArrow(back), FadeIn(lb), run_time=1)
        self.say("경계 2의 메아리를 보자. 수진기가 트럭 바로 옆이라\n탄성파는 거의 수직으로 내려갔다가 올라온다", wait=3.6)
        self.say("그러니 0.50 s 동안 움직인 길이는 '깊이의 2배'", wait=2.4)

        # 4. 공식
        f1 = eq_row("깊이", "=", frac([("탄성파 속력", ORANGE), ("×", WHITE_T), ("시간 차", GREEN)],
                                      [("2", WHITE_T)], 30))
        nt = T("← 갔다가 되돌아왔으니 2로 나눈다", 18, GRAY_T)
        nt.next_to(f1[2][2], RIGHT, buff=0.35)
        r1 = VGroup(f1, nt)
        f2 = frac(colored([("(2000 m/s)", ORANGE), ("×", WHITE_T), ("(0.50 s)", GREEN)], 30),
                  colored([("2", WHITE_T)], 30))
        res = T("= 500 m", 32, GREEN, bold=True)
        r2 = eq_row("=", f2, res)
        r2.next_to(r1, DOWN, buff=0.3, aligned_edge=LEFT).shift(RIGHT * 1.05)
        unit = T("단위: m/s × s = m", 18, GRAY_T).next_to(r2, DOWN, buff=0.22, aligned_edge=LEFT)
        body = VGroup(r1, r2, unit)
        pnl = panel(body, buff=0.3, pos=[3.0, -0.8, 0])
        pnl.shift(RIGHT * (6.8 - pnl.get_right()[0]))
        self.play(FadeOut(sn), FadeOut(clock), FadeIn(pnl[0]), Write(r1), run_time=1.2)
        self.say("모든 지층에서 탄성파 속력이 2000 m/s로 같다고 가정한다", wait=2.4)
        self.play(FadeIn(r2[0]), FadeIn(f2), run_time=1)
        self.say("속력과 시간 차 0.50 s를 대입한다 (단위: m/s × s = m)", wait=2.6)
        self.play(FadeIn(unit), FadeIn(res, shift=LEFT * 0.2), run_time=0.7)
        self.play(FadeOut(go), FadeOut(back), FadeOut(lg), FadeOut(lb), run_time=0.5)
        dl = dim_line([XS_L + 1.0, SURF, 0], [XS_L + 1.0, BYS[1], 0], "500 m",
                      side=RIGHT * 0.55, size=22)
        self.play(Create(dl), run_time=0.9)
        self.say("경계 2는 땅속 500 m 깊이에 있다", wait=2.0)
        dtags = VGroup(*[T(f"{d} m", 16, GREEN, bold=True).next_to(blabs[i], RIGHT, buff=0.15)
                         for i, d in enumerate(DEPTHS)])
        self.play(FadeIn(dtags, lag_ratio=0.3), run_time=1)
        self.say("시간 차가 2배(0.25 s → 0.50 s)면 깊이도 2배(250 m → 500 m)\n→ 0.75 s면 750 m", wait=3.6)

        # 4-1. 진동수 메모
        self.play(FadeOut(pnl), FadeOut(r1), FadeOut(r2), FadeOut(unit), FadeOut(res),
                  run_time=0.5)
        memo = VGroup(
            T("참고: 어떤 파동을 쓸까?", 22, CYAN, bold=True),
            T("· 초음파 (20000 Hz 이상): 땅속에서 금방 약해진다", 19),
            T("· 탐사용 탄성파 (수 Hz ~ 100 Hz 정도): 멀리·깊이 간다", 19),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        mp = panel(memo, buff=0.28, pos=[3.0, -0.8, 0])
        self.play(FadeIn(mp, shift=UP * 0.15), run_time=0.7)
        self.say("단층 조사에서는 초음파보다 진동수가 낮은 탄성파를 쓴다\n(멀리·깊이 가도록)", wait=3.6)
        self.play(FadeOut(mp), FadeOut(rec), FadeOut(tags), FadeOut(hl), FadeOut(dl),
                  FadeOut(dtags), run_time=0.6)

        # 5. 단층 찾기 — 땅속은 보이지 않는다
        self.say("이제 단층을 찾아보자. 실제로는 땅속을 직접 볼 수 없다", wait=0.3)
        cover = Rectangle(width=15.2, height=SURF - BOT, stroke_width=0, fill_color="#120D0A",
                          fill_opacity=0.9).move_to([0, (SURF + BOT) / 2, 0])
        qm = T("?", 90, "#6E5E4E", bold=True).move_to([0, -0.9, 0])
        self.play(FadeIn(cover), FadeIn(qm), FadeOut(blabs), run_time=1.0)
        gnd_f = ground(SLIP)                 # 덮개 아래에서 몰래 단층 지층으로 교체
        self.remove(gnd)
        self.add(gnd_f, surf_line, cover, qm, recs, trk)
        self.wait(1.0)

        bys_l = BYS
        bys_r = [b - SLIP for b in BYS]
        ech_l = echoes
        ech_r = [e + 0.10 for e in echoes]   # 0.35, 0.60, 0.85 s
        tA, tB = ValueTracker(0), ValueTracker(0)
        rec2 = Recorder(tA, [("A", ech_l, ORANGE, tA), ("B", ech_r, ORANGE, tB)], row_h=0.62)
        sn2 = slow_note()
        clock2 = Clock(tA, "s", "{:.2f}")
        mA = T("A", 26, WHITE_T, bold=True).move_to([XS_L, SURF + 1.0, 0])
        self.play(FadeIn(rec2), FadeIn(sn2), FadeIn(clock2), FadeIn(mA), run_time=0.8)
        wl = always_redraw(lambda: wave_field(tA.get_value(), XS_L, bys_l))
        self.add(wl)
        self.say("왼쪽(A)에서 한 번 재고", wait=0.2)
        self.play(tA.animate.set_value(0.95), run_time=5.5, rate_func=linear)
        self.remove(wl)
        self.play(FadeOut(clock2), run_time=0.3)
        clock3 = Clock(tB, "s", "{:.2f}")

        mB = T("B", 26, WHITE_T, bold=True).move_to([XS_R, SURF + 1.0, 0])
        self.play(trk.animate.shift(RIGHT * (XS_R - XS_L)), run_time=1.6)
        self.play(FadeIn(mB), FadeIn(clock3), run_time=0.5)
        wr = always_redraw(lambda: wave_field(tB.get_value(), XS_R, bys_r))
        self.add(wr)
        self.say("오른쪽(B)에서 또 한 번 잰다", wait=0.2)
        self.play(tB.animate.set_value(0.98), run_time=5.8, rate_func=linear)
        self.remove(wr)

        ta = rec2.tag(0, 0.50, "0.50 s")
        tb = rec2.tag(1, 0.60, "0.60 s", up=False)
        ya, yb = rec2.base_y
        guide = VGroup(*[DashedLine([rec2.x_of(e), ya + 0.05, 0], [rec2.x_of(e + 0.1), yb + 0.05, 0],
                                    color=GREEN, stroke_width=2, dash_length=0.06)
                         for e in ech_l])
        self.play(FadeIn(ta), FadeIn(tb), Create(guide), run_time=1.0)
        self.say("두 기록의 무늬는 똑같은데, B가 모두 0.10 s씩 늦다\n→ 같은 지층들이 B 쪽에서 모두 100 m씩 더 깊다", wait=3.8)

        # 6. 계산
        rowA = colored([("A:  깊이 =", WHITE_T), ("(2000 m/s)", ORANGE), ("×", WHITE_T),
                        ("(0.50 s)", GREEN), ("÷ 2 =", WHITE_T), ("500 m", GREEN)], 26)
        rowB = colored([("B:  깊이 =", WHITE_T), ("(2000 m/s)", ORANGE), ("×", WHITE_T),
                        ("(0.60 s)", GREEN), ("÷ 2 =", WHITE_T), ("600 m", GREEN)], 26)
        rowD = colored([("차이 = 600 m − 500 m =", WHITE_T), ("100 m", RED_T)], 28)
        calc = VGroup(rowA, rowB, rowD).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        cp = panel(calc, buff=0.3, pos=[0, -0.75, 0])
        self.play(FadeIn(cp[0]), FadeOut(qm), FadeIn(rowA), run_time=0.8)
        self.wait(1.2)
        self.play(FadeIn(rowB), run_time=0.7)
        self.wait(1.2)
        self.play(FadeIn(rowD, shift=UP * 0.1), run_time=0.7)
        self.say("같은 지층(경계 2)이 A에서는 500 m, B에서는 600 m\n→ 100 m 어긋나 있다", wait=3.4)

        # 7. 공개: 단층
        self.play(FadeOut(cp), FadeOut(calc), FadeOut(rec2), FadeOut(mA), FadeOut(mB),
                  FadeOut(ta), FadeOut(tb), FadeOut(guide), FadeOut(clock3), FadeOut(sn2),
                  run_time=0.6)
        self.play(FadeOut(cover), run_time=1.2)
        fault = DashedLine([FX(SURF), SURF, 0], [FX(BOT), BOT, 0], color=RED_T, stroke_width=5,
                           dash_length=0.16)
        self.play(Create(fault), run_time=1.0)
        d = np.array([0.27, -1, 0]) / np.linalg.norm([0.27, -1])
        pl = np.array([FX(-0.9) - 0.32, -0.9, 0])
        pr = np.array([FX(-0.9) + 0.32, -0.9, 0])
        aup = Arrow(pl + d * 0.55, pl - d * 0.55, buff=0, color=RED_T, stroke_width=5,
                    tip_length=0.18)
        adn = Arrow(pr - d * 0.55, pr + d * 0.55, buff=0, color=RED_T, stroke_width=5,
                    tip_length=0.18)
        cf = callout([FX(-2.0), -2.0, 0], "단층", "지층이 끊어져 어긋난 면", LEFT + UP * 0.15, 0.7, color=RED_T)
        self.play(GrowArrow(aup), GrowArrow(adn), Create(cf), run_time=1.0)
        ghost = DashedLine([FX(BYS[1]), BYS[1], 0], [6.2, BYS[1], 0], color=WHITE_T,
                           stroke_width=2, dash_length=0.1, stroke_opacity=0.8)
        glab = T("끊기지 않았다면 여기", 16, WHITE_T).next_to([6.2, BYS[1], 0], UL, buff=0.06)
        gx = XS_R + 1.25
        slip = DoubleArrow([gx, BYS[1], 0], [gx, BYS[1] - SLIP, 0], buff=0, color=GREEN,
                           stroke_width=3, tip_length=0.12, max_tip_length_to_length_ratio=0.4)
        slab = T("100 m", 20, GREEN, bold=True).next_to(slip, RIGHT, buff=0.1)
        dA = dim_line([XS_L + 1.0, SURF, 0], [XS_L + 1.0, BYS[1], 0], "500 m",
                      side=RIGHT * 0.55, size=20)
        dB = dim_line([XS_R - 0.75, SURF, 0], [XS_R - 0.75, BYS[1] - SLIP, 0], "600 m",
                      side=LEFT * 0.55, size=20)
        self.play(Create(ghost), FadeIn(glab), Create(dA), Create(dB), run_time=1.0)
        self.play(GrowFromCenter(slip), FadeIn(slab), run_time=0.7)
        self.say("땅속 지층이 끊어져 한쪽이 다른 쪽보다 100 m 내려가 있다\n→ 단층이 있다!", wait=3.4,
                 color=WHITE_T)
        self.wait(0.6)

        # 8. 정리
        self.clear_all(keep=(sky,))
        summ = VGroup(
            T("단층 조사 정리", 30, CYAN, bold=True),
            T("· 진동 트럭이 만든 탄성파가 지층 경계면마다 일부 반사된다", 24),
            T("· 깊은 경계면일수록 메아리가 늦게 온다", 24),
            T("· 깊이 = 속력 × 시간 차 ÷ 2  →  2000 × 0.50 ÷ 2 = 500 m", 24),
            T("· 같은 지층의 깊이가 어느 곳에서 갑자기 달라지면(500 m → 600 m) → 단층", 24),
            T("· 땅속 탐사에는 진동수가 낮은 탄성파를 쓴다", 24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        sp_ = panel(summ, buff=0.5, pos=ORIGIN + UP * 0.3)
        self.play(FadeIn(sp_, shift=UP * 0.2), run_time=0.8)
        self.wait(5.5)
        self.play(FadeOut(sp_), run_time=0.6)

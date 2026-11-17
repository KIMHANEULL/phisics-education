"""탄성파의 활용 시리즈 공통 스타일.

자동차 후방 센서 영상(초음파로 거리 재기 v2)의 디자인을 따른다.
- 남색 배경 + 원근 격자 바닥
- 청록: 보낸 파동 / 주황: 반사파 / 초록: 시간·결과
- 왼쪽 위 '※ 실제보다 아주 느리게 보여 줌', 오른쪽 위 경과 시간 카운터
- 아래 시간축(신호 발신 시각 / 신호 수신 시각), 수식 패널, 오른쪽 아래 'Orbit Otter'
한글은 Text, LaTeX 는 쓰지 않는다(분수도 Text + 선으로 만든다).
"""
from manim import *
import numpy as np

config.background_color = "#0A1220"

FONT = "Noto Sans CJK KR"
MONO = "DejaVu Sans Mono"

BG_TOP = "#070E19"
BG_HZ = "#15263B"
GRID = "#5B7C9E"
CYAN = "#3FD3FF"
ORANGE = "#FFB547"
GREEN = "#5BE39B"
WHITE_T = "#F2F5F8"
GRAY_T = "#93A3B5"
RED_T = "#FF6B6B"
PANEL_FILL = "#0C1726"
PANEL_STROKE = "#3E6E8E"
WATER_TOP = "#0F3550"
WATER_DEEP = "#071A2B"
GROUND = "#3A2E26"


def T(s, size=28, color=WHITE_T, bold=False, **kw):
    return Text(s, font=FONT, font_size=size, color=color,
                weight=BOLD if bold else NORMAL, **kw)


def M(s, size=28, color=WHITE_T, bold=True):
    return Text(s, font=MONO, font_size=size, color=color,
                weight=BOLD if bold else NORMAL)


# ---------------------------------------------------------------- 배경
def studio_bg(horizon=0.6, grid=True, floor_color=BG_HZ):
    """남색 그라데이션 + 원근 격자 바닥."""
    g = VGroup()
    sky = Rectangle(width=config.frame_width + 1, height=8.5 - (horizon + 4.25) + 4.25,
                    stroke_width=0)
    sky.set_fill(color=[BG_TOP, "#0B1626"], opacity=1)
    sky.stretch_to_fit_height(4.3 - horizon).move_to([0, (4.3 + horizon) / 2, 0])
    sky.set_sheen_direction(DOWN)
    floor = Rectangle(width=config.frame_width + 1, height=horizon + 4.3, stroke_width=0)
    floor.set_fill(color=[floor_color, "#0A1424"], opacity=1)
    floor.set_sheen_direction(DOWN)
    floor.move_to([0, (horizon - 4.3) / 2, 0])
    g.add(floor, sky)
    if grid:
        g.add(perspective_grid(horizon))
    return g


def perspective_grid(horizon=0.6, vx=0.0, color=GRID):
    lines = VGroup()
    bottom = -4.3
    for i in range(-24, 25):
        xb = i * 0.9
        ln = Line([vx + (xb - vx) * 0.04, horizon - 0.02, 0], [xb, bottom, 0],
                  stroke_width=1.2, color=color)
        lines.add(ln)
    # 수평선: 원근으로 간격이 좁아짐
    for k in range(1, 22):
        z = k * 0.55
        y = horizon - (horizon - bottom) * (1.4 / (z + 0.4)) * 0.75
        if y < bottom:
            continue
        lines.add(Line([-8, y, 0], [8, y, 0], stroke_width=1.1, color=color))
    # 멀수록 흐리게
    for ln in lines:
        y = min(ln.get_start()[1], ln.get_end()[1])
        ln.set_stroke(opacity=0.22)
    fade = Rectangle(width=17, height=1.6, stroke_width=0).move_to([0, horizon - 0.6, 0])
    fade.set_fill(color=["#0B1626", "#0B1626"], opacity=0.0)
    return lines


def sea_bg(surface_y=1.2):
    g = VGroup()
    sky = Rectangle(width=16, height=4.3 - surface_y, stroke_width=0)
    sky.set_fill(color=[BG_TOP, "#132236"], opacity=1).set_sheen_direction(DOWN)
    sky.move_to([0, (4.3 + surface_y) / 2, 0])
    water = Rectangle(width=16, height=surface_y + 4.3, stroke_width=0)
    water.set_fill(color=[WATER_TOP, WATER_DEEP], opacity=1).set_sheen_direction(DOWN)
    water.move_to([0, (surface_y - 4.3) / 2, 0])
    surf = Line([-8, surface_y, 0], [8, surface_y, 0], color=CYAN, stroke_width=2,
                stroke_opacity=0.5)
    g.add(sky, water, surf)
    return g


# ---------------------------------------------------------------- 고정 UI
def watermark():
    return T("Orbit Otter", 17, GRAY_T, bold=True).to_corner(DR, buff=0.32)


def slow_note(text="※ 실제보다 아주 느리게 보여 줌"):
    return T(text, 18, GRAY_T).to_corner(UL, buff=0.35)


def title_card(title, sub=None, case_no=None):
    if sub is None:  # 사례 1~5: 104쪽 본문, 사례 6~9: 105쪽 탐구
        sub = "도플러 효과 · 교과서 110~114쪽"
    s = sub if case_no is None else f"{sub}  |  사례 {case_no}"
    st = T(s, 21, GRAY_T)
    tt = T(title, 50, WHITE_T, bold=True)
    grp = VGroup(st, tt).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    bar = Rectangle(width=0.06, height=grp.height + 0.1, stroke_width=0)
    bar.set_fill(CYAN, 1)
    bar.next_to(grp, LEFT, buff=0.22)
    card = VGroup(bar, grp)
    card.to_corner(DL, buff=0.7).shift(UP * 0.35)
    return card


def caption(text, color=WHITE_T, size=27):
    """하단 자막. 여러 줄이면 \n 사용."""
    lines = [T(s, size, color, bold=True) for s in text.split("\n")]
    grp = VGroup(*lines).arrange(DOWN, buff=0.12)
    if grp.width > 10.6:  # 워터마크(Orbit Otter)·화면 끝을 덮지 않게
        grp.scale_to_fit_width(10.6)
    grp.to_edge(DOWN, buff=0.42)
    shade = BackgroundRectangle(grp, color="#050B14", fill_opacity=0.55, buff=0.16,
                                stroke_width=0)
    return VGroup(shade, grp)


class Clock(VGroup):
    """오른쪽 위 경과 시간 카운터. tracker 값(실제 단위) → 문자열."""

    def __init__(self, tracker, unit="ms", fmt="{:.2f}", label="경과 시간 (실제 시간으로 환산)",
                 scale=1.0, **kw):
        super().__init__(**kw)
        self.tracker = tracker
        lab = T(label, 18, GRAY_T)
        self.lab = lab
        self.unit = unit
        self.fmt = fmt
        self.scale_ = scale

        def make():
            v = tracker.get_value() * scale
            m = M(f"{fmt.format(v)} {unit}", 40, CYAN)
            m.next_to(lab, DOWN, buff=0.12, aligned_edge=RIGHT)
            return m

        self.add(lab)
        lab.to_corner(UR, buff=0.4)
        self.num = always_redraw(make)
        self.add(self.num)


class Timeline(VGroup):
    """아래 시간축. 0~tmax, 진행 막대(청록)와 점."""

    def __init__(self, tmax, step, tracker, unit="ms", x0=-4.2, x1=4.6, y=-2.0,
                 label=None, num_fmt="{:g}", **kw):
        super().__init__(**kw)
        self.tmax, self.x0, self.x1, self.y = tmax, x0, x1, y
        self.tracker = tracker
        axis = Line([x0, y, 0], [x1 + 0.25, y, 0], color=GRAY_T, stroke_width=2)
        tip = Triangle(fill_opacity=1, stroke_width=0, color=GRAY_T).scale(0.06)
        tip.rotate(-PI / 2).move_to([x1 + 0.3, y, 0])
        ticks = VGroup()
        nums = VGroup()
        n = int(round(tmax / step))
        for i in range(n + 1):
            x = self.x_of(i * step)
            ticks.add(Line([x, y - 0.06, 0], [x, y + 0.06, 0], color=GRAY_T, stroke_width=2))
            nums.add(T(num_fmt.format(round(i * step, 6)), 17, GRAY_T).move_to([x, y - 0.27, 0]))
        lab = T(label or f"시간 ({unit})", 18, GRAY_T).next_to(tip, RIGHT, buff=0.12)
        self.add(axis, tip, ticks, nums, lab)

        def bar():
            t = min(max(tracker.get_value(), 0), tmax)
            x = self.x_of(t)
            ln = Line([x0, y, 0], [max(x, x0 + 1e-3), y, 0], color=CYAN, stroke_width=5)
            dot = Dot([x, y, 0], radius=0.07, color=WHITE)
            return VGroup(ln, dot)

        self.bar = always_redraw(bar)
        self.add(self.bar)

    def x_of(self, t):
        return self.x0 + (self.x1 - self.x0) * t / self.tmax

    def marker(self, t, text, color, up=True):
        x = self.x_of(t)
        h = 0.45
        ln = Line([x, self.y, 0], [x, self.y + h, 0], color=color, stroke_width=2.5)
        lab = T(text, 20, color, bold=True).next_to(ln, UP, buff=0.08)
        return VGroup(ln, lab)

    def span(self, t0, t1, text, color=WHITE_T):
        a, b = self.x_of(t0), self.x_of(t1)
        yy = self.y + 0.25
        br = DoubleArrow([a, yy, 0], [b, yy, 0], buff=0, stroke_width=2.5, color=color,
                         tip_length=0.12, max_tip_length_to_length_ratio=0.2)
        lab = T(text, 20, color, bold=True).next_to(br, UP, buff=0.06)
        return VGroup(br, lab)


def callout(point, title, sub=None, direction=UR, length=1.1, color=ORANGE):
    """점 + 꺾인 지시선 + 굵은 제목 / 회색 부제 (자동차 영상의 '덮개 / 알루미늄' 스타일)."""
    p = np.array(point)
    d = np.array(direction, dtype=float)
    d = d / np.linalg.norm(d)
    mid = p + d * length
    side = RIGHT if d[0] >= 0 else LEFT
    end = mid + side * 0.35
    dot = Dot(p, radius=0.06, color=color)
    ln = VMobject(stroke_color=color, stroke_width=2).set_points_as_corners([p, mid, end])
    tt = T(title, 25, WHITE_T, bold=True)
    grp = VGroup(tt)
    if sub:
        grp.add(T(sub, 18, GRAY_T))
    grp.arrange(DOWN, aligned_edge=LEFT if side[0] > 0 else RIGHT, buff=0.06)
    grp.next_to(end, side, buff=0.1)
    grp.shift(UP * (grp.height / 2 - tt.height / 2))
    return VGroup(ln, dot, grp)


# ---------------------------------------------------------------- 수식
def colored(parts, size=34):
    """[(문자열, 색), ...] → 한 줄 VGroup."""
    g = VGroup(*[T(s, size, c, bold=True) for s, c in parts])
    g.arrange(RIGHT, buff=0.12)
    for m in g:  # 기호(=, ×, ÷)가 아래로 처지지 않게 세로 가운데 정렬
        m.set_y(g.get_y())
    return g


def frac(num, den, size=34, color=WHITE_T):
    """num, den: [(문자열, 색)] 또는 Mobject."""
    n = num if isinstance(num, Mobject) else colored(num, size)
    d = den if isinstance(den, Mobject) else colored(den, size)
    w = max(n.width, d.width) + 0.25
    bar = Line(LEFT * w / 2, RIGHT * w / 2, stroke_width=3, color=color)
    n.next_to(bar, UP, buff=0.12)
    d.next_to(bar, DOWN, buff=0.12)
    return VGroup(n, bar, d)


def eq_row(*items, buff=0.22, size=34):
    """항목들을 가로로 배치. 문자열은 흰색 Text 로."""
    ms = [T(i, size, WHITE_T, bold=True) if isinstance(i, str) else i for i in items]
    return VGroup(*ms).arrange(RIGHT, buff=buff)


def distance_formula(size=34):
    """거리 = 음속 × 시간 차 / 2  (자동차 영상과 같은 색)"""
    f = frac([("음속", ORANGE), ("×", WHITE_T), ("시간 차", GREEN)], [("2", WHITE_T)], size)
    return eq_row("거리", "=", f, size=size)


def panel(mob, buff=0.35, pos=None):
    box = RoundedRectangle(corner_radius=0.12, width=mob.width + 2 * buff,
                           height=mob.height + 2 * buff, stroke_color=PANEL_STROKE,
                           stroke_width=1.5, fill_color=PANEL_FILL, fill_opacity=0.97)
    box.move_to(mob)
    g = VGroup(box, mob)
    if pos is not None:
        g.move_to(pos)
    return g


def note(text, size=20, color=GRAY_T):
    return T(text, size, color)


# ---------------------------------------------------------------- 파동
def ring_arc(center, r, direction, spread, color, width=4, opacity=1.0):
    """center 에서 direction 방향으로 펼친 반지름 r 의 호(+ 은은한 빛)."""
    ang = np.arctan2(direction[1], direction[0])
    a = Arc(radius=r, start_angle=ang - spread / 2, angle=spread, arc_center=center,
            stroke_color=color, stroke_width=width, stroke_opacity=opacity)
    glow = a.copy().set_stroke(width=width * 4, opacity=opacity * 0.18)
    return VGroup(glow, a)


def echo_group(s, src, tgt, gap, n, spread_out, spread_back, color_out=CYAN,
               color_back=ORANGE, back_only=False, out_only=False, fade=True,
               width=4, back_dir=None):
    """진행량 s(거리 단위)에 따른 송신파 + 반사파 고리들.

    송신파: src 에서 반지름 r_k = s - k*gap (0 < r < D)
    반사파: tgt 에서 반지름 r_k = s - D - k*gap (0 < r < D)
    """
    src, tgt = np.array(src, dtype=float), np.array(tgt, dtype=float)
    v = tgt - src
    D = np.linalg.norm(v)
    u = v / D
    g = VGroup()
    for k in range(n):
        if not back_only:
            r = s - k * gap
            if 0.03 < r < D:
                op = 1 - 0.55 * (r / D) if fade else 1
                g.add(ring_arc(src, r, u, spread_out, color_out, width, op))
        if not out_only:
            r = s - D - k * gap
            if 0.03 < r < D:
                op = 1 - 0.45 * (r / D) if fade else 1
                bd = -u if back_dir is None else np.array(back_dir, dtype=float)
                g.add(ring_arc(tgt, r, bd, spread_back, color_back, width, op))
    return g


def dim_line(a, b, text, color=WHITE_T, text_color=GREEN, offset=DOWN * 0.35, size=26,
             side=None):
    """치수선 |----| 과 값."""
    a, b = np.array(a), np.array(b)
    ln = Line(a, b, stroke_width=2.5, color=color)
    d = (b - a) / np.linalg.norm(b - a)
    nrm = np.array([-d[1], d[0], 0])
    t1 = Line(a - nrm * 0.12, a + nrm * 0.12, stroke_width=2.5, color=color)
    t2 = Line(b - nrm * 0.12, b + nrm * 0.12, stroke_width=2.5, color=color)
    lab = T(text, size, text_color, bold=True)
    lab.move_to((a + b) / 2 + (offset if side is None else side))
    return VGroup(ln, t1, t2, lab)


class CaseScene(Scene):
    """공통 틀: 워터마크 상시 표시, 자막 교체 도우미."""

    def setup(self):
        self.wm = watermark()
        self.add_foreground_mobject(self.wm)
        self.cap = None

    def say(self, text, wait=None, color=WHITE_T, run=0.5):
        """자막 교체. wait 을 안 주면 글자 수로 읽는 시간 자동 계산."""
        new = caption(text, color)
        if self.cap is None:
            self.play(FadeIn(new, shift=UP * 0.1), run_time=run)
        else:
            self.play(FadeOut(self.cap), FadeIn(new), run_time=run)
        self.cap = new
        self.add_foreground_mobject(new)
        if wait is None:
            n = len(text.replace(" ", "").replace("\n", ""))
            wait = max(1.8, 0.75 + n * 0.11)
        if wait > 0:
            self.wait(wait)

    def unsay(self, run=0.4):
        if self.cap is not None:
            self.play(FadeOut(self.cap), run_time=run)
            self.remove_foreground_mobject(self.cap)
            self.cap = None

    def clear_all(self, run=0.6, keep=()):
        mobs = [m for m in self.mobjects if m is not self.wm and m not in keep]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run)
        self.cap = None
        self.foreground_mobjects = [self.wm]


# ---------------------------------------------------------------- 소리 (도플러 영상용)
import os, wave as _wave

SND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")


def tone(freq, dur, vol=0.35, name=None, fade=0.02):
    """사인파 '삐—' 소리 wav 를 만들고 경로를 돌려준다. freq 는 숫자 또는 (시작, 끝) 튜플(미끄러지는 소리)."""
    os.makedirs(SND_DIR, exist_ok=True)
    sr = 44100
    n = int(sr * dur)
    t = np.arange(n) / sr
    if isinstance(freq, (tuple, list)):
        f = np.linspace(freq[0], freq[1], n)
        ph = 2 * np.pi * np.cumsum(f) / sr
    else:
        ph = 2 * np.pi * freq * t
    y = np.sin(ph) * vol
    k = max(1, int(sr * fade))
    env = np.ones(n)
    env[:k] = np.linspace(0, 1, k)
    env[-k:] = np.linspace(1, 0, k)
    y = (y * env * 32767).astype(np.int16)
    if name is None:
        fs = f"{freq[0]:.0f}-{freq[1]:.0f}" if isinstance(freq, (tuple, list)) else f"{freq:.0f}"
        name = f"tone_{fs}_{dur:.2f}.wav"
    path = os.path.join(SND_DIR, name)
    with _wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(y.tobytes())
    return path

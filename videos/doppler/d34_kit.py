"""③·④ 영상(관찰자가 움직일 때 / 일반식과 이용) 전용 도우미. common.py 는 건드리지 않는다."""
from common import *

OBS_C = ORANGE        # 관찰자 속력 v_o
SRC_C = "#FF7EB6"     # 음원 속력 v_s
F_C = "#FFE066"       # 진동수 f
WAVE_C = CYAN         # 음속 v
OBS_SUB = "o"         # 관찰자 속력 아래 첨자 (교과서 표기에 맞춰 바꿀 수 있음)


# ---------------------------------------------------------------- 수식 조각
def sym(base, sub=None, color=WHITE_T, size=34):
    """아래 첨자 기호 (예: v_o, f_A). 기준선 정렬용 .core = 본 글자."""
    b = T(base, size, color, bold=True)
    g = VGroup(b)
    if sub:
        s = T(sub, int(size * 0.62), color, bold=True)
        s.next_to(b, RIGHT, buff=0.03).align_to(b, DOWN).shift(DOWN * size * 0.0045)
        g.add(s)
    g.core = b
    return g


def vo(color=OBS_C, size=34):
    return sym("v", OBS_SUB, color, size)


def vs_(color=SRC_C, size=34):
    return sym("v", "s", color, size)


def _item(i, size):
    if isinstance(i, Mobject):
        return i
    if isinstance(i, tuple):
        return T(i[0], size, i[1], bold=True)
    return T(i, size, WHITE_T, bold=True)


def mrow(*items, size=34, buff=0.12):
    """가로 한 줄. 문자열=흰색, (문자열, 색), Mobject 섞어 쓰기. 가운데(분수선) 높이 맞춤."""
    ms = [_item(i, size) for i in items]
    g = VGroup(*ms).arrange(RIGHT, buff=buff)
    y = 0
    for m in ms:
        core = getattr(m, "core", m)
        m.shift(UP * (y - core.get_center()[1]))
    g.core = g  # 한 줄 전체
    return g


def mfrac(num, den, size=34, color=WHITE_T):
    """num, den: mrow 에 넣을 항목 리스트 또는 Mobject."""
    n = num if isinstance(num, Mobject) else mrow(*num, size=size)
    d = den if isinstance(den, Mobject) else mrow(*den, size=size)
    w = max(n.width, d.width) + 0.25
    bar = Line(LEFT * w / 2, RIGHT * w / 2, stroke_width=3, color=color)
    n.next_to(bar, UP, buff=0.12)
    d.next_to(bar, DOWN, buff=0.12)
    g = VGroup(n, bar, d)
    g.core = bar
    return g


# ---------------------------------------------------------------- 그림
def speaker(scale=1.0, color="#C7CFD8", face=RIGHT):
    body = RoundedRectangle(corner_radius=0.05, width=0.32, height=0.5, fill_color=color,
                            fill_opacity=1, stroke_color=WHITE_T, stroke_width=1.5)
    cone = Polygon([0.16, 0.25, 0], [0.55, 0.55, 0], [0.55, -0.55, 0], [0.16, -0.25, 0],
                   fill_color=color, fill_opacity=1, stroke_color=WHITE_T, stroke_width=1.5)
    g = VGroup(body, cone).move_to(ORIGIN)
    if face[0] < 0:
        g.flip(UP)
    return g.scale(scale)


def speaker_icon(color=WHITE_T, scale=0.42):
    """작은 '소리 나는 중' 아이콘 (스피커 + 소리 호 2개)."""
    sp = speaker(1.0, color=color)
    arcs = VGroup(*[Arc(radius=r, start_angle=-0.6, angle=1.2, arc_center=[0.35, 0, 0],
                        stroke_color=color, stroke_width=5) for r in (0.45, 0.75)])
    return VGroup(sp, arcs).scale(scale)


def person(color=ORANGE, scale=1.0):
    head = Circle(radius=0.17, fill_color=color, fill_opacity=1, stroke_color=WHITE_T,
                  stroke_width=1.5).move_to([0, 0.55, 0])
    body = Line([0, 0.38, 0], [0, -0.15, 0], stroke_color=color, stroke_width=7)
    arms = VMobject(stroke_color=color, stroke_width=6).set_points_as_corners(
        [[-0.25, -0.02, 0], [0, 0.25, 0], [0.25, -0.02, 0]])
    legs = VMobject(stroke_color=color, stroke_width=7).set_points_as_corners(
        [[-0.2, -0.6, 0], [0, -0.15, 0], [0.2, -0.6, 0]])
    g = VGroup(legs, body, arms, head)
    g.head = head
    return g.scale(scale)


def now_playing(freq, label=None, color=GREEN):
    """'지금 들리는 소리' 배지: 스피커 아이콘 + '1320 Hz' (+ 설명)."""
    ic = speaker_icon(color)
    num = M(f"{freq} Hz", 34, color)
    row = VGroup(ic, num).arrange(RIGHT, buff=0.22)
    body = VGroup(row)
    if label:
        body.add(T(label, 20, GRAY_T))
        body.arrange(DOWN, buff=0.1)
    p = panel(body, buff=0.22)
    p.icon = ic
    return p


def play_tone(scene, badge, freq, dur=1.2, vol=0.3, extra=0.5):
    """소리를 실제로 틀고 배지 아이콘의 소리 호를 깜빡인다."""
    scene.add_sound(tone(freq, dur, vol=vol))
    arcs = badge.icon[1]
    scene.play(Indicate(arcs, scale_factor=1.25, color=WHITE_T), run_time=dur)
    if extra > 0:
        scene.wait(extra)


def front_field(t, src, c, period, rmax, hmax=1.75, color=WAVE_C, width=4, direction=RIGHT,
                tmin=-1e9):
    """정지한 음원에서 나오는 파면들 (t: 화면 시간). 반지름 r = c (t - k T)."""
    g = VGroup()
    k_hi = int(np.floor(t / period))
    k_lo = int(np.floor((t - rmax / c) / period))
    for k in range(k_lo, k_hi + 1):
        if k * period < tmin:
            continue
        r = c * (t - k * period)
        if 0.04 < r < rmax:
            spread = 2 * np.arcsin(min(1.0, hmax / r)) if r > hmax else PI
            spread = min(spread, PI)
            op = 1 - 0.45 * (r / rmax)
            g.add(ring_arc(src, r, direction, spread, color, width, op))
    return g


def summary_reveal(scene, lines, title, pos=ORIGIN + UP * 0.3, per_line=2.4, hold=4.0,
                   size=26, title_color=CYAN):
    """정리 패널: 제목 → 한 줄씩."""
    tt = T(title, 30, title_color, bold=True)
    ls = [T(s, size) if isinstance(s, str) else s for s in lines]
    body = VGroup(tt, *ls).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
    p = panel(body, buff=0.5, pos=pos)
    scene.play(FadeIn(p[0]), FadeIn(tt), run_time=0.7)
    for l in ls:
        scene.play(FadeIn(l, shift=RIGHT * 0.15), run_time=0.5)
        scene.wait(per_line - 0.5)
    scene.wait(hold)
    return p

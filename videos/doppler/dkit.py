"""도플러 효과 영상(d1, d2)용 추가 도우미. common.py 는 그대로 두고 여기에 둔다."""
from common import *

# 색 약속: v(소리 속력) 주황, λ(파장) 청록, f(진동수) 초록, v_s(음원 속력) 빨강
C_V = ORANGE
C_L = CYAN
C_F = GREEN
C_S = RED_T

TOP_OF_CAPTION = -2.55  # 두 줄 자막의 대략 윗선 (그림은 이보다 위에)


# ---------------------------------------------------------------- 수식 조각
def sym(base, sub=None, color=WHITE_T, size=34):
    """아래 첨자가 있는 기호 (λ_A, v_s ...). .base 로 줄 맞춤."""
    b = T(base, size, color, bold=True)
    g = VGroup(b)
    if sub:
        s = T(sub, max(18, int(size * 0.62)), color, bold=True)
        s.next_to(b, RIGHT, buff=0.03).align_to(b, DOWN).shift(DOWN * 0.09 * size / 34)
        g.add(s)
    g.base = b
    return g


def _mk(i, size):
    if isinstance(i, str):
        return T(i, size, WHITE_T, bold=True)
    if isinstance(i, tuple):
        return T(i[0], size, i[1], bold=True)
    return i


def row(*items, size=34, buff=0.13):
    """문자열 / (문자열, 색) / Mobject 를 가로로. 분수 막대·기호 몸통을 한 높이에 맞춘다."""
    ms = [_mk(i, size) for i in items]
    g = VGroup(*ms).arrange(RIGHT, buff=buff)
    y = 0
    for m in ms:
        ref = getattr(m, "base", m)
        m.shift(UP * (y - ref.get_center()[1]))
    g.base = None
    return g


def fr(num, den, size=34, color=WHITE_T):
    """분수. num/den: row() 결과나 Mobject, 또는 items 리스트."""
    n = num if isinstance(num, Mobject) else row(*num, size=size)
    d = den if isinstance(den, Mobject) else row(*den, size=size)
    w = max(n.width, d.width) + 0.22
    bar = Line(LEFT * w / 2, RIGHT * w / 2, stroke_width=3, color=color)
    n.next_to(bar, UP, buff=0.1)
    d.next_to(bar, DOWN, buff=0.1)
    g = VGroup(n, bar, d)
    g.base = bar
    return g


def hl_box(m, color=ORANGE, buff=0.08):
    return SurroundingRectangle(m, color=color, buff=buff, corner_radius=0.06, stroke_width=2.5)


# ---------------------------------------------------------------- 그림
def speaker_icon(color=WHITE_T, h=0.36):
    box = Rectangle(width=0.13, height=0.17, stroke_width=0).set_fill(color, 1)
    cone = Polygon([0.065, 0.085, 0], [0.22, 0.2, 0], [0.22, -0.2, 0], [0.065, -0.085, 0],
                   stroke_width=0).set_fill(color, 1)
    arcs = VGroup(*[Arc(radius=r, start_angle=-0.75, angle=1.5, arc_center=[0.2, 0, 0],
                        stroke_color=color, stroke_width=3) for r in (0.13, 0.25)])
    g = VGroup(box, cone, arcs)
    g.scale_to_fit_height(h)
    return g


def sound_badge(hz, color=CYAN, sub=None, size=30):
    """스피커 그림 + '1200 Hz' (+ 작은 설명). 지금 재생 중인 소리 표시."""
    ic = speaker_icon(color, 0.4)
    num = M(f"{hz} Hz", size, color)
    top = VGroup(ic, num).arrange(RIGHT, buff=0.16)
    body = VGroup(top)
    if sub:
        body.add(T(sub, 19, GRAY_T))
        body.arrange(DOWN, buff=0.08)
    p = panel(body, buff=0.16)
    p.icon = ic
    return p


def play_beep(scene, hz, dur=1.2, badge=None, extra=0.3, vol=0.3):
    """badge(이미 화면에 있는) 의 스피커를 흔들며 hz 소리를 dur 초 재생."""
    path = tone(hz, dur, vol=vol)
    scene.add_sound(path)
    if badge is not None:
        scene.play(Wiggle(badge.icon, scale_value=1.25, rotation_angle=0.05 * TAU, n_wiggles=int(dur * 4)),
                   run_time=dur)
    else:
        scene.wait(dur)
    if extra > 0:
        scene.wait(extra)


def person(h=1.1, color="#C9D3DD"):
    """옆에서 본 사람(막대 인형)."""
    s = h / 1.1
    head = Circle(radius=0.15, stroke_color=color, stroke_width=3, fill_color="#0A1220",
                  fill_opacity=1).move_to([0, 0.93, 0])
    body = Line([0, 0.78, 0], [0, 0.38, 0], stroke_color=color, stroke_width=4)
    arms = VMobject(stroke_color=color, stroke_width=4).set_points_as_corners(
        [[-0.22, 0.45, 0], [0, 0.68, 0], [0.22, 0.45, 0]])
    legs = VMobject(stroke_color=color, stroke_width=4).set_points_as_corners(
        [[-0.17, 0, 0], [0, 0.38, 0], [0.17, 0, 0]])
    g = VGroup(legs, body, arms, head).scale(s, about_point=ORIGIN)
    return g


def ear_icon(color="#E8C9A8", h=0.6):
    """귀 모양(관찰자)."""
    outer = VMobject(stroke_color=color, stroke_width=5)
    pts = [[0.0, -0.25, 0], [-0.12, -0.05, 0], [-0.14, 0.18, 0], [0.0, 0.32, 0], [0.16, 0.25, 0],
           [0.2, 0.05, 0], [0.1, -0.08, 0], [0.08, -0.22, 0], [0.0, -0.25, 0]]
    outer.set_points_smoothly([np.array(p) for p in pts])
    outer.set_fill(color, 0.25)
    inner = Arc(radius=0.08, start_angle=PI * 0.9, angle=-PI * 1.2, arc_center=[0.02, 0.12, 0],
                stroke_color=color, stroke_width=3.5)
    g = VGroup(outer, inner)
    g.scale_to_fit_height(h)
    return g


def ambulance(w=2.3):
    """오른쪽을 향한 구급차(옆모습)."""
    body = RoundedRectangle(corner_radius=0.08, width=1.55, height=0.78, stroke_color="#D7DEE6",
                            stroke_width=2, fill_color="#F4F6F8", fill_opacity=1).move_to([-0.25, 0.47, 0])
    cab = Polygon([0.52, 0.08, 0], [0.52, 0.72, 0], [0.82, 0.72, 0], [1.02, 0.38, 0], [1.02, 0.08, 0],
                  stroke_color="#D7DEE6", stroke_width=2, fill_color="#F4F6F8", fill_opacity=1)
    win = Polygon([0.6, 0.42, 0], [0.6, 0.65, 0], [0.8, 0.65, 0], [0.93, 0.42, 0], stroke_width=0,
                  fill_color="#7FB8E0", fill_opacity=1)
    stripe = Rectangle(width=2.04, height=0.09, stroke_width=0, fill_color=RED_T,
                       fill_opacity=1).move_to([-0.01, 0.3, 0])
    cx = Rectangle(width=0.32, height=0.1, stroke_width=0, fill_color=RED_T, fill_opacity=1)
    cy = Rectangle(width=0.1, height=0.32, stroke_width=0, fill_color=RED_T, fill_opacity=1)
    cross = VGroup(cx, cy).move_to([-0.3, 0.56, 0])
    lr = Rectangle(width=0.16, height=0.1, stroke_width=0, fill_color=RED_T, fill_opacity=1).move_to([-0.5, 0.91, 0])
    lb = Rectangle(width=0.16, height=0.1, stroke_width=0, fill_color="#4D8BFF", fill_opacity=1).move_to([-0.3, 0.91, 0])
    wh = VGroup(*[VGroup(Circle(radius=0.15, stroke_width=0, fill_color="#20262E", fill_opacity=1),
                         Circle(radius=0.06, stroke_width=0, fill_color="#9AA5B1", fill_opacity=1)).move_to([x, 0.08, 0])
                  for x in (-0.7, 0.62)])
    g = VGroup(body, cab, win, stripe, cross, lr, lb, wh)
    g.shift(DOWN * (g.get_bottom()[1]))  # 바퀴 아래 = y 0
    g.scale(w / g.width, about_point=ORIGIN)
    return g


def circle_front(center, r, color=CYAN, width=3, opacity=1.0):
    return Circle(radius=max(r, 1e-3), arc_center=center, stroke_color=color, stroke_width=width,
                  stroke_opacity=opacity)


def fronts(t, center_of, c, rmax, color=CYAN, width=3, kmin=0, fade=0.55, hl=None):
    """주기 T=1 단위의 시간 t 에서 k=kmin..floor(t) 번째 파면(원).
    center_of(k): k 번째 파면을 낸 자리. 반지름 c(t-k)."""
    g = VGroup()
    if t < kmin:
        return g
    for k in range(kmin, int(np.floor(t + 1e-9)) + 1):
        r = c * (t - k)
        if r <= 0.005 or r > rmax:
            continue
        op = 1 - fade * min(r / rmax, 1)
        col = color
        w = width
        if hl is not None and k in hl:
            col, w, op = ORANGE, width + 2, 1
        g.add(circle_front(center_of(k), r, col, w, op))
    return g


def time_driver(scene, rate=1.0):
    """scene 시간(초)에 따라 저절로 증가하는 ValueTracker. wait 동안에도 움직인다."""
    vt = ValueTracker(0)
    vt.rate = rate
    vt.add_updater(lambda m, dt: m.increment_value(dt * m.rate))
    scene.add(vt)
    return vt


def tag(text, color=ORANGE, size=20):
    t = T(text, size, color, bold=True)
    box = RoundedRectangle(corner_radius=0.08, width=t.width + 0.3, height=t.height + 0.2,
                           stroke_color=color, stroke_width=1.8, fill_color=PANEL_FILL, fill_opacity=0.95)
    box.move_to(t)
    return VGroup(box, t)


def label_bg(m, buff=0.06):
    """선 위에 놓일 수 있는 글자 뒤 배경."""
    return VGroup(BackgroundRectangle(m, color="#0A1220", fill_opacity=0.9, buff=buff), m)


def summary(scene, title, lines, per=2.4, hold=4.0, size=25, pos=UP * 0.25):
    """정리 패널: 한 줄씩."""
    head = T(title, 30, CYAN, bold=True)
    body = [T(s, size) for s in lines]
    grp = VGroup(head, *body).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
    if grp.width > 11.6:
        grp.scale_to_fit_width(11.6)
    p = panel(grp, buff=0.45, pos=pos)
    scene.play(FadeIn(p[0]), FadeIn(head), run_time=0.8)
    for b in body:
        scene.play(FadeIn(b, shift=RIGHT * 0.15), run_time=0.5)
        n = len(b.text.replace(" ", ""))
        scene.wait(max(per - 0.5, 0.75 + 0.06 * n))
    scene.wait(hold)
    return p

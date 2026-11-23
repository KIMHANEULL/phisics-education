"""소리의 간섭(e2)·소음 제거(e3) 영상용 도우미. common.py 는 그대로 두고 여기에 둔다."""
from common import *

C_LOUD = RED_T        # 보강
C_SOFT = "#4D8BFF"    # 상쇄
C_NOISE = "#4D8BFF"   # 소음(파랑)
C_ANTI = RED_T        # 반대 위상(빨강)
C_SUM = GREEN         # 합성파

V = 0.8               # 화면 속 파동 속력 (모든 장면 공통, 단위/초)


def time_driver(scene, rate=1.0):
    vt = ValueTracker(0)
    vt.rate = rate
    vt.add_updater(lambda m, dt: m.increment_value(dt * m.rate))
    scene.add(vt)
    return vt


def speaker_icon(color=WHITE_T, h=0.36):
    box = Rectangle(width=0.13, height=0.17, stroke_width=0).set_fill(color, 1)
    cone = Polygon([0.065, 0.085, 0], [0.22, 0.2, 0], [0.22, -0.2, 0], [0.065, -0.085, 0],
                   stroke_width=0).set_fill(color, 1)
    arcs = VGroup(*[Arc(radius=r, start_angle=-0.75, angle=1.5, arc_center=[0.2, 0, 0],
                        stroke_color=color, stroke_width=3) for r in (0.13, 0.25)])
    g = VGroup(box, cone, arcs)
    g.scale_to_fit_height(h)
    return g


def badge(title, color=CYAN, sub=None, size=26):
    """지금 재생 중인 소리 표시: 스피커 그림 + 제목 (+ 작은 설명)."""
    ic = speaker_icon(color, 0.4)
    tt = T(title, size, color, bold=True)
    top = VGroup(ic, tt).arrange(RIGHT, buff=0.16)
    body = VGroup(top)
    if sub:
        body.add(T(sub, 19, GRAY_T))
        body.arrange(DOWN, buff=0.08)
    p = panel(body, buff=0.16)
    p.icon = ic
    return p


def wiggle_icon(b, dur):
    return Wiggle(b.icon, scale_value=1.2, rotation_angle=0.04 * TAU, n_wiggles=max(1, int(dur * 3)),
                  run_time=dur)


def front_speaker(h=0.9):
    """앞에서 본 스피커."""
    w = h * 0.62
    box = RoundedRectangle(corner_radius=0.06, width=w, height=h, stroke_color=GRAY_T, stroke_width=2,
                           fill_color="#1B2A3D", fill_opacity=1)
    tw = Circle(radius=w * 0.14, stroke_color=WHITE_T, stroke_width=2, fill_color="#5B6B7E",
                fill_opacity=1).move_to(box.get_center() + UP * h * 0.25)
    wf = Circle(radius=w * 0.32, stroke_color=WHITE_T, stroke_width=2, fill_color="#5B6B7E",
                fill_opacity=1).move_to(box.get_center() + DOWN * h * 0.13)
    dot = Dot(wf.get_center(), radius=w * 0.08, color="#2A3A4E")
    return VGroup(box, tw, wf, dot)


def person(h=1.1, color="#C9D3DD"):
    s = h / 1.1
    head = Circle(radius=0.15, stroke_color=color, stroke_width=3, fill_color="#0A1220",
                  fill_opacity=1).move_to([0, 0.93, 0])
    body = Line([0, 0.78, 0], [0, 0.38, 0], stroke_color=color, stroke_width=4)
    arms = VMobject(stroke_color=color, stroke_width=4).set_points_as_corners(
        [[-0.22, 0.45, 0], [0, 0.68, 0], [0.22, 0.45, 0]])
    legs = VMobject(stroke_color=color, stroke_width=4).set_points_as_corners(
        [[-0.17, 0, 0], [0, 0.38, 0], [0.17, 0, 0]])
    return VGroup(legs, body, arms, head).scale(s, about_point=ORIGIN)


def tag(text, color=ORANGE, size=22):
    t = T(text, size, color, bold=True)
    box = RoundedRectangle(corner_radius=0.08, width=t.width + 0.3, height=t.height + 0.2,
                           stroke_color=color, stroke_width=1.8, fill_color=PANEL_FILL, fill_opacity=0.95)
    box.move_to(t)
    return VGroup(box, t)


def label_bg(m, buff=0.06):
    return VGroup(BackgroundRectangle(m, color="#0A1220", fill_opacity=0.9, buff=buff), m)


def sym(base, sub, color=WHITE_T, size=30):
    """S₁ 처럼 아래 첨자가 있는 기호."""
    b = T(base, size, color, bold=True)
    s = T(sub, max(18, int(size * 0.62)), color, bold=True)
    s.next_to(b, RIGHT, buff=0.03).align_to(b, DOWN).shift(DOWN * 0.08 * size / 30)
    return VGroup(b, s)


def wave_line(f, x0, x1, y, color, width=4, n=220):
    """y + f(x) 곡선."""
    xs = np.linspace(x0, x1, n)
    pts = [np.array([x, y + f(x), 0]) for x in xs]
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_smoothly(pts)
    return m


def end_panel(scene, text, color=WHITE_T, size=34, hold=None):
    parts = text.split("\n")
    lines = VGroup(*[T(s, size, color, bold=True) for s in parts]).arrange(DOWN, buff=0.22)
    p = panel(lines, buff=0.5, pos=UP * 0.3)
    scene.play(FadeIn(p, scale=0.96), run_time=0.8)
    n = len(text.replace(" ", "").replace("\n", ""))
    scene.wait(hold if hold is not None else max(3.0, 0.75 + 0.11 * n + 1.0))
    return p

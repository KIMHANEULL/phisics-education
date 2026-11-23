"""충격파 (교과서 112~113쪽).

세 칸(정지 / 음속보다 느림 / 음속과 같음) 파면이 실시간으로 퍼짐 → 압력의 벽 →
음속보다 빠름(vₛ = 1.6v): 지난 자리 S₀~S₃ 의 원, 접선 → 원뿔 모양 충격파면, sinθ = v/vₛ →
전투기 소닉 붐 → 보트 V자 물결 → 한 줄 정리.
화면 속 소리 속력은 소닉 붐 장면을 제외한 모든 장면에서 0.5 (화면 단위/초)로 같다.
"""
from common import *
import os
import wave as _wave

C_S = RED_T          # 음원 속력 vₛ
U = 0.5              # 화면 속 소리 속력 (단위/초) — 영상 전체 공통


# ---------------------------------------------------------------- 도우미
def label_bg(m, buff=0.06):
    return VGroup(BackgroundRectangle(m, color="#0A1220", fill_opacity=0.9, buff=buff), m)


def tag(text, color=ORANGE, size=20):
    t = T(text, size, color, bold=True)
    box = RoundedRectangle(corner_radius=0.08, width=t.width + 0.3, height=t.height + 0.2,
                           stroke_color=color, stroke_width=1.8, fill_color=PANEL_FILL,
                           fill_opacity=0.95)
    box.move_to(t)
    return VGroup(box, t)


def fronts(t, center_of, c, rmax, color=CYAN, width=3, fade=0.55):
    """주기 1 단위 시간 t 에서 k = 0..floor(t) 번째 파면(원). 반지름 c(t-k)."""
    g = VGroup()
    if t < 0:
        return g
    for k in range(0, int(np.floor(t + 1e-9)) + 1):
        r = c * (t - k)
        if r <= 0.005 or r > rmax:
            continue
        op = 1 - fade * min(r / rmax, 1)
        g.add(Circle(radius=r, arc_center=center_of(k), stroke_color=color,
                     stroke_width=width, stroke_opacity=op))
    return g


def person(h=1.0, color="#C9D3DD"):
    s = h / 1.1
    head = Circle(radius=0.15, stroke_color=color, stroke_width=3, fill_color="#0A1220",
                  fill_opacity=1).move_to([0, 0.93, 0])
    body = Line([0, 0.78, 0], [0, 0.38, 0], stroke_color=color, stroke_width=4)
    arms = VMobject(stroke_color=color, stroke_width=4).set_points_as_corners(
        [[-0.22, 0.45, 0], [0, 0.68, 0], [0.22, 0.45, 0]])
    legs = VMobject(stroke_color=color, stroke_width=4).set_points_as_corners(
        [[-0.17, 0, 0], [0, 0.38, 0], [0.17, 0, 0]])
    return VGroup(legs, body, arms, head).scale(s, about_point=ORIGIN)


def jet(w=1.6, color="#D7DEE6"):
    """오른쪽을 향한 전투기 옆모습. 기수 끝 = 원점."""
    body = Polygon([0, 0, 0], [-0.35, 0.09, 0], [-1.5, 0.11, 0], [-1.6, 0.05, 0],
                   [-1.6, -0.06, 0], [-0.35, -0.08, 0], stroke_width=0,
                   fill_color=color, fill_opacity=1)
    wing = Polygon([-0.55, -0.02, 0], [-1.05, -0.02, 0], [-1.25, -0.2, 0], [-1.0, -0.2, 0],
                   stroke_width=0, fill_color="#AEB8C3", fill_opacity=1)
    tail = Polygon([-1.25, 0.1, 0], [-1.6, 0.1, 0], [-1.62, 0.42, 0], [-1.48, 0.42, 0],
                   stroke_width=0, fill_color="#AEB8C3", fill_opacity=1)
    can = Polygon([-0.3, 0.08, 0], [-0.62, 0.17, 0], [-0.8, 0.1, 0], stroke_width=0,
                  fill_color="#7FB8E0", fill_opacity=1)
    g = VGroup(tail, wing, body, can)
    g.scale(w / 1.62, about_point=ORIGIN)
    return g


def boat(w=0.9):
    """위에서 본 배(오른쪽을 향함). 뱃머리 끝 = 원점."""
    hull = Polygon([0, 0, 0], [-0.3, 0.17, 0], [-0.9, 0.17, 0], [-0.9, -0.17, 0], [-0.3, -0.17, 0],
                   stroke_color="#D7DEE6", stroke_width=2, fill_color="#F4F6F8", fill_opacity=1)
    deck = Rectangle(width=0.3, height=0.18, stroke_width=0, fill_color=ORANGE,
                     fill_opacity=1).move_to([-0.55, 0, 0])
    g = VGroup(hull, deck)
    g.scale(w / 0.9, about_point=ORIGIN)
    return g


def boom_wav(name="boom_e1.wav", dur=0.9, vol=0.75):
    """'쾅' — 낮은 음 + 잡음이 빠르게 줄어드는 소리."""
    os.makedirs(SND_DIR, exist_ok=True)
    sr = 44100
    n = int(sr * dur)
    t = np.arange(n) / sr
    rng = np.random.default_rng(3)
    noise = rng.standard_normal(n)
    k = 60
    noise = np.convolve(noise, np.ones(k) / k, mode="same") * 4  # 낮은 소리만 남김
    f = 70 * np.exp(-t * 2.5) + 38
    y = 0.8 * np.sin(2 * np.pi * np.cumsum(f) / sr) + 0.6 * noise
    env = np.exp(-t * 5.5)
    a = int(sr * 0.006)
    env[:a] *= np.linspace(0, 1, a)
    y = np.clip(y * env * vol, -1, 1)
    y[-200:] *= np.linspace(1, 0, 200)
    path = os.path.join(SND_DIR, name)
    with _wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((y * 32767).astype(np.int16).tobytes())
    return path


# ---------------------------------------------------------------- 장면
class E1Shock(CaseScene):
    def construct(self):
        card = title_card("충격파")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.wait(2.4)
        self.play(FadeOut(card), run_time=0.6)
        self.three_panels()
        self.faster()
        self.sonic_boom()
        self.boat_wake()
        self.ending()

    # ------------------------------------------------------------ 1. 세 칸
    def three_panels(self):
        note = T("※ 실제보다 아주 느리게 보여 줌", 18, GRAY_T).to_corner(UL, buff=0.3)
        TP = 0.8           # 화면 속 1 주기 (초)
        c = U * TP         # 한 주기 동안 퍼지는 거리 = 0.4
        N = 4.0
        XS = [-4.5, 0.0, 4.5]
        BY = 0.35
        specs = [("정지한 음원", "(vₛ = 0)", 0.0), ("음속보다 느림", "(vₛ < v)", 0.5),
                 ("음속과 같음", "(vₛ = v)", 1.0)]
        tw = ValueTracker(0)
        boxes = VGroup()
        live = []
        for (t1, t2, r), x in zip(specs, XS):
            box = RoundedRectangle(corner_radius=0.1, width=4.15, height=3.75,
                                   stroke_color=PANEL_STROKE, stroke_width=1.5,
                                   fill_color=PANEL_FILL, fill_opacity=0.9).move_to([x, BY, 0])
            ttl = VGroup(T(t1, 24, WHITE_T, bold=True), T(t2, 20, GRAY_T)).arrange(RIGHT, buff=0.12)
            ttl.next_to(box, UP, buff=0.14)
            boxes.add(box, ttl)
            vs = r * c
            x0 = x - 0.0
            cen = (lambda x0, vs: (lambda k: np.array([x0 + vs * k, BY, 0])))(x0, vs)
            w = always_redraw((lambda cen: lambda: fronts(tw.get_value(), cen, c, 1.65, CYAN, 3,
                                                           fade=0.45))(cen))
            sd = always_redraw((lambda x0, vs: lambda: Dot([x0 + vs * tw.get_value(), BY, 0],
                                                            radius=0.1, color=ORANGE))(x0, vs))
            live += [w, sd]
        self.play(FadeIn(boxes), FadeIn(note), run_time=0.7)
        self.add(*live)
        self.say("음원이 빨라지면 파면은 어떻게 될까?", wait=0.1)
        self.play(tw.animate.set_value(N), run_time=N * TP, rate_func=linear)
        self.say("빨라질수록 앞쪽 파면이 촘촘해진다", wait=2.6)
        # 압력의 벽
        wx = XS[2] + c * N
        wall = Line([wx, BY - 1.25, 0], [wx, BY + 1.25, 0], color=ORANGE, stroke_width=9)
        glow = wall.copy().set_stroke(width=26, opacity=0.25)
        wl = label_bg(T("압력의 벽", 21, ORANGE, bold=True)).next_to(wall, LEFT, buff=0.12)
        wl.shift(UP * 1.05)
        self.play(Create(wall), FadeIn(glow), FadeIn(wl), run_time=0.7)
        self.play(Indicate(wall, color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.say("음속과 같으면 파면이 음원 앞에 겹겹이 쌓여\n진폭이 매우 커진다 (압력의 벽)", wait=4.2)
        self.remove(*live)
        self.clear_all()

    # ------------------------------------------------------------ 2. 음속보다 빠름
    def faster(self):
        hd = T("음원이 음속보다 빠르면  (vₛ = 1.6 v)", 28, WHITE_T, bold=True).to_edge(UP, buff=0.3)
        TP = 1.2
        c = U * TP           # 0.6
        vs = 1.6 * c         # 0.96
        X0, Y = -3.0, 0.35
        N = 4
        tw = ValueTracker(0)
        cen = lambda k: np.array([X0 + vs * k, Y, 0])
        waves = always_redraw(lambda: fronts(tw.get_value(), cen, c, 6.0, CYAN, 3, fade=0.5))
        sp = lambda: np.array([X0 + vs * tw.get_value(), Y, 0])

        def src():
            p = sp()
            ar = Arrow(p + RIGHT * 0.12, p + RIGHT * 0.9, buff=0, color=C_S, stroke_width=5,
                       tip_length=0.17)
            return VGroup(ar, Dot(p, radius=0.11, color=ORANGE))

        sd = always_redraw(src)
        self.play(FadeIn(hd), run_time=0.5)
        self.add(waves, sd)
        self.say("음원이 자기가 낸 파면보다 앞서 나간다", wait=0.1)
        self.play(tw.animate.set_value(N), run_time=N * TP, rate_func=linear)
        self.wait(0.4)

        # 지난 자리 S0~S3
        dots = VGroup(*[Dot(cen(k), radius=0.06, color=WHITE_T) for k in range(N)])
        labs = VGroup(*[label_bg(T(f"S{'₀₁₂₃'[k]}", 21, WHITE_T, bold=True)).next_to(cen(k), DOWN, buff=0.14)
                        for k in range(N)])
        sl = label_bg(T("S", 21, ORANGE, bold=True)).next_to(cen(N), DOWN, buff=0.18)
        self.play(FadeIn(dots), FadeIn(labs), FadeIn(sl), run_time=0.6)
        self.say("S₀, S₁, S₂, S₃ 에서 낸 파면들", wait=2.4)

        th = np.arcsin(1 / 1.6)

        def cone(t, extra=1.12):
            p = np.array([X0 + vs * t, Y, 0])
            L = t * np.sqrt(vs ** 2 - c ** 2) * extra
            u1 = np.array([-np.cos(th), np.sin(th), 0])
            u2 = np.array([-np.cos(th), -np.sin(th), 0])
            g = VGroup()
            for u in (u1, u2):
                ln = Line(p, p + L * u, color=ORANGE, stroke_width=6)
                g.add(ln.copy().set_stroke(width=18, opacity=0.2), ln)
            return g

        cn = cone(N)
        S = cen(N)
        clab = label_bg(T("충격파면", 26, ORANGE, bold=True)).move_to(S + np.array([-1.3, 1.75, 0]))
        self.play(Create(cn), run_time=1.0)
        self.play(FadeIn(clab), run_time=0.4)
        self.say("파면들에 공통으로 접하는 선 → 원뿔 모양의 충격파면", wait=3.2)

        # vt, vₛt, sinθ
        S0 = cen(0)
        # 접점: S0 에서 원뿔 선에 수직인 방향 (위쪽 선)
        nrm = np.array([np.sin(th), np.cos(th), 0])
        tp = S0 + c * N * nrm
        r_ln = Line(S0, tp, color=CYAN, stroke_width=5)
        a_ln = Line(S0, S, color=C_S, stroke_width=5).shift(DOWN * 0.0)
        r_lab = label_bg(T("vt", 24, CYAN, bold=True)).move_to((S0 + tp) / 2 + np.array([-0.3, 0.1, 0]))
        a_lab = label_bg(T("vₛt", 24, C_S, bold=True)).move_to((S0 + S) / 2 + DOWN * 0.42)
        ang = Arc(radius=0.75, start_angle=PI - th, angle=th, arc_center=S, stroke_color=WHITE_T,
                  stroke_width=3)
        th_lab = label_bg(T("θ", 22, WHITE_T, bold=True)).move_to(S + 1.0 * np.array([-np.cos(th / 2), np.sin(th / 2), 0]))
        ra = RightAngle(Line(tp, S0), Line(tp, S), length=0.18, quadrant=(1, 1), color=WHITE_T,
                        stroke_width=2)
        self.play(FadeOut(labs[1:]), FadeOut(dots[1:]), FadeOut(clab), run_time=0.4)
        self.play(Create(a_ln), FadeIn(a_lab), run_time=0.7)
        self.play(Create(r_ln), FadeIn(r_lab), FadeIn(ra), run_time=0.7)
        self.play(Create(ang), FadeIn(th_lab), run_time=0.5)
        fm = VGroup(T("sin θ =", 28, WHITE_T, bold=True), T("v", 28, CYAN, bold=True),
                    T("/", 28, WHITE_T, bold=True), T("vₛ", 28, C_S, bold=True)).arrange(RIGHT, buff=0.12)
        fp = panel(fm, buff=0.22).to_corner(UR, buff=0.3).shift(DOWN * 0.75)
        self.play(FadeIn(fp), run_time=0.5)
        self.say("같은 시간 t 동안 파면은 vt, 음원은 vₛt 만큼 간다", wait=3.6)
        self.say("음원이 빠를수록 원뿔이 뾰족해진다", wait=2.6)

        # 원뿔이 음원과 함께 나아감
        self.play(*[FadeOut(m) for m in (r_ln, a_ln, r_lab, a_lab, ang, th_lab, ra, labs[0],
                                          dots[0], sl, fp, hd)], FadeOut(cn), run_time=0.5)
        cnl = always_redraw(lambda: cone(tw.get_value(), 1.0))
        self.add(cnl)
        self.say("충격파면은 음원과 함께 계속 나아간다", wait=0.1)
        self.play(tw.animate.set_value(N + 1.8), run_time=1.8 * TP, rate_func=linear)
        self.wait(0.8)
        self.remove(waves, sd, cnl)
        self.clear_all()

    # ------------------------------------------------------------ 3. 소닉 붐
    def sonic_boom(self):
        GY = -1.55
        JY = 1.5
        sky = Rectangle(width=16, height=9, stroke_width=0).set_fill(color=["#060C16", "#13263C"], opacity=1)
        sky.set_sheen_direction(DOWN)
        ground = Rectangle(width=16, height=3.0, stroke_width=0, fill_color=GROUND,
                           fill_opacity=0.9).move_to([0, GY - 1.5, 0])
        gl = Line([-8, GY, 0], [8, GY, 0], color=GRAY_T, stroke_width=2)
        PX = 1.6
        man = person(0.95).move_to([PX, GY, 0], aligned_edge=DOWN)
        self.play(FadeIn(sky), FadeIn(ground), FadeIn(gl), FadeIn(man), run_time=0.6)

        th = np.arcsin(1 / 1.6)
        jt = jet(1.5)
        L_dn = (JY - GY) / np.sin(th)
        u1 = np.array([-np.cos(th), np.sin(th), 0])
        u2 = np.array([-np.cos(th), -np.sin(th), 0])
        c_up = Line(ORIGIN, 2.6 * u1, color=ORANGE, stroke_width=5)
        c_dn = Line(ORIGIN, L_dn * u2, color=ORANGE, stroke_width=5)
        cone = VGroup(c_up.copy().set_stroke(width=16, opacity=0.2), c_up,
                      c_dn.copy().set_stroke(width=16, opacity=0.2), c_dn)
        plane = VGroup(cone, jt)
        plane.shift(np.array([-7.6, JY, 0]))
        self.add(plane)
        self.add_foreground_mobject(jt)
        hit_x = PX + (JY - GY) / np.tan(th)   # 기수가 이 자리일 때 충격파면이 사람에게 닿음
        spd = 3.2
        t1 = (hit_x - (-7.6)) / spd
        self.say("음속보다 빠른 전투기", wait=0.1)
        self.add_sound(boom_wav(), time_offset=t1)
        self.play(plane.animate.shift(RIGHT * (hit_x + 7.6)), run_time=t1, rate_func=linear)
        bang = T("쾅!", 40, YELLOW, bold=True).next_to(man, UP, buff=0.25).shift(LEFT * 0.2)
        ring = Circle(radius=0.3, color=YELLOW, stroke_width=5).move_to(man.get_center())
        rest = 10.0 - hit_x
        self.play(plane.animate.shift(RIGHT * rest), FadeIn(bang, scale=1.6),
                  ring.animate.scale(4).set_stroke(opacity=0),
                  Wiggle(man, scale_value=1.1, rotation_angle=0.06 * TAU),
                  run_time=rest / spd, rate_func=linear)
        self.remove(ring)
        self.remove_foreground_mobject(jt)
        self.say("충격파면이 지나갈 때 '쾅' — 소닉 붐", wait=3.0)
        self.clear_all()

    # ------------------------------------------------------------ 4. 보트 V자 물결
    def boat_wake(self):
        water = Rectangle(width=16, height=9, stroke_width=0).set_fill(color=[WATER_TOP, WATER_DEEP], opacity=1)
        water.set_sheen_direction(DOWN)
        top = T("위에서 본 모습", 20, GRAY_T).to_corner(UL, buff=0.3)
        self.play(FadeIn(water), FadeIn(top), run_time=0.5)
        Y = 0.4
        X0 = -5.4
        TP = 0.3             # 물결 하나 내는 간격 (초)
        cw = U * TP          # 물결파 속력
        vb = 2.2 * cw        # 배 속력 (물결파의 2.2배)
        tw = ValueTracker(0)
        cen = lambda k: np.array([X0 + vb * k - 0.75, Y, 0])
        rip = always_redraw(lambda: fronts(tw.get_value(), cen, cw, 2.0, "#BFE9FF", 2.2, fade=0.85))
        bt = boat(0.9)
        bt.add_updater(lambda m: m.shift(np.array([X0 + vb * tw.get_value(), Y, 0]) - m.get_right()))
        th = np.arcsin(1 / 2.2)

        def vee():
            t = tw.get_value()
            p = cen(t)
            L = min(t * np.sqrt(vb ** 2 - cw ** 2), 2.0 / cw * np.sqrt(vb ** 2 - cw ** 2))
            g = VGroup()
            for s in (1, -1):
                u = np.array([-np.cos(th), s * np.sin(th), 0])
                g.add(Line(p, p + L * u, color=WHITE_T, stroke_width=4, stroke_opacity=0.85))
            return g

        v = always_redraw(vee)
        self.add(rip, v, bt)
        T_end = 19
        self.say("물결파보다 빨리 달리는 배", wait=0.1)
        self.play(tw.animate.set_value(T_end), run_time=T_end * TP, rate_func=linear)
        bt.clear_updaters()
        self.say("배 뒤의 V자 물결도 충격파와 비슷한 모습", wait=3.2)
        self.remove(rip, v)
        self.clear_all()

    # ------------------------------------------------------------ 5. 한 줄 정리
    def ending(self):
        line = VGroup(T("음원 속력 > 소리 속력", 32, C_S, bold=True), T("→", 32, WHITE_T, bold=True),
                      T("파면이 겹쳐 원뿔 모양 충격파", 32, ORANGE, bold=True)).arrange(RIGHT, buff=0.25)
        p = panel(line, buff=0.45, pos=UP * 0.3)
        self.play(FadeIn(p, shift=UP * 0.15), run_time=0.8)
        self.wait(3.2)
        self.play(FadeOut(p), run_time=0.6)

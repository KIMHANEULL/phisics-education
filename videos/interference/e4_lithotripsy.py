"""체외 충격파 쇄석술 (교과서 112~119쪽 '충격파의 이용').

타원 반쪽 모양 반사판: 한 초점 F₁ 에 충격파 발생 장치, 다른 초점 F₂ 에 결석.
F₁ → 반사판 → F₂ 의 길이는 어느 길이든 2a 로 같다 → 모든 충격파가 동시에 F₂ 에 도착 →
보강 간섭으로 결석 자리에서만 진폭이 매우 커짐 → 결석이 금 가고 부서짐.
"""
from common import *

# 타원 (반사판): 중심, 긴반지름 a, 짧은반지름 b
CX, CY = -0.9, 0.35
A_, B_ = 3.0, 1.95
CF = np.sqrt(A_ ** 2 - B_ ** 2)
F1 = np.array([CX - CF, CY, 0])
F2 = np.array([CX + CF, CY, 0])
SPEED = 2.0          # 화면 속 충격파 속력 (단위/초)
PHI0, PHI1 = np.radians(46), np.radians(314)   # 반사판(왼쪽 반)에 닿는 방향 범위
SKIN = "#E3B9A0"
STONE = "#E8D9A0"


def label_bg(m, buff=0.06):
    return VGroup(BackgroundRectangle(m, color="#0A1220", fill_opacity=0.9, buff=buff), m)


def hit(phi):
    """F₁ 에서 각 phi 로 나간 직선이 타원과 만나는 거리 d 와 점 P."""
    u = np.array([np.cos(phi), np.sin(phi), 0])
    px, py = F1[0] - CX, F1[1] - CY
    qa = (u[0] / A_) ** 2 + (u[1] / B_) ** 2
    qb = 2 * (px * u[0] / A_ ** 2 + py * u[1] / B_ ** 2)
    qc = (px / A_) ** 2 + (py / B_) ** 2 - 1
    d = (-qb + np.sqrt(qb * qb - 4 * qa * qc)) / (2 * qa)
    return d, F1 + d * u


def ray_point(phi, s):
    """F₁ 에서 phi 방향으로 나가 반사판에서 반사된 충격파가 길이 s 만큼 갔을 때의 자리."""
    d, P = hit(phi)
    if s <= d:
        return F1 + s * np.array([np.cos(phi), np.sin(phi), 0]), 0
    w = F2 - P
    w = w / np.linalg.norm(w)
    return P + (s - d) * w, (1 if s <= 2 * A_ else 2)


def front(s, n=140):
    """길이 s 에서의 파면. 나가는 부분(청록) / 반사되어 모이는 부분(주황) / 지나간 뒤(흐린 주황)."""
    g = VGroup()
    if s <= 0.02:
        return g
    phis = np.linspace(PHI0, PHI1, n)
    pts = [ray_point(p, s) for p in phis]
    runs, cur, st = [], [], None
    for p, k in pts:
        if st is None or k == st:
            cur.append(p)
        else:
            runs.append((st, cur))
            cur = [cur[-1], p]
        st = k
    runs.append((st, cur))
    for k, ps in runs:
        if len(ps) < 2:
            continue
        if k == 0:
            col, op, w = CYAN, 1.0, 4
        elif k == 1:
            col, op, w = ORANGE, 1.0, 4 + 3 * (s / (2 * A_))
        else:
            col, op, w = ORANGE, max(0.0, 0.5 - 0.35 * (s - 2 * A_)), 2.5
        if op <= 0:
            continue
        m = VMobject(stroke_color=col, stroke_width=w, stroke_opacity=op)
        m.set_points_as_corners(ps)
        g.add(m.copy().set_stroke(width=w * 3.5, opacity=op * 0.15), m)
    return g


def stone_shape(r=0.3):
    pts = [[r * 1.0, 0.1 * r, 0], [0.55 * r, 0.8 * r, 0], [-0.2 * r, 0.95 * r, 0],
           [-0.85 * r, 0.45 * r, 0], [-0.95 * r, -0.3 * r, 0], [-0.35 * r, -0.9 * r, 0],
           [0.5 * r, -0.8 * r, 0]]
    return Polygon(*pts, stroke_color="#B8A66A", stroke_width=2, fill_color=STONE, fill_opacity=1)


class E4Lithotripsy(CaseScene):
    def construct(self):
        card = title_card("체외 충격파 쇄석술")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.wait(2.4)
        self.play(FadeOut(card), run_time=0.6)
        self.main()

    def pulse(self, extra=0.0, wait_cap=None):
        s = ValueTracker(0.0)
        fr = always_redraw(lambda: front(s.get_value()))
        dots = always_redraw(lambda: VGroup(*[
            Dot(ray_point(p, s.get_value())[0], radius=0.06, color=WHITE_T)
            for p in self.ray_phis if s.get_value() < 2 * A_ - 0.02]))
        self.add(fr, dots)
        self.play(s.animate.set_value(2 * A_), run_time=2 * A_ / SPEED, rate_func=linear)
        self.remove(dots)
        return s, fr

    def main(self):
        note = T("※ 실제보다 아주 느리게 보여 줌", 18, GRAY_T).to_corner(UL, buff=0.3)
        # 몸 (누운 환자의 단면) 과 콩팥
        body = RoundedRectangle(corner_radius=1.1, width=6.3, height=2 * B_, stroke_color=SKIN,
                                stroke_width=2.5, fill_color="#241B20", fill_opacity=1)
        body.move_to([CX + 3.15, CY, 0])   # 몸의 왼쪽 면이 반사판 테두리에 맞닿음
        body_lab = label_bg(T("몸", 22, SKIN, bold=True)).move_to([CX + 5.6, CY + 1.45, 0])
        kid = Ellipse(width=1.55, height=0.95, stroke_color="#C9706B", stroke_width=3,
                      fill_color="#6B2E33", fill_opacity=0.9).rotate(0.35).move_to(F2 + np.array([0.12, 0.05, 0]))
        stone = stone_shape(0.28).move_to(F2)
        # 반사판 (타원 왼쪽 반) + 물
        refl = ParametricFunction(lambda t: np.array([CX + A_ * np.cos(t), CY + B_ * np.sin(t), 0]),
                                  t_range=[PI / 2, 3 * PI / 2], color="#C8D3DE", stroke_width=7)
        water = VMobject(stroke_width=0, fill_color=WATER_TOP, fill_opacity=0.55)
        water.set_points_as_corners([np.array([CX + A_ * np.cos(t), CY + B_ * np.sin(t), 0])
                                     for t in np.linspace(PI / 2, 3 * PI / 2, 60)] + [[CX, CY + B_, 0]])
        pad = Rectangle(width=1.15, height=2 * B_, stroke_width=0, fill_color=WATER_TOP,
                        fill_opacity=0.55).move_to([CX + 0.575, CY, 0])   # 몸 모서리 틈을 채우는 물(젤)
        water = VGroup(pad, water)
        w_lab = label_bg(T("물(젤)로 맞닿게", 18, GRAY_T)).move_to([CX - 0.95, CY - 1.35, 0])
        gen = VGroup(Circle(radius=0.2, stroke_width=0, fill_color=CYAN, fill_opacity=0.25),
                     Circle(radius=0.11, stroke_color=WHITE_T, stroke_width=2, fill_color=CYAN,
                            fill_opacity=1)).move_to(F1)
        c_gen = callout(F1, "초음파 발생 장치", "충격파를 만든다", direction=DL, length=1.05, color=CYAN)
        c_ref = callout([CX + A_ * np.cos(2.2), CY + B_ * np.sin(2.2), 0], "반사판", "타원의 반쪽",
                        direction=UL, length=0.7, color=GRAY_T)
        c_st = callout(F2 + np.array([0.15, 0.2, 0]), "결석", "콩팥 속", direction=UR, length=0.85,
                       color=STONE)

        self.add(note)
        self.play(FadeIn(water[0]), FadeIn(body), FadeIn(body_lab), FadeIn(kid), FadeIn(stone), run_time=0.8)
        self.play(FadeIn(c_st), run_time=0.4)
        self.play(FadeIn(water[1]), FadeIn(w_lab), Create(refl), FadeIn(gen), run_time=1.0)
        self.play(FadeIn(c_gen), FadeIn(c_ref), run_time=0.5)
        self.say("몸 밖의 장치로 몸속 결석을 겨눈다", wait=2.6)

        # 여러 방향의 길
        self.ray_phis = np.radians(np.linspace(62, 298, 9))
        rays = VGroup()
        for p in self.ray_phis:
            d, P = hit(p)
            rays.add(VMobject(stroke_color=GRAY_T, stroke_width=1.6, stroke_opacity=0.45)
                     .set_points_as_corners([F1, P, F2]))
        self.play(FadeOut(c_gen), FadeOut(c_ref), FadeOut(w_lab), Create(rays), run_time=1.0)

        # 1번째 충격파
        self.say("여러 방향의 충격파가\n결석 한 점에 동시에 모인다", wait=0.1)
        s, fr = self.pulse()
        flash = Flash(F2, color=YELLOW, line_length=0.35, num_lines=12, flash_radius=0.4, run_time=0.6)
        cr1 = VGroup(Line(F2 + np.array([-0.2, 0.18, 0]), F2 + np.array([0.08, -0.02, 0]),
                          stroke_color="#4A3B1C", stroke_width=3),
                     Line(F2 + np.array([0.08, -0.02, 0]), F2 + np.array([0.02, -0.22, 0]),
                          stroke_color="#4A3B1C", stroke_width=3))
        self.play(flash, s.animate.set_value(2 * A_ + 1.3), FadeIn(cr1), run_time=0.65, rate_func=linear)
        self.remove(fr)
        self.wait(1.4)

        # 길이가 같다
        f1l = label_bg(T("F₁ (초점)", 20, GRAY_T, bold=True)).next_to(F1, UP + RIGHT, buff=0.15)
        f2l = label_bg(T("F₂ (초점)", 20, GRAY_T, bold=True)).next_to(F2, DOWN, buff=0.42)
        two = VGroup(rays[1].copy().set_stroke(GREEN, 4, 1), rays[6].copy().set_stroke(GREEN, 4, 1))
        tn = panel(T("F₁ → 반사판 → F₂ : 가는 길이가 모두 같아(= 2a) 동시에 도착", 20, GREEN), buff=0.16)
        tn.to_corner(UR, buff=0.3)
        self.play(FadeIn(f1l), FadeIn(f2l), Create(two), FadeIn(tn), run_time=0.8)
        self.add_foreground_mobjects(f1l, f2l)
        self.wait(4.0)
        self.play(FadeOut(two), FadeOut(tn), run_time=0.5)

        # 진폭 비교 막대
        rows = VGroup()
        bars = []
        for name, col in (("결석 자리", ORANGE), ("주변 조직", CYAN)):
            lab = T(name, 20, WHITE_T, bold=True)
            track = Rectangle(width=2.2, height=0.26, stroke_color=PANEL_STROKE, stroke_width=1.2)
            r = VGroup(lab, track).arrange(RIGHT, buff=0.2)
            rows.add(r)
            bars.append((track, col))
        rows.arrange(DOWN, aligned_edge=RIGHT, buff=0.16)
        head = T("진폭", 20, GRAY_T, bold=True)
        mb = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        meter = panel(mb, buff=0.18).to_corner(UR, buff=0.3)
        self.play(FadeIn(meter), run_time=0.5)

        def fill(track, col, frac):
            w = max(track.width * frac, 0.01)
            return Rectangle(width=w, height=track.height, stroke_width=0, fill_color=col,
                             fill_opacity=1).align_to(track, LEFT).set_y(track.get_y())

        self.say("보강 간섭으로 그 점에서만\n진폭이 매우 커진다", wait=0.1)
        s, fr = self.pulse()
        b1 = fill(*bars[0], 1.0)
        b2 = fill(*bars[1], 0.12)
        cr2 = VGroup(Line(F2 + np.array([0.08, -0.02, 0]), F2 + np.array([0.25, 0.12, 0]),
                          stroke_color="#4A3B1C", stroke_width=3),
                     Line(F2 + np.array([-0.05, 0.05, 0]), F2 + np.array([-0.22, -0.12, 0]),
                          stroke_color="#4A3B1C", stroke_width=3))
        self.play(Flash(F2, color=YELLOW, line_length=0.4, num_lines=12, flash_radius=0.45),
                  s.animate.set_value(2 * A_ + 1.3), GrowFromEdge(b1, LEFT), GrowFromEdge(b2, LEFT),
                  FadeIn(cr2), run_time=0.65, rate_func=linear)
        self.remove(fr)
        self.wait(1.6)
        tissue = callout([CX + 3.2, CY - 1.05, 0], "주변 조직", "약한 파동만 지나감", direction=RIGHT,
                         length=0.25, color=CYAN)
        self.play(FadeIn(tissue), run_time=0.5)
        self.say("다른 곳은 약한 파동만 지나가 손상이 적다", wait=2.8)
        self.play(FadeOut(tissue), FadeOut(b1), FadeOut(b2), run_time=0.4)

        # 3번째: 결석이 부서짐
        self.say("여러 번(실제로는 수천 번) 되풀이하면\n결석이 잘게 부서진다", wait=0.1)
        s, fr = self.pulse()
        self.play(Flash(F2, color=YELLOW, line_length=0.45, num_lines=14, flash_radius=0.5),
                  s.animate.set_value(2 * A_ + 1.3), run_time=0.65, rate_func=linear)
        self.remove(fr, stone, cr1, cr2)
        rng = np.random.default_rng(5)
        frags = VGroup()
        for i in range(7):
            ang = TAU * i / 7 + rng.uniform(-0.3, 0.3)
            fpiece = stone_shape(rng.uniform(0.07, 0.12)).rotate(rng.uniform(0, TAU)).move_to(
                F2 + 0.07 * np.array([np.cos(ang), np.sin(ang), 0]))
            fpiece.dir = np.array([np.cos(ang), np.sin(ang), 0])
            frags.add(fpiece)
        self.add(frags)
        self.play(*[f.animate.shift(f.dir * rng.uniform(0.25, 0.42)).rotate(rng.uniform(-1, 1))
                    for f in frags], run_time=0.8, rate_func=rate_functions.ease_out_cubic)
        self.wait(1.0)
        self.say("수술 없이 몸 밖에서 결석을 부순다", wait=2.8)
        self.clear_all()

        line = VGroup(T("여러 충격파를 한 점에 모음", 30, ORANGE, bold=True), T("→", 30, WHITE_T, bold=True),
                      T("보강 간섭으로 결석을 부순다", 30, WHITE_T, bold=True)).arrange(RIGHT, buff=0.22)
        p = panel(line, buff=0.45, pos=UP * 0.3)
        self.play(FadeIn(p, shift=UP * 0.15), run_time=0.8)
        self.wait(3.2)
        self.play(FadeOut(p), run_time=0.6)

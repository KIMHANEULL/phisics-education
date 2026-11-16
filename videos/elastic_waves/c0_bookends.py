"""시리즈 여는 장면(C0Intro)과 마무리 정리 장면(C10Outro)."""
from common import *

CASES = [
    ("1", "박쥐"), ("2", "돌고래"), ("3", "자동차 후방 센서"),
    ("4", "해저 지형 조사"), ("5", "단층 조사"), ("6", "초음파 세척"),
    ("7", "태아 초음파"), ("8", "비파괴 검사"), ("9", "지진파"),
]


def chip(no, name, w=3.6):
    box = RoundedRectangle(corner_radius=0.12, width=w, height=0.78, stroke_color=PANEL_STROKE,
                           stroke_width=1.5, fill_color=PANEL_FILL, fill_opacity=0.92)
    c = Circle(radius=0.22, fill_color=CYAN, fill_opacity=1, stroke_width=0)
    n = T(no, 22, "#06121F", bold=True).move_to(c)
    t = T(name, 26, WHITE_T, bold=True)
    row = VGroup(VGroup(c, n), t).arrange(RIGHT, buff=0.25)
    row.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.25)
    return VGroup(box, row)


class C0Intro(CaseScene):
    def construct(self):
        bg = studio_bg(horizon=0.9)
        self.add(bg)
        card = title_card("초음파로 거리 재기 — 9가지 사례", sub="탄성파의 활용 · 교과서 104~105쪽")
        card.move_to(ORIGIN + UP * 2.6).to_edge(LEFT, buff=0.9)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        chips = VGroup(*[chip(n, s) for n, s in CASES]).arrange_in_grid(3, 3, buff=(0.35, 0.3))
        chips.move_to(DOWN * 0.15)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in chips], lag_ratio=0.15),
                  run_time=2.2)
        self.wait(1.2)
        self.say("박쥐부터 지진파까지, 탄성파가 쓰이는 9가지 사례를 살펴보자", wait=3.2)
        f = distance_formula()
        nt = T("← 갔다가 되돌아왔으니 2로 나눈다", 20, GRAY_T)
        pf = panel(VGroup(f, nt).arrange(RIGHT, buff=0.35))
        pf.move_to(DOWN * 0.15)
        self.play(chips.animate.set_opacity(0.15), FadeIn(pf, scale=0.95), run_time=0.9)
        self.say("핵심 공식은 하나 — 반사되어 돌아온 시간으로 거리를 구한다", wait=3.2)
        self.say("사례마다 이 공식이 어떻게 쓰이는지 확인하자", wait=3.2)
        self.clear_all()
        self.wait(0.3)


ROWS = [
    # 사례, 매질, 속력, 시간, 결과, 비고
    ("1 박쥐", "공기", "340 m/s", "20 ms", "3.4 m", "왕복 ÷2"),
    ("2 돌고래", "물", "1500 m/s", "40 ms", "30 m", "왕복 ÷2"),
    ("3 자동차 센서", "공기", "340 m/s", "5.0 ms", "0.85 m", "왕복 ÷2"),
    ("4 해저 지형", "바닷물", "1500 m/s", "4.0 s", "3000 m", "왕복 ÷2"),
    ("5 단층 조사", "암석", "2000 m/s*", "0.50 s", "500 m", "왕복 ÷2"),
    ("6 초음파 세척", "물", "1500 m/s", "—", "—", "에너지 이용"),
    ("7 태아 초음파", "몸속 조직", "1540 m/s", "0.10 ms", "7.7 cm", "왕복 ÷2"),
    ("8 비파괴 검사", "강철", "5900 m/s", "4.0 μs", "1.2 cm", "왕복 ÷2"),
    ("9 지진파", "암석", "6 km/s*", "10 s", "60 km", "편도 그대로"),
]


class C10Outro(CaseScene):
    def construct(self):
        bg = studio_bg(horizon=0.9, grid=False)
        self.add(bg)
        head = T("한눈에 정리", 36, CYAN, bold=True).to_edge(UP, buff=0.45)
        self.play(FadeIn(head), run_time=0.6)
        cols = ["사례", "매질", "속력", "시간", "거리", "계산"]
        xs = [-5.2, -2.7, -0.9, 1.0, 2.75, 4.75]
        hdr = VGroup(*[T(c, 22, GRAY_T, bold=True).move_to([x, 2.65, 0]) for c, x in zip(cols, xs)])
        line = Line([-6.4, 2.38, 0], [6.1, 2.38, 0], color=PANEL_STROKE, stroke_width=1.5)
        self.play(FadeIn(hdr), Create(line), run_time=0.6)
        rows = VGroup()
        for i, r in enumerate(ROWS):
            y = 2.0 - i * 0.5
            cs = [WHITE_T, GRAY_T, ORANGE, GREEN, GREEN, WHITE_T]
            if r[5] == "편도 그대로":
                cs[5] = CYAN
            if r[5] == "에너지 이용":
                cs[5] = GRAY_T
            row = VGroup(*[T(s, 22, c, bold=(j in (0, 4))).move_to([x, y, 0])
                           for j, (s, c, x) in enumerate(zip(r, cs, xs))])
            row[0].align_to([-6.3, 0, 0], LEFT)
            rows.add(row)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.25),
                  run_time=3.5)
        star = T("* 계산을 쉽게 하려고 가정한 값", 17, GRAY_T).next_to(rows, DOWN, buff=0.22)
        star.align_to([-6.3, 0, 0], LEFT)
        self.play(FadeIn(star), run_time=0.4)
        self.wait(4)
        hl = SurroundingRectangle(VGroup(*[r[5] for r in rows]), color=CYAN, buff=0.12,
                                  corner_radius=0.08, stroke_width=2)
        self.play(Create(hl), run_time=0.8)
        self.say("반사되어 돌아오면(왕복) ÷2,  한 번만 가면(편도) 그대로", wait=3.5)
        self.say("거리 = 속력 × 시간 — 탄성파의 활용은 모두 이 관계에서 출발한다", wait=3.5)
        self.clear_all()
        end = T("탄성파의 활용 · 끝", 40, WHITE_T, bold=True)
        self.play(FadeIn(end), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(end), run_time=0.8)

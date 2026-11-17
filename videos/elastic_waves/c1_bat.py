"""사례 1. 박쥐 — 초음파로 먹이까지의 거리 재기."""
from common import *


def bat_shape(scale=1.0, color="#AEB8C4"):
    wing_r = [[0, 0.05], [0.35, 0.25], [0.8, 0.55], [1.35, 0.45], [1.25, 0.2], [1.05, 0.05],
              [0.85, -0.12], [0.62, -0.05], [0.42, -0.2], [0.2, -0.05]]
    wr = Polygon(*[[x, y, 0] for x, y in wing_r], stroke_color=WHITE_T, stroke_width=1.5,
                 fill_color=color, fill_opacity=0.85)
    wl = wr.copy().flip(UP, about_point=ORIGIN)
    body = Ellipse(width=0.32, height=0.5, fill_color="#C7CFD8", fill_opacity=1,
                   stroke_color=WHITE_T, stroke_width=1.5).move_to([0, -0.02, 0])
    head = Circle(radius=0.13, fill_color="#C7CFD8", fill_opacity=1, stroke_color=WHITE_T,
                  stroke_width=1.5).move_to([0, 0.27, 0])
    e1 = Polygon([-0.11, 0.33, 0], [-0.05, 0.38, 0], [-0.12, 0.52, 0], fill_color="#C7CFD8",
                 fill_opacity=1, stroke_color=WHITE_T, stroke_width=1.2)
    e2 = e1.copy().flip(UP, about_point=ORIGIN)
    g = VGroup(wl, wr, body, e1, e2, head)
    return g.scale(scale)


def moth_shape(scale=1.0):
    c = "#D9B97A"
    w1 = Ellipse(width=0.42, height=0.26, fill_color=c, fill_opacity=0.9, stroke_width=1.2,
                 stroke_color=WHITE_T).rotate(0.5).move_to([0.17, 0.08, 0])
    w2 = w1.copy().flip(UP, about_point=ORIGIN)
    w3 = Ellipse(width=0.28, height=0.18, fill_color=c, fill_opacity=0.8, stroke_width=1.2,
                 stroke_color=WHITE_T).rotate(-0.5).move_to([0.13, -0.11, 0])
    w4 = w3.copy().flip(UP, about_point=ORIGIN)
    body = Ellipse(width=0.09, height=0.36, fill_color="#8E7444", fill_opacity=1,
                   stroke_width=1, stroke_color=WHITE_T)
    return VGroup(w1, w2, w3, w4, body).scale(scale)


class C1Bat(CaseScene):
    def construct(self):
        bg = studio_bg(horizon=0.9)
        self.add(bg)

        BAT = np.array([-4.6, 0.9, 0])
        MOTH = np.array([3.4, 0.4, 0])
        bat = bat_shape(1.15).move_to(BAT).rotate(-0.06)
        moth = moth_shape(1.1).move_to(MOTH)

        # 0. 제목
        card = title_card("박쥐의 초음파 탐지", case_no=1)
        self.play(FadeIn(bat, shift=RIGHT * 0.3), FadeIn(moth), run_time=1)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(card), run_time=0.6)

        # 1. 등장 요소
        cb = callout(BAT + np.array([0.05, 0.3, 0]), "박쥐", "입·코로 초음파를 낸다", UP + RIGHT * 0.5, 1.2)
        cm = callout(MOTH + np.array([0.1, 0.1, 0]), "나방", "먹이 (목표물)", UR, 0.8)
        self.play(Create(cb), run_time=0.8)
        self.play(Create(cm), run_time=0.8)
        self.say("박쥐는 사람이 듣지 못하는 높은 소리,\n초음파(진동수 20 kHz 이상)를 짧게 끊어서 낸다")
        self.say("어두운 곳에서는 눈 대신,\n되돌아온 소리(메아리)로 먹이를 찾는다")
        self.play(FadeOut(cb), FadeOut(cm), run_time=0.5)

        # 2. 송신 → 반사 → 수신 (시간 측정)
        tt = ValueTracker(0)  # 시계·시간축 (ms) — 되감기지 않게 cap 에서 멈춤
        tw = ValueTracker(0)  # 파동 (ms) — 뒤따르는 고리까지 보여 주려고 조금 더 진행
        cap = [20.0]
        tt.add_updater(lambda m: m.set_value(min(tw.get_value(), cap[0])))
        self.add(tt)
        TRIP = 10.0  # 한 방향 걸리는 시간 (ms) : 3.4 m / 340 m/s
        src = BAT + RIGHT * 0.45
        tgt = MOTH + LEFT * 0.2
        D = np.linalg.norm(tgt - src)
        waves = always_redraw(lambda: echo_group(tw.get_value() / TRIP * D, src, tgt,
                                                 0.32, 4, 0.85, 0.8))
        clock = Clock(tt, "ms", "{:.2f}")
        tl = Timeline(25, 5, tt, "ms")
        sn = slow_note()
        self.play(FadeIn(sn), FadeIn(clock), FadeIn(tl), run_time=0.8)
        self.add(waves)
        m0 = tl.marker(0, "신호 발신 시각", ORANGE)
        self.play(FadeIn(m0), run_time=0.4)
        self.say("초음파를 내는 순간 시간을 0으로 놓는다", wait=0.2)
        self.play(tw.animate.set_value(TRIP), run_time=5, rate_func=linear)
        refl = callout(MOTH + np.array([0, 0.25, 0]), "나방에서 반사", None, UR, 0.7)
        self.play(FadeIn(refl), run_time=0.4)
        self.say("나방에 부딪힌 초음파가 반사되어 되돌아온다", wait=0.2)
        self.play(tw.animate.set_value(2 * TRIP + 1.4), run_time=5.7, rate_func=linear)
        self.remove(waves)
        rcv = callout(BAT + np.array([0.15, -0.2, 0]), "반사파 수신", None, DOWN + RIGHT * 0.4, 0.6)
        m1 = tl.marker(2 * TRIP, "신호 수신 시각", GREEN)
        self.play(FadeIn(rcv), FadeIn(m1), FadeOut(refl), run_time=0.6)
        sp = tl.span(0, 2 * TRIP, "시간 차 = 20 ms")
        sp.shift(UP * 0.75)
        self.play(FadeIn(sp), run_time=0.6)
        self.say("보낸 시각과 받은 시각의 차이 = 시간 차 20 ms (= 0.020 s)")
        self.play(FadeOut(rcv), run_time=0.4)

        # 3. 갔다가 되돌아온 경로
        go = Arrow(src + UP * 0.35, tgt + UP * 0.35, buff=0, color=CYAN, stroke_width=4,
                   tip_length=0.2)
        back = Arrow(tgt + DOWN * 0.35, src + DOWN * 0.35, buff=0, color=ORANGE,
                     stroke_width=4, tip_length=0.2)
        lg = T("갈 때", 22, CYAN, bold=True).next_to(go, UP, buff=0.08)
        lb = T("올 때", 22, ORANGE, bold=True).next_to(back, DOWN, buff=0.08)
        self.play(GrowArrow(go), FadeIn(lg), run_time=1)
        self.play(GrowArrow(back), FadeIn(lb), run_time=1)
        self.say("이 20 ms 동안 초음파는 나방까지 갔다가 다시 왔다\n→ 초음파가 이동한 거리는 '박쥐~나방 거리의 2배'")

        # 4. 공식
        f1 = distance_formula()
        nt = T("← 갔다가 되돌아왔으니 2로 나눈다", 20, GRAY_T)
        r1 = VGroup(f1, nt).arrange(RIGHT, buff=0.35)
        f2n = colored([("340 m/s", ORANGE), ("×", WHITE_T), ("0.020 s", GREEN)])
        f2 = frac(f2n, colored([("2", WHITE_T)]))
        res = T("= 3.4 m", 34, GREEN, bold=True)
        r2 = eq_row("=", f2, res)
        r2.next_to(r1, DOWN, buff=0.35, aligned_edge=LEFT).shift(RIGHT * 1.15)
        body = VGroup(r1, r2)
        pnl = panel(body).scale(0.88)
        pnl.move_to([1.4, 0, 0]).to_edge(UP, buff=0.3)
        self.play(FadeOut(sn), FadeOut(clock), FadeIn(pnl[0]), Write(r1), run_time=1.2)
        self.say("공기 속 음속은 약 340 m/s\n(박쥐와 나방은 멈춰 있다고 본다)", wait=2.6)
        self.play(FadeIn(r2[0]), FadeIn(f2), run_time=1)
        self.say("음속과 시간 차를 대입한다 (단위: m/s × s = m)", wait=1.6)
        self.play(FadeIn(res, shift=LEFT * 0.2), run_time=0.7)
        self.play(FadeOut(go), FadeOut(back), FadeOut(lg), FadeOut(lb), run_time=0.5)
        dl = dim_line(src + DOWN * 0.55, tgt + DOWN * 0.55, "3.4 m", offset=DOWN * 0.32)
        self.play(Create(dl), run_time=1)
        self.say("나방까지의 거리는 3.4 m")
        self.wait(0.8)

        # 5. 가까워지면?
        self.play(FadeOut(pnl), FadeOut(dl), FadeOut(m1), FadeOut(sp), run_time=0.6)
        self.unsay()
        MOTH2 = np.array([-0.275, 0.65, 0])  # tgt2 = src~tgt 중간점 → D2 = D/2
        self.play(moth.animate.move_to(MOTH2), run_time=1.5)
        tgt2 = MOTH2 + LEFT * 0.2
        D2 = np.linalg.norm(tgt2 - src)
        cap[0] = 10.0
        tw.set_value(0)
        waves2 = always_redraw(lambda: echo_group(tw.get_value() / 5.0 * D2, src, tgt2,
                                                  0.32, 4, 0.85, 0.8))
        self.add(waves2)
        self.say("먹이가 절반 거리(1.7 m)로 가까워지면?", wait=0.2)
        self.play(tw.animate.set_value(11.4), run_time=5.7, rate_func=linear)
        self.remove(waves2)
        m2 = tl.marker(10, "수신", GREEN)
        sp2 = tl.span(0, 10, "시간 차 = 10 ms").shift(UP * 0.75)
        self.play(FadeIn(m2), FadeIn(sp2), run_time=0.6)
        self.say("거리가 절반이면 시간 차도 절반 (10 ms)\n→ 거리와 시간 차는 비례한다")
        self.say("그래서 박쥐는 메아리가 빨리 올수록 먹이가 가깝다는 것을 안다.\n가까워지면 초음파를 더 자주 내서 위치를 계속 확인한다", wait=6.0)

        # 6. 정리
        self.clear_all(keep=(bg,))
        summ = VGroup(
            T("박쥐 정리", 30, CYAN, bold=True),
            T("· 공기 속 초음파의 속력: 약 340 m/s (음속과 같다)", 26),
            T("· 시간 차 20 ms → 거리 = 340 × 0.020 ÷ 2 = 3.4 m", 26),
            T("· 시간 차가 짧을수록 먹이가 가깝다", 26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        sp_ = panel(summ, buff=0.5, pos=ORIGIN + UP * 0.3)
        self.play(FadeIn(sp_, shift=UP * 0.2), run_time=0.8)
        self.wait(10)
        self.play(FadeOut(sp_), run_time=0.6)

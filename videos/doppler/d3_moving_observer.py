"""도플러 효과 ③ 관찰자가 움직일 때 (교과서 그림 III-15)."""
from d34_kit import *

SRC = np.array([-5.5, 0.2, 0])      # 스피커 위치
EMIT = SRC + RIGHT * 0.3            # 파면이 나오는 점
C = 1.2                             # 화면 속 파동 속력 (단위/초) — 모든 장면 같음
P = 5.0 / 6.0                       # 화면 속 주기 (초) → 화면 속 파장 1.0
RMAX = 11.6
V_OBS = 0.6                         # 화면 속 관찰자 속력 (과장: 파동 속력의 절반)
RUN = 5.0                           # 화면 5초 = '관찰자의 1초' (가만히 있으면 6개)
AXIS_Y = 0.2


def tag(text, color=WHITE_T, size=22):
    t = T(text, size, color, bold=True)
    bg = BackgroundRectangle(t, color=config.background_color, fill_opacity=0.85, buff=0.08)
    return VGroup(bg, t)


def bcallout(*a, **k):
    c = callout(*a, **k)
    g = c[2]
    bgr = BackgroundRectangle(g, color=config.background_color, fill_opacity=0.85, buff=0.08)
    return VGroup(c[0], c[1], bgr, g)


def tagm(mob):
    bg = BackgroundRectangle(mob, color=config.background_color, fill_opacity=0.85, buff=0.08)
    return VGroup(bg, mob)


class D3MovingObserver(CaseScene):
    def construct(self):
        bg = studio_bg(horizon=0.9)
        self.add(bg)

        # 0. 제목만 먼저
        card = title_card("도플러 효과 ③ 관찰자가 움직일 때")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.wait(2.4)
        self.play(FadeOut(card), run_time=0.6)

        # ---------------------------------------------------------- 무대
        st = {"run": True, "x0": 2.0, "vel": 0.0, "t0": 0.0}
        tw = ValueTracker(0.0)  # 화면 시간 (되감기 없음)
        tw.add_updater(lambda m, dt: m.increment_value(dt if st["run"] else 0))
        self.add(tw)

        def x_obs(t=None):
            t = tw.get_value() if t is None else t
            if st["vel"] == 0 or t < st["t0"]:
                return st["x0"]
            return st["x0"] + st["vel"] * min(t - st["t0"], RUN)

        spk = speaker(1.0).move_to(SRC)
        waves = always_redraw(lambda: front_field(tw.get_value(), EMIT, C, P, RMAX, tmin=0.0))
        sn = slow_note("※ 실제보다 아주 느리게, 관찰자 속력은 과장해서 보여 줌")
        st["run"] = False
        self.play(FadeIn(spk, shift=RIGHT * 0.2), FadeIn(sn), run_time=0.8)
        cs = callout(SRC + UP * 0.45, "음원 (스피커)", "제자리에 가만히 있다", UR, 0.9)
        self.play(FadeIn(cs), run_time=0.6)
        self.wait(1.2)
        self.play(FadeOut(cs), run_time=0.4)
        st["run"] = True
        self.add(waves)
        badge = now_playing(1200, "음원이 내는 소리").to_corner(UR, buff=0.3)
        self.play(FadeIn(badge), run_time=0.5)
        play_tone(self, badge, 1200, extra=0)
        self.play(badge.animate.set_opacity(0.3), run_time=0.4)
        self.say("음원은 제자리에서 1200 Hz 소리를 낸다.\n파면이 같은 간격으로 퍼져 나간다", wait=4.5)

        # 파장 표시 (잠깐 멈춤)
        st["run"] = False
        t = tw.get_value()
        rs = sorted([C * (t - k * P) for k in range(int(t / P) + 1) if 0 < C * (t - k * P) < RMAX])
        r1 = [r for r in rs if r > 6.5][0]
        r2 = r1 + C * P
        yy = AXIS_Y - 1.0
        xa = EMIT[0] + np.sqrt(r1 ** 2 - (yy - AXIS_Y) ** 2)
        xb = EMIT[0] + np.sqrt(r2 ** 2 - (yy - AXIS_Y) ** 2)
        lam = dim_line([xa, yy, 0], [xb, yy, 0], "λ", color=GREEN, offset=DOWN * 0.35, size=30)
        self.play(Create(lam), run_time=0.8)
        self.say("파면 사이 간격 = 파장 λ\n이번 영상 내내 이 간격은 바뀌지 않는다")
        self.play(FadeOut(lam), FadeOut(badge), run_time=0.5)
        st["run"] = True

        # ---------------------------------------------------------- 관찰자 + 세기
        obs = person(ORANGE, 0.9)
        obs.add_updater(lambda m: m.move_to([x_obs(), AXIS_Y + 0.05, 0]))

        def glow():
            t = tw.get_value()
            d = x_obs() - EMIT[0]
            k = np.round((t - d / C) / P)
            gap = abs(C * (t - k * P) - d)
            op = max(0.0, 1 - gap / 0.25) if k >= 0 else 0
            hc = obs.head.get_center()
            return Circle(radius=0.3, stroke_color=F_C, stroke_width=6,
                          stroke_opacity=op).move_to(hc)

        gl = always_redraw(glow)
        self.play(FadeIn(obs), run_time=0.6)
        self.add(gl)
        co = bcallout(obs.head.get_center() + UP * 0.15, "관찰자", "귀에 닿는 파면을 센다",
                     UR, 0.7)
        self.play(FadeIn(co), run_time=0.5)
        self.say("관찰자의 귀에 1초 동안 닿는\n파면의 개수를 세어 보자")
        self.play(FadeOut(co), run_time=0.4)

        # 카운터 패널 (오른쪽 위)
        cnt = {"base": 0, "on": False, "final": None}

        def idx(t):
            d = x_obs(t) - EMIT[0]
            return int(np.floor((t - d / C) / P))

        def count_val():
            if cnt["final"] is not None:
                return cnt["final"]
            if not cnt["on"]:
                return 0
            t = min(tw.get_value(), st["t0"] + RUN)
            if t < st["t0"]:
                return 0
            return idx(t) - cnt["base"]

        c_lab = T("1초 동안 만난 파면 수", 20, GRAY_T)
        bar_bg = Rectangle(width=2.6, height=0.14, stroke_color=GRAY_T, stroke_width=1.2)
        c_box = VGroup(c_lab, Rectangle(width=2.6, height=0.62, stroke_width=0), bar_bg)
        c_box.arrange(DOWN, buff=0.12)
        c_pan = panel(c_box, buff=0.22).to_corner(UR, buff=0.3)
        num_slot = c_box[1]

        def num():
            return M(f"{count_val()} 개", 44, F_C).move_to(num_slot)

        def bar():
            if cnt["final"] is not None:
                fr = 1
            elif not cnt["on"]:
                fr = 0
            else:
                fr = min(max((tw.get_value() - st["t0"]) / RUN, 0), 1)
            w = max(2.6 * fr, 0.001)
            return Rectangle(width=w, height=0.14, stroke_width=0, fill_color=GREEN,
                             fill_opacity=1).align_to(bar_bg, LEFT).set_y(bar_bg.get_y())

        bar_lab = T("관찰자의 1초", 18, GRAY_T).next_to(c_pan, DOWN, buff=0.08).align_to(c_pan, RIGHT)
        c_num = always_redraw(num)
        c_bar = always_redraw(bar)
        self.play(FadeIn(c_pan), FadeIn(bar_lab), run_time=0.5)
        self.add(c_num, c_bar)

        tally = VGroup()

        def do_run(x0, vel, text):
            # 시작 위치로 옮기고, 파면 사이(반 칸) 순간에 세기 시작
            st["vel"] = 0.0
            cnt["on"] = False
            cnt["final"] = None
            if abs(st["x0"] - x0) > 1e-6:
                self.play(FadeOut(obs), FadeOut(gl), run_time=0.4)
                st["x0"] = x0
                obs.update()
                self.play(FadeIn(obs), FadeIn(gl), run_time=0.4)
            arr = None
            if vel != 0:
                d = LEFT if vel < 0 else RIGHT
                hc = obs.head.get_center() + UP * 0.5
                arr = always_redraw(lambda: Arrow(obs.head.get_center() + UP * 0.45 - d * 0.45,
                                                  obs.head.get_center() + UP * 0.45 + d * 0.55,
                                                  buff=0, color=ORANGE, stroke_width=5,
                                                  tip_length=0.2))
                self.play(FadeIn(arr), run_time=0.4)
            self.say(text, wait=0.3)
            tn = tw.get_value() + 0.4
            d0 = x0 - EMIT[0]
            n = np.ceil((tn - d0 / C) / P - 0.5)
            t0 = (n + 0.5) * P + d0 / C
            st["t0"] = t0
            st["vel"] = vel
            cnt["base"] = idx(t0)
            cnt["on"] = True
            self.wait(t0 - tw.get_value() + RUN + 0.3)
            cnt["final"] = count_val()
            st["x0"] = x_obs()
            st["vel"] = 0.0
            st["t0"] = 0.0
            return arr

        def add_tally(label, n, color):
            row = VGroup(T(label, 22, WHITE_T, bold=True), M(f"{n} 개", 30, color))
            row.arrange(RIGHT, buff=0.25)
            p = panel(row, buff=0.16)
            tally.add(p)
            tally.arrange(RIGHT, buff=0.25).next_to(c_pan, LEFT, buff=0.35)
            self.play(FadeIn(p, shift=DOWN * 0.1), run_time=0.5)

        # 1) 가만히
        do_run(2.0, 0.0, "① 먼저 가만히 서서 센다")
        add_tally("가만히", 6, F_C)
        self.say("가만히 있으면 6개\n(실제로는 1초에 1200개 — 화면은 줄여서 보여 줌)")

        # 2) 다가가며
        a2 = do_run(4.4, -V_OBS, "② 이번엔 음원 쪽으로 걸어가면서 센다")
        add_tally("다가갈 때", 9, GREEN)
        self.play(FadeOut(a2), run_time=0.3)
        self.say("9개! 파면을 마중 나가니 더 자주 만난다\n(화면은 속력을 과장 — 실제 34 m/s면 1.1배)")
        self.say("마주 오는 자동차 쪽으로 걸어가면\n차와 더 자주 마주치는 것과 같다")

        # 3) 멀어지며
        a3 = do_run(-1.6, V_OBS, "③ 이번엔 음원에서 멀어지면서 센다")
        add_tally("멀어질 때", 3, RED_T)
        self.play(FadeOut(a3), run_time=0.3)
        self.say("3개! 파면에서 달아나니 덜 만난다\n(화면은 속력을 과장 — 실제 34 m/s면 0.9배)")
        self.say("세 번 모두 파면 간격(λ)은 똑같았다.\n달라진 것은 파면을 만나는 속력!")

        # ---------------------------------------------------------- 상대 속력
        st["run"] = False
        self.remove(c_num, c_bar, gl)
        frozen = waves.copy()
        frozen.clear_updaters()
        self.remove(waves)
        self.add(frozen)
        dim = frozen.copy()
        for rg in dim:
            for sm in rg:
                sm.set_stroke(opacity=sm.get_stroke_opacity() * 0.35)
        self.play(FadeOut(c_pan), FadeOut(bar_lab), FadeOut(tally), FadeOut(sn),
                  Transform(frozen, dim), run_time=0.6)
        obs.clear_updaters()
        self.play(obs.animate.move_to([2.6, AXIS_Y + 0.05, 0]), run_time=0.8)
        la = tag("A", ORANGE, 26).next_to(obs, DOWN, buff=0.1)

        wv_arr = Arrow([-1.2, AXIS_Y - 1.0, 0], [0.8, AXIS_Y - 1.0, 0], buff=0, color=CYAN,
                       stroke_width=6, tip_length=0.25)
        wv_lab = tagm(mrow(("파면", CYAN), sym("v", None, CYAN, 26), ("= 340 m/s", CYAN),
                           size=26)).next_to(wv_arr, DOWN, buff=0.12)
        hc = obs.head.get_center()
        ob_arr = Arrow(hc + UP * 0.5 + RIGHT * 0.4, hc + UP * 0.5 + LEFT * 1.2, buff=0,
                       color=ORANGE, stroke_width=6, tip_length=0.25)
        ob_lab = tagm(mrow(("관찰자", ORANGE), vo(size=26), ("= 34 m/s", ORANGE),
                           size=26)).next_to(ob_arr, UP, buff=0.1)
        self.play(FadeIn(la), GrowArrow(wv_arr), FadeIn(wv_lab), run_time=0.8)
        self.play(GrowArrow(ob_arr), FadeIn(ob_lab), run_time=0.8)

        eqA = mrow(sym("v′", None, WHITE_T), "=", sym("v", None, CYAN), "+", vo(), "=",
                   ("340", CYAN), "+", ("34", OBS_C), "=", ("374 m/s", GREEN))
        qa = VGroup(T("A가 느끼는 파면의 속력 (상대 속력)", 22, GRAY_T), eqA)
        qa.arrange(DOWN, buff=0.15)
        pa = panel(qa, buff=0.25).move_to([0.2, 0, 0]).to_edge(UP, buff=0.3)
        self.play(FadeIn(pa), run_time=0.7)
        self.say("A는 → 로 오는 파면을 향해 ← 로 걷는다\n마주 보고 다가가면 속력이 더해진다  v′ = v + vₒ")

        # B: 멀어질 때
        ob_arrB = Arrow(hc + UP * 0.5 + LEFT * 0.4, hc + UP * 0.5 + RIGHT * 1.2, buff=0,
                        color=ORANGE, stroke_width=6, tip_length=0.25)
        ob_labB = ob_lab.copy().next_to(ob_arrB, UP, buff=0.1)
        lb = tag("B", ORANGE, 26).move_to(la)
        eqB = mrow(sym("v″", None, WHITE_T), "=", sym("v", None, CYAN), "−", vo(), "=",
                   ("340", CYAN), "−", ("34", OBS_C), "=", ("306 m/s", RED_T))
        qb = VGroup(T("B가 느끼는 파면의 속력 (상대 속력)", 22, GRAY_T), eqB)
        qb.arrange(DOWN, buff=0.15)
        pb = panel(qb, buff=0.25).move_to(pa)
        self.play(ReplacementTransform(ob_arr, ob_arrB), ReplacementTransform(ob_lab, ob_labB),
                  ReplacementTransform(la, lb), FadeOut(pa), FadeIn(pb), run_time=0.9)
        self.say("B: 관찰자가 파면과 같은 방향으로 달아나면\n속력을 뺀다  v″ = v − vₒ")

        # ---------------------------------------------------------- 유도 (A)
        self.unsay()
        self.clear_all(keep=(bg,))
        fA = sym("f", "A", F_C)
        l1 = mrow(fA, "=", mfrac([sym("v′")], [("λ", GREEN)]), "=",
                  mfrac([sym("v", None, CYAN), "+", vo()], [("λ", GREEN)]))
        l2 = mrow("=", mfrac([sym("v", None, CYAN), "+", vo()],
                             [mfrac([sym("v", None, CYAN)], [sym("f", None, F_C)], size=30)]),
                  "=", mfrac([sym("v", None, CYAN), "+", vo()], [sym("v", None, CYAN)]),
                  "×", sym("f", None, F_C))
        l3a = mrow("=", mfrac([("(340)", CYAN), "+", ("(34)", OBS_C)], [("(340)", CYAN)]),
                   "×", ("(1200)", F_C))
        l3b = mrow("=", ("1.1", GREEN), "×", "1200", "=", ("1320 Hz", GREEN))
        l3 = VGroup(l3a, l3b).arrange(RIGHT, buff=0.25)
        body = VGroup(l1, l2, l3).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        l2.shift(RIGHT * (fA.width + 0.12))
        l3.shift(RIGHT * (fA.width + 0.12))
        hdr = T("관찰자 A (다가갈 때)", 22, ORANGE, bold=True)
        hdr.next_to(body, UP, buff=0.25, aligned_edge=LEFT)
        lnote = mrow(("λ", GREEN), "=", mfrac([sym("v", None, CYAN, 26)], [sym("f", None, F_C, 26)],
                                              size=26), ("(①의 f = v/λ 에서)", GRAY_T), size=26)
        lnote.next_to(l2, RIGHT, buff=0.8)
        allb = VGroup(hdr, body, lnote)
        pd = panel(allb, buff=0.3)
        if pd.width > 12.6:
            pd.scale_to_fit_width(12.6)
        pd.move_to(ORIGIN).to_edge(UP, buff=0.3)
        self.play(FadeIn(pd[0]), FadeIn(hdr), run_time=0.6)
        self.play(FadeIn(l1[0]), FadeIn(l1[1]), FadeIn(l1[2]), run_time=0.7)
        self.say("들리는 진동수 = 1초에 만나는 파면 수\n= 만나는 속력 ÷ 파면 간격")
        self.play(FadeIn(l1[3]), FadeIn(l1[4]), run_time=0.7)
        self.say("만나는 속력 v′ 자리에 v + vₒ", wait=2.2)
        self.play(FadeIn(lnote), run_time=0.5)
        self.play(FadeIn(l2[0]), FadeIn(l2[1]), run_time=0.8)
        self.say("파장 λ 자리에 v / f 를 넣고", wait=2.4)
        self.play(FadeIn(l2[2:]), run_time=0.8)
        self.say("정리하면  (v + vₒ) / v × f", wait=2.4)
        self.play(FadeIn(l3a), run_time=0.8)
        self.say("v = 340 m/s, vₒ = 34 m/s, f = 1200 Hz 를 대입")
        self.play(FadeIn(l3b), run_time=0.8)
        self.say("만나는 속력이 1.1배 → 1초에 만나는 파면도 1.1배\n→ 1200 Hz가 1320 Hz로 높아진다")
        bA = now_playing(1320, "A가 듣는 소리").next_to(pd, DOWN, buff=0.35).align_to(pd, LEFT)
        self.unsay()
        self.play(FadeIn(bA), run_time=0.4)
        play_tone(self, bA, 1320)

        # ---------------------------------------------------------- 유도 (B)
        self.play(FadeOut(pd), FadeOut(bA), run_time=0.5)
        fB = sym("f", "B", F_C)
        m1 = mrow(fB, "=", mfrac([sym("v″")], [("λ", GREEN)]), "=",
                  mfrac([sym("v", None, CYAN), "−", vo()], [sym("v", None, CYAN)]),
                  "×", sym("f", None, F_C))
        m2 = mrow("=", mfrac([("(340)", CYAN), "−", ("(34)", OBS_C)], [("(340)", CYAN)]),
                  "×", ("(1200)", F_C), "=", ("0.9", RED_T), "×", "1200", "=",
                  ("1080 Hz", RED_T))
        bodyB = VGroup(m1, m2).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        m2.shift(RIGHT * (fB.width + 0.12))
        hdrB = T("관찰자 B (멀어질 때)", 22, ORANGE, bold=True)
        hdrB.next_to(bodyB, UP, buff=0.25, aligned_edge=LEFT)
        pdB = panel(VGroup(hdrB, bodyB), buff=0.3).move_to(ORIGIN).to_edge(UP, buff=0.3)
        self.play(FadeIn(pdB[0]), FadeIn(hdrB), FadeIn(m1), run_time=0.8)
        self.say("B도 똑같이: 만나는 속력 v″ = v − vₒ 를 λ로 나눈다")
        self.play(FadeIn(m2), run_time=0.8)
        self.say("만나는 속력이 0.9배 → 1200 Hz가 1080 Hz로 낮아진다")
        bB = now_playing(1080, "B가 듣는 소리").next_to(pdB, DOWN, buff=0.35).align_to(pdB, LEFT)
        self.unsay()
        self.play(FadeIn(bB), run_time=0.4)
        play_tone(self, bB, 1080)
        self.play(FadeOut(pdB), FadeOut(bB), run_time=0.5)

        # ---------------------------------------------------------- 비교해서 듣기
        b0 = now_playing(1200, "가만히")
        b1 = now_playing(1320, "다가갈 때 (A)")
        b2 = now_playing(1080, "멀어질 때 (B)")
        brow = VGroup(b0, b1, b2).arrange(RIGHT, buff=0.5).move_to(UP * 0.6)
        self.say("차례로 들어 보자", wait=0.6)
        for b, f in ((b0, 1200), (b1, 1320), (b2, 1080)):
            self.play(FadeIn(b, shift=UP * 0.1), run_time=0.4)
            play_tone(self, b, f, extra=0.4)
        self.say("다가가면 높게, 멀어지면 낮게 들린다", wait=2.4)
        self.play(FadeOut(brow), run_time=0.5)

        # ---------------------------------------------------------- ②와 비교
        self.unsay()
        boxL = self.mini_source_moving()
        boxR = self.mini_observer_moving()
        tL = VGroup(T("음원이 움직이면", 24, SRC_C, bold=True),
                    T("파장 λ가 바뀐다", 24, WHITE_T, bold=True),
                    T("(앞은 촘촘, 뒤는 성김)", 20, GRAY_T)).arrange(DOWN, buff=0.1)
        tR = VGroup(T("관찰자가 움직이면", 24, ORANGE, bold=True),
                    T("파장은 그대로,", 24, WHITE_T, bold=True),
                    T("만나는 속력(상대 속력)이 바뀐다", 24, WHITE_T, bold=True))
        tR.arrange(DOWN, buff=0.1)
        colL = VGroup(boxL, tL).arrange(DOWN, buff=0.3)
        colR = VGroup(boxR, tR).arrange(DOWN, buff=0.3)
        cols = VGroup(colL, colR).arrange(RIGHT, buff=1.0, aligned_edge=UP)
        ttl = T("②와 비교", 28, CYAN, bold=True)
        cmp_ = VGroup(ttl, cols).arrange(DOWN, buff=0.3)
        pc = panel(cmp_, buff=0.35).move_to(ORIGIN).to_edge(UP, buff=0.3)
        self.play(FadeIn(pc[0]), FadeIn(ttl), run_time=0.6)
        self.play(FadeIn(colL), run_time=0.8)
        self.wait(2.6)
        self.play(FadeIn(colR), run_time=0.8)
        self.wait(1.0)
        self.say("둘 다 진동수가 바뀌지만, 바뀌는 이유가 다르다")
        self.play(FadeOut(pc), run_time=0.6)
        self.unsay()

        # ---------------------------------------------------------- 정리
        def lineF(head, sub, sign, res, rc):
            return mrow((head, WHITE_T), sym("f", sub, F_C, 26), "=",
                        mfrac([sym("v", None, CYAN, 26), sign, vo(size=26)],
                              [sym("v", None, CYAN, 26)], size=26),
                        "×", sym("f", None, F_C, 26), "=", (res, rc), size=26)

        lines = [
            T("· 음원은 가만히, 관찰자가 움직이면 → 파장 λ는 그대로", 26, bold=True),
            mrow("· 바뀌는 것은 파면을 만나는 속력 (", sym("v", None, CYAN, 26), "+", vo(size=26),
                 "또는", sym("v", None, CYAN, 26), "−", vo(size=26), ")", size=26),
            lineF("· 다가갈 때  ", "A", "+", "1320 Hz (높게)", GREEN),
            lineF("· 멀어질 때  ", "B", "−", "1080 Hz (낮게)", RED_T),
        ]
        summary_reveal(self, lines, "관찰자가 움직일 때 정리", pos=UP * 0.2, hold=4.0)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.wm and m is not bg],
                  run_time=0.6)

    # ------------------------------------------------------------------ 작은 그림
    def mini_source_moving(self):
        box = RoundedRectangle(corner_radius=0.1, width=4.6, height=2.2, stroke_color=GRAY_T,
                               stroke_width=1, fill_opacity=0)
        g = VGroup()
        cx = box.get_center()
        sx = cx + RIGHT * 0.4
        for i in range(4):  # 오래된 파면일수록 중심이 뒤(왼쪽): 앞 간격 0.12, 뒤 간격 0.38
            r = 0.32 + 0.25 * i
            g.add(Circle(radius=r, stroke_color=CYAN, stroke_width=3).move_to(sx + LEFT * 0.13 * i))
        spk = speaker(0.26).move_to(sx)
        arr = Arrow(cx + RIGHT * 1.25, cx + RIGHT * 2.05, buff=0, color=SRC_C,
                    stroke_width=5, tip_length=0.18)
        grp = VGroup(box, g, spk, arr)
        return grp

    def mini_observer_moving(self):
        box = RoundedRectangle(corner_radius=0.1, width=4.6, height=2.2, stroke_color=GRAY_T,
                               stroke_width=1, fill_opacity=0)
        cx = box.get_center()
        sc = cx + LEFT * 1.0
        g = VGroup(*[Circle(radius=0.32 + 0.25 * i, stroke_color=CYAN, stroke_width=3).move_to(sc)
                     for i in range(4)])
        spk = speaker(0.26).move_to(sc)
        p = person(ORANGE, 0.55).move_to(cx + RIGHT * 1.45)
        arr = Arrow(p.get_top() + UP * 0.12 + RIGHT * 0.3, p.get_top() + UP * 0.12 + LEFT * 0.5,
                    buff=0, color=ORANGE, stroke_width=5, tip_length=0.16)
        return VGroup(box, g, spk, p, arr)

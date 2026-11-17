import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
plt.rcParams["font.family"] = "WenQuanYi Zen Hei"

W, H = 500, 600
fig, ax = plt.subplots(figsize=(18, 16.5))
ax.set_aspect("equal"); ax.axis("off")
ax.set_xlim(-265, W + 730); ax.set_ylim(-505, H + 90)
GREY, BROWN, BLUE, BLACK, HOLE = "#6b6b6b", "#8b4513", "#1f5fd6", "black", "#d62728"
Y = lambda t: H - t
def box(x, t, w, h, label, size, fc, fs=8.5, sfs=7, ldy=8, sdy=-10):
    ax.add_patch(Rectangle((x, Y(t + h)), w, h, fc=fc, ec="black", lw=1.2, zorder=5))
    ax.text(x + w/2, Y(t + h/2) + ldy, label, ha="center", va="center", fontsize=fs, weight="bold", zorder=6)
    ax.text(x + w/2, Y(t + h/2) + sdy, size, ha="center", va="center", fontsize=sfs, zorder=6)
def hdim(x1, x2, y, txt, bg="#f4f4f4"):
    ax.annotate("", (x1, y), (x2, y), arrowprops=dict(arrowstyle="<->", lw=0.7))
    ax.text((x1+x2)/2, y + 3, txt, ha="center", va="bottom", fontsize=7.5, bbox=dict(fc=bg, ec="none", pad=0.3))
def vdim(y1, y2, x, txt, bg="white", right=False):
    ax.annotate("", (x, y1), (x, y2), arrowprops=dict(arrowstyle="<->", lw=0.7))
    ax.text(x + 4 if right else x - 4, (y1+y2)/2, txt, ha="left" if right else "right", va="center", fontsize=7.5, rotation=90, bbox=dict(fc=bg, ec="none", pad=0.3))
def line(pts, c, lw, z=3):
    ax.plot([p[0] for p in pts], [Y(p[1]) for p in pts], color=c, lw=lw, zorder=z, solid_capstyle="round")
def dot(x, t, c="black", z=7): ax.plot(x, Y(t), "o", ms=3.5, color=c, zorder=z)

ax.add_patch(Rectangle((0, 0), W, H, fc="#f4f4f4", ec="black", lw=2.2))

# ---- layout ----
ex0, et = 32, 30                                   # ELB (horizontal)
box(ex0, et, 70, 32, "ELB (2P)", "70 x 32 x 39", "#ffe9a8", fs=8, sfs=6.5, ldy=6, sdy=-7)
st = 100; sx = (W - 145) / 2; sb = st + 90         # Sonoff centered
box(sx, st, 145, 90, "SONOFF 4CH PRO R3", "145 x 90 x 34", "#cfe8ff", ldy=14, sdy=-4)
cw, ch, cg = 94, 140, 20
ct = sb + 170                                      # wider gap for 16SQ routing
cx0 = (W - (4*cw + 3*cg)) / 2
mcx = [cx0 + i*(cw+cg) for i in range(4)]
mcc = [x + cw/2 for x in mcx]
for i, x in enumerate(mcx):
    box(x, ct, cw, ch, f"MC-85a #{i+1}", "94 x 140\nx 172.3", "#d9f2d0")

# ---- holes ----
def side_hole(cy, d, txt):
    ax.add_patch(Rectangle((-5, Y(cy + d/2)), 10, d, fc="white", ec=HOLE, lw=1.4, zorder=9))
    ax.text(8, Y(cy - d/2) - 1, txt, fontsize=6.5, color=HOLE, va="top", zorder=9,
            bbox=dict(fc="#f4f4f4", ec="none", pad=0.2))
def bottom_hole(cx, d, txt):
    ax.add_patch(Rectangle((cx - d/2, -5), d, 10, fc="white", ec=HOLE, lw=1.4, zorder=9))
    ax.text(cx + d/2 + 2, 8, txt, fontsize=6.5, color=HOLE, va="bottom", zorder=9,
            bbox=dict(fc="#f4f4f4", ec="none", pad=0.2))
hE, hU, hL = 46, 240, 320                          # side hole centers (from top)
side_hole(hE, 30, "Ø30")
side_hole(hU, 50, "Ø50")
side_hole(hL, 50, "Ø50")
for c in mcc: bottom_hole(c, 50, "Ø50")
GL = "#c9c9c9"
def gland(c, d, side):
    nut, body, L = d + 14, d - 4, 34          # 외부 너트 폭 / 캡 / 돌출 길이 (개략)
    from matplotlib.patches import Polygon
    if side == "L":
        y = Y(c)
        ax.add_patch(Rectangle((-14, y - nut/2), 9, nut, fc=GL, ec="#666", lw=0.8, zorder=1))
        ax.add_patch(Polygon([(-14, y - body/2), (-L, y - body/2 + 4), (-L, y + body/2 - 4), (-14, y + body/2)],
                             fc=GL, ec="#666", lw=0.8, zorder=1))
    else:
        ax.add_patch(Rectangle((c - nut/2, -14), nut, 9, fc=GL, ec="#666", lw=0.8, zorder=1))
        ax.add_patch(Polygon([(c - body/2, -14), (c - body/2 + 4, -L), (c + body/2 - 4, -L), (c + body/2, -14)],
                             fc=GL, ec="#666", lw=0.8, zorder=1))
gland(hE, 30, "L"); gland(hU, 50, "L"); gland(hL, 50, "L")
for c in mcc: gland(c, 50, "B")

# ---- main circuit 16SQ (SUB 분전반 -> MC line side -> load) ----
xs = -120
line([(xs, hU), (mcc[3], hU)], GREY, 4.5, 2)       # CB3·CB4 -> MC3·MC4 (6선)
line([(xs, hL), (mcc[1], hL)], GREY, 4.5, 2)       # CB1·CB2 -> MC1·MC2 (6선)
for i in (2, 3): line([(mcc[i], hU), (mcc[i], ct)], GREY, 4.5, 2)
for i in (0, 1): line([(mcc[i], hL), (mcc[i], ct)], GREY, 4.5, 2)
dot(mcc[2], hU, GREY, 3); dot(mcc[0], hL, GREY, 3)
ax.text(xs - 5, Y(hU), "CB3·CB4 → MC3·MC4\n16SQ KIV x 6", ha="right", va="center", fontsize=7, color=GREY)
ax.text(xs - 5, Y(hL), "CB1·CB2 → MC1·MC2\n16SQ KIV x 6", ha="right", va="center", fontsize=7, color=GREY)
ax.text(xs - 5, Y((hU + hL)/2), "SUB 분전반 (Grid Simulator)", ha="right", va="center", fontsize=8,
        color=GREY, weight="bold")
for i, c in enumerate(mcc):
    line([(c, ct + ch), (c, H + 45)], GREY, 4.5, 2)
    ax.text(c, -74, f"부하{i+1}", fontsize=7.5, color=GREY, ha="center")
    ax.text(c + 5, Y(ct + ch + 55), "16SQ KIV x 3", fontsize=6.5, color=GREY, rotation=90, va="center",
            bbox=dict(fc="#f4f4f4", ec="none", pad=0.2))

# ---- Sonoff bottom terminals ----
T = {"N": 38.4, "L": 43.6}
for i, o in enumerate([52.6, 71.2, 91.3, 110.4]):
    T[f"NO{i+1}"], T[f"COM{i+1}"], T[f"NC{i+1}"] = o, o + 5.3, o + 10.6
T = {k: sx + v for k, v in T.items()}
for x in T.values():
    ax.plot(x, Y(sb - 3), "o", ms=3.2, mfc="white", mec="black", mew=0.8, zorder=8)
ax.text((T["N"] + T["L"])/2, Y(sb - 10), "N  L", ha="center", fontsize=5.5, zorder=8)
for i in range(4):
    ax.text(T[f"COM{i+1}"], Y(sb - 10), f"R{i+1}", ha="center", fontsize=5.5, zorder=8)
    ax.plot([T[f"NO{i+1}"] - 1, T[f"NC{i+1}"] + 1], [Y(sb - 7)] * 2, color="black", lw=0.5, zorder=8)

# ---- control power: Main 분전반 -> ELB -> Sonoff ----
yLin, yNin = et + 9, et + 23
line([(xs, yLin), (ex0, yLin)], BROWN, 1.6)
line([(xs, yNin), (ex0, yNin)], BLUE, 1.6)
ax.text(xs - 5, Y((yLin + yNin)/2), "Main 분전반 (KR 계통)\nAC 220V  4SQ KIV x 2", ha="right", va="center",
        fontsize=7.5, color=BROWN)
ax.text(xs + 3, Y(yLin) + 2, "L", fontsize=6.5, color=BROWN, va="bottom")
ax.text(xs + 3, Y(yNin) + 2, "N", fontsize=6.5, color=BLUE, va="bottom")
for yy, c in [(yLin, BROWN), (yNin, BLUE)]:
    dot(ex0, yy, c); dot(ex0 + 70, yy, c)
nx_, lx_ = ex0 + 78, ex0 + 86
yN, yL = sb + 12, sb + 22
line([(ex0 + 70, yNin), (nx_, yNin), (nx_, yN), (T["N"], yN), (T["N"], sb - 3)], BLUE, 1.5, 5)
line([(ex0 + 70, yLin), (lx_, yLin), (lx_, yL), (T["L"], yL), (T["L"], sb - 3)], BROWN, 1.5, 5)
ax.text(lx_ + 3, Y(125), "HIV 1.5SQ", fontsize=6.5, color=BROWN, rotation=90, va="center")
yj = sb + 5
line([(T["L"], yj), (T["COM4"], yj)], BROWN, 1.3, 5); dot(T["L"], yj, BROWN)
for i in range(4): line([(T[f"COM{i+1}"], sb - 3), (T[f"COM{i+1}"], yj)], BROWN, 1.3, 5)

# ---- coil wiring (top of MC) ----
A1x = [x + 12 for x in mcx]; A2x = [x + cw - 12 for x in mcx]
for i in range(4):
    dot(A1x[i], ct, z=8); ax.text(A1x[i], Y(ct + 7), "A1", fontsize=6, ha="center", va="center", zorder=8)
    dot(A2x[i], ct, BLUE, 8); ax.text(A2x[i], Y(ct + 7), "A2", fontsize=6, ha="center", va="center", zorder=8)
hy = [sb + 30, sb + 36, sb + 42, sb + 30]
for i in range(4):
    xo = T[f"NO{i+1}"]
    line([(xo, sb - 3), (xo, hy[i]), (A1x[i], hy[i]), (A1x[i], ct)], BLACK, 1.1, 4)
chy = ct - 10
dot(nx_, yN, BLUE)
line([(nx_, yN), (nx_, chy), (A2x[3], chy)], BLUE, 1.4, 4)
for i in range(4):
    line([(A2x[i], chy), (A2x[i], ct)], BLUE, 1.4, 4)
    if i < 3: dot(A2x[i], chy, BLUE)
ax.text(A1x[1] + 8, Y((hU + hL)/2), "코일 배선\nHIV 1.5SQ", fontsize=6, va="center",
        bbox=dict(fc="#f4f4f4", ec="none", pad=0.2), zorder=6)

# ---- dimensions ----
hdim(0, W, H + 25, "500", bg="white")
pts = [0]
for x in mcx: pts += [x, x + cw]
pts += [W]
for a, b in zip(pts[:-1], pts[1:]): hdim(a, b, -55, f"{b-a:g}", bg="white")
for a, b in [(0, sx), (sx, sx + 145), (sx + 145, W)]: hdim(a, b, Y(st) + 10, f"{b-a:g}")
hdim(0, ex0, Y(12), f"{ex0:g}")
vdim(Y(0), Y(et), ex0 + 50, f"{et:g}", bg="#f4f4f4")
vdim(H, 0, W + 55, "600", right=True)
m = [0, st, sb, ct, ct + ch, H]
for a, b in zip(m[:-1], m[1:]): vdim(Y(a), Y(b), W + 20, f"{b-a:g}", right=True)

# ---- 경첩 (좌) / 걸쇠 (우) ----
HG = "#555555"
for t_ in (130, 530):
    ax.add_patch(Rectangle((-5, Y(t_ + 20)), 10, 40, fc=HG, ec="black", lw=0.8, zorder=8))
    ax.text(9, Y(t_), "경첩", fontsize=7.5, va="center", ha="left", weight="bold", color=HG, zorder=8)
ax.add_patch(Rectangle((W - 12, Y(320)), 12, 40, fc=HG, ec="black", lw=0.8, zorder=8))
ax.add_patch(Circle((W - 6, Y(300)), 3, fc="white", ec="black", lw=0.6, zorder=9))
ax.text(W - 15, Y(300), "걸쇠", fontsize=7.5, va="center", ha="right", weight="bold", color=HG, zorder=8)

# ---- legend / notes (below front view, 2 columns) ----
def col(x, y0, lines):
    for k, t in enumerate(lines):
        ax.text(x, y0 - k*19, t, fontsize=8, va="top", weight="bold" if t.startswith("■") else "normal")
c1, c2, ly0 = -240, 140, -128
ax.text(c1, ly0, "■ 배선 범례", fontsize=8, weight="bold", va="top")
for k, (c, w_, t) in enumerate([(GREY, 4.5, "주회로 L1·L2·N (SUB 분전반)"), (BROWN, 1.6, "제어 L (Main 분전반)"),
                                (BLUE, 1.6, "N (Sonoff N, MC A2 점프)"), (BLACK, 1.2, "NO1~4 → MC1~4 A1 (L 출력)")]):
    yy = ly0 - 26 - k*19
    ax.plot([c1 + 5, c1 + 35], [yy, yy], color=c, lw=w_); ax.text(c1 + 43, yy, t, va="center", fontsize=8)
yy = ly0 - 26 - 4*19
ax.add_patch(Rectangle((c1 + 15, yy - 5), 10, 10, fc="white", ec=HOLE, lw=1.4))
ax.text(c1 + 43, yy, "타공", va="center", fontsize=8)
col(c1, ly0 - 130, ["■ 타공 (중심 위치는 상단 기준)",
         "· 좌측면 Ø30 (46): 220V 인입 4SQ x 2",
         "· 좌측면 Ø50 (240): MC3·MC4 인입 16SQ x 6",
         "· 좌측면 Ø50 (320): MC1·MC2 인입 16SQ x 6",
         "· 하단 Ø50 x 4: 부하1~4 인출 16SQ x 3씩",
         "· 타공 깊이 방향 중심: 100 (박스 깊이 중앙)",
         "· 한 회로 L1·L2·N은 반드시 같은 구멍으로", "",
         "■ 타공 마감: 케이블 그랜드 (나일론, 전 타공)",
         "· Ø50 x 6 → PG36 그랜드 (나사 47 / 너트 52)",
         "· Ø30 x 1 → PG21 그랜드 (나사 28.3 / 너트 33)",
         "· 고정용 아님 (헐겁게 통과, 마감 목적)",
         "· 좌측 Ø50 간격 80: 그랜드 너트 간섭 방지"])
col(c2, ly0, ["■ 전선 규격",
         "· 220V 인입 (Main → ELB 1차측): 4SQ KIV",
         "· ELB 2차측 → Sonoff N/L: HIV 1.5SQ",
         "· L → COM1~4 점프선: HIV 1.5SQ",
         "· 코일 배선 (NO → A1, A2 N 점프): HIV 1.5SQ",
         "· SUB → 접촉기 INPUT: 16SQ KIV (회로당 3선)",
         "· 접촉기 OUTPUT (→ 부하1~4): 16SQ KIV", "",
         "■ 참고",
         "· Main / SUB 분전반은 하이박스 좌측에 나란히",
         "· CB1~4 (3P)는 SUB 분전반 측",
         "· 2P ELB = 제어용 CP 역할",
         "· Sonoff ~ 접촉기 간격 170: 16SQ 굴곡 공간"])

# ================= views =================
from matplotlib.patches import Circle
D = 200
ax.text(W/2, -100, "[ 정면도 ]", ha="center", fontsize=11, weight="bold")

# ---- 좌측면도 (정면도 우측 배치, 오른쪽이 도어/정면) ----
L0 = W + 140                                  # back face x; front (door) = L0 + D
ax.add_patch(Rectangle((L0, 0), D, H, fc="#f4f4f4", ec="black", lw=2.2))
ax.text(L0 + 3, Y(-6), "후면 (취부판)", fontsize=6.5, ha="left", va="bottom", color="#555")
ax.text(L0 + D - 3, Y(-6), "정면 (도어)", fontsize=6.5, ha="right", va="bottom", color="#555")
for t_, h_, d_, nm in [(et, 32, 39, "ELB 39"), (st, 90, 34, "Sonoff\n34"), (ct, ch, 172.3, "MC-85a 172.3")]:
    ax.add_patch(Rectangle((L0, Y(t_ + h_)), d_, h_, fc="none", ec="#888", lw=0.9, ls="--", zorder=4))
    ax.text(L0 + d_ / 2, Y(t_ + h_ / 2), nm, fontsize=6.5, ha="center", va="center", color="#666", zorder=4)
for cy, d, ty, txt in [(hE, 30, hE, "Ø30  220V 인입 (4SQ x 2)"),
                       (hU, 50, hU - 18, "Ø50  MC3·MC4 인입 (16SQ x 6)"),
                       (hL, 50, hL + 18, "Ø50  MC1·MC2 인입 (16SQ x 6)")]:
    ax.add_patch(Circle((L0 + D/2, Y(cy)), (26 if d > 40 else 16.5), fc="none", ec="#999", lw=0.8, ls="--", zorder=6))
    ax.add_patch(Circle((L0 + D/2, Y(cy)), d/2, fc="white", ec=HOLE, lw=1.6, zorder=6))
    ax.plot([L0 + D/2 - d/2 - 6, L0 + D/2 + d/2 + 6], [Y(cy)] * 2, color=HOLE, lw=0.5, ls="-.", zorder=7)
    ax.plot([L0 + D/2] * 2, [Y(cy) - d/2 - 6, Y(cy) + d/2 + 6], color=HOLE, lw=0.5, ls="-.", zorder=7)
    ax.plot([L0 + D/2 + d/2 * 0.7, L0 + D + 10, L0 + D + 18], [Y(cy) + d/2 * 0.7 * (1 if ty < cy else -1 if ty > cy else 0), Y(ty), Y(ty)],
            color=HOLE, lw=0.7, zorder=7)
    ax.text(L0 + D + 21, Y(ty), txt, fontsize=7, color=HOLE, va="center", weight="bold")
for t_ in (130, 530):
    ax.add_patch(Rectangle((L0 + D - 5, Y(t_ + 20)), 10, 40, fc=HG, ec="black", lw=0.8, zorder=8))
    ax.text(L0 + D - 9, Y(t_), "경첩", fontsize=7.5, va="center", ha="right", weight="bold", color=HG, zorder=8)
hdim(L0, L0 + D, H + 25, "200", bg="white")
hdim(L0, L0 + D/2, -25, "100", bg="white")
o = [0, hE, hU, hL, H]
for a, b in zip(o[:-1], o[1:]): vdim(Y(a), Y(b), L0 - 15, f"{b-a:g}")
ax.text(L0 + D/2, -100, "[ 좌측면도 ]", ha="center", fontsize=11, weight="bold")

# ---- 밑면도 (정면도 우측 배치, 위쪽이 도어/정면) ----
BX, B0 = W + 140, -165                     # left x, front (door) edge y; back = B0 - D
ax.add_patch(Rectangle((BX, B0 - D), W, D, fc="#f4f4f4", ec="black", lw=2.2))
ax.text(BX - 4, B0 - 3, "정면\n(도어)", fontsize=6.5, va="top", ha="right", color="#555")
ax.text(BX - 4, B0 - D + 3, "후면\n(취부판)", fontsize=6.5, va="bottom", ha="right", color="#555")
for i, c0 in enumerate(mcc):
    c = BX + c0
    ax.add_patch(Rectangle((BX + mcx[i], B0 - D), cw, 172.3, fc="none", ec="#888", lw=0.9, ls="--", zorder=4))
    ax.add_patch(Circle((c, B0 - D/2), 26, fc="none", ec="#999", lw=0.8, ls="--", zorder=6))
    ax.add_patch(Circle((c, B0 - D/2), 25, fc="white", ec=HOLE, lw=1.6, zorder=6))
    ax.plot([c - 31, c + 31], [B0 - D/2] * 2, color=HOLE, lw=0.5, ls="-.", zorder=7)
    ax.plot([c, c], [B0 - D/2 - 31, B0 - D/2 + 31], color=HOLE, lw=0.5, ls="-.", zorder=7)
    ax.text(c + 20, B0 - D/2 + 22, "Ø50", fontsize=8, color=HOLE, weight="bold", zorder=7)
    ax.text(c, B0 - D/2 - 34, f"부하{i+1} 인출\n(16SQ x 3)", fontsize=6.5, color=HOLE, ha="center", va="top", zorder=7,
            bbox=dict(fc="#f4f4f4", ec="none", pad=0.2))
hp = [BX] + [BX + c for c in mcc] + [BX + W]
for a_, b_ in zip(hp[:-1], hp[1:]): hdim(a_, b_, B0 - D - 22, f"{b_-a_:g}", bg="white")
hdim(BX, BX + W, B0 + 18, "500", bg="white")
vdim(B0, B0 - D/2, BX + W + 20, "100", right=True)
vdim(B0, B0 - D, BX + W + 55, "200", right=True)
ax.text(BX + W/2, B0 - D - 45, "[ 밑면도 ]", ha="center", fontsize=11, weight="bold")
ax.text(BX + W/2, B0 - D - 68, "점선: MC-85a 설치 위치 (깊이 172.3)", fontsize=7, ha="center", va="top", color="#666")

ax.text(W/2 + 235, H + 60, "MC-85A 회로 및 배선도", ha="center", fontsize=15, weight="bold")
ax.text(W/2 + 235, -420, "※ 깊이 확인: 접촉기 172.3 / 박스 200 → 여유 27.7 (내부판 띄움 거리 포함 여부 확인 필요)",
        ha="center", fontsize=8.5, color="#c00000")
ax.text(W/2 + 235, -442, "단위: mm   |   표기: 가로 x 세로 x 깊이", ha="center", fontsize=8, color="#555")
import os; out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "drawings", "MC-85A_회로및배선도.png")
plt.savefig(out, dpi=200, bbox_inches="tight"); print(out)

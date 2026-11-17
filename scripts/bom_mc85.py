import csv, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "WenQuanYi Zen Hei"
import os; F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bom", "")
hdr = ["No", "구분", "품명", "규격", "수량", "단위", "용도 / 위치", "비고"]
rows = [
 ["외함", "하이박스", "500 x 600 x 200", "1", "EA", "외함", "경첩 좌 / 걸쇠 우, 깊이 여유 확인"],
 ["주요 기기", "전자접촉기 LS MC-85a", "3P, 코일 AC 220V", "4", "EA", "MC1~4", "94 x 140 x 172.3"],
 ["주요 기기", "Sonoff 4CH Pro R3", "4채널 릴레이", "1", "EA", "코일 ON/OFF 제어", "145 x 90 x 34"],
 ["주요 기기", "누전차단기 ELB 2P", "SIE-32 20/30A", "1", "EA", "제어전원 (Main 분전반)", "70 x 32 x 39"],
 ["타공 마감", "케이블 그랜드 PG36", "나사 47 / 너트 52", "6", "EA", "Ø50 타공 (좌측 2, 하단 4)", "고정용 아님, 마감용"],
 ["타공 마감", "케이블 그랜드 PG21", "나사 28.3 / 너트 33", "1", "EA", "Ø30 타공 (220V 인입)", ""],
 ["전선", "KIV 16SQ", "주회로", "24", "가닥", "SUB→MC 12 + MC→부하 12", "길이 현장 실측"],
 ["전선", "KIV 4SQ", "220V 인입", "2", "가닥", "Main 분전반 → ELB 1차측", "길이 현장 실측"],
 ["전선", "HIV 1.5SQ (갈색)", "제어 L", "3", "m", "ELB→Sonoff L, L→COM1~4", "예비 포함"],
 ["전선", "HIV 1.5SQ (청색)", "제어 N", "3", "m", "ELB→Sonoff N, A2 점프", "예비 포함"],
 ["전선", "HIV 1.5SQ (흑색)", "코일", "4", "m", "NO1~4 → MC1~4 A1", "예비 포함"],
 ["단자", "16SQ 링 압착단자", "접촉기 단자 나사에 맞춤", "24", "EA", "MC1~4 주단자 (IN/OUT)", "상대측(CB/부하) 별도"],
 ["단자", "4SQ 압착단자", "ELB 단자에 맞춤", "2", "EA", "ELB 1차측", "상대측 별도"],
 ["단자", "1.5SQ 핀단자", "", "20", "EA", "Sonoff 단자대, ELB 2차측", "예비 포함"],
 ["단자", "1.5SQ 링 압착단자", "코일 단자 나사에 맞춤", "15", "EA", "MC1~4 A1 / A2", "예비 포함"],
 ["부자재", "수축튜브 (적·흑·청 등)", "16SQ용", "1", "식", "16SQ 단자 상 구분", ""],
 ["부자재", "케이블 타이 / 새들", "", "1", "식", "배선 정리", ""],
 ["부자재", "마킹 라벨 / 마킹튜브", "", "1", "식", "MC1~4, 부하1~4, L1·L2·N", ""],
 ["부자재", "취부 나사", "내부판에 맞춤", "1", "식", "MC·Sonoff·ELB 고정", ""],
]
rows = [[str(i+1)] + r for i, r in enumerate(rows)]
with open(F + "물품표_MC-85A.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(hdr); w.writerows(rows)

fig, ax = plt.subplots(figsize=(16, 8.3)); ax.axis("off")
ax.set_title("MC-85A 회로 및 배선도 - 필요 물품 목록", fontsize=16, weight="bold", pad=14)
t = ax.table(cellText=rows, colLabels=hdr, loc="upper center", cellLoc="center",
             colWidths=[0.04, 0.08, 0.18, 0.15, 0.05, 0.05, 0.22, 0.2])
t.auto_set_font_size(False); t.set_fontsize(10); t.scale(1, 1.75)
groups = {"외함": "#ffffff", "주요 기기": "#eef6ff", "타공 마감": "#fff4e6", "전선": "#f2f2f2", "단자": "#eefae9", "부자재": "#ffffff"}
for (r, c), cell in t.get_celld().items():
    cell.set_edgecolor("#999")
    if r == 0: cell.set_facecolor("#2f5597"); cell.get_text().set_color("white"); cell.get_text().set_weight("bold")
    else:
        cell.set_facecolor(groups[rows[r-1][1]])
        if c in (2, 6, 7): cell.get_text().set_ha("left"); cell._loc = "left"
ax.text(0.0, 0.0, "※ 전선 길이는 SUB/Main 분전반 ~ 하이박스 거리 실측 후 확정  |  압착단자 크기는 실제 단자 나사 규격 확인 후 구매",
        transform=ax.transAxes, fontsize=9, color="#c00000")
plt.savefig(F + "물품표_MC-85A.png", dpi=170, bbox_inches="tight", facecolor="white")
print("ok")

#!/usr/bin/env python3
import os
import shutil
import sqlite3
import datetime as dt
from typing import List, Tuple

from ratings import open_db, init_db, handle_import_xlsx, RatingsRepository, TrueSkillService
import argparse

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'ratings.db')
XLSX_PATH = os.path.join(os.path.dirname(__file__), 'data', 'Oregon Arm Wrestling Rankings.xlsx')
OUT_PATH = os.path.join(os.path.dirname(__file__), 'test_results.txt')

# Utility

def reset_db():
	if os.path.exists(DB_PATH):
		os.remove(DB_PATH)
	conn = open_db(DB_PATH)
	init_db(conn)
	return conn


def import_seed(conn: sqlite3.Connection):
	args = argparse.Namespace(
		file=XLSX_PATH,
		men_rankings=None,
		women_rankings=None,
		men_weights=None,
		women_weights=None,
		mode='adhoc'
	)
	handle_import_xlsx(conn, args)


def conservative(mu: float, sigma: float) -> float:
	return mu - 3.0 * sigma


def fetch_rating(repo: RatingsRepository, name: str, hand: str) -> Tuple[float, float, float]:
	pid = repo.get_or_create_player(name)
	r = repo.get_rating(pid, hand, TrueSkillService().env)
	return float(r.mu), float(r.sigma), conservative(float(r.mu), float(r.sigma))


def fmt_change(label: str, name: str, b: float, a: float, width_mu=7, width_sig=5) -> str:
	return f"[{name} {b:{width_mu}.3f} -> {a:{width_mu}.3f}]"


def fmt_line_event(f, title: str, hand: str, winner: str, loser: str,
		before_w: Tuple[float,float,float], after_w: Tuple[float,float,float],
		before_l: Tuple[float,float,float], after_l: Tuple[float,float,float]) -> None:
	w_mu_b, w_sig_b, w_con_b = before_w
	w_mu_a, w_sig_a, w_con_a = after_w
	l_mu_b, l_sig_b, l_con_b = before_l
	l_mu_a, l_sig_a, l_con_a = after_l
	cons_part = f"[{winner} {w_con_b:7.3f} -> {w_con_a:7.3f}] [{loser} {l_con_b:7.3f} -> {l_con_a:7.3f}]"
	mu_part = f"[{winner} mu {w_mu_b:7.3f} -> {w_mu_a:7.3f}] [{loser} mu {l_mu_b:7.3f} -> {l_mu_a:7.3f}]"
	sig_part = f"[{winner} sigma {w_sig_b:5.3f} -> {w_sig_a:5.3f}] [{loser} sigma {l_sig_b:5.3f} -> {l_sig_a:5.3f}]"
	f.write(f"{title} | {cons_part} | {mu_part} | {sig_part}\n")


def do_tournament_pin(repo: RatingsRepository, logic: TrueSkillService, hand: str, winner: str, loser: str):
	from ratings import resolve_tournament
	resolve_tournament(repo, logic, name=f"TEST_TOURN_{winner}_vs_{loser}", date_iso=dt.date.today().isoformat(), hand=hand, placements=[winner, loser])


def do_supermatch(repo: RatingsRepository, logic: TrueSkillService, hand: str, a: str, b: str, aw: int, bw: int):
	from ratings import resolve_supermatch
	resolve_supermatch(repo, logic, name=f"TEST_SM_{a}_vs_{b}_{aw}-{bw}", date_iso=dt.date.today().isoformat(), hand=hand, a_name=a, b_name=b, a_wins=aw, b_wins=bw, best_of=(aw+bw if (aw+bw)>0 else None))


def run_pair_tests(f, conn: sqlite3.Connection, hand: str, a: str, b: str):
	repo = RatingsRepository(conn)
	logic = TrueSkillService()
	# Tournament pin: a beats b
	before_a = fetch_rating(repo, a, hand)
	before_b = fetch_rating(repo, b, hand)
	do_tournament_pin(repo, logic, hand, a, b)
	a1 = fetch_rating(repo, a, hand)
	b1 = fetch_rating(repo, b, hand)
	fmt_line_event(f, f"{a} pinned {b}", hand, a, b, before_a, a1, before_b, b1)
	# Close before reset
	try:
		conn.close()
	except Exception:
		pass
	# Reset and do b beats a
	conn2 = reset_db()
	import_seed(conn2)
	repo2 = RatingsRepository(conn2)
	logic2 = TrueSkillService()
	before_a = fetch_rating(repo2, a, hand)
	before_b = fetch_rating(repo2, b, hand)
	do_tournament_pin(repo2, logic2, hand, b, a)
	a2 = fetch_rating(repo2, a, hand)
	b2 = fetch_rating(repo2, b, hand)
	fmt_line_event(f, f"{b} pinned {a}", hand, b, a, before_b, b2, before_a, a2)
	try:
		conn2.close()
	except Exception:
		pass
	# Reset supermatch perfect a>b
	conn3 = reset_db()
	import_seed(conn3)
	repo3 = RatingsRepository(conn3)
	logic3 = TrueSkillService()
	before_a = fetch_rating(repo3, a, hand)
	before_b = fetch_rating(repo3, b, hand)
	do_supermatch(repo3, logic3, hand, a, b, 3, 0)
	a3 = fetch_rating(repo3, a, hand)
	b3 = fetch_rating(repo3, b, hand)
	fmt_line_event(f, f"{a} beat {b} 3-0", hand, a, b, before_a, a3, before_b, b3)
	try:
		conn3.close()
	except Exception:
		pass
	# Reset supermatch perfect b>a
	conn4 = reset_db()
	import_seed(conn4)
	repo4 = RatingsRepository(conn4)
	logic4 = TrueSkillService()
	before_a = fetch_rating(repo4, a, hand)
	before_b = fetch_rating(repo4, b, hand)
	do_supermatch(repo4, logic4, hand, b, a, 3, 0)
	a4 = fetch_rating(repo4, a, hand)
	b4 = fetch_rating(repo4, b, hand)
	fmt_line_event(f, f"{b} beat {a} 3-0", hand, b, a, before_b, b4, before_a, a4)
	try:
		conn4.close()
	except Exception:
		pass
	# Reset supermatch 3-2 a>b
	conn5 = reset_db()
	import_seed(conn5)
	repo5 = RatingsRepository(conn5)
	logic5 = TrueSkillService()
	before_a = fetch_rating(repo5, a, hand)
	before_b = fetch_rating(repo5, b, hand)
	do_supermatch(repo5, logic5, hand, a, b, 3, 2)
	a5 = fetch_rating(repo5, a, hand)
	b5 = fetch_rating(repo5, b, hand)
	fmt_line_event(f, f"{a} beat {b} 3-2", hand, a, b, before_a, a5, before_b, b5)
	try:
		conn5.close()
	except Exception:
		pass
	# Reset supermatch 3-2 b>a
	conn6 = reset_db()
	import_seed(conn6)
	repo6 = RatingsRepository(conn6)
	logic6 = TrueSkillService()
	before_a = fetch_rating(repo6, a, hand)
	before_b = fetch_rating(repo6, b, hand)
	do_supermatch(repo6, logic6, hand, b, a, 3, 2)
	a6 = fetch_rating(repo6, a, hand)
	b6 = fetch_rating(repo6, b, hand)
	fmt_line_event(f, f"{b} beat {a} 3-2", hand, b, a, before_b, b6, before_a, a6)
	try:
		conn6.close()
	except Exception:
		pass


def pick_examples(conn: sqlite3.Connection) -> Tuple[List[str], List[str]]:
	# Grab top-10 and bottom-10 by conservative as example pools
	cur = conn.cursor()
	cur.execute("SELECT p.name, (r.mu - 3*r.sigma) AS cons FROM ratings r JOIN players p ON p.id=r.player_id WHERE r.context_hand='RH' ORDER BY cons DESC LIMIT 10")
	high = [row[0] for row in cur.fetchall()]
	cur.execute("SELECT p.name, (r.mu - 3*r.sigma) AS cons FROM ratings r JOIN players p ON p.id=r.player_id WHERE r.context_hand='RH' ORDER BY cons ASC LIMIT 10")
	low = [row[0] for row in cur.fetchall()]
	# Fallbacks if empty
	return high or ["A","B","C","D","E"], low or ["U","V","W","X","Y"]


def main():
	# Start fresh to get pools
	conn0 = reset_db()
	import_seed(conn0)
	high, low = pick_examples(conn0)
	try:
		conn0.close()
	except Exception:
		pass
	pairs: List[Tuple[str,str]] = []
	# High vs high (adjacent): take pairs [0,1], [2,3]
	for i in range(0, min(4, len(high)-1), 2):
		pairs.append((high[i], high[i+1]))
	# Low vs low (adjacent)
	for i in range(0, min(4, len(low)-1), 2):
		pairs.append((low[i], low[i+1]))
	# Cross: top vs low
	if high and low:
		pairs.append((high[0], low[0]))
		pairs.append((low[0], high[0]))
	with open(OUT_PATH, 'w', encoding='utf-8') as f:
		f.write(f"Rating Tests Run: {dt.datetime.utcnow().isoformat()} UTC\n")
		f.write(f"Source: {os.path.relpath(XLSX_PATH)}\n\n")
		for hand in ("RH","LH"):
			for (a,b) in pairs:
				f.write(f"=== Scenario: {a} vs {b} ({hand}) ===\n")
				c = reset_db()
				import_seed(c)
				run_pair_tests(f, c, hand, a, b)
				f.write("\n")
	print(f"Wrote results to {OUT_PATH}")

if __name__ == '__main__':
	main() 
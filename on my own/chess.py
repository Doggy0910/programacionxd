#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AJEDREZ EN PYTHON  ·  motor propio + IA con 7 niveles + interfaz gráfica
=========================================================================
Sin dependencias externas (solo biblioteca estándar: tkinter).

Ejecutar:   python ajedrez.py
Test motor: python ajedrez.py --perft

Motor
  - Tablero mailbox 10x12, reglas completas (enroque, al paso, coronación,
    jaque mate, ahogado, 50 movimientos, triple repetición, material insuficiente)
  - Hash Zobrist incremental, evaluación incremental (material + tablas de casillas
    con interpolación medio juego / final, pareja de alfiles)
IA
  - Negamax + poda alfa-beta, profundización iterativa con control de tiempo
  - Tabla de transposición, PVS, ordenación MVV-LVA, killers, historial
  - Movimiento nulo, reducciones (LMR), extensión por jaque, búsqueda de quietud
  - Pequeño libro de aperturas, niveles con "ruido" para jugar de forma humana
"""
import random
import sys
import time
import threading
import queue

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, simpledialog
except ImportError:  # pragma: no cover
    tk = None

# ======================================================================
#  CONSTANTES Y TABLAS
# ======================================================================
OFF = 99
PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING = 1, 2, 3, 4, 5, 6
START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
FILES = "abcdefgh"

ROW = [0] * 120
COL = [0] * 120
SQUARES = []
for _r in range(8):
    for _c in range(8):
        _s = 21 + _r * 10 + _c
        SQUARES.append(_s)
        ROW[_s] = _r
        COL[_s] = _c


def sq_name(s):
    return FILES[COL[s]] + str(8 - ROW[s])


def name_sq(n):
    return 21 + (8 - int(n[1])) * 10 + FILES.index(n[0])


KN_D = (-21, -19, -12, -8, 8, 12, 19, 21)
BI_D = (-11, -9, 9, 11)
RO_D = (-10, -1, 1, 10)
KG_D = (-11, -10, -9, -1, 1, 9, 10, 11)

# derechos de enroque: 1=K blanco 2=Q blanco 4=k negro 8=q negro
CMASK = [15] * 120
CMASK[95] = 12
CMASK[98] = 14
CMASK[91] = 13
CMASK[25] = 3
CMASK[28] = 11
CMASK[21] = 7

# Zobrist
_rnd = random.Random(0xC0FFEE)
ZOB = [[_rnd.getrandbits(64) for _ in range(120)] for _ in range(13)]
ZSIDE = _rnd.getrandbits(64)
ZCASTLE = [_rnd.getrandbits(64) for _ in range(16)]
ZEP = [_rnd.getrandbits(64) for _ in range(120)]

# ---------- Evaluación: tablas (perspectiva blanca, fila 0 = fila 8) ----------
MAT = [0, 100, 320, 330, 500, 900, 0]
VAL = [0, 100, 320, 330, 500, 900, 20000]
PHASE = [0, 0, 1, 1, 2, 4, 0]

_PST = {
    1: [0, 0, 0, 0, 0, 0, 0, 0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5, 5, 10, 25, 25, 10, 5, 5,
        0, 0, 0, 20, 20, 0, 0, 0,
        5, -5, -10, 0, 0, -10, -5, 5,
        5, 10, 10, -20, -20, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0],
    2: [-50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20, 0, 0, 0, 0, -20, -40,
        -30, 0, 10, 15, 15, 10, 0, -30,
        -30, 5, 15, 20, 20, 15, 5, -30,
        -30, 0, 15, 20, 20, 15, 0, -30,
        -30, 5, 10, 15, 15, 10, 5, -30,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50],
    3: [-20, -10, -10, -10, -10, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10, 5, 0, 0, 0, 0, 5, -10,
        -20, -10, -10, -10, -10, -10, -10, -20],
    4: [0, 0, 0, 0, 0, 0, 0, 0,
        5, 10, 10, 10, 10, 10, 10, 5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        0, 0, 0, 5, 5, 0, 0, 0],
    5: [-20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -5, 0, 5, 5, 5, 5, 0, -5,
        0, 0, 5, 5, 5, 5, 0, -5,
        -10, 5, 5, 5, 5, 5, 0, -10,
        -10, 0, 5, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20],
    6: [-30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        20, 20, 0, 0, 0, 0, 20, 20,
        20, 30, 10, 0, 0, 10, 30, 20],
}
_KING_EG = [-50, -40, -30, -20, -20, -30, -40, -50,
            -30, -20, -10, 0, 0, -10, -20, -30,
            -30, -10, 20, 30, 30, 20, -10, -30,
            -30, -10, 30, 40, 40, 30, -10, -30,
            -30, -10, 30, 40, 40, 30, -10, -30,
            -30, -10, 20, 30, 30, 20, -10, -30,
            -30, -30, 0, 0, 0, 0, -30, -30,
            -50, -30, -30, -30, -30, -30, -30, -50]
_PAWN_ROW_EG = [0, 90, 60, 35, 20, 10, 0, 0]
_PST_EG = dict(_PST)
_PST_EG[6] = _KING_EG
_PST_EG[1] = [_PAWN_ROW_EG[r] for r in range(8) for _ in range(8)]

PMG = [[0] * 120 for _ in range(13)]
PEG = [[0] * 120 for _ in range(13)]
for _t in range(1, 7):
    for _r in range(8):
        for _c in range(8):
            _s = 21 + _r * 10 + _c
            _i = _r * 8 + _c
            _m = (7 - _r) * 8 + _c
            PMG[6 + _t][_s] = MAT[_t] + _PST[_t][_i]
            PMG[6 - _t][_s] = -(MAT[_t] + _PST[_t][_m])
            PEG[6 + _t][_s] = MAT[_t] + _PST_EG[_t][_i]
            PEG[6 - _t][_s] = -(MAT[_t] + _PST_EG[_t][_m])

INF = 10 ** 6
MATE = 100000
MATE_MAX = MATE - 1000
MAXPLY = 100


def uci(m):
    s = sq_name(m & 127) + sq_name((m >> 7) & 127)
    p = m >> 14
    return s + ("  nbrq"[p] if p else "")


# ======================================================================
#  POSICIÓN
# ======================================================================
class Position:
    def __init__(self, fen=START_FEN):
        self.set_fen(fen)

    # ---------------- FEN ----------------
    def set_fen(self, fen):
        b = [OFF] * 120
        for s in SQUARES:
            b[s] = 0
        parts = fen.split()
        r = c = 0
        for ch in parts[0]:
            if ch == '/':
                r += 1
                c = 0
            elif ch.isdigit():
                c += int(ch)
            else:
                t = ".pnbrqk".index(ch.lower())
                b[21 + r * 10 + c] = t if ch.isupper() else -t
                c += 1
        self.board = b
        self.side = 1 if parts[1] == 'w' else -1
        cs = parts[2] if len(parts) > 2 else "-"
        self.castle = (1 if 'K' in cs else 0) | (2 if 'Q' in cs else 0) | \
                      (4 if 'k' in cs else 0) | (8 if 'q' in cs else 0)
        self.ep = name_sq(parts[3]) if len(parts) > 3 and parts[3] != '-' else 0
        self.half = int(parts[4]) if len(parts) > 4 else 0
        self.full = int(parts[5]) if len(parts) > 5 else 1
        self.ksq = [0, 0]
        self.cnt = [0] * 13
        self.mg = self.eg = self.phase = 0
        h = 0
        for s in SQUARES:
            p = b[s]
            if p:
                self.cnt[p + 6] += 1
                self.mg += PMG[p + 6][s]
                self.eg += PEG[p + 6][s]
                self.phase += PHASE[abs(p)]
                h ^= ZOB[p + 6][s]
                if p == 6:
                    self.ksq[0] = s
                elif p == -6:
                    self.ksq[1] = s
        if self.side == -1:
            h ^= ZSIDE
        h ^= ZCASTLE[self.castle]
        if self.ep:
            h ^= ZEP[self.ep]
        self.hash = h
        self.stack = []
        self.nstack = []
        self.hist = [h]

    def fen(self):
        rows = []
        for r in range(8):
            e = 0
            s = ""
            for c in range(8):
                p = self.board[21 + r * 10 + c]
                if p == 0:
                    e += 1
                else:
                    if e:
                        s += str(e)
                        e = 0
                    ch = ".pnbrqk"[abs(p)]
                    s += ch.upper() if p > 0 else ch
            if e:
                s += str(e)
            rows.append(s)
        cs = "".join(ch for bit, ch in ((1, "K"), (2, "Q"), (4, "k"), (8, "q")) if self.castle & bit) or "-"
        ep = sq_name(self.ep) if self.ep else "-"
        return "%s %s %s %s %d %d" % ("/".join(rows), "w" if self.side == 1 else "b", cs, ep, self.half, self.full)

    def copy(self):
        n = Position.__new__(Position)
        n.board = self.board[:]
        n.side = self.side
        n.castle = self.castle
        n.ep = self.ep
        n.half = self.half
        n.full = self.full
        n.ksq = self.ksq[:]
        n.cnt = self.cnt[:]
        n.mg, n.eg, n.phase = self.mg, self.eg, self.phase
        n.hash = self.hash
        n.hist = self.hist[:]
        n.stack = []
        n.nstack = []
        return n

    # ---------------- ataques ----------------
    def attacked(self, s, by):
        b = self.board
        if by == 1:
            if b[s + 9] == 1 or b[s + 11] == 1:
                return True
        else:
            if b[s - 9] == -1 or b[s - 11] == -1:
                return True
        n = 2 * by
        for d in KN_D:
            if b[s + d] == n:
                return True
        k = 6 * by
        for d in KG_D:
            if b[s + d] == k:
                return True
        bi = 3 * by
        q = 5 * by
        for d in BI_D:
            t = s + d
            while b[t] == 0:
                t += d
            if b[t] == bi or b[t] == q:
                return True
        ro = 4 * by
        for d in RO_D:
            t = s + d
            while b[t] == 0:
                t += d
            if b[t] == ro or b[t] == q:
                return True
        return False

    def in_check(self):
        return self.attacked(self.ksq[0 if self.side == 1 else 1], -self.side)

    def illegal(self):
        """Tras make(): ¿el bando que movió dejó su rey en jaque?"""
        mover = -self.side
        return self.attacked(self.ksq[0 if mover == 1 else 1], self.side)

    def has_pieces(self, side):
        c = self.cnt
        if side == 1:
            return c[8] + c[9] + c[10] + c[11] > 0
        return c[4] + c[3] + c[2] + c[1] > 0

    # ---------------- generación ----------------
    def gen_moves(self, caps_only=False):
        b = self.board
        side = self.side
        ep = self.ep
        out = []
        add = out.append
        att = self.attacked
        for s in SQUARES:
            p = b[s]
            if p * side <= 0:
                continue
            t = p if p > 0 else -p
            if t == 1:
                d = -10 * side
                pr = 0 if side == 1 else 7
                to = s + d
                if b[to] == 0:
                    if ROW[to] == pr:
                        for pc in ((5,) if caps_only else (5, 4, 3, 2)):
                            add(s | to << 7 | pc << 14)
                    elif not caps_only:
                        add(s | to << 7)
                        if ROW[s] == (6 if side == 1 else 1) and b[to + d] == 0:
                            add(s | (to + d) << 7)
                for to in (s + d - 1, s + d + 1):
                    tp = b[to]
                    if tp == OFF:
                        continue
                    if tp * side < 0:
                        if ROW[to] == pr:
                            for pc in (5, 4, 3, 2):
                                add(s | to << 7 | pc << 14)
                        else:
                            add(s | to << 7)
                    elif ep and to == ep:
                        add(s | to << 7)
            elif t == 2 or t == 6:
                for d in (KN_D if t == 2 else KG_D):
                    to = s + d
                    tp = b[to]
                    if tp == 0:
                        if not caps_only:
                            add(s | to << 7)
                    elif tp != OFF and tp * side < 0:
                        add(s | to << 7)
                if t == 6 and not caps_only and self.castle:
                    cr = self.castle
                    if side == 1 and s == 95:
                        if cr & 1 and b[96] == 0 and b[97] == 0 and b[98] == 4 and \
                                not att(95, -1) and not att(96, -1) and not att(97, -1):
                            add(95 | 97 << 7)
                        if cr & 2 and b[94] == 0 and b[93] == 0 and b[92] == 0 and b[91] == 4 and \
                                not att(95, -1) and not att(94, -1) and not att(93, -1):
                            add(95 | 93 << 7)
                    elif side == -1 and s == 25:
                        if cr & 4 and b[26] == 0 and b[27] == 0 and b[28] == -4 and \
                                not att(25, 1) and not att(26, 1) and not att(27, 1):
                            add(25 | 27 << 7)
                        if cr & 8 and b[24] == 0 and b[23] == 0 and b[22] == 0 and b[21] == -4 and \
                                not att(25, 1) and not att(24, 1) and not att(23, 1):
                            add(25 | 23 << 7)
            else:
                dirs = BI_D if t == 3 else RO_D if t == 4 else KG_D
                for d in dirs:
                    to = s + d
                    while True:
                        tp = b[to]
                        if tp == 0:
                            if not caps_only:
                                add(s | to << 7)
                            to += d
                            continue
                        if tp != OFF and tp * side < 0:
                            add(s | to << 7)
                        break
        return out

    def legal_moves(self):
        res = []
        for m in self.gen_moves():
            self.make(m)
            if not self.illegal():
                res.append(m)
            self.unmake()
        return res

    def has_legal(self):
        for m in self.gen_moves():
            self.make(m)
            ok = not self.illegal()
            self.unmake()
            if ok:
                return True
        return False

    # ---------------- hacer / deshacer ----------------
    def make(self, m):
        b = self.board
        side = self.side
        frm = m & 127
        to = (m >> 7) & 127
        promo = m >> 14
        p = b[frm]
        cap = b[to]
        t = p if p > 0 else -p
        self.stack.append((m, cap, self.castle, self.ep, self.half, self.hash, self.mg, self.eg, self.phase))
        h = self.hash ^ ZSIDE ^ ZCASTLE[self.castle]
        if self.ep:
            h ^= ZEP[self.ep]
        mg = self.mg
        eg = self.eg
        ph = self.phase
        cnt = self.cnt
        if cap:
            i = cap + 6
            h ^= ZOB[i][to]
            mg -= PMG[i][to]
            eg -= PEG[i][to]
            ph -= PHASE[cap if cap > 0 else -cap]
            cnt[i] -= 1
        elif t == 1 and (to - frm) % 10:  # captura al paso
            cs = to + 10 * side
            i = 6 - side
            b[cs] = 0
            h ^= ZOB[i][cs]
            mg -= PMG[i][cs]
            eg -= PEG[i][cs]
            cnt[i] -= 1
        b[frm] = 0
        i = p + 6
        h ^= ZOB[i][frm]
        mg -= PMG[i][frm]
        eg -= PEG[i][frm]
        if promo:
            np_ = promo * side
            cnt[i] -= 1
            cnt[np_ + 6] += 1
            ph += PHASE[promo]
        else:
            np_ = p
        b[to] = np_
        j = np_ + 6
        h ^= ZOB[j][to]
        mg += PMG[j][to]
        eg += PEG[j][to]
        ep = 0
        if t == 1:
            if to - frm == 20 or frm - to == 20:
                ep = (frm + to) >> 1
        elif t == 6:
            self.ksq[0 if side == 1 else 1] = to
            rf = rt = 0
            if to - frm == 2:
                rf, rt = to + 1, to - 1
            elif frm - to == 2:
                rf, rt = to - 2, to + 1
            if rf:
                r = 4 * side
                k = r + 6
                b[rf] = 0
                b[rt] = r
                h ^= ZOB[k][rf] ^ ZOB[k][rt]
                mg += PMG[k][rt] - PMG[k][rf]
                eg += PEG[k][rt] - PEG[k][rf]
        self.castle &= CMASK[frm] & CMASK[to]
        h ^= ZCASTLE[self.castle]
        if ep:
            h ^= ZEP[ep]
        self.ep = ep
        self.half = 0 if (t == 1 or cap) else self.half + 1
        self.hash = h
        self.mg = mg
        self.eg = eg
        self.phase = ph
        self.side = -side
        if side == -1:
            self.full += 1
        self.hist.append(h)

    def unmake(self):
        m, cap, castle, ep, half, h, mg, eg, ph = self.stack.pop()
        self.hist.pop()
        b = self.board
        side = -self.side
        self.side = side
        if side == -1:
            self.full -= 1
        frm = m & 127
        to = (m >> 7) & 127
        promo = m >> 14
        p = b[to]
        cnt = self.cnt
        if promo:
            cnt[p + 6] -= 1
            p = side
            cnt[p + 6] += 1
        b[frm] = p
        b[to] = cap
        if cap:
            cnt[cap + 6] += 1
        t = p if p > 0 else -p
        if t == 1:
            if not cap and (to - frm) % 10 and to == ep:
                b[to + 10 * side] = -side
                cnt[6 - side] += 1
        elif t == 6:
            self.ksq[0 if side == 1 else 1] = frm
            if to - frm == 2:
                b[to + 1] = 4 * side
                b[to - 1] = 0
            elif frm - to == 2:
                b[to - 2] = 4 * side
                b[to + 1] = 0
        self.castle = castle
        self.ep = ep
        self.half = half
        self.hash = h
        self.mg = mg
        self.eg = eg
        self.phase = ph

    def make_null(self):
        self.nstack.append((self.ep, self.hash, self.half))
        h = self.hash ^ ZSIDE
        if self.ep:
            h ^= ZEP[self.ep]
        self.ep = 0
        self.hash = h
        self.side = -self.side
        self.half += 1
        self.hist.append(h)

    def unmake_null(self):
        self.ep, self.hash, self.half = self.nstack.pop()
        self.side = -self.side
        self.hist.pop()

    # ---------------- evaluación / tablas ----------------
    def evaluate(self):
        ph = self.phase if self.phase < 24 else 24
        sc = (self.mg * ph + self.eg * (24 - ph)) // 24
        c = self.cnt
        if c[9] >= 2:
            sc += 30
        if c[3] >= 2:
            sc -= 30
        return (sc if self.side == 1 else -sc) + 8

    def is_repetition(self):
        h = self.hash
        hist = self.hist
        n = len(hist)
        lim = min(self.half, n - 1)
        for i in range(4, lim + 1, 2):
            if hist[n - 1 - i] == h:
                return True
        return False

    def insufficient(self):
        c = self.cnt
        if c[7] or c[5] or c[10] or c[2] or c[11] or c[1]:
            return False
        return c[8] + c[9] + c[4] + c[3] <= 1


# ======================================================================
#  SAN
# ======================================================================
_PCH = {2: "N", 3: "B", 4: "R", 5: "Q", 6: "K"}


def san(pos, m, legal):
    b = pos.board
    frm = m & 127
    to = (m >> 7) & 127
    promo = m >> 14
    p = abs(b[frm])
    if p == 6 and abs(to - frm) == 2:
        s = "O-O" if to > frm else "O-O-O"
    else:
        cap = b[to] != 0 or (p == 1 and (to - frm) % 10 != 0)
        if p == 1:
            s = (FILES[COL[frm]] + "x" if cap else "") + sq_name(to)
            if promo:
                s += "=" + _PCH[promo]
        else:
            s = _PCH[p]
            amb = [o for o in legal if o != m and ((o >> 7) & 127) == to and abs(b[o & 127]) == p]
            if amb:
                if all(COL[o & 127] != COL[frm] for o in amb):
                    s += FILES[COL[frm]]
                elif all(ROW[o & 127] != ROW[frm] for o in amb):
                    s += str(8 - ROW[frm])
                else:
                    s += sq_name(frm)
            if cap:
                s += "x"
            s += sq_name(to)
    pos.make(m)
    if pos.in_check():
        s += "+" if pos.has_legal() else "#"
    pos.unmake()
    return s


def perft(pos, depth):
    if depth == 0:
        return 1
    n = 0
    for m in pos.gen_moves():
        pos.make(m)
        if not pos.illegal():
            n += perft(pos, depth - 1) if depth > 1 else 1
        pos.unmake()
    return n


# ======================================================================
#  MOTOR DE BÚSQUEDA
# ======================================================================
class Timeout(Exception):
    pass


EXACT, LOWER, UPPER = 0, 1, 2


def fmt_score(sc):
    if abs(sc) > MATE_MAX:
        n = (MATE - abs(sc) + 1) // 2
        return ("+M%d" if sc > 0 else "-M%d") % n
    return "%+.2f" % (sc / 100.0)


class Engine:
    def __init__(self):
        self.tt = {}
        self.killers = [[0, 0] for _ in range(MAXPLY + 4)]
        self.htab = [0] * 16384
        self.nodes = 0
        self.deadline = 0
        self.info = ""

    def stop(self):
        self.deadline = 0

    # ---- ordenación ----
    def order(self, pos, moves, tt_move, ply):
        b = pos.board
        k1, k2 = self.killers[ply]
        htab = self.htab
        scored = []
        for m in moves:
            frm = m & 127
            to = (m >> 7) & 127
            if m == tt_move:
                sc = 10 ** 7
            else:
                v = b[to]
                if v:
                    sc = 10 ** 6 + VAL[v if v > 0 else -v] * 16 - VAL[abs(b[frm])]
                elif (b[frm] == 1 or b[frm] == -1) and (to - frm) % 10:
                    sc = 10 ** 6 + 1500
                elif m >> 14:
                    sc = 9 * 10 ** 5 + (m >> 14)
                elif m == k1:
                    sc = 8 * 10 ** 5
                elif m == k2:
                    sc = 7 * 10 ** 5
                else:
                    sc = htab[m & 16383]
            scored.append((sc, m))
        scored.sort(reverse=True)
        return [m for _, m in scored]

    # ---- quietud ----
    def qsearch(self, pos, alpha, beta, ply):
        self.nodes += 1
        if not (self.nodes & 1023) and time.time() > self.deadline:
            raise Timeout
        stand = pos.evaluate()
        if ply >= MAXPLY or stand >= beta:
            return stand
        if stand > alpha:
            alpha = stand
        moves = pos.gen_moves(True)
        if not moves:
            return alpha
        b = pos.board
        for m in self.order(pos, moves, 0, ply):
            if not (m >> 14):
                v = abs(b[(m >> 7) & 127]) or 1
                if stand + VAL[v] + 200 < alpha:
                    continue
            pos.make(m)
            if pos.illegal():
                pos.unmake()
                continue
            sc = -self.qsearch(pos, -beta, -alpha, ply + 1)
            pos.unmake()
            if sc >= beta:
                return sc
            if sc > alpha:
                alpha = sc
        return alpha

    # ---- búsqueda principal ----
    def negamax(self, pos, depth, alpha, beta, ply, null_ok=True):
        self.nodes += 1
        if not (self.nodes & 1023) and time.time() > self.deadline:
            raise Timeout
        if ply:
            if pos.half >= 100 or pos.is_repetition():
                return 0
            alpha = max(alpha, -MATE + ply)
            beta = min(beta, MATE - ply - 1)
            if alpha >= beta:
                return alpha
        if ply >= MAXPLY:
            return pos.evaluate()
        in_check = pos.in_check()
        if in_check:
            depth += 1
        if depth <= 0:
            return self.qsearch(pos, alpha, beta, ply)
        pv = beta - alpha > 1
        key = pos.hash
        tt_move = 0
        e = self.tt.get(key)
        if e:
            ed, flag, esc, tt_move = e
            if ed >= depth and ply:
                if esc > MATE_MAX:
                    esc -= ply
                elif esc < -MATE_MAX:
                    esc += ply
                if flag == EXACT:
                    return esc
                if flag == LOWER:
                    if esc > alpha:
                        alpha = esc
                elif esc < beta:
                    beta = esc
                if alpha >= beta:
                    return esc
        if not pv and not in_check and abs(beta) < MATE_MAX:
            if depth <= 3:
                static = pos.evaluate()
                if static - 130 * depth >= beta:
                    return static
            if null_ok and depth >= 3 and pos.has_pieces(pos.side):
                pos.make_null()
                sc = -self.negamax(pos, depth - 3, -beta, -beta + 1, ply + 1, False)
                pos.unmake_null()
                if sc >= beta:
                    return beta
        b = pos.board
        a0 = alpha
        best = -INF
        best_move = 0
        legal = 0
        for m in self.order(pos, pos.gen_moves(), tt_move, ply):
            frm = m & 127
            to = (m >> 7) & 127
            quiet = not b[to] and not (m >> 14) and not (abs(b[frm]) == 1 and (to - frm) % 10)
            pos.make(m)
            if pos.illegal():
                pos.unmake()
                continue
            legal += 1
            if legal == 1:
                sc = -self.negamax(pos, depth - 1, -beta, -alpha, ply + 1)
            else:
                red = 0
                if depth >= 3 and legal > 4 and quiet and not in_check:
                    red = 2 if legal > 10 else 1
                    if pos.in_check():
                        red = 0
                sc = -self.negamax(pos, depth - 1 - red, -alpha - 1, -alpha, ply + 1)
                if sc > alpha:
                    sc = -self.negamax(pos, depth - 1, -beta, -alpha, ply + 1)
            pos.unmake()
            if sc > best:
                best = sc
                best_move = m
                if sc > alpha:
                    alpha = sc
                    if alpha >= beta:
                        if quiet:
                            kl = self.killers[ply]
                            if kl[0] != m:
                                kl[1] = kl[0]
                                kl[0] = m
                            self.htab[m & 16383] += depth * depth
                        break
        if legal == 0:
            return -MATE + ply if in_check else 0
        flag = UPPER if best <= a0 else (LOWER if best >= beta else EXACT)
        st = best
        if st > MATE_MAX:
            st += ply
        elif st < -MATE_MAX:
            st -= ply
        self.tt[key] = (depth, flag, st, best_move)
        return best

    def search_root(self, pos, depth, root):
        alpha = -INF
        beta = INF
        best = -INF
        best_move = root[0]
        for i, m in enumerate(root):
            pos.make(m)
            if i == 0:
                sc = -self.negamax(pos, depth - 1, -beta, -alpha, 1)
            else:
                sc = -self.negamax(pos, depth - 1, -alpha - 1, -alpha, 1)
                if sc > alpha:
                    sc = -self.negamax(pos, depth - 1, -beta, -alpha, 1)
            pos.unmake()
            if sc > best:
                best = sc
                best_move = m
                if sc > alpha:
                    alpha = sc
        return best_move, best

    # ---- API pública ----
    def think(self, pos, depth, tlimit, noise=0.0):
        """Devuelve dict(move, score, depth, nodes) o None si no hay jugadas."""
        pos = pos.copy()
        root = pos.legal_moves()
        if not root:
            return None
        if len(self.tt) > 700000:
            self.tt.clear()
        self.nodes = 0
        t0 = time.time()
        self.deadline = t0 + tlimit
        self.killers = [[0, 0] for _ in range(MAXPLY + 4)]
        if len(root) == 1:
            return dict(move=root[0], score=0, depth=0, nodes=0)
        root = self.order(pos, root, 0, 0)

        if noise > 0:  # niveles bajos: evalúa cada jugada y añade ruido gaussiano
            scored = []
            try:
                for m in root:
                    pos.make(m)
                    sc = -self.negamax(pos, max(depth - 1, 0), -INF, INF, 1)
                    pos.unmake()
                    scored.append((sc + (random.gauss(0, noise) if abs(sc) < MATE_MAX else 0), sc, m))
            except Timeout:
                pass
            if not scored:
                return dict(move=root[0], score=0, depth=0, nodes=self.nodes)
            _, sc, m = max(scored)
            return dict(move=m, score=sc, depth=depth, nodes=self.nodes)

        best, bs, done = root[0], 0, 0
        for d in range(1, depth + 1):
            try:
                mv, sc = self.search_root(pos, d, root)
            except Timeout:
                break
            best, bs, done = mv, sc, d
            root.remove(mv)
            root.insert(0, mv)
            self.info = "prof. %d · %s · %dk nodos" % (d, fmt_score(sc), self.nodes // 1000)
            if abs(sc) > MATE_MAX:
                break
            if time.time() - t0 > tlimit * 0.4:
                break
        return dict(move=best, score=bs, depth=done, nodes=self.nodes)


# ======================================================================
#  NIVELES Y LIBRO
# ======================================================================
LEVELS = [
    ("1 · Principiante", dict(depth=1, time=1.0, noise=260, rand=0.25, book=False)),
    ("2 · Fácil",        dict(depth=2, time=2.0, noise=130, rand=0.06, book=False)),
    ("3 · Aficionado",   dict(depth=3, time=3.0, noise=45,  rand=0.0,  book=True)),
    ("4 · Intermedio",   dict(depth=4, time=3.0, noise=0,   rand=0.0,  book=True)),
    ("5 · Avanzado",     dict(depth=6, time=6.0, noise=0,   rand=0.0,  book=True)),
    ("6 · Experto",      dict(depth=8, time=12.0, noise=0,  rand=0.0,  book=True)),
    ("7 · Maestro",      dict(depth=14, time=25.0, noise=0, rand=0.0,  book=True)),
]

BOOK = {
    (): ["e2e4", "d2d4", "g1f3", "c2c4"],
    ("e2e4",): ["e7e5", "c7c5", "e7e6", "c7c6"],
    ("e2e4", "e7e5"): ["g1f3", "f1c4", "b1c3"],
    ("e2e4", "e7e5", "g1f3"): ["b8c6", "g8f6"],
    ("e2e4", "e7e5", "g1f3", "b8c6"): ["f1b5", "f1c4", "d2d4"],
    ("e2e4", "c7c5"): ["g1f3", "b1c3"],
    ("e2e4", "c7c5", "g1f3"): ["d7d6", "b8c6", "e7e6"],
    ("e2e4", "e7e6"): ["d2d4"],
    ("e2e4", "e7e6", "d2d4"): ["d7d5"],
    ("e2e4", "c7c6"): ["d2d4"],
    ("e2e4", "c7c6", "d2d4"): ["d7d5"],
    ("d2d4",): ["d7d5", "g8f6"],
    ("d2d4", "d7d5"): ["c2c4", "g1f3"],
    ("d2d4", "d7d5", "c2c4"): ["e7e6", "c7c6"],
    ("d2d4", "g8f6"): ["c2c4", "g1f3"],
    ("d2d4", "g8f6", "c2c4"): ["e7e6", "g7g6"],
    ("g1f3",): ["d7d5", "g8f6"],
    ("c2c4",): ["e7e5", "g8f6", "c7c5"],
}


def pick_move(engine, pos, cfg, uci_hist=None):
    """Elige jugada según el nivel (libro -> error aleatorio -> búsqueda)."""
    legal = pos.legal_moves()
    if not legal:
        return None
    if cfg["book"] and uci_hist is not None and tuple(uci_hist) in BOOK:
        cands = [m for m in legal if uci(m) in BOOK[tuple(uci_hist)]]
        if cands:
            return dict(move=random.choice(cands), score=0, depth=0, nodes=0, book=True)
    if cfg["rand"] and random.random() < cfg["rand"]:
        return dict(move=random.choice(legal), score=0, depth=0, nodes=0)
    return engine.think(pos, cfg["depth"], cfg["time"], cfg["noise"])


# ======================================================================
#  INTERFAZ GRÁFICA
# ======================================================================
GLYPH = {1: "\u265F", 2: "\u265E", 3: "\u265D", 4: "\u265C", 5: "\u265B", 6: "\u265A"}
NAMES = {5: "Dama", 4: "Torre", 3: "Alfil", 2: "Caballo"}

LIGHT, DARK = "#f0d9b5", "#b58863"
LAST_L, LAST_D = "#f7ec74", "#dac33b"
SEL_C, CHK_C = "#8fd18f", "#ff6b6b"
BG, FG = "#2b2b2b", "#eeeeee"


class ChessApp:
    SQ = 76

    def __init__(self, root):
        self.root = root
        root.title("Ajedrez en Python · motor propio con IA")
        root.configure(bg=BG)
        root.resizable(False, False)
        if sys.platform.startswith("win"):
            self.font = "Segoe UI Symbol"
        elif sys.platform == "darwin":
            self.font = "Apple Symbols"
        else:
            self.font = "DejaVu Sans"
        self.q = queue.Queue()
        self.engine = Engine()
        self.sid = 0
        self.thinking = False
        self.flipped = False
        self.build_ui()
        self.new_game()

    # ---------- UI ----------
    def build_ui(self):
        SQ = self.SQ
        main = tk.Frame(self.root, bg=BG)
        main.pack(padx=12, pady=12)
        self.canvas = tk.Canvas(main, width=SQ * 8, height=SQ * 8, highlightthickness=0, bg=BG)
        self.canvas.grid(row=0, column=0, rowspan=2)
        self.canvas.bind("<Button-1>", self.on_click)

        side = tk.Frame(main, bg=BG)
        side.grid(row=0, column=1, sticky="n", padx=(14, 0))
        tk.Label(side, text="♞  AJEDREZ", font=("Helvetica", 18, "bold"), bg=BG, fg=FG).pack(anchor="w")

        tk.Label(side, text="Nivel de la IA", bg=BG, fg="#aaa").pack(anchor="w", pady=(10, 0))
        self.level_var = tk.StringVar(value=LEVELS[3][0])
        ttk.Combobox(side, textvariable=self.level_var, values=[n for n, _ in LEVELS],
                     state="readonly", width=24).pack(anchor="w")

        tk.Label(side, text="Modo (se aplica en «Nueva partida»)", bg=BG, fg="#aaa").pack(anchor="w", pady=(8, 0))
        self.mode_var = tk.StringVar(value="Juego con Blancas")
        ttk.Combobox(side, textvariable=self.mode_var, state="readonly", width=24,
                     values=["Juego con Blancas", "Juego con Negras", "Dos jugadores"]).pack(anchor="w")

        bf = tk.Frame(side, bg=BG)
        bf.pack(anchor="w", pady=10)
        for i, (txt, cmd) in enumerate([
            ("Nueva partida", self.new_game), ("Deshacer", self.undo),
            ("Pista", self.hint_cmd), ("Girar", self.flip),
            ("Copiar FEN", self.copy_fen), ("Cargar FEN", self.load_fen)]):
            ttk.Button(bf, text=txt, command=cmd, width=12).grid(row=i // 2, column=i % 2, padx=2, pady=2)

        self.status = tk.StringVar()
        tk.Label(side, textvariable=self.status, bg=BG, fg="#ffd479", font=("Helvetica", 11, "bold"),
                 wraplength=250, justify="left").pack(anchor="w", pady=(4, 0))
        self.info_var = tk.StringVar()
        tk.Label(side, textvariable=self.info_var, bg=BG, fg="#9ad", wraplength=250,
                 justify="left").pack(anchor="w")

        tk.Label(side, text="Jugadas", bg=BG, fg="#aaa").pack(anchor="w", pady=(8, 0))
        tf = tk.Frame(side)
        tf.pack(anchor="w")
        self.movebox = tk.Text(tf, width=30, height=16, bg="#1e1e1e", fg=FG, font=("Courier", 11),
                               state="disabled", relief="flat")
        sb = ttk.Scrollbar(tf, command=self.movebox.yview)
        self.movebox.configure(yscrollcommand=sb.set)
        self.movebox.pack(side="left")
        sb.pack(side="left", fill="y")

    # ---------- partida ----------
    def cfg(self):
        for n, c in LEVELS:
            if n == self.level_var.get():
                return c
        return LEVELS[3][1]

    def new_game(self, fen=None):
        self.cancel_search()
        mode = self.mode_var.get()
        self.human = {1: True, -1: True}
        if mode == "Juego con Blancas":
            self.human[-1] = False
            self.flipped = False
        elif mode == "Juego con Negras":
            self.human[1] = False
            self.flipped = True
        self.pos = Position(fen) if fen else Position()
        self.standard = fen is None
        self.uci_hist = []
        self.san_list = []
        self.last_moves = []
        self.selected = None
        self.hint = None
        self.game_over = False
        self.engine = Engine()
        self.legal = self.pos.legal_moves()
        self.info_var.set("")
        self.refresh_all()
        self.after_move()

    def cancel_search(self):
        self.sid += 1
        self.thinking = False
        self.engine.stop()

    def flip(self):
        self.flipped = not self.flipped
        self.draw()

    def copy_fen(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.pos.fen())
        self.info_var.set("FEN copiado al portapapeles")

    def load_fen(self):
        f = simpledialog.askstring("Cargar FEN", "Pega una posición en notación FEN:", parent=self.root)
        if f:
            try:
                p = Position(f.strip())
                if p.ksq[0] == 0 or p.ksq[1] == 0:
                    raise ValueError
                self.new_game(f.strip())
            except Exception:
                messagebox.showerror("FEN no válido", "No se pudo leer esa posición.")

    def refresh_all(self):
        self.update_movelist()
        self.draw()

    def update_movelist(self):
        t = self.movebox
        t.configure(state="normal")
        t.delete("1.0", "end")
        for i in range(0, len(self.san_list), 2):
            line = "%3d. %-9s" % (i // 2 + 1, self.san_list[i])
            if i + 1 < len(self.san_list):
                line += " " + self.san_list[i + 1]
            t.insert("end", line + "\n")
        t.see("end")
        t.configure(state="disabled")

    # ---------- dibujo ----------
    def to_xy(self, r, c):
        if self.flipped:
            return (7 - c) * self.SQ, (7 - r) * self.SQ
        return c * self.SQ, r * self.SQ

    def draw(self):
        c = self.canvas
        c.delete("all")
        SQ = self.SQ
        b = self.pos.board
        chk = self.pos.ksq[0 if self.pos.side == 1 else 1] if self.pos.in_check() else None
        last = set()
        if self.last_moves:
            last = set(self.last_moves[-1])
        targets = set()
        if self.selected is not None:
            targets = {(m >> 7) & 127 for m in self.legal if (m & 127) == self.selected}
        for r in range(8):
            for col in range(8):
                s = 21 + r * 10 + col
                x, y = self.to_xy(r, col)
                light = (r + col) % 2 == 0
                color = LIGHT if light else DARK
                if s in last:
                    color = LAST_L if light else LAST_D
                if s == self.selected:
                    color = SEL_C
                if s == chk:
                    color = CHK_C
                c.create_rectangle(x, y, x + SQ, y + SQ, fill=color, width=0)
                tc = DARK if light else LIGHT
                dr, dc = int(y // SQ), int(x // SQ)
                if dc == 0:
                    c.create_text(x + 6, y + 8, text=str(8 - r), fill=tc, font=("Helvetica", 9, "bold"))
                if dr == 7:
                    c.create_text(x + SQ - 7, y + SQ - 8, text=FILES[col], fill=tc, font=("Helvetica", 9, "bold"))
        for s in targets:
            x, y = self.to_xy(ROW[s], COL[s])
            if b[s]:
                c.create_oval(x + 4, y + 4, x + SQ - 4, y + SQ - 4, outline="#3a8f3a", width=5)
            else:
                c.create_oval(x + SQ / 2 - 9, y + SQ / 2 - 9, x + SQ / 2 + 9, y + SQ / 2 + 9,
                              fill="#3a8f3a", outline="")
        fs = int(SQ * 0.72)
        for s in SQUARES:
            p = b[s]
            if not p:
                continue
            x, y = self.to_xy(ROW[s], COL[s])
            cx, cy = x + SQ / 2, y + SQ / 2 + 2
            ch = GLYPH[abs(p)]
            fill, edge = ("#ffffff", "#1a1a1a") if p > 0 else ("#161616", "#c8c8c8")
            for dx, dy in ((-1.5, 0), (1.5, 0), (0, -1.5), (0, 1.5), (-1, -1), (1, 1), (-1, 1), (1, -1)):
                c.create_text(cx + dx, cy + dy, text=ch, font=(self.font, fs), fill=edge)
            c.create_text(cx, cy, text=ch, font=(self.font, fs), fill=fill)
        if self.hint:
            f, t = self.hint
            x1, y1 = self.to_xy(ROW[f], COL[f])
            x2, y2 = self.to_xy(ROW[t], COL[t])
            c.create_line(x1 + SQ / 2, y1 + SQ / 2, x2 + SQ / 2, y2 + SQ / 2, arrow=tk.LAST,
                          width=8, fill="#3a7bd5", arrowshape=(18, 20, 8), capstyle="round")

    # ---------- interacción ----------
    def on_click(self, ev):
        if self.thinking or self.game_over or not self.human[self.pos.side]:
            return
        SQ = self.SQ
        dc, dr = int(ev.x // SQ), int(ev.y // SQ)
        if not (0 <= dc < 8 and 0 <= dr < 8):
            return
        r, c = (7 - dr, 7 - dc) if self.flipped else (dr, dc)
        s = 21 + r * 10 + c
        self.hint = None
        if self.selected is not None:
            ms = [m for m in self.legal if (m & 127) == self.selected and ((m >> 7) & 127) == s]
            if ms:
                if len(ms) > 1:
                    pv = self.ask_promo()
                    ms = [m for m in ms if (m >> 14) == pv]
                self.play(ms[0])
                return
        if self.pos.board[s] * self.pos.side > 0:
            self.selected = None if self.selected == s else s
        else:
            self.selected = None
        self.draw()

    def ask_promo(self):
        win = tk.Toplevel(self.root)
        win.title("Coronación")
        win.transient(self.root)
        win.resizable(False, False)
        res = {"v": 5}

        def pick(v):
            res["v"] = v
            win.destroy()

        tk.Label(win, text="Elige la pieza:", font=("Helvetica", 12)).pack(padx=20, pady=6)
        for v in (5, 4, 3, 2):
            tk.Button(win, text="%s  %s" % (GLYPH[v], NAMES[v]), font=(self.font, 16), width=12,
                      command=lambda v=v: pick(v)).pack(padx=10, pady=2)
        win.update_idletasks()
        x = self.root.winfo_x() + 200
        y = self.root.winfo_y() + 150
        win.geometry("+%d+%d" % (x, y))
        win.grab_set()
        self.root.wait_window(win)
        return res["v"]

    def play(self, m):
        s = san(self.pos, m, self.legal)
        self.san_list.append(s)
        self.uci_hist.append(uci(m))
        self.last_moves.append((m & 127, (m >> 7) & 127))
        self.pos.make(m)
        self.selected = None
        self.hint = None
        self.legal = self.pos.legal_moves()
        self.refresh_all()
        self.after_move()

    def after_move(self):
        p = self.pos
        msg = None
        if not self.legal:
            if p.in_check():
                msg = "¡Jaque mate! Ganan las %s." % ("Blancas" if p.side == -1 else "Negras")
            else:
                msg = "Tablas por rey ahogado."
        elif p.insufficient():
            msg = "Tablas por material insuficiente."
        elif p.half >= 100:
            msg = "Tablas por la regla de los 50 movimientos."
        elif p.hist.count(p.hash) >= 3:
            msg = "Tablas por triple repetición."
        if msg:
            self.game_over = True
            self.status.set(msg)
            self.root.after(250, lambda: messagebox.showinfo("Fin de la partida", msg))
            return
        turno = "Blancas" if p.side == 1 else "Negras"
        self.status.set("Turno: %s%s" % (turno, "  ¡JAQUE!" if p.in_check() else ""))
        if not self.human[p.side]:
            self.start_ai("move")

    # ---------- IA en hilo ----------
    def start_ai(self, kind):
        self.thinking = True
        self.sid += 1
        sid = self.sid
        posc = self.pos.copy()
        cfg = dict(self.cfg()) if kind == "move" else dict(depth=6, time=3.0, noise=0, rand=0, book=False)
        hist = list(self.uci_hist) if self.standard else None
        eng = Engine()
        self.engine = eng
        self.status.set("Pensando…" if kind == "move" else "Buscando pista…")

        def work():
            try:
                res = pick_move(eng, posc, cfg, hist)
            except Exception as ex:  # pragma: no cover
                res = None
                print("Error IA:", ex)
            self.q.put((sid, kind, res))

        threading.Thread(target=work, daemon=True).start()
        self.root.after(80, self.poll)

    def poll(self):
        if not self.thinking:
            return
        try:
            sid, kind, res = self.q.get_nowait()
        except queue.Empty:
            if self.engine.info:
                self.info_var.set(self.engine.info)
            self.root.after(80, self.poll)
            return
        if sid != self.sid:
            self.root.after(80, self.poll)
            return
        self.thinking = False
        if not res:
            return
        m = res["move"]
        sc = res["score"] * self.pos.side  # perspectiva blanca
        if res.get("book"):
            self.info_var.set("Libro de aperturas")
        else:
            self.info_var.set("prof. %d · eval %s · %dk nodos" % (res["depth"], fmt_score(sc), res["nodes"] // 1000))
        if kind == "move":
            self.play(m)
        else:
            self.hint = (m & 127, (m >> 7) & 127)
            self.status.set("Pista mostrada (flecha azul)")
            self.draw()

    def hint_cmd(self):
        if self.thinking or self.game_over or not self.human[self.pos.side]:
            return
        self.start_ai("hint")

    def undo(self):
        if not self.san_list:
            return
        self.cancel_search()
        self.game_over = False
        while self.san_list:
            self.pos.unmake()
            self.san_list.pop()
            self.uci_hist.pop()
            self.last_moves.pop()
            if self.human[self.pos.side]:
                break
        self.selected = None
        self.hint = None
        self.legal = self.pos.legal_moves()
        self.refresh_all()
        self.after_move()


# ======================================================================
def run_perft():
    tests = [
        ("Posición inicial", START_FEN, 4, 197281),
        ("Kiwipete", "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1", 3, 97862),
        ("Final (pos. 3)", "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1", 4, 43238),
        ("Pos. 4", "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1", 3, 9467),
        ("Pos. 5", "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8", 3, 62379),
    ]
    ok = True
    for name, fen, d, exp in tests:
        t = time.time()
        n = perft(Position(fen), d)
        good = n == exp
        ok &= good
        print("%-18s perft(%d)=%d  esperado=%d  %s  (%.1fs)" % (name, d, n, exp, "OK" if good else "FALLO", time.time() - t))
    print("TODO CORRECTO" if ok else "HAY ERRORES")


def main():
    if "--perft" in sys.argv:
        run_perft()
        return
    if tk is None:
        print("Tkinter no está instalado. En Linux: sudo apt install python3-tk")
        return
    root = tk.Tk()
    ChessApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
(set-logic QF_LIA)
(set-info :source |
Alberto Griggio

|)
(set-info :smt-lib-version 2.0)
(set-info :category "random")
(set-info :status unsat)
(declare-fun x0 () Int)
(declare-fun x1 () Int)
(declare-fun x2 () Int)
(declare-fun x3 () Int)
(declare-fun x4 () Int)
(declare-fun x5 () Int)
(declare-fun x6 () Int)
(declare-fun x7 () Int)
(declare-fun x8 () Int)
(declare-fun x9 () Int)
(assert (let ((?v_14 (* 0 x1)) (?v_3 (* 0 x2)) (?v_19 (* 0 x7)) (?v_0 (* 0 x0)) (?v_11 (* 1 x8)) (?v_25 (* 1 x3)) (?v_2 (* 0 x8)) (?v_26 (* 1 x7)) (?v_4 (* 1 x6)) (?v_7 (* 1 x9)) (?v_20 (* 0 x6)) (?v_6 (* 0 x9)) (?v_8 (* 0 x4)) (?v_18 (* 1 x0)) (?v_16 (* 0 x5)) (?v_12 (* 0 x3)) (?v_24 (* 1 x5)) (?v_13 (* (- 1) x9)) (?v_5 (* (- 1) x6)) (?v_1 (* (- 1) x8)) (?v_23 (* (- 1) x3)) (?v_9 (* (- 1) x5)) (?v_10 (* (- 1) x0)) (?v_15 (* (- 1) x7)) (?v_21 (* (- 1) x2)) (?v_17 (* (- 1) x4)) (?v_22 (* (- 1) x1))) (and (<= (+ ?v_14 ?v_0 (* 1 x4) ?v_13 ?v_5 ?v_3 ?v_19 ?v_2 ?v_0 ?v_0) (- 1)) (<= (+ ?v_11 ?v_1 ?v_0 ?v_1 ?v_25 ?v_23 ?v_2 ?v_2 ?v_8 ?v_2) 1) (<= (+ ?v_26 ?v_4 ?v_7 ?v_9 ?v_20 ?v_10 ?v_6 ?v_0 ?v_3 ?v_3) 0) (<= (+ ?v_4 ?v_5 ?v_15 ?v_6 ?v_6 ?v_7 ?v_0 ?v_3 ?v_3 ?v_8) 1) (<= (+ ?v_18 ?v_5 ?v_3 ?v_9 ?v_12 ?v_3 ?v_3 ?v_16 ?v_9 ?v_10) 1) (<= (+ ?v_0 ?v_0 ?v_2 ?v_11 ?v_12 ?v_7 ?v_13 ?v_14 ?v_7 ?v_15) 0) (<= (+ ?v_16 ?v_8 ?v_2 ?v_16 ?v_6 ?v_4 ?v_12 ?v_21 ?v_17 ?v_2) 0) (<= (+ ?v_11 ?v_12 ?v_12 ?v_17 ?v_5 ?v_24 ?v_14 ?v_3 ?v_0 ?v_12) 0) (<= (+ ?v_16 ?v_14 ?v_18 ?v_19 ?v_16 ?v_4 ?v_3 ?v_10 ?v_10 ?v_19) (- 1)) (<= (+ ?v_3 ?v_12 ?v_14 ?v_4 ?v_0 ?v_20 ?v_0 ?v_14 ?v_16 ?v_12) (- 1)) (<= (+ ?v_4 ?v_21 ?v_8 ?v_9 ?v_22 (* 1 x2) ?v_11 ?v_9 ?v_14 ?v_13) 0) (<= (+ ?v_0 ?v_0 ?v_12 ?v_2 ?v_9 ?v_6 ?v_2 ?v_17 ?v_8 ?v_16) 0) (<= (+ ?v_19 ?v_22 ?v_6 ?v_14 ?v_5 ?v_1 ?v_21 ?v_23 ?v_10 ?v_6) 1) (<= (+ ?v_11 ?v_20 ?v_1 ?v_3 ?v_12 ?v_12 ?v_16 ?v_18 ?v_21 ?v_24) 0) (<= (+ ?v_6 ?v_24 ?v_25 ?v_14 ?v_23 ?v_0 ?v_11 ?v_9 ?v_2 ?v_26) (- 1)))))
(check-sat)
(exit)


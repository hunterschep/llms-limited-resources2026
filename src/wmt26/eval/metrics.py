from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Iterable


def normalize_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value).strip())


def exact_accuracy(predictions: Iterable[object], references: Iterable[object]) -> float:
    pairs = list(zip(predictions, references))
    if not pairs:
        return 0.0
    correct = sum(normalize_text(p) == normalize_text(r) for p, r in pairs)
    return correct / len(pairs)


def normalize_choice_answer(value: object) -> str:
    text = normalize_text(value).strip()
    if not text:
        return ""
    text = text.replace("`", "").strip()
    answer_pattern = re.compile(
        r"(?:answer|option|choice|відповідь|відповiдь|варіант|вариант)\s*(?:is|=|:|-)?\s*([A-Za-zА-Яа-яІіЇїЄєҐґ]|\d+)",
        re.IGNORECASE,
    )
    match = answer_pattern.search(text)
    if match:
        token = match.group(1)
    else:
        first_line = next((line.strip() for line in str(value).splitlines() if line.strip()), text)
        lead = re.match(r"^\s*[\(\[]?([A-Za-zА-Яа-яІіЇїЄєҐґ]|\d+)[\)\]\.\:,\s]*", first_line)
        token = lead.group(1) if lead else text
    return token.strip().strip(".:;,()[]{}\"'").upper()


def _normalize_numeric_token(token: str) -> str:
    token = token.strip().replace("−", "-").replace("–", "-").replace("—", "-")
    token = re.sub(r"(?<=\d)[\s_](?=\d{3}\b)", "", token)
    token = token.replace(",", "")
    if token.endswith(".0"):
        token = token[:-2]
    try:
        value = Decimal(token)
    except InvalidOperation:
        return token
    if value == value.to_integral_value():
        return str(int(value))
    return format(value.normalize(), "f").rstrip("0").rstrip(".")


def normalize_mr_answer(value: object) -> str:
    text = normalize_text(value)
    if not text:
        return ""
    text = re.sub(r"\\boxed\{([^{}]+)\}", r"\1", text)
    text = re.sub(r"\bboxed\{([^{}]+)\}", r"\1", text, flags=re.IGNORECASE)
    text = re.sub(
        r"(?i)(?:final answer|answer|the answer is|відповідь|відповiдь|результат|відповідь така)\s*(?:is|=|:|-)?",
        " ",
        text,
    )
    numeric = re.findall(r"[-+]?\d+(?:[\s_,]\d{3})*(?:\.\d+)?|[-+]?\d+(?:\.\d+)?", text)
    if numeric:
        return _normalize_numeric_token(numeric[-1])
    return text.strip().strip(".:;,()[]{}\"'").lower()


def normalized_accuracy(predictions: Iterable[object], references: Iterable[object], task: str) -> float:
    pairs = list(zip(predictions, references))
    if not pairs:
        return 0.0
    if task == "QA":
        correct = sum(normalize_choice_answer(p) == normalize_choice_answer(r) for p, r in pairs)
    elif task == "MR":
        correct = sum(normalize_mr_answer(p) == normalize_mr_answer(r) for p, r in pairs)
    else:
        correct = sum(normalize_text(p) == normalize_text(r) for p, r in pairs)
    return correct / len(pairs)


def _word_ngrams(tokens: list[str], n: int) -> Counter[tuple[str, ...]]:
    return Counter(tuple(tokens[i : i + n]) for i in range(max(0, len(tokens) - n + 1)))


def fallback_bleu(predictions: list[str], references: list[str], max_order: int = 4) -> float:
    """Small BLEU fallback for smoke tests when sacrebleu is unavailable."""
    if not predictions:
        return 0.0
    precisions = []
    pred_len = 0
    ref_len = 0
    for n in range(1, max_order + 1):
        overlap = 0
        total = 0
        for pred, ref in zip(predictions, references):
            pred_tokens = normalize_text(pred).split()
            ref_tokens = normalize_text(ref).split()
            pred_len += len(pred_tokens) if n == 1 else 0
            ref_len += len(ref_tokens) if n == 1 else 0
            pred_counts = _word_ngrams(pred_tokens, n)
            ref_counts = _word_ngrams(ref_tokens, n)
            overlap += sum((pred_counts & ref_counts).values())
            total += max(1, sum(pred_counts.values()))
        precisions.append((overlap + 1) / (total + 1))
    bp = 1.0 if pred_len > ref_len else math.exp(1 - ref_len / max(1, pred_len))
    return 100 * bp * math.exp(sum(math.log(p) for p in precisions) / max_order)


def fallback_chrf(predictions: list[str], references: list[str], max_order: int = 6, beta: float = 2.0) -> float:
    if not predictions:
        return 0.0
    scores = []
    for pred, ref in zip(predictions, references):
        pred = normalize_text(pred)
        ref = normalize_text(ref)
        order_scores = []
        for n in range(1, max_order + 1):
            pred_counts = Counter(pred[i : i + n] for i in range(max(0, len(pred) - n + 1)))
            ref_counts = Counter(ref[i : i + n] for i in range(max(0, len(ref) - n + 1)))
            overlap = sum((pred_counts & ref_counts).values())
            precision = overlap / max(1, sum(pred_counts.values()))
            recall = overlap / max(1, sum(ref_counts.values()))
            denom = beta * beta * precision + recall
            order_scores.append(0.0 if denom == 0 else (1 + beta * beta) * precision * recall / denom)
        scores.append(sum(order_scores) / len(order_scores))
    return 100 * sum(scores) / len(scores)


def mt_scores(predictions: list[str], references: list[str]) -> dict[str, float]:
    try:
        import sacrebleu

        bleu = sacrebleu.corpus_bleu(predictions, [references]).score
        chrf = sacrebleu.corpus_chrf(predictions, [references], word_order=2).score
    except Exception:
        bleu = fallback_bleu(predictions, references)
        chrf = fallback_chrf(predictions, references)
    return {"bleu": bleu, "chrf++": chrf}


@dataclass
class BinaryF1:
    precision: float
    recall: float
    f1: float


def binary_f1(predictions: Iterable[bool], references: Iterable[bool]) -> BinaryF1:
    pairs = list(zip(predictions, references))
    if pairs and not any(p for p, _ in pairs) and not any(r for _, r in pairs):
        return BinaryF1(precision=1.0, recall=1.0, f1=1.0)
    tp = sum(p and r for p, r in pairs)
    fp = sum(p and not r for p, r in pairs)
    fn = sum((not p) and r for p, r in pairs)
    precision = tp / max(1, tp + fp)
    recall = tp / max(1, tp + fn)
    f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    return BinaryF1(precision=precision, recall=recall, f1=f1)


def _normalize_edit_token(value: str) -> str:
    token = normalize_text(value).strip().strip("`\"'.,;:()[]{}")
    return "CORRECT" if token.upper() == "CORRECT" else token


def parse_edit_output(text: str) -> tuple[str, str]:
    wrong = ""
    correct = ""
    for line in str(text).splitlines():
        normalized = line.strip()
        wrong_match = re.match(r"(?i)^\s*(?:wrong word|wrong|incorrect word|incorrect|помилкове слово|неправильне слово)\s*[:=-]\s*(.+?)\s*$", normalized)
        correct_match = re.match(r"(?i)^\s*(?:correct word|correct|correction|правильне слово|виправлення)\s*[:=-]\s*(.+?)\s*$", normalized)
        if wrong_match:
            wrong = wrong_match.group(1).strip()
        elif correct_match:
            correct = correct_match.group(1).strip()
    if not wrong and not correct:
        stripped = normalize_text(text)
        if stripped.upper() == "CORRECT":
            return "CORRECT", "CORRECT"
    return _normalize_edit_token(wrong or "CORRECT"), _normalize_edit_token(correct or "CORRECT")


def scgc_diagnostics(predictions: list[str], references: list[str]) -> dict[str, int]:
    pred_pairs = [parse_edit_output(p) for p in predictions]
    ref_pairs = [parse_edit_output(r) for r in references]
    pred_has_error = [wrong != "CORRECT" for wrong, _ in pred_pairs]
    ref_has_error = [wrong != "CORRECT" for wrong, _ in ref_pairs]
    tp = sum(p and r for p, r in zip(pred_has_error, ref_has_error))
    fp = sum(p and not r for p, r in zip(pred_has_error, ref_has_error))
    fn = sum((not p) and r for p, r in zip(pred_has_error, ref_has_error))
    tn = sum((not p) and (not r) for p, r in zip(pred_has_error, ref_has_error))
    wrong_exact = sum(
        p_wrong == r_wrong and r_wrong != "CORRECT"
        for (p_wrong, _), (r_wrong, _) in zip(pred_pairs, ref_pairs)
    )
    correction_exact = sum(
        p_wrong == r_wrong and p_correct == r_correct and r_wrong != "CORRECT"
        for (p_wrong, p_correct), (r_wrong, r_correct) in zip(pred_pairs, ref_pairs)
    )
    return {
        "total": len(ref_pairs),
        "gold_error": sum(ref_has_error),
        "gold_correct": len(ref_has_error) - sum(ref_has_error),
        "pred_error": sum(pred_has_error),
        "pred_correct": len(pred_has_error) - sum(pred_has_error),
        "detection_tp": tp,
        "detection_fp": fp,
        "detection_fn": fn,
        "detection_tn": tn,
        "wrong_word_exact": wrong_exact,
        "correction_exact": correction_exact,
    }


def scgc_scores(predictions: list[str], references: list[str]) -> dict[str, float]:
    pred_pairs = [parse_edit_output(p) for p in predictions]
    ref_pairs = [parse_edit_output(r) for r in references]
    pred_has_error = [wrong != "CORRECT" for wrong, _ in pred_pairs]
    ref_has_error = [wrong != "CORRECT" for wrong, _ in ref_pairs]
    detection = binary_f1(pred_has_error, ref_has_error).f1
    correction_flags = [
        p_wrong == r_wrong and p_correct == r_correct and r_wrong != "CORRECT"
        for (p_wrong, p_correct), (r_wrong, r_correct) in zip(pred_pairs, ref_pairs)
    ]
    correction_refs = [wrong != "CORRECT" for wrong, _ in ref_pairs]
    correction = binary_f1(correction_flags, correction_refs).f1
    return {"detection_f1": detection, "correction_f1": correction}


def aggregate_wmt_scores(task_scores: dict[str, dict[str, float]]) -> dict[str, float]:
    mt = task_scores.get("MT", {})
    qa = task_scores.get("QA", {})
    sc = task_scores.get("SC", {})
    gc = task_scores.get("GC", {})
    mr = task_scores.get("MR", {})
    mt_score = mt.get("chrf++", 0.0)
    qa_score = qa.get("accuracy", 0.0) * 100
    sc_score = ((sc.get("detection_f1", 0.0) + sc.get("correction_f1", 0.0)) / 2) * 100
    gc_score = ((gc.get("detection_f1", 0.0) + gc.get("correction_f1", 0.0)) / 2) * 100
    mr_score = mr.get("accuracy", 0.0) * 100
    overall = (mt_score + qa_score + sc_score + gc_score + mr_score) / 5
    return {
        "MT_score": mt_score,
        "QA_score": qa_score,
        "SC_score": sc_score,
        "GC_score": gc_score,
        "MR_score": mr_score,
        "overall_score": overall,
    }

def analyze_samples(samples, slow_threshold=50, min_required=5):
    """
    Analyzes queue behavior based on samples collected.
    Returns one of: STUCK, SLOW, HEALTHY, or INSUFFICIENT DATA
    """
    print("\n🔍 Analyzing collected samples...")

    if len(samples) < min_required:
        print(f"[!] Not enough data to analyze. Collected {len(samples)} sample(s).")
        return "INSUFFICIENT DATA"

    total_in = sum(s["in"] for s in samples)
    total_out = sum(s["out"] for s in samples)
    avg_delta = sum(s["delta"] for s in samples) / len(samples)
    stuck = all(s["out"] == 0 for s in samples) and any(s["in"] > 0 for s in samples)

    print(f"- Samples collected: {len(samples)}")
    print(f"- Total In: {total_in}")
    print(f"- Total Out: {total_out}")
    print(f"- Avg Δ (In - Out): {avg_delta:.2f}")

    if stuck:
        print("🚨 Verdict: STUCK — no items are being processed.")
        return "STUCK"
    elif avg_delta > slow_threshold:
        print("⚠️ Verdict: SLOW — queue is growing too fast.")
        return "SLOW"
    else:
        print("✅ Verdict: HEALTHY — system is processing requests normally.")
        return "HEALTHY"

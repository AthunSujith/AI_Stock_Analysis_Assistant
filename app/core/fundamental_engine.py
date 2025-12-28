def fundamental_score(row):
    score = 0
    score += 20 if row['roic'] > 15 else 0
    score += 20 if row['rev_growth'] > 10 else 0
    score += 20 if row['de_ratio'] < 1 else 0
    score += 20 if row['fcf'] > 0 else 0
    score += 20 if row['margin_trend'] > 0 else 0
    return score

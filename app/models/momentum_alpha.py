def momentum_prob(df):
    ret = df['close'].pct_change(20)
    return (ret > 0).rolling(10).mean().iloc[-1]

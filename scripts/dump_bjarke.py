import pandas as pd
import json
p = 'data/user_dfs/Bjarke_Ha'
try:
    df = pd.read_pickle(p)
except Exception as e:
    print(json.dumps({'error': str(e)}))
    raise
cols = [c for c in df.columns if 'final' in c.lower() or 'top scorer' in c.lower()]
out = {
    'shape': df.shape,
    'cols': cols,
    'row0': {c: df.at[0,c] for c in cols},
    'row1': {c: df.at[1,c] for c in cols},
    'row2': {c: (float(df.at[2,c]) if pd.notna(df.at[2,c]) else None) for c in cols},
    'total': float(pd.to_numeric(df.loc[2], errors='coerce').sum())
}
print(json.dumps(out, ensure_ascii=False, indent=2))

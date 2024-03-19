import os
import pandas as pd
from supabase import create_client, Client

class SupabaseClient:
    def __init__(self):
        if not os.getenv('SUPABASE_URL'):
            raise ValueError('SUPABASE_URL is not set')
        if not os.getenv('SUPABASE_KEY'):
            raise ValueError('SUPABASE_KEY is not set')
        self.client : Client = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY'),
        )
    
    def fetch_candidate(self) -> pd.DataFrame:
        query = self.client.table('TOSS_GATHERING')\
                .select('symbol')
        result = query.execute()
        return pd.DataFrame(result.data)
    
    # def update_score(self, symbol: str, score: float) -> None:
    #     query = self.client.table('TOSS_GATHERING')\
    #             .update({
    #                 'score': score,
    #             }).eq('symbol', symbol)
    #     return query.execute()
    
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    supabase = SupabaseClient()
    print(supabase.fetch_candidate())
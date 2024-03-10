from unittest import TestCase, main, skip
import os

from dotenv import load_dotenv
load_dotenv()

class FinanceTests(TestCase):
    def test_fetch_history(self):
        from src.finance import Finance
        finance = Finance()
        data = finance.fetch_history('TQQQ')
        self.assertIsNotNone(data)

    def test_update_momentum(self):
        from src.finance import Finance
        finance = Finance()
        score = finance.update_momentum('TQQQ')
        self.assertIsInstance(score, float)

class SupabaseTests(TestCase):
    def test_url(self):
        url = os.getenv('SUPABASE_URL')
        self.assertIsInstance(url, str)

    def test_key(self):
        key = os.getenv('SUPABASE_KEY')
        self.assertIsInstance(key, str)
    
    def test_fetch_candidate(self):
        import pandas as pd
        from src.sb import SupabaseClient
        supabase = SupabaseClient()
        data = supabase.fetch_candidate()
        self.assertIsInstance(data, pd.DataFrame)

    # def test_fetch_token_from_cano(self):
    #     from src.sb import SupabaseClient
    #     supabase = SupabaseClient()
    #     token = supabase.fetch_token_from_cano(os.getenv('KIS_CANO'))
    #     self.assertIsInstance(token, dict)
    #     self.assertIn('access_token', token)
    #     self.assertIn('token_expired', token)

class TelegramTests(TestCase):        
    def test_bot_token(self):
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.assertIsInstance(bot_token, str)

    def test_chat_id(self):
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.assertIsInstance(chat_id, str)

    def test_send_message(self):
        from src.telegram import TelegramBot
        bot = TelegramBot()
        bot.send_message('Hello World!')

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.WARNING)
    main()
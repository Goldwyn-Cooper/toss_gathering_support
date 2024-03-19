def main():
    import requests
    from src.sb import SupabaseClient
    from src.telegram import TelegramBot
    from src.finance import Finance

    bot = TelegramBot()
    bot.send_message(f'📌 TOSS_GATHERING_SUPPORT')
    try:
        supabase = SupabaseClient()
        finance = Finance()

        candidate = supabase.fetch_candidate()
        candidate['score'] = candidate['symbol'].apply(finance.update_momentum).round(3)
        candidate['hold'] = candidate.score > 0
        candidate.set_index('symbol', inplace=True)
        message = ''
        for symbol, data in candidate.iterrows():
            if data.hold:
                message += f'✅ {symbol}\n'
            elif not data.hold:
                message += f'❌ {symbol}\n'
        bot.send_message(message.strip())
        print(candidate.loc[:, ['score', 'hold']])
    except requests.exceptions.RequestException as e:
        print(e.response.status_code)
        print(e.response.reason)
    except Exception as e:
        print(type(e))
        print(e)
        bot.send_message(f'{type(e)}\n{e}')

if __name__ == "__main__":
    import logging
    import warnings
    logging.basicConfig(level=logging.WARNING)
    warnings.filterwarnings('ignore')

    from dotenv import load_dotenv
    load_dotenv()
    
    main()
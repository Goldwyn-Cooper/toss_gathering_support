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
        candidate['hold_prev'] = candidate.score > 0
        candidate.score = candidate.index.map(finance.update_momentum).round(3)
        candidate.sort_values('score', ascending=False, inplace=True)
        candidate['hold'] = candidate.score > 0
        message = ''
        for symbol, data in candidate.iterrows():
            if data.hold and not data.hold_prev:
                message += f'✅ {symbol}\n'
            elif not data.hold and data.hold_prev:
                message += f'❌ {symbol}\n'
            supabase.update_score(symbol, data.score)
        if message:
            bot.send_message(message.strip())
        else:
            bot.send_message('🫥 No Change')
        print(candidate.loc[:, ['score']])
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
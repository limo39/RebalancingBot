import alpaca_trade_api as tradeapi

# Set your API credentials
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'
APCA_API_KEY_ID = 'YOUR_API_KEY_ID'
APCA_API_SECRET_KEY = 'YOUR_API_SECRET_KEY'


api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL, api_version='v2')

def rebalance_portfolio(target_weights):
    account = api.get_account()
    account_value = float(account.equity)

    positions = api.list_positions()
    current_portfolio_value = 0

    for position in positions:
        symbol = position.symbol
        qty = int(position.qty)
        latest_price = float(position.current_price)
        current_portfolio_value += qty * latest_price

    target_allocation_value = account_value * target_weights

    orders = []
    for position in positions:
        symbol = position.symbol
        qty = int(position.qty)
        latest_price = float(position.current_price)
        target_allocation = target_allocation_value[symbol]

        target_qty = int(target_allocation / latest_price)

        qty_diff = target_qty - qty


        if qty_diff != 0:
            side = 'buy' if qty_diff > 0 else 'sell'
            abs_qty_diff = abs(qty_diff)
            orders.append({
                'symbol': symbol,
                'qty': abs_qty_diff,
                'side': side,
            })

    for order in orders:
        symbol = order['symbol']
        qty = order['qty']
        side = order['side']
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='market',
            time_in_force='gtc'
        )

target_weights = {
    'AAPL': 0.4,
    'GOOGL': 0.3,
    'AMZN': 0.3
}
rebalance_portfolio(target_weights)

from .. schemas import StockStatus


def determine_stock_status(quantity: int) -> StockStatus:
    if quantity == 0:
        return StockStatus.out_of_stock
    elif quantity < 10:
        return StockStatus.low_stock
    else:
        return StockStatus.in_stock

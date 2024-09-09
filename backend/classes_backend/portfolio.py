class Portfolio:
    def __init__(self, port_name: str, stock_list: dict):
        self.port_name = port_name
        if stock_list is None:
            stock_list = dict()
        self.stocks = stock_list

    def to_dict(self):
        return {
            "port_name": self.port_name,
            "stock_list": self.stocks
        }
